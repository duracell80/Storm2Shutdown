#!/bin/bash
while true
do
 echo -e "\n \n- Data checked every 5 to 15 minutes"
 echo -e "- Run in Chron or with & to background"
 echo -e "- Press [CTRL+C] to stop \n \n"
 python3 storm2shutdown.py
 sleep 600
done
