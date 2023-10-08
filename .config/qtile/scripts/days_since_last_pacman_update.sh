#! /bin/bash

# This script will output the number of days since the last pacman system update.

days=$((($(date +%s) - $(date -d $(sed -n '/upgrade$/x;${x;s/.\([0-9-]*\).*/\1/p}' /var/log/pacman.log) +%s)) / 86400))
echo $days


