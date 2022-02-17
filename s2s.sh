#!/bin/bash
clear

echo -e "\n \nWeather data obtained from The National Weather Service every 25 to 30 minutes"
echo -e "- Press [CTRL+C] to stop"
echo -e "- Change state and county alerted on in storm2shutdown.py \n\n"
#echo -e "- Change state for EPA energy mix data in egrid.py \n\n"

#python3 egrid.py

while true
do
 python3 storm2shutdown.py
 #python3 powertop.py
 sleep 1780
done
