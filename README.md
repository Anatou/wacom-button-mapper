# wacom-button-mapper
A CLI made with python that maps the buttons of your Wacom Tablet. 

I made this because of a bug preventing me from mapping my button over bluetooth. It uses xsetwacom to map the buttons of your wacom tablet and pen

This app is not finished, it's a minimium viable product because I'm lazy. Yes the code is ugly
## Dependences
python : os, json, subprocess, pyinput

You also need all the wacom drivers and library for your system too, which are already preinstalled for a lot of distributions nowaday. You specifically need xsetwacom as this app is basically a neater version of this tool
