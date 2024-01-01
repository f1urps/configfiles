#!/bin/sh

run() {
    if ! pgrep -f "$1" ; then
        "$@" &
    fi
}

run picom
#run picom --experimental-backends
#run xscreensaver -no-splash
run xbindkeys

dropbox-cli start
xrandr --dpi 189 \
    --output DP-4 --scale 1 --pos 3840x2160 --preferred \
    --output DP-2 --scale 2 --pos 0x0 \
    --output HDMI-0 --scale 2 --pos 0x2160

nitrogen --restore

