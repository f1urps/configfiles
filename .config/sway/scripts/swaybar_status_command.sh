#! /usr/bin/bash

function _print_status() {
    local datetime=$(date +'%Y-%m-%d %I:%M:%S %p')
    #local battery_message=$(_get_battery_message)
    #echo "$battery_message | $datetime"
    echo "$datetime"
}

function _get_battery_message() {
    local battery_capacity=$(cat /sys/class/power_supply/BAT0/capacity)
    local battery_status=$(cat /sys/class/power_supply/BAT0/status)
    local battery_percent="$battery_capacity%"
    if [[ "$battery_capacity" -le "25" ]]; then
        battery_percent="<span foreground=\"red\">$battery_percent</span>"
    fi
    local battery_symbol=
    if [[ "$battery_status" == "Charging" ]]; then
        battery_symbol="🗲 "
    fi
    echo "$battery_symbol$battery_percent"
}

# Print a new status every second.
while _print_status; do sleep 1; done

