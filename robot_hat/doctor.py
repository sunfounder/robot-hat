#!/usr/bin/env python3
"""
Robot HAT health check.

The doctor looks at everything that has to be right for a Robot HAT to work:
the HAT itself, the I2C bus to the onboard MCU, the GPIO setup, the installed
library and its dependencies, and the I2S audio path (overlay, sound card,
ALSA, PulseAudio, speaker enable pin and I2S clock).

Run 'robot_hat doctor' to report, 'robot_hat doctor --fix' to repair the
common problems automatically.
"""

import os
import platform
import sys

from .audio import (
    CARD_V5,
    active_i2s_overlay,
    command_path,
    asound_conf_card,
    board_profile,
    command_exists,
    default_sink,
    find_card,
    find_config_txt,
    find_pa_node,
    i2s_clock_check,
    pa_info,
    pa_sinks,
    pa_sources,
    prime_i2s,
    run,
    set_default_sink,
    set_default_source,
    set_sink_volume,
    set_source_volume,
    speaker_pin_state,
    volume_is_audible,
)
from .version import __version__

GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
BOLD = "\033[1m"
RESET = "\033[0m"

#: Python modules the library needs at runtime
PYTHON_MODULES = ("smbus2", "lgpio", "spidev", "serial", "gpiozero", "pyaudio", "pygame")

#: (command, package) pairs needed by the audio path
REQUIRED_TOOLS = (("aplay", "alsa-utils"), ("amixer", "alsa-utils"), ("sox", "sox"),
                  ("i2cdetect", "i2c-tools"))
OPTIONAL_TOOLS = (("pactl", "pulseaudio-utils"), ("jq", "jq"), ("espeak", "espeak"))


def _icon(ok):
    return "%s\u2713%s" % (GREEN, RESET) if ok else "%s\u2717%s" % (RED, RESET)


def _print_check(name, ok, detail=""):
    """Print one check result."""
    suffix = " (%s)" % detail if detail else ""
    # \033[K clears the spinner that was printed before this line
    sys.stdout.write("  %s %s%s\033[K\n" % (_icon(ok), name, suffix))
    sys.stdout.flush()


def _print_section(title):
    print("")
    print("  %s%s%s" % (BOLD, title, RESET))
    print("  " + "-" * 42)


def _device():
    """The Robot HAT device object, or None when it cannot be read."""
    try:
        from . import __device__
        return __device__
    except Exception:
        return None


#: I2C addresses the onboard MCU answers on
MCU_ADDRESSES = (0x14, 0x15, 0x16)


def _i2c_devices(bus=1):
    """Set of I2C addresses found on the bus, or None when the scan failed."""
    i2cdetect = command_path("i2cdetect")
    if not i2cdetect:
        return None
    status, out = run("%s -y %s" % (i2cdetect, bus), timeout=10)
    if status != 0:
        return None
    found = set()
    for line in out.splitlines():
        if ":" not in line:
            continue
        head, _, rest = line.partition(":")
        head = head.strip()
        try:
            base = int(head, 16)
        except ValueError:
            continue
        if base % 16 != 0:
            continue
        for index, token in enumerate(rest.split()):
            if token in ("--", "UU"):
                continue
            try:
                int(token, 16)
            except ValueError:
                continue
            found.add(base + index)
    return found


# ---- board -----------------------------------------------------------------

def _check_hat():
    """Robot HAT identification through the HAT EEPROM."""
    device = _device()
    if device is None:
        return False, "cannot read /proc/device-tree - not a Raspberry Pi?"
    if device.uuid and device.uuid in device.HAT_UUIDs:
        name = (device.name or "Robot HAT").replace("\x00", "").strip()
        # the board is named after the decimal values, e.g. O1902V50
        return True, "%s O%dV%d" % (name, device.product_id, device.product_ver)
    return True, "no HAT EEPROM - assuming Robot HAT V4"


def _check_i2c_bus():
    """The I2C bus must be enabled, the MCU lives on it."""
    if os.path.exists("/dev/i2c-1"):
        return True, ""
    return False, "/dev/i2c-1 not found - I2C is disabled"


def _check_mcu():
    """The onboard MCU must answer on the I2C bus.

    It uses one of 0x14, 0x15 or 0x16 - which one depends on the board, so
    the library probes all of them.
    """
    if not command_path("i2cdetect"):
        return False, "i2cdetect is missing (install i2c-tools)"
    devices = _i2c_devices(1)
    if devices is None:
        return False, "i2cdetect failed"
    found = sorted(set(MCU_ADDRESSES) & devices)
    if found:
        return True, "0x%02X" % found[0]
    return False, "no device at 0x14/0x15/0x16 - check the HAT is seated"


def _check_gpio():
    """lgpio must be able to open the GPIO chip that drives the 40-pin header."""
    try:
        import lgpio
    except ImportError:
        return False, "lgpio is not installed"
    try:
        from .pin import _get_gpiochip_num
        chip_num = _get_gpiochip_num()
    except Exception:
        chip_num = 0
    try:
        handle = lgpio.gpiochip_open(chip_num)
    except Exception as e:
        return False, ("cannot open gpiochip%s (%s) - ROBOT_HAT_GPIOCHIP can force "
                       "the /dev/gpiochipN index" % (chip_num, e))
    try:
        lgpio.gpiochip_close(handle)
    except Exception:
        pass
    return True, "gpiochip%s" % chip_num


def _check_pinctrl():
    """pinctrl (or raspi-gpio) is what enable_speaker() uses."""
    for cmd in ("pinctrl", "raspi-gpio"):
        if command_exists(cmd):
            return True, cmd
    return False, "neither pinctrl nor raspi-gpio is available"


# ---- library ---------------------------------------------------------------

def _check_library():
    """The installed robot_hat library."""
    try:
        import robot_hat
        path = os.path.dirname(os.path.abspath(robot_hat.__file__))
    except Exception as e:
        return False, "cannot import robot_hat (%s)" % e
    return True, "v%s (%s)" % (__version__, path)


def _check_python_modules():
    """Python modules used by the library."""
    import importlib.util
    missing = [name for name in PYTHON_MODULES if importlib.util.find_spec(name) is None]
    if missing:
        return False, "missing: " + ", ".join(missing)
    return True, ""


def _check_cli_tools():
    """Command line tools needed to configure and test the audio path."""
    missing = [name for name, _ in REQUIRED_TOOLS if not command_exists(name)]
    if missing:
        return False, "missing: " + ", ".join(missing)
    optional = [name for name, _ in OPTIONAL_TOOLS if not command_exists(name)]
    if optional:
        return True, "missing optional: " + ", ".join(optional)
    return True, ""


# ---- audio -----------------------------------------------------------------

def _check_dtoverlay():
    """The I2S overlay of this board revision must be active in config.txt."""
    profile = board_profile()
    active = active_i2s_overlay()
    if active == profile["overlay"]:
        return True, active
    if active:
        return False, "%s is active, expected %s" % (active, profile["overlay"])
    return False, "%s missing in %s" % (profile["overlay"], find_config_txt())


def _check_sound_card():
    """The I2S sound card must be registered with ALSA."""
    profile = board_profile()
    index, _ = find_card(profile["card_names"])
    if index is None:
        return False, "%s not found (reboot after enabling the overlay?)" % profile["card_short"]
    return True, "hw:%s,0" % index


def _check_capture_device():
    """Robot HAT V5 has an onboard microphone."""
    profile = board_profile()
    if not profile["has_mic"]:
        return True, "no onboard mic on %s - skipped" % profile["revision"]
    index, _ = find_card(CARD_V5, capture=True)
    if index is None:
        return False, "capture device not found"
    return True, "hw:%s,0" % index


def _check_asound_conf():
    """/etc/asound.conf must route to the sound card of this board revision."""
    profile = board_profile()
    card = asound_conf_card()
    if not card:
        return False, "/etc/asound.conf missing or does not reference the sound card"
    if card in profile["card_names"]:
        return True, card
    return False, "asound.conf uses %s, expected %s" % (card, profile["card_short"])


def _check_pa_sink():
    """PulseAudio must send audio to the Robot HAT, not to the headphone jack."""
    profile = board_profile()
    if not pa_info():
        return True, "PulseAudio not running - skipped"
    sink_name = default_sink()
    if not sink_name:
        return True, "no default sink - skipped"
    node = None
    for sink in pa_sinks():
        if sink.get("name") == sink_name:
            node = sink
            break
    if node is None:
        return False, "default sink '%s' not found" % sink_name
    card_name = node.get("properties", {}).get("alsa.card_name", "")
    if any(name in card_name for name in profile["card_names"]):
        return True, sink_name
    return False, "default sink is '%s'" % (card_name or sink_name)


def _check_volume():
    """A muted or 0% speaker volume looks exactly like a broken speaker."""
    profile = board_profile()
    return volume_is_audible(profile["card_short"])


def _check_speaker_pin():
    """Report the state of the speaker enable GPIO."""
    profile = board_profile()
    state = speaker_pin_state(profile["speaker_pin"])
    if state is None:
        return True, "GPIO%s unknown" % profile["speaker_pin"]
    return True, "GPIO%s %s" % (profile["speaker_pin"], "enabled" if state else "disabled")


def _check_i2s_clock():
    """The I2S clocks must start when audio is played (hot speaker symptom)."""
    profile = board_profile()
    return i2s_clock_check(profile["card_names"])


#: The checks, grouped by section
SECTIONS = (
    ("Board", (
        ("HAT EEPROM", _check_hat),
        ("I2C bus", _check_i2c_bus),
        ("onboard MCU", _check_mcu),
        ("GPIO chip", _check_gpio),
        ("pinctrl", _check_pinctrl),
    )),
    ("Library", (
        ("robot_hat", _check_library),
        ("python modules", _check_python_modules),
        ("audio tools", _check_cli_tools),
    )),
    ("Audio", (
        ("I2S dtoverlay", _check_dtoverlay),
        ("sound card", _check_sound_card),
        ("capture device", _check_capture_device),
        ("asound.conf", _check_asound_conf),
        ("PulseAudio sink", _check_pa_sink),
        ("speaker volume", _check_volume),
        ("speaker enable pin", _check_speaker_pin),
        ("I2S clock (PCM)", _check_i2s_clock),
    )),
)


def _run_checks(show=True):
    """Run every check.

    :param show: print each result while it runs
    :type show: bool
    :return: dict with 'by_name' (name -> bool), 'detail' (name -> str),
        'sections' (section -> bool) and 'overall'
    :rtype: dict
    """
    by_name = {}
    detail = {}
    sections = {}
    for title, checks in SECTIONS:
        ok_section = True
        if show:
            _print_section(title)
        for name, func in checks:
            if show:
                sys.stdout.write("  ... %s\r" % name)
                sys.stdout.flush()
            try:
                ok, info = func()
            except Exception as e:
                ok, info = False, "check failed: %s" % e
            by_name[name] = ok
            detail[name] = info
            if not ok:
                ok_section = False
            if show:
                _print_check(name, ok, info)
        sections[title] = ok_section
    return {
        "by_name": by_name,
        "detail": detail,
        "sections": sections,
        "overall": all(sections.values()),
    }


def _print_fix_hint(fix_mode=False):
    if not fix_mode:
        print("  -> Run: %srobot_hat doctor --fix%s" % (BOLD, RESET))


def doctor(fix_mode=False):
    """Check the Robot HAT installation and print the result.

    :param fix_mode: adapt the summary for '--fix' (do not suggest it again)
    :type fix_mode: bool
    :return: the check results, see :func:'_run_checks'
    :rtype: dict
    """
    profile = board_profile()
    machine = platform.uname()
    print("")
    print("=" * 50)
    print("  Robot HAT Doctor")
    print("=" * 50)
    print("  %s %s (%s)" % (machine.system, machine.release,
                           getattr(machine, "machine", "")))
    print("  board: Robot HAT %s - %s, speaker on GPIO%s" % (
        profile["revision"], profile["overlay"], profile["speaker_pin"]))

    results = _run_checks(show=True)

    print("")
    if results["overall"]:
        print("  %sAll checks passed.%s" % (GREEN, RESET))
    else:
        for title, ok in results["sections"].items():
            if not ok:
                print("  %s%s: problems found.%s" % (YELLOW, title, RESET))
        _print_fix_hint(fix_mode)
    print("")
    print("=" * 50)
    print("")
    return results


def _audio_setup_script():
    """Path of the bundled audio setup script ('' when it is not there)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "scripts", "setup_robot_hat_audio.sh")
    return path if os.path.isfile(path) else ""


def _wait_for_pa_node(lister, card_names, timeout=10):
    """Wait for a PulseAudio node of the sound card to appear (or None)."""
    import time
    deadline = time.time() + timeout
    while True:
        node = find_pa_node(lister(), card_names)
        if node is not None or time.time() >= deadline:
            return node
        time.sleep(1)


def _as_root(cmd):
    """Prefix a command with sudo when the doctor is not run as root."""
    if os.geteuid() == 0:
        return cmd
    return "sudo " + cmd


def _run_audio_setup():
    """Run the bundled audio setup script (overlay + ALSA + PulseAudio)."""
    script = _audio_setup_script()
    if not script:
        return False
    status, _ = run(_as_root("bash %s --skip-test --no-deps" % script), timeout=300)
    return status == 0


def doctor_fix():
    """Run the doctor and repair what can be repaired.

    :return: dict with 'before', 'after', 'fixes', 'fixed' and 'reboot'
    :rtype: dict
    """
    before = doctor(fix_mode=True)
    by_name = before["by_name"]
    fixes = []

    # ── I2C ──────────────────────────────────────────────────────────────
    if by_name.get("I2C bus") is False or by_name.get("onboard MCU (0x14)") is False:
        if run(_as_root("raspi-config nonint do_i2c 0"), timeout=60)[0] == 0:
            fixes.append("enabled I2C")
        else:
            fixes.append("could not enable I2C (raspi-config failed)")
        run(_as_root("modprobe i2c-dev"), timeout=30)

    # ── audio configuration ──────────────────────────────────────────────
    audio_checks = ("I2S dtoverlay", "sound card", "capture device",
                    "asound.conf", "PulseAudio sink", "speaker volume")
    audio_setup_ran = False
    if any(by_name.get(name) is False for name in audio_checks):
        if _run_audio_setup():
            fixes.append("ran the Robot HAT audio setup (overlay, ALSA, PulseAudio)")
            audio_setup_ran = True
        else:
            fixes.append("could not run the audio setup script")

    # ── PulseAudio routing ───────────────────────────────────────────────
    # After the audio setup (which may restart PipeWire/PulseAudio) the sink
    # needs a moment to come back, so wait for it before setting it.
    if by_name.get("PulseAudio sink") is False or audio_setup_ran:
        profile = board_profile()
        sink = _wait_for_pa_node(pa_sinks, profile["card_names"])
        if sink and set_default_sink(sink.get("name", "")):
            fixes.append("set the PulseAudio default sink to the Robot HAT")
            set_sink_volume(100)
            if profile["has_mic"]:
                source = _wait_for_pa_node(pa_sources, profile["card_names"])
                if source:
                    set_default_source(source.get("name", ""))
                    set_source_volume(100)

    # ── hot speaker / stuck I2S ──────────────────────────────────────────
    if by_name.get("I2S clock (PCM)") is False:
        if prime_i2s():
            fixes.append("enabled the speaker and primed I2S with a short burst")

    # ── re-check ─────────────────────────────────────────────────────────
    after = _run_checks(show=False)
    reboot = False
    if after["by_name"].get("sound card") is False and after["by_name"].get("I2S dtoverlay"):
        reboot = True

    print("")
    print("  --- Fixes ---")
    if fixes:
        for action in fixes:
            print("  * %s" % action)
    else:
        print("  nothing to fix")
    print("")

    return {
        "before": before,
        "after": after,
        "fixes": fixes,
        "fixed": after["overall"],
        "reboot": reboot,
    }
