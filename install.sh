#!/bin/bash
# =============================================================================
#  Robot HAT Installer
#  =============================================================================
#  One-command install:
#    curl -sSL https://raw.githubusercontent.com/sunfounder/robot-hat/2.5.x/install.sh | sudo bash
#
#  A specific branch, for testing:
#    ROBOT_HAT_BRANCH=develop sudo -E bash install.sh
#
#  Run inside a checkout of this repository and the checkout is used as is,
#  instead of cloning a fresh copy into the home directory.
#  =============================================================================

set -e

# ---- branch overrides -------------------------------------------------------
ROBOT_HAT_BRANCH="${ROBOT_HAT_BRANCH:-2.5.x}"
INSTALLER_BRANCH="${INSTALLER_BRANCH:-main}"

INSTALLER_URL="https://raw.githubusercontent.com/sunfounder/sunfounder-installer-scripts/refs/heads/${INSTALLER_BRANCH}/tools/installer_1.1.0.sh"

# ---- shared installer utilities --------------------------------------------
curl -fsSL "$INSTALLER_URL" -o /tmp/installer.sh
if [ $? -ne 0 ]; then
    echo "Network error: failed to download installer utilities."
    echo "Please check your internet connection."
    exit 1
fi
source /tmp/installer.sh
rm -f /tmp/installer.sh

# ---- dependencies -----------------------------------------------------------
APT_INSTALL_LIST=(
    "git"
    "python3"
    "python3-pip"
    "python3-dev"
    "python3-venv"
    "i2c-tools"
    "raspi-config"
    "espeak"
    "libsdl2-dev"
    "libsdl2-mixer-dev"
    "portaudio19-dev"
    "sox"
    "libsox-fmt-mp3"
    "libttspico-utils"
    # runtime dependencies of the library, as Debian packages so that no
    # python package has to be compiled on the Pi
    "python3-smbus2"
    "python3-lgpio"
    "python3-gpiozero"
    "python3-pyaudio"
    "python3-pygame"
    "python3-pil"
    "python3-serial"
    "python3-spidev"
)

# ---- arguments --------------------------------------------------------------
SKIP_AUDIO_TEST=true
for arg in "$@"; do
    case $arg in
        --plain-text) ;;
        --test)      SKIP_AUDIO_TEST=false ;;
        --skip-test) SKIP_AUDIO_TEST=true ;;
    esac
done

# ---- pip flags --------------------------------------------------------------
# Debian 12 (Bookworm) and later refuse system wide pip installs unless
# --break-system-packages is given; older releases do not know the flag.
IS_BSPS=""
if pip3 help install 2>/dev/null | grep -q break-system-packages; then
    IS_BSPS="--break-system-packages"
fi

# ---- install ----------------------------------------------------------------
TITLE "Install Robot HAT\n"

TITLE "Install dependencies"
RUN "apt-get update" "Update apt"
RUN "apt-get install -y ${APT_INSTALL_LIST[*]}" "Install apt dependencies"

# Use the checkout this script lives in when there is one (running the script
# from a git clone must not delete that clone).
SCRIPT_PATH=$(readlink -f "$0" 2>/dev/null || echo "$0")
SCRIPT_DIR=$(cd "$(dirname "$SCRIPT_PATH")" 2>/dev/null && pwd)
if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/pyproject.toml" ] && [ -f "$SCRIPT_DIR/robot_hat/version.py" ]; then
    ROBOT_HAT_DIR="$SCRIPT_DIR"
    TITLE "Install robot-hat library (existing checkout)"
    RUN "chown -R ${USERNAME}:${USERNAME} $ROBOT_HAT_DIR" "Change ownership to ${USERNAME}"
else
    TITLE "Install robot-hat library"
    CD "$HOME/" "Change to home directory"
    RUN "rm -rf $HOME/robot-hat" "Remove existing robot-hat library"
    CLONE "robot-hat" "${ROBOT_HAT_BRANCH}"
    if [ $? -ne 0 ]; then
        installer_log_failed "Failed to clone robot-hat."
        exit 1
    fi
    ROBOT_HAT_DIR="$HOME/robot-hat"
    RUN "chown -R ${USERNAME}:${USERNAME} $ROBOT_HAT_DIR" "Change ownership to ${USERNAME}"
fi

TITLE "Install Python library"
CD "$ROBOT_HAT_DIR" "Change to robot-hat directory"
RUN "pip3 install . $IS_BSPS" "Install robot_hat"

TITLE "Enable interfaces"
RUN "raspi-config nonint do_i2c 0" "Enable I2C"
RUN "raspi-config nonint do_spi 0" "Enable SPI"

TITLE "Install device tree overlays"
RUN "cp $ROBOT_HAT_DIR/dtoverlays/*.dtbo /boot/firmware/overlays/ 2>/dev/null || cp $ROBOT_HAT_DIR/dtoverlays/*.dtbo /boot/overlays/" \
    "Copy device tree overlays"

TITLE "Install sunfounder-voice-assistant"
CD "$HOME/" "Change to home directory"
RUN "rm -rf $HOME/sunfounder-voice-assistant" "Remove existing sunfounder-voice-assistant"
CLONE "sunfounder-voice-assistant" "main"
CD "$HOME/sunfounder-voice-assistant" "Change to sunfounder-voice-assistant directory"
RUN "pip3 install . $IS_BSPS" "Install sunfounder-voice-assistant"

TITLE "Setup audio"
if [ "$SKIP_AUDIO_TEST" = true ]; then
    RUN "bash $ROBOT_HAT_DIR/robot_hat/scripts/setup_robot_hat_audio.sh --skip-test" "Configure the I2S sound card"
else
    RUN "bash $ROBOT_HAT_DIR/robot_hat/scripts/setup_robot_hat_audio.sh" "Configure the I2S sound card"
fi

installer_install

installer_prompt_reboot "After the reboot run 'robot_hat doctor' to check the installation, then 'robot_hat speaker test'."
