#!/bin/bash
echo -e "RTL_433 Weather Sensor Monitor Loop"
echo -e "Press [CTRL+X] to exit"
echo ""
echo ""

while true
do
	../sensors/wx_front.sh
	../sensors/wx_porch.sh
	../sensors/wx_storm.sh
	../sensors/wx_kitchen.sh
	../sensors/wx_bedroom.sh
	sleep 240
done
