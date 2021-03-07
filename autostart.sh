#! /bin/bash

nitrogen --restore &
redshift-gtk &
pa-applet &
nm-applet --no-agent &
xscreensaver -no-splash &
setxkbmap -model pc104 -layout us,ua -option grp:alt_shift_toggle &
xinput set-prop 11 276 1
