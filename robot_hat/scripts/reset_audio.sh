#!/bin/bash
# =============================================================================
#  Reset the Robot HAT audio configuration
# =============================================================================
#  Undoes everything setup_robot_hat_audio.sh changed, so the audio path can
#  be built up again from a clean state. Useful while testing, or when the
#  sound card was configured for another HAT before.
#
#  Usage:
#    sudo bash reset_audio.sh
# =============================================================================
set -e

if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root: sudo bash $0"
    exit 1
fi

echo "Resetting the Robot HAT audio configuration..."

ASOUND_CONF="/etc/asound.conf"

if [ -f "$ASOUND_CONF" ]; then
    rm -f "$ASOUND_CONF"
    echo "  removed $ASOUND_CONF"
fi
if [ -f "$ASOUND_CONF.old" ]; then
    rm -f "$ASOUND_CONF.old"
    echo "  removed $ASOUND_CONF.old"
fi

# custom PipeWire / WirePlumber rules
for f in /etc/wireplumber/main.lua.d/*robot* \
         /etc/pipewire/pipewire.conf.d/*robot* \
         /usr/share/pipewire/pipewire.conf.d/*robot* \
         /etc/pipewire/pipewire-pulse.conf.d/*robot*; do
    if [ -f "$f" ]; then
        rm -f "$f"
        echo "  removed $f"
    fi
done

# dynamic device tree overlays loaded by the setup script
for overlay in hifiberry-dac googlevoicehat-soundcard; do
    dtoverlay -r "$overlay" >/dev/null 2>&1 && echo "  removed dynamic overlay $overlay" || true
done

# restart the audio services of every desktop user
for home_dir in /home/*; do
    [ -d "$home_dir" ] || continue
    user_name=$(stat -c '%U' "$home_dir" 2>/dev/null)
    [ -n "$user_name" ] || continue
    user_uid=$(id -u "$user_name" 2>/dev/null) || continue
    [ "$user_uid" -ge 1000 ] 2>/dev/null || continue
    sudo -u "$user_name" env XDG_RUNTIME_DIR="/run/user/$user_uid" \
        DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/$user_uid/bus" \
        systemctl --user restart pipewire pipewire-pulse wireplumber >/dev/null 2>&1 || true
    sudo -u "$user_name" env XDG_RUNTIME_DIR="/run/user/$user_uid" \
        pulseaudio -k >/dev/null 2>&1 || true
done

systemctl restart alsa-utils >/dev/null 2>&1 || true

echo ""
echo "Reset complete. config.txt was not changed."
echo "Run 'sudo bash setup_robot_hat_audio.sh' to configure the audio again."
