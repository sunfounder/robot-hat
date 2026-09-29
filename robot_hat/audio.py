#!/usr/bin/env python3
"""
Robot HAT audio helpers.

Shared by the 'robot_hat doctor' and 'robot_hat speaker' commands.

The Robot HAT uses the Raspberry Pi I2S peripheral to drive the onboard
amplifier. Two hardware revisions behave differently:

* Robot HAT V4 - no HAT EEPROM, 'hifiberry-dac' overlay, speaker enable
  on GPIO 20, no onboard microphone.
* Robot HAT V5 (O1902V50) - HAT EEPROM, 'googlevoicehat-soundcard'
  overlay, speaker enable on GPIO 12, onboard microphone.

The speaker amplifier keeps drawing current as long as the I2S clocks run
without data, which is what makes the speaker hot. Enabling the speaker
must therefore always be followed by a short silence burst, see
:func:'prime_i2s'.
"""

import json
import os
import pwd
import re
import shutil
import subprocess

ASOUND_CONF = "/etc/asound.conf"
CONFIG_TXT_CANDIDATES = ("/boot/firmware/config.txt", "/boot/config.txt")
PCM_CLK_PATH = "/sys/kernel/debug/clk/clk_summary"
TEST_SOUND = "/usr/share/sounds/alsa/Front_Center.wav"

# I2S dtoverlay and sound card names
DTOVERLAY_V4 = "hifiberry-dac"
DTOVERLAY_V5 = "googlevoicehat-soundcard"
CARD_V4 = ("sndrpihifiberry", "snd_rpi_hifiberry_dac")
CARD_V5 = ("sndrpigooglevoi", "snd_rpi_googlevoicehat_soundcar")

# ALSA softvol control names written by setup_robot_hat_audio.sh
SOFTVOL_SPEAKER = "robot-hat speaker"
SOFTVOL_MIC = "robot-hat mic"


def run(cmd, timeout=10, as_user=False):
    """Run a shell command.

    :param cmd: command to run
    :type cmd: str
    :param timeout: timeout in seconds
    :type timeout: int
    :param as_user: run as the desktop user instead of root
    :type as_user: bool
    :return: (status, output); status 124 means the command timed out
    :rtype: tuple
    """
    if as_user:
        user = desktop_user()
        if user is None:
            return 1, "no desktop user"
        if os.geteuid() == 0:
            env = ("XDG_RUNTIME_DIR=/run/user/%s "
                   "DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/%s/bus"
                   % (user.pw_uid, user.pw_uid))
            cmd = "sudo -u %s env %s sh -c %s" % (
                user.pw_name, env, shell_quote(cmd))
    proc = None
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        out, _ = proc.communicate(timeout=timeout)
        return proc.returncode, out.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        if proc is not None:
            proc.kill()
            proc.communicate()
        return 124, "timeout"
    except Exception as e:
        return 1, str(e)


def shell_quote(text):
    """Quote a string for a POSIX shell."""
    return "'" + str(text).replace("'", "'\"'\"'") + "'"


#: directories that hold tools users need but that are not in PATH
SBIN_DIRS = ("/usr/sbin", "/sbin", "/usr/local/sbin")


def command_path(name, extra_dirs=SBIN_DIRS):
    """Full path of a command, also searching the sbin directories.

    On Debian the PATH of a normal user has no /usr/sbin, so tools like
    i2cdetect are installed but not found by name.
    """
    path = shutil.which(name)
    if path:
        return path
    for directory in extra_dirs:
        candidate = os.path.join(directory, name)
        if os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    return ""


def command_exists(name):
    """Check whether a command is available (PATH or an sbin directory)."""
    return command_path(name) != ""


def desktop_user():
    """Return the pwd entry of the desktop user (uid 1000-65533), or None.

    Users with a running session (/run/user/<uid>) are preferred, as
    PulseAudio/PipeWire can only be controlled from their session.
    """
    users = [u for u in pwd.getpwall() if 1000 <= u.pw_uid < 65534]
    for user in users:
        if os.path.isdir("/run/user/%s" % user.pw_uid):
            return user
    return users[0] if users else None


# ---- board / audio profile -------------------------------------------------

def board_profile():
    """Audio profile of the detected Robot HAT.

    :return: dict with keys 'revision', 'is_v5', 'overlay', 'card_short',
        'card_names', 'has_mic' and 'speaker_pin'
    :rtype: dict
    """
    is_v5 = False
    speaker_pin = 20
    try:
        from . import __device__ as device
        is_v5 = device.uuid in device.HAT_UUIDs
        speaker_pin = device.spk_en
    except Exception:
        pass
    if is_v5:
        return {
            "revision": "V5",
            "is_v5": True,
            "overlay": DTOVERLAY_V5,
            "card_short": CARD_V5[0],
            "card_names": CARD_V5,
            "has_mic": True,
            "speaker_pin": speaker_pin,
        }
    return {
        "revision": "V4",
        "is_v5": False,
        "overlay": DTOVERLAY_V4,
        "card_short": CARD_V4[0],
        "card_names": CARD_V4,
        "has_mic": False,
        "speaker_pin": speaker_pin,
    }


# ---- config.txt ------------------------------------------------------------

def find_config_txt():
    """Path of the active Raspberry Pi config.txt (may not exist)."""
    for path in CONFIG_TXT_CANDIDATES:
        if os.path.isfile(path):
            return path
    return CONFIG_TXT_CANDIDATES[0]


def config_lines():
    """Content of config.txt as a list of lines (empty on error)."""
    try:
        with open(find_config_txt(), "r") as f:
            return f.read().splitlines()
    except OSError:
        return []


def active_dtoverlays():
    """Names of the uncommented dtoverlay= entries in config.txt."""
    names = []
    for line in config_lines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "dtoverlay=" not in stripped:
            continue
        name = stripped.split("dtoverlay=", 1)[1].split()[0].split(",")[0].strip()
        if name:
            names.append(name)
    return names


def active_i2s_overlay():
    """The uncommented I2S overlay in config.txt ('' when there is none)."""
    known = (DTOVERLAY_V4, DTOVERLAY_V5)
    for name in active_dtoverlays():
        if name in known or "soundcard" in name or "hifiberry" in name:
            return name
    return ""


# ---- ALSA ------------------------------------------------------------------

def find_card(short_names, capture=False):
    """Find an ALSA card by its short name.

    :param short_names: names as printed by aplay -l, e.g. 'sndrpihifiberry'
    :type short_names: tuple
    :param capture: look at capture devices (arecord -l) instead
    :type capture: bool
    :return: (card index, card line) or (None, '')
    :rtype: tuple
    """
    cmd = "arecord -l" if capture else "aplay -l"
    status, out = run(cmd, timeout=5)
    if status != 0:
        return None, ""
    for line in out.splitlines():
        if not any(name in line for name in short_names):
            continue
        match = re.search(r"card (\d+):", line)
        if match:
            return int(match.group(1)), line.strip()
    return None, ""


def asound_conf_card():
    """Sound card name referenced by /etc/asound.conf ('' when missing)."""
    try:
        with open(ASOUND_CONF, "r") as f:
            content = f.read()
    except OSError:
        return ""
    for name in CARD_V4 + CARD_V5:
        if name in content:
            return name
    return ""


def amixer_control(short_name, control):
    """Read one ALSA control; returns the raw amixer output ('' on error)."""
    status, out = run("amixer -c %s sget '%s'" % (short_name, control), timeout=5)
    return out if status == 0 else ""


def volume_is_audible(short_name):
    """Check the speaker volume control is present and not muted or 0%.

    :return: (ok, detail). 'ok' is True when the control cannot be found,
        because older images do not always expose it.
    :rtype: tuple
    """
    for control in (SOFTVOL_SPEAKER, "Playback", "Master", "PCM"):
        out = amixer_control(short_name, control)
        if not out:
            continue
        if "Playback" not in out and "Front Left" not in out and "Mono" not in out:
            continue
        if "[off]" in out or "[0%]" in out or "[0dB]" in out:
            return False, "'%s' is muted or 0%%" % control
        return True, ""
    return True, "no speaker volume control - skipped"


# ---- PulseAudio ------------------------------------------------------------

def pa_info():
    """Output of 'pactl info' as a dict, or an empty dict when PA is down."""
    status, out = run("pactl -f json info", timeout=5, as_user=True)
    if status != 0:
        return {}
    try:
        return json.loads(out)
    except ValueError:
        return {}


def pa_sinks():
    """PulseAudio sinks as a list of dicts (empty when PA is not running)."""
    status, out = run("pactl -f json list sinks", timeout=5, as_user=True)
    if status != 0:
        return []
    try:
        return json.loads(out)
    except ValueError:
        return []


def pa_sources():
    """PulseAudio sources as a list of dicts (empty when PA is not running)."""
    status, out = run("pactl -f json list sources", timeout=5, as_user=True)
    if status != 0:
        return []
    try:
        return json.loads(out)
    except ValueError:
        return []


def find_pa_node(nodes, card_names):
    """Find the PulseAudio node that belongs to the Robot HAT sound card."""
    for node in nodes:
        card = node.get("properties", {}).get("alsa.card_name", "")
        if any(name in card for name in card_names):
            return node
    return None


def default_sink():
    """Name of the current PulseAudio default sink ('' when unknown)."""
    return pa_info().get("default_sink_name", "")


def set_default_sink(name):
    """Set the PulseAudio default sink."""
    status, _ = run("pactl set-default-sink %s" % name, timeout=5, as_user=True)
    return status == 0


def set_default_source(name):
    """Set the PulseAudio default source."""
    status, _ = run("pactl set-default-source %s" % name, timeout=5, as_user=True)
    return status == 0


def set_sink_volume(percent):
    """Set the volume of the default sink."""
    status, _ = run("pactl set-sink-volume @DEFAULT_SINK@ %s%%" % percent,
                    timeout=5, as_user=True)
    return status == 0


def set_source_volume(percent):
    """Set the volume of the default source."""
    status, _ = run("pactl set-source-volume @DEFAULT_SOURCE@ %s%%" % percent,
                    timeout=5, as_user=True)
    return status == 0


def get_default_sink_volume():
    """Volume of the default sink as an integer percentage, or None."""
    _, out = run("pactl get-sink-volume @DEFAULT_SINK@", timeout=5, as_user=True)
    match = re.search(r"(\d+)%", out)
    return int(match.group(1)) if match else None


# ---- I2S clock health ------------------------------------------------------

def pcm_enable_count():
    """Enable count of the I2S 'pcm' clock, or -1 when it is not readable.

    A count that never leaves 0 is the symptom of a stuck I2S peripheral:
    the amplifier gets no data while the clocks keep running, which is what
    heats up the speaker.
    """
    try:
        with open(PCM_CLK_PATH, "r") as f:
            lines = f.readlines()
    except OSError:
        return -1
    for line in lines:
        if not line.strip().startswith("pcm"):
            continue
        for part in line.split():
            if part.isdigit():
                return int(part)
    return -1


def i2s_clock_check(short_names):
    """Play a short tone and check the I2S PCM clock actually starts.

    :return: (ok, detail)
    :rtype: tuple
    """
    card_index, _ = find_card(short_names)
    if card_index is None:
        return True, "no sound card - skipped"
    before = pcm_enable_count()
    if before < 0:
        return True, "debugfs not available - skipped"

    wav_path = "/tmp/_robot_hat_i2s_check.wav"
    status, _ = run("sox -n -r 48000 -b 32 -c 2 %s synth 0.5 sin 440" % wav_path,
                    timeout=10)
    if status != 0 or not os.path.isfile(wav_path):
        return True, "sox not available - skipped"
    during = before
    try:
        proc = subprocess.Popen("aplay -D hw:%s,0 %s" % (card_index, wav_path),
                                shell=True, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
        try:
            import time
            time.sleep(0.3)
            during = pcm_enable_count()
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()
    finally:
        try:
            os.unlink(wav_path)
        except OSError:
            pass

    if during > before:
        return True, "PCM clock started (%s -> %s)" % (before, during)
    if before > 0:
        # the clock is already enabled by the sound card, which is fine
        return True, "PCM clock already enabled (%s)" % before
    return False, "I2S clock stuck - PCM enable count stayed 0 during playback"


def prime_i2s():
    """Enable the speaker and push a short burst to unstick the I2S bus.

    This is the Robot HAT fix for a hot speaker: enabling the amplifier is
    always followed by 0.5 s of silence so the I2S peripheral has data.
    """
    try:
        from .device import enable_speaker
        enable_speaker()
        return True
    except Exception:
        return False


def speaker_pin_state(pin=None):
    """State of the speaker enable GPIO: True/False, or None when unknown."""
    if pin is None:
        pin = board_profile()["speaker_pin"]
    if command_exists("pinctrl"):
        cmd = "pinctrl get %s" % pin
    elif command_exists("raspi-gpio"):
        cmd = "raspi-gpio get %s" % pin
    else:
        return None
    status, out = run(cmd, timeout=5)
    if status != 0 or "|" not in out:
        return None
    try:
        value = out.split("|")[-1].strip().split()[0]
    except IndexError:
        return None
    if value == "hi":
        return True
    if value == "lo":
        return False
    return None


def speaker_test():
    """Play the ALSA test sound through the Robot HAT speaker.

    :return: True when the test sound finished without an error
    :rtype: bool
    """
    from .device import enable_speaker, disable_speaker
    print("Test Robot HAT speaker.")
    saved_volume = get_default_sink_volume()
    if saved_volume is not None:
        set_sink_volume(80)
    try:
        enable_speaker()
        status, output = run("aplay -q %s" % TEST_SOUND, timeout=15)
    finally:
        if saved_volume is not None:
            set_sink_volume(saved_volume)
        try:
            disable_speaker()
        except Exception:
            pass
    if status != 0:
        print(output.strip())
    return status == 0
