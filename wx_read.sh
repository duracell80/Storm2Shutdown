#!/bin/bash
# $1 Tower Name: Acurite-Tower
# $2 Tower ID: 2235
# Run rtl_433 as a palin command to find tower name and id

echo "Scanning Local Weather Sensors on 433MHZ ..."

DATA_TEMP=$(rtl_433 -T 30 -C customary > wx_data.txt 2>&1 && cat wx_data.txt | grep -i -B 1 -A 5 "$1" | grep -i -A 4 "$2" | grep -i "Temperature" | uniq)
DATA_HUMI=$(cat wx_data.txt | grep -i -B 1 -A 5 "$1" | grep -i -A 4 "$2" | egrep -i "Humidity" | uniq)


IFS=': '
read -ra WX_TEMP <<< "$DATA_TEMP"
read -ra WX_HUMI <<< "$DATA_HUMI"

# Thunderstorm detector! Noice!
if [[ "$1" == *"Acurite-6045M"* ]]; then
	DATA_BOLT=$(cat wx_data.txt | grep -i -B 1 -A 7 "$1" | grep -i -A 6 "$2" | egrep -i "strike_count" | uniq)
	read -ra WX_BOLT <<< "$DATA_BOLT"

	DATA_MILE=$(cat wx_data.txt | grep -i -B 1 -A 7 "$1" | grep -i -A 6 "$2" | egrep -i "storm_distance" | uniq)
        read -ra WX_MILE <<< "$DATA_MILE"
fi

# Calculate the basic "Comfort Index"
DATA_COMF=$(bc -l <<< "((${WX_TEMP[1]}+${WX_HUMI[1]})/4)")
IFS='.'
read -ra WX_COMF <<< "$DATA_COMF"

# Friendly output
echo ""
echo "[i] $1 ($2)"
echo "[-] Temperature      : ${WX_TEMP[1]}F"
echo "[-] Humidity         : ${WX_HUMI[1]}%"
echo "[-] Comfort Index    : ${WX_COMF[0]}"

if [[ "$1" == *"Acurite-6045M"* && "${WX_MILE[1]}" -lt "30" ]]; then
	echo -e "[-] Stored Strikes   : ${WX_BOLT[1]}"
	echo -e "[-] No Storm Nearby"
else
	echo -e "[\u26A0] Stored Strikes   : ${WX_BOLT[1]}"
        echo -e "[\u26A0] Storm Distance   : ${WX_MILE[1]} Miles"
fi
