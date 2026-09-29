#!/usr/bin/env python3
"""
Command line interface of the Robot HAT library.

Usage: robot_hat [command]
"""

import argparse
import os
import sys


def _info(msg):
    from .utils import info
    info(msg)


def _warn(msg):
    from .utils import warn
    warn(msg)


def _deprecated(old, new):
    print("[WARN] '%s' is deprecated, use '%s' instead." % (old, new),
          file=sys.stderr)


def _audio_script():
    """Path of the bundled audio setup script ('' when it is missing)."""
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "scripts", "setup_robot_hat_audio.sh")
    return path if os.path.isfile(path) else ""


def _run_as_root(cmd):
    if os.geteuid() != 0:
        cmd = "sudo " + cmd
    return os.system(cmd)


# ---- commands --------------------------------------------------------------

def print_version():
    """Print the library version."""
    from .version import __version__
    print("Robot HAT library version: %s" % __version__)


def scan_i2c():
    """Scan the I2C bus."""
    from .i2c import I2C
    devices = ["0x%02X" % addr for addr in I2C().scan()]
    print("Found I2C devices: %s" % (", ".join(devices) if devices else "none"))


def reset_mcu():
    """Reset the onboard MCU."""
    from .device import reset_mcu as _reset_mcu
    _reset_mcu()
    _info("Onboard MCU reset.")


def enable_speaker():
    """Enable the speaker."""
    from .device import enable_speaker as _enable_speaker
    _enable_speaker()
    _info("Robot HAT speaker enabled.")


def disable_speaker():
    """Disable the speaker."""
    from .device import disable_speaker as _disable_speaker
    _disable_speaker()
    _info("Robot HAT speaker disabled.")


def test_speaker():
    """Play a test sound through the speaker."""
    from .audio import speaker_test
    if speaker_test():
        _info("Speaker test finished.")
    else:
        _warn("Speaker test failed - run 'robot_hat doctor' for details.")


def setup_speaker(skip_test=False):
    """Configure the I2S overlay, ALSA and PulseAudio for the speaker."""
    script = _audio_script()
    if not script:
        _warn("Audio setup script not found.")
        return
    print("Setting up the Robot HAT audio...")
    args = " --skip-test" if skip_test else ""
    status = _run_as_root("bash %s%s" % (script, args))
    if status == 0:
        _info("Audio setup finished.")
    else:
        _warn("Audio setup failed with exit code %s." % status)


def print_doctor(fix=False):
    """Run the health checks, optionally repairing what can be repaired."""
    os.system("sudo -v 2>/dev/null")
    if not fix:
        from .doctor import doctor
        doctor()
        return

    from .doctor import doctor_fix
    result = doctor_fix()
    after = result["after"]
    if result["fixed"]:
        print("  All checks pass now.")
    elif result["reboot"]:
        print("  Some changes need a reboot to take effect.")
    else:
        print("  Some checks still fail - see the report above.")
        print("  Report the result to service@sunfounder.com if it keeps failing.")

    if result["reboot"]:
        try:
            answer = input("  Reboot now? (y/N): ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            answer = ""
        if answer in ("y", "yes"):
            print("  Rebooting...")
            os.system("sudo reboot")
        else:
            print("  Reboot later with: sudo reboot")
    print("")


def print_info():
    """Print board, firmware and audio information."""
    from . import __device__ as device
    from . import get_firmware_version
    from .audio import board_profile, find_card, speaker_pin_state
    from .version import __version__

    profile = board_profile()
    data = {"Name": (device.name or "Robot HAT").replace("\x00", "").strip()}

    if device.uuid:
        data["PCB ID"] = "O%dV%d" % (device.product_id, device.product_ver)
        data["Vendor"] = (device.vendor or "").replace("\x00", "").strip()
        data["UUID"] = device.uuid
    else:
        data["HAT EEPROM"] = "not found (Robot HAT V4)"

    data["Library Version"] = __version__

    try:
        firmware = get_firmware_version()
        data["Firmware Version"] = "%s.%s.%s" % tuple(firmware[:3])
    except Exception as e:
        data["Firmware Version"] = "unknown (%s)" % e

    try:
        from .device import get_battery_voltage
        data["Battery Voltage"] = "%.2f V" % get_battery_voltage()
    except Exception:
        pass

    state = speaker_pin_state(profile["speaker_pin"])
    data["Speaker"] = "enabled" if state else ("disabled" if state is False else "unknown")

    index, _ = find_card(profile["card_names"])
    data["Sound Card"] = "hw:%s,0" % index if index is not None else "not found"

    print("")
    print("=" * 50)
    print("  Robot HAT Device Info")
    print("=" * 50)
    print("")
    for key, value in data.items():
        print("  %18s: %s" % (key, value))
    print("")
    print("=" * 50)
    print("")


def update():
    """Update the library from the install script."""
    from .version import __version__
    url = "https://raw.githubusercontent.com/sunfounder/robot-hat/2.5.x/install.sh"
    print("")
    print("  Current version: %s" % __version__)
    print("  Running installer: %s" % url)
    print("")
    status = os.system("curl -fsSL %s | sudo bash" % url)
    if status != 0:
        _warn("Installer exited with code %s" % status)


# ---- argument parsing ------------------------------------------------------

def main(argv=None):
    """Entry point of the 'robot_hat' command."""
    parser = argparse.ArgumentParser(
        prog="robot_hat", description="Robot HAT command line interface")
    sub = parser.add_subparsers(dest="option")

    p = sub.add_parser("doctor", help="Check the Robot HAT installation")
    p.add_argument("--fix", action="store_true", help="repair what can be repaired")
    p.set_defaults(_func=lambda a: print_doctor(fix=a.fix))

    speaker = sub.add_parser("speaker", help="Speaker control")
    speaker_sub = speaker.add_subparsers(dest="speaker_action")

    sp = speaker_sub.add_parser("enable", help="Enable the speaker")
    sp.set_defaults(_func=lambda a: enable_speaker())

    sp = speaker_sub.add_parser("disable", help="Disable the speaker")
    sp.set_defaults(_func=lambda a: disable_speaker())

    sp = speaker_sub.add_parser("test", help="Play a test sound")
    sp.set_defaults(_func=lambda a: test_speaker())

    sp = speaker_sub.add_parser("setup", help="Configure overlay, ALSA and PulseAudio")
    sp.add_argument("--skip-test", action="store_true", help="skip the speaker test")
    sp.set_defaults(_func=lambda a: setup_speaker(skip_test=a.skip_test))

    p = sub.add_parser("info", help="Show board and firmware information")
    p.set_defaults(_func=lambda a: print_info())

    p = sub.add_parser("version", help="Print the library version")
    p.set_defaults(_func=lambda a: print_version())

    p = sub.add_parser("scan_i2c", help="Scan the I2C bus")
    p.set_defaults(_func=lambda a: scan_i2c())

    p = sub.add_parser("reset_mcu", help="Reset the onboard MCU")
    p.set_defaults(_func=lambda a: reset_mcu())

    p = sub.add_parser("update", help="Update the library with install.sh")
    p.set_defaults(_func=lambda a: update())

    # deprecated top-level speaker commands, kept for existing scripts
    p = sub.add_parser("enable_speaker", help="[deprecated] use 'speaker enable'")
    p.set_defaults(_func=lambda a: (_deprecated("enable_speaker", "speaker enable"),
                                    enable_speaker()))

    p = sub.add_parser("disable_speaker", help="[deprecated] use 'speaker disable'")
    p.set_defaults(_func=lambda a: (_deprecated("disable_speaker", "speaker disable"),
                                    disable_speaker()))

    p = sub.add_parser("test_speaker", help="[deprecated] use 'speaker test'")
    p.set_defaults(_func=lambda a: (_deprecated("test_speaker", "speaker test"),
                                    test_speaker()))

    p = sub.add_parser("setup_speaker", help="[deprecated] use 'speaker setup'")
    p.add_argument("--skip-test", action="store_true", help="skip the speaker test")
    p.set_defaults(_func=lambda a: (_deprecated("setup_speaker", "speaker setup"),
                                    setup_speaker(skip_test=a.skip_test)))

    args = parser.parse_args(argv)

    if args.option is None:
        parser.print_help()
        return

    if args.option == "speaker" and getattr(args, "speaker_action", None) is None:
        speaker.print_help()
        return

    args._func(args)


if __name__ == "__main__":
    main()
