# Robot Hat

Robot Hat Python library for Raspberry Pi.

Quick Links:

- [Robot Hat](#robot-hat)
  - [About Robot Hat](#about-robot-hat)
  - [Update](#update)
  - [Installation](#installation)
  - [Command line tools](#command-line-tools)
  - [Debug commands](#debug-commands)
  - [Trouble Shooting](#trouble-shooting)
  - [About SunFounder](#about-sunfounder)
  - [License](#license)
  - [Contact us](#contact-us)

## About Robot Hat

Robot HAT is a multifunctional expansion board that allows Raspberry Pi to be quickly turned into a robot. An MCU is on board to extend the PWM output and ADC input for the Raspberry Pi, as well as a motor driver chip, Bluetooth module, I2S audio module and mono speaker. As well as the GPIOs that lead out of the Raspberry Pi itself.


## Update
2026-09-29:
- Add `robot_hat doctor`: one command that checks the HAT, the I2C bus to the onboard MCU, the GPIO setup, the installed library and dependencies, and the whole I2S audio path (overlay, sound card, ALSA, PulseAudio, speaker enable pin, I2S clock). `robot_hat doctor --fix` repairs the common problems automatically
- Add `robot_hat speaker enable|disable|test|setup` and the bundled `robot_hat/scripts/setup_robot_hat_audio.sh` audio setup for Robot HAT V4 and V5, including the fix for a hot speaker (the amplifier is always primed with a short burst, so the I2S clocks never run without data)
- Add `install.sh`: a one command installer built on the shared SunFounder installer utilities, the same way Fusion HAT installs
- `robot_hat` now has a proper command line interface; the old `enable_speaker` / `disable_speaker` commands keep working

2026-09-11:
- Fix `can not open gpiochip` on Raspberry Pi 5: the GPIO chip that drives the 40-pin header is now auto-detected instead of hard-coding `gpiochip0`, because the kernel has renumbered it more than once (`ROBOT_HAT_GPIOCHIP` can force a number if needed)

2023-11-29:
- Add more about Robot HAT's Hardware Introduction


2022-08-26:
- New Release

## Installation

### One command

```bash
curl -sSL https://raw.githubusercontent.com/sunfounder/robot-hat/2.5.x/install.sh | sudo bash
```

The installer clones the library, installs the dependencies, enables I2C and
SPI, copies the device tree overlays, configures the I2S sound card and asks
for a reboot. To test another branch:

```bash
curl -sSL https://raw.githubusercontent.com/sunfounder/robot-hat/2.5.x/install.sh | sudo ROBOT_HAT_BRANCH=develop bash
```

### From a git clone

```bash
git clone https://github.com/sunfounder/robot-hat.git -b 2.5.x
cd robot-hat
sudo bash install.sh
# or the older python installer, it does the same thing
sudo python3 install.py
```

### Speaker

The speaker is driven over I2S, so the sound card has to be configured once
(the installer already does this):

```bash
sudo robot_hat speaker setup
robot_hat speaker test
```

## Command line tools

```bash
robot_hat doctor              # check the whole installation, one line per check
robot_hat doctor --fix        # repair the common problems, then report again
robot_hat speaker enable      # turn the onboard amplifier on
robot_hat speaker disable     # turn the onboard amplifier off
robot_hat speaker test        # play a test sound
robot_hat speaker setup       # configure the I2S overlay, ALSA and PulseAudio
robot_hat info                # board, firmware, library and audio information
robot_hat scan_i2c            # scan the I2C bus
robot_hat reset_mcu           # reset the onboard MCU
robot_hat version
robot_hat update              # re-run install.sh
```

`robot_hat doctor` is the place to start when something does not work. It
checks, in order:

- **Board** - HAT EEPROM identification, I2C bus, the onboard MCU at 0x14, the
  GPIO chip and `pinctrl`/`raspi-gpio`
- **Library** - the installed `robot_hat` version, the Python modules it
  imports and the audio tools (`aplay`, `amixer`, `sox`, `pactl`, `jq`)
- **Audio** - the I2S overlay in `config.txt`, the sound card, the microphone
  (V5), `/etc/asound.conf`, the PulseAudio default sink, the speaker volume,
  the speaker enable pin and the I2S clock

The last one is the reason why a speaker can get hot: if the I2S clocks keep
running without data, the amplifier drives the speaker with a DC offset.
`robot_hat doctor --fix` re-configures the audio path and primes the I2S
peripheral with a short burst; the library does the same every time it enables
the speaker.

## Debug commands

All command records for debug

```bash
cd ~/robot-hat && git pull && sudo pip3 install . --break --no-deps --no-build-isolation
sudo pip3 uninstall -y robot_hat --break && sudo pip3 install ~/robot-hat --break --no-deps --no-build-isolation

sudo python3 ~/robot-hat/examples/tts_piper.py
sudo python3 ~/robot-hat/examples/stt_vosk_stream.py
```


## Trouble Shooting

Run `robot_hat doctor` first, it names the part that is broken. The usual cases:

### The HAT is not detected, I2C errors

- Check the HAT is pushed all the way onto the 40-pin header, then run
  `robot_hat doctor`. If `I2C bus` fails the bus is still disabled
  (`sudo raspi-config nonint do_i2c 0`, or `robot_hat doctor --fix`)
- If `onboard MCU (0x14)` fails but I2C works, the MCU does not answer:
  `robot_hat reset_mcu` and check `robot_hat scan_i2c`

### No sound

- `robot_hat speaker test` plays the ALSA test sound
- `robot_hat doctor` and read the **Audio** section
- `sound card` fails right after the overlay was enabled: reboot, the
  overlay is only loaded during boot
- `PulseAudio sink` fails: audio is going to the headphone jack instead of
  the HAT. `robot_hat doctor --fix` or `sudo robot_hat speaker setup`
- `speaker volume` fails: `amixer -c sndrpihifiberry sset 'robot-hat speaker' 100%`
  (V5: `sndrpigooglevoi`)

### The speaker gets hot while nothing is playing

The amplifier is enabled by a GPIO and the I2S clocks keep running even when
there is no audio. Without data the amplifier drives the speaker with a DC
offset, which heats the coil. The library always sends a short silence burst
directly after it enables the speaker, and `robot_hat speaker disable` turns
the amplifier off when it is not needed.

- `robot_hat doctor` reports a stuck I2S clock under `I2S clock (PCM)`
- `robot_hat speaker disable` then `robot_hat speaker enable` to reset the bus
- `robot_hat doctor --fix` does both and re-checks

### The library was installed but `import robot_hat` fails

- `robot_hat doctor` lists the missing Python modules and audio tools
- `pip3 install ./ --break-system-packages` inside the checkout reinstalls it

----------------------------------------------

## About SunFounder

SunFounder is a technology company focused on Raspberry Pi and Arduino open source community development. Committed to the promotion of open source culture, we strives to bring the fun of electronics making to people all around the world and enable everyone to be a maker. Our products include learning kits, development boards, robots, sensor modules and development tools. In addition to high quality products, SunFounder also offers video tutorials to help you make your own project. If you have interest in open source or making something cool, welcome to join us!

----------------------------------------------

## License

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied wa rranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

{Repository Name} comes with ABSOLUTELY NO WARRANTY; for details run ./show w. This is free software, and you are welcome to redistribute it under certain conditions; run ./show c for details.

SunFounder, Inc., hereby disclaims all copyright interest in the program '{Repository Name}' (which makes passes at compilers).

Mike Huang, 21 August 2015

Mike Huang, Chief Executive Officer

Email: service@sunfounder.com, support@sunfounder.com

----------------------------------------------

## Contact us

website:
    www.sunfounder.com

E-mail:
    service@sunfounder.com, support@sunfounder.com
