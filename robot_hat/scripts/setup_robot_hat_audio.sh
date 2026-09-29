#!/bin/bash
# =============================================================================
#  Robot HAT Audio Setup
# =============================================================================
#  Configures the I2S sound card, ALSA and PulseAudio for the Robot HAT
#  (V4 and V5). Run it once after installing the library - the settings
#  survive a reboot.
#
#  Usage:
#    sudo bash setup_robot_hat_audio.sh               # setup + speaker test
#    sudo bash setup_robot_hat_audio.sh --skip-test   # no speaker test
#    sudo bash setup_robot_hat_audio.sh --no-deps     # skip the apt install
# =============================================================================

set -e

VERSION="1.0.0"

SKIP_TEST=false
SKIP_DEPS=false
for arg in "$@"; do
    case $arg in
        --skip-test) SKIP_TEST=true ;;
        --no-deps)   SKIP_DEPS=true ;;
    esac
done

if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root: sudo bash $0"
    exit 1
fi

# ---- output helpers ---------------------------------------------------------
GREEN='\033[32m'; YELLOW='\033[33m'; CYAN='\033[36m'; RED='\033[31m'
BOLD='\033[1m'; RESET='\033[0m'
ok()   { printf "  %b%s%b %s\n" "$GREEN" "v" "$RESET" "$1"; }
warn() { printf "  %b%s%b %s\n" "$YELLOW" "!" "$RESET" "$1"; }
info() { printf "  %b%s%b %s\n" "$CYAN" "-" "$RESET" "$1"; }
fail() { printf "  %b%s%b %s\n" "$RED" "x" "$RESET" "$1"; }
stage() { printf "\n%b-- %s --%b\n" "$BOLD" "$1" "$RESET"; }

# ---- configuration ----------------------------------------------------------
CONFIG="/boot/firmware/config.txt"
if [ ! -f "$CONFIG" ]; then
    CONFIG="/boot/config.txt"
fi
ASOUND_CONF="/etc/asound.conf"

# Robot HAT V4 - HiFiBerry DAC (no onboard microphone)
DTOVERLAY_WITHOUT_MIC="hifiberry-dac"
AUDIO_CARD_WITHOUT_MIC="sndrpihifiberry"
ALSA_CARD_WITHOUT_MIC="snd_rpi_hifiberry_dac"

# Robot HAT V5 - Google Voice HAT sound card (onboard microphone)
DTOVERLAY_WITH_MIC="googlevoicehat-soundcard"
AUDIO_CARD_WITH_MIC="sndrpigooglevoi"
ALSA_CARD_WITH_MIC="snd_rpi_googlevoicehat_soundcar"

SOFTVOL_SPEAKER_NAME="robot-hat speaker"
SOFTVOL_MIC_NAME="robot-hat mic"

ROBOTHAT5_UUID="9daeea78-0000-076e-0032-582369ac3e02"
ROBOTHAT5_PRODUCT_VER=50

BOARD_REV="V4"
HAS_MIC=false
SPEAKER_PIN=20
DTOVERLAY_NAME="$DTOVERLAY_WITHOUT_MIC"
AUDIO_CARD_NAME="$AUDIO_CARD_WITHOUT_MIC"
ALSA_CARD_NAME="$ALSA_CARD_WITHOUT_MIC"

echo ""
echo "================================================"
echo "  Robot HAT Audio Setup  v$VERSION"
echo "================================================"

# ---- board detection --------------------------------------------------------
detect_board() {
    local hat_dir=""
    local dir uuid product_ver

    # find(1) cannot walk /proc/device-tree, so glob the HAT nodes instead.
    # The board revision is decided by the HAT EEPROM UUID, exactly like
    # robot_hat/device.py does it.
    for dir in /proc/device-tree/*hat*; do
        [ -d "$dir" ] || continue
        [ -f "$dir/uuid" ] || continue
        uuid=$(tr -d '\0' < "$dir/uuid")
        if [ "$uuid" = "$ROBOTHAT5_UUID" ]; then
            hat_dir="$dir"
            BOARD_REV="V5"
            break
        fi
    done

    if [ -z "$hat_dir" ]; then
        BOARD_REV="V4"
        info "no Robot HAT 5 EEPROM, assuming Robot HAT V4"
        return
    fi

    product_ver=$(tr -d '\0' < "$hat_dir/product_ver" 2>/dev/null)
    [ -n "$product_ver" ] && info "HAT product_ver: $product_ver"
    if [ -f "$hat_dir/product" ]; then
        info "HAT: $(tr -d '\0' < "$hat_dir/product")"
    fi
}

apply_profile() {
    if [ "$BOARD_REV" = "V5" ]; then
        HAS_MIC=true
        SPEAKER_PIN=12
        DTOVERLAY_NAME="$DTOVERLAY_WITH_MIC"
        AUDIO_CARD_NAME="$AUDIO_CARD_WITH_MIC"
        ALSA_CARD_NAME="$ALSA_CARD_WITH_MIC"
    else
        HAS_MIC=false
        SPEAKER_PIN=20
        DTOVERLAY_NAME="$DTOVERLAY_WITHOUT_MIC"
        AUDIO_CARD_NAME="$AUDIO_CARD_WITHOUT_MIC"
        ALSA_CARD_NAME="$ALSA_CARD_WITHOUT_MIC"
    fi
}

# ---- stages -----------------------------------------------------------------
install_dependencies() {
    stage "Dependencies"
    if [ "$SKIP_DEPS" = true ]; then
        info "skipped (--no-deps)"
        return
    fi
    info "apt update"
    apt-get update -qq >/dev/null 2>&1 || true
    info "install alsa-utils pulseaudio pulseaudio-utils jq sox"
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
        alsa-utils pulseaudio pulseaudio-utils jq sox >/dev/null 2>&1 || true
    ok "dependencies ready"
}

configure_overlay() {
    stage "Sound card"
    if [ ! -f "$CONFIG" ]; then
        fail "$CONFIG not found"
        exit 1
    fi

    if grep -q "^dtoverlay=$DTOVERLAY_NAME" "$CONFIG"; then
        info "dtoverlay=$DTOVERLAY_NAME already enabled"
    elif grep -q "dtoverlay=$DTOVERLAY_NAME" "$CONFIG"; then
        # present but commented out - uncomment it
        sed -i "s|^#*dtoverlay=$DTOVERLAY_NAME.*|dtoverlay=$DTOVERLAY_NAME|" "$CONFIG"
        info "enabled dtoverlay=$DTOVERLAY_NAME"
    else
        echo "dtoverlay=$DTOVERLAY_NAME" >> "$CONFIG"
        info "added dtoverlay=$DTOVERLAY_NAME"
    fi

    # make sure the overlay of the other revision is commented out
    if [ "$HAS_MIC" = true ]; then
        sed -i "s|^dtoverlay=$DTOVERLAY_WITHOUT_MIC.*|#dtoverlay=$DTOVERLAY_WITHOUT_MIC|" "$CONFIG"
    else
        sed -i "s|^dtoverlay=$DTOVERLAY_WITH_MIC.*|#dtoverlay=$DTOVERLAY_WITH_MIC|" "$CONFIG"
    fi
    ok "config.txt updated ($CONFIG)"

    # try to load it right away so a reboot is not strictly required
    info "loading dtoverlay $DTOVERLAY_NAME"
    dtoverlay "$DTOVERLAY_NAME" >/dev/null 2>&1 || true
    sleep 1
}

configure_alsa() {
    stage "ALSA config"

    card_index=$(aplay -l 2>/dev/null | grep "$AUDIO_CARD_NAME" | awk '{print $2}' | tr -d ':' | head -n 1)
    if [ -z "$card_index" ]; then
        warn "sound card not found - reboot and run this script again"
        return 1
    fi
    ok "sound card found (hw:$card_index,0)"

    if [ -f "$ASOUND_CONF" ]; then
        cp "$ASOUND_CONF" "$ASOUND_CONF.old" 2>/dev/null || true
    fi

    if [ "$HAS_MIC" = true ]; then
        cat > "$ASOUND_CONF" <<EOF

pcm.robothat {
    type asym
    playback.pcm { type plug; slave.pcm "speaker" }
    capture.pcm  { type plug; slave.pcm "mic" }
}

pcm.speaker_hw {
    type hw
    card $AUDIO_CARD_NAME
    device 0
}

pcm.dmixer {
    type dmix
    ipc_key 1024
    ipc_perm 0666
    slave {
        pcm "speaker_hw"
        period_time 0
        period_size 1024
        buffer_size 8192
        rate 44100
        channels 2
    }
}

ctl.dmixer { type hw; card $AUDIO_CARD_NAME }

pcm.speaker {
    type softvol
    slave { pcm "dmixer" }
    control { name "$SOFTVOL_SPEAKER_NAME Playback Volume"; card $AUDIO_CARD_NAME }
    min_dB -51.0
    max_dB 0.0
}

pcm.mic_hw { type hw; card $AUDIO_CARD_NAME; device 0 }

pcm.mic {
    type softvol
    slave { pcm "mic_hw" }
    control { name "$SOFTVOL_MIC_NAME Capture Volume"; card $AUDIO_CARD_NAME }
    min_dB -26.0
    max_dB 25.0
}

ctl.robothat { type hw; card $AUDIO_CARD_NAME }

pcm.!default robothat
ctl.!default robothat

EOF
    else
        cat > "$ASOUND_CONF" <<EOF

pcm.speaker {
    type hw
    card $AUDIO_CARD_NAME
}

pcm.dmixer {
    type dmix
    ipc_key 1024
    ipc_perm 0666
    slave {
        pcm "speaker"
        period_time 0
        period_size 1024
        buffer_size 8192
        rate 44100
        channels 2
    }
}

ctl.dmixer {
    type hw
    card $AUDIO_CARD_NAME
}

pcm.softvol {
    type softvol
    slave.pcm "dmixer"
    control {
        name "$SOFTVOL_SPEAKER_NAME Playback Volume"
        card $AUDIO_CARD_NAME
    }
    min_dB -51.0
    max_dB 0.0
}

pcm.robothat {
    type plug
    slave.pcm "softvol"
}

ctl.robothat { type hw; card $AUDIO_CARD_NAME }

pcm.!default robothat
ctl.!default robothat

EOF
    fi
    ok "wrote $ASOUND_CONF"

    systemctl restart alsa-utils >/dev/null 2>&1 || true

    # a short burst creates the softvol control, then set it to 100%
    play -n trim 0.0 0.5 >/dev/null 2>&1 || true
    amixer -c "$AUDIO_CARD_NAME" sset "$SOFTVOL_SPEAKER_NAME" 100% >/dev/null 2>&1 || true
    ok "speaker volume 100%"

    if [ "$HAS_MIC" = true ]; then
        rec /tmp/_robot_hat_mic.wav trim 0 0.5 >/dev/null 2>&1 || true
        amixer -c "$AUDIO_CARD_NAME" sset "$SOFTVOL_MIC_NAME" 100% >/dev/null 2>&1 || true
        rm -f /tmp/_robot_hat_mic.wav
        ok "microphone volume 100%"
    fi
    return 0
}

pa_node_name() {
    # pa_node_name sinks|sources - name of the node of the Robot HAT sound card
    local kind="$1"
    $RUN_AS pactl -f json list "$kind" 2>/dev/null | jq -r \
        ".[] | select(.properties[\"alsa.card_name\"] == \"$ALSA_CARD_NAME\" and .properties[\"device.class\"] == \"sound\") | .name" 2>/dev/null | head -n 1
}

configure_pulseaudio() {
    stage "PulseAudio"

    USERNAME=$(getent passwd 1000 | cut -d: -f1)
    if [ -z "$USERNAME" ]; then
        warn "no desktop user (uid 1000) - skipping PulseAudio"
        return 0
    fi
    USER_UID=$(id -u "$USERNAME")
    RUN_AS="sudo -u $USERNAME env XDG_RUNTIME_DIR=/run/user/$USER_UID DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$USER_UID/bus"

    raspi-config nonint do_audioconf 1 >/dev/null 2>&1 || true
    $RUN_AS pulseaudio -D >/dev/null 2>&1 || true
    sleep 1

    # The sound card takes a moment to show up in PipeWire/PulseAudio, and the
    # audio system may have to be restarted after the overlay was loaded.
    local sink_name="" i
    for i in 1 2 3 4 5 6 7 8 9 10; do
        sink_name=$(pa_node_name sinks)
        [ -n "$sink_name" ] && [ "$sink_name" != "null" ] && break
        sleep 1
    done
    if [ -z "$sink_name" ] || [ "$sink_name" = "null" ]; then
        info "restarting the user audio services"
        $RUN_AS systemctl --user restart pipewire pipewire-pulse wireplumber >/dev/null 2>&1 || true
        sleep 4
        for i in 1 2 3 4 5; do
            sink_name=$(pa_node_name sinks)
            [ -n "$sink_name" ] && [ "$sink_name" != "null" ] && break
            sleep 1
        done
    fi
    if [ -z "$sink_name" ] || [ "$sink_name" = "null" ]; then
        warn "sound card sink not found - reboot and run this script again"
        return 0
    fi

    $RUN_AS pactl set-default-sink "$sink_name" >/dev/null 2>&1 || true
    $RUN_AS pactl set-sink-volume @DEFAULT_SINK@ 100% >/dev/null 2>&1 || true
    ok "default sink: $sink_name"

    if [ "$HAS_MIC" = true ]; then
        local source_name=""
        for i in 1 2 3 4 5; do
            source_name=$(pa_node_name sources)
            [ -n "$source_name" ] && [ "$source_name" != "null" ] && break
            sleep 1
        done
        if [ -n "$source_name" ] && [ "$source_name" != "null" ]; then
            $RUN_AS pactl set-default-source "$source_name" >/dev/null 2>&1 || true
            $RUN_AS pactl set-source-volume @DEFAULT_SOURCE@ 100% >/dev/null 2>&1 || true
            ok "default source: $source_name"
        fi
    fi
}

enable_speaker_pin() {
    # The amplifier is enabled with a GPIO. Before enabling it, make sure the
    # I2S peripheral has data - a short silence burst avoids a hot speaker.
    if command -v pinctrl >/dev/null 2>&1; then
        pinctrl set "$SPEAKER_PIN" op dh >/dev/null 2>&1 || true
    elif command -v raspi-gpio >/dev/null 2>&1; then
        raspi-gpio set "$SPEAKER_PIN" op dh >/dev/null 2>&1 || true
    else
        warn "pinctrl/raspi-gpio not found - cannot enable the speaker"
    fi
    play -n trim 0.0 0.5 >/dev/null 2>&1 || true
}

test_speaker() {
    stage "Speaker test"
    enable_speaker_pin
    info "playing a test sound"
    if speaker-test -l 3 -c 2 -t wav >/dev/null 2>&1; then
        ok "speaker test passed"
    elif aplay /usr/share/sounds/alsa/Front_Center.wav >/dev/null 2>&1; then
        ok "speaker test passed"
    else
        warn "speaker test failed - run 'robot_hat doctor' for details"
    fi
}

# ---- main -------------------------------------------------------------------
stage "Board"
detect_board
apply_profile
ok "Robot HAT $BOARD_REV - $DTOVERLAY_NAME, speaker on GPIO$SPEAKER_PIN"

install_dependencies
configure_overlay
configure_alsa || true
configure_pulseaudio

if [ "$SKIP_TEST" = false ]; then
    test_speaker
fi

echo ""
printf "%b%s%b\n" "$GREEN$BOLD" "Audio setup complete" "$RESET"
echo ""
echo "  Test the speaker:  robot_hat speaker test"
echo "  Health check:      robot_hat doctor"
echo ""
