#!/bin/bash
echo -e "\n \nWeather data checked via RSS from The National Weather Service every 5 to 15 minutes"
echo -e "- Press [CTRL+C] to stop \n \n"
echo -e "- Change state and county alerted on in storm2shutdown.py"
 
while true
do
 python3 storm2shutdown.py
 sleep 300
done
