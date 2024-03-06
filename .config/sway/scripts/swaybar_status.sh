#! /usr/bin/bash

function __swaybar_status {
    local func
    local interval='0.1'
    case "$(cat /etc/hostname)" in
        ripley) func=__swaybar_status_ripley;;
        viviancox-glaptop) func=__swaybar_status_glaptop;;
        *) echo >&2 "Error: I don't know this machine!"; return 1;;
    esac
    while $func; do sleep $interval; done
}

function __swaybar_status_ripley {
    local datetime="$(date +'%Y-%m-%d %I:%M:%S %p')"
    local volume="$(pamixer --get-volume-human)"
    local pacman="$(__swaybar_status_pacman)"
    local dropbox="$(__swaybar_status_dropbox)"
    echo "$dropbox | $pacman | $volume | $datetime "
}

function __swaybar_status_glaptop {
    local datetime="$(date +'%Y-%m-%d %I:%M:%S %p')"
    local volume="$(pamixer --get-volume-human)"
    local battery="$(__swaybar_status_battery)"
    echo "$battery | $volume | $datetime "
}

function __swaybar_status_pacman {
    local date_today="$(date +%s)"
    local date_last_update="$(sed -n '/upgrade$/x;${x;s/.\([0-9-]*\).*/\1/p}' /var/log/pacman.log | xargs date +%s -d)"
    local days="$(( ("$date_today" - "$date_last_update") / 86400 ))"
    local days_fmt="${days}d"
    if [[ "$days" -ge "14" ]]; then
        days_fmt="<span foreground=\"red\">$days_fmt</span>"
    fi
    echo "$days_fmt"
}

function __swaybar_status_dropbox {
    local status="$(dropbox-cli status 2>/dev/null)"
    if echo "$status" | grep -q "Dropbox isn't running!"; then
        echo "<span foreground=\"red\">!!</span>"
    elif echo "$status" | grep -q 'Syncing'; then
        echo "Syncing..."
    elif echo "$status" | grep -q 'Up to date'; then
        echo "✓"
    else
        echo "?"
    fi
}

function __swaybar_status_battery {
    local battery_info_dir='/sys/class/power_supply/BAT0'
    if [[ ! -d "$battery_info_dir" ]]; then
        return 0
    fi
    local battery_status=$(cat "$battery_info_dir/status")
    local battery_capacity=$(cat "$battery_info_dir/capacity")
    local battery_percent="$battery_capacity%"
    if [[ "$battery_capacity" -le "25" ]]; then
        battery_percent="<span foreground=\"red\">$battery_percent</span>"
    fi
    local charging_symbol="🗲 "
    if [[ "$battery_status" == "Charging" ]]; then
        echo -n "$charging_symbol"
    fi
    echo "$battery_percent"
}

__swaybar_status

