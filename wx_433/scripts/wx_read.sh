#!/bin/bash
# $1 Tower Name: Acurite-Tower
# $2 Tower ID: 2235
# Uses cached data for 10 minutes, run rtl_433 to find id and name

DATA_SCAN="90"
DATA_MNTH=$(date +%m)
DATA_TIME=$(date +%s)

if find ../data/wx_data.txt -mmin +4 | grep -iq "../data/wx_data.txt" ; then
	echo "[i] SCANNING: Local Weather Sensors on 433MHZ (for ${DATA_SCAN} seconds) ..."
	echo ""
	rtl_433 -T $DATA_SCAN -C customary > ../data/wx_data.txt 2>&1
fi

if grep -iq "${1}" ../data/wx_data.txt && grep -iq "${2}" ../data/wx_data.txt ; then

#DATA_TEMP=$(rtl_433 -T 30 -C customary > ./data/wx_data.txt 2>&1 && cat ./data/wx_data.txt | grep -i -B 1 -A 5 "${1}" | grep -i -A 4 "${2}" | grep -i "Temperature" | uniq)
DATA_TEMP=$(cat ../data/wx_data.txt | grep -i -B 1 -A 5 "${1}" | grep -i -A 4 "${2}" | grep -i "Temperature" | uniq)
DATA_HUMI=$(cat ../data/wx_data.txt | grep -i -B 1 -A 5 "${1}" | grep -i -A 4 "${2}" | egrep -i "Humidity" | uniq)
DATA_CSV=""
DATA_STORM=""

IFS=': '
read -ra WX_TEMP <<< "$DATA_TEMP"
read -ra WX_HUMI <<< "$DATA_HUMI"

WX_DEWP=$(echo "((${WX_TEMP[1]})-(100-${WX_HUMI[1]})/5)" | bc)


# Thunderstorm detector! Noice!
# The strike counter will roll over @ 255 and start over @ 0.
# https://eu.mouser.com/pdfdocs/AMS_AS3935_Datasheet_v4.pdf
# https://www.acurite.com/media/manuals/06045-instructions.pdf
RX_STORM="Acurite-6045M"
if [[ "$1" == "$RX_STORM" ]]; then
	DATA_BOLT=$(cat ../data/wx_data.txt | grep -i -B 1 -A 7 "${1}" | grep -i -A 6 "${2}" | egrep -i "strike_count" | uniq) ; read -ra WX_BOLT <<< "$DATA_BOLT"
	DATA_MILE=$(cat ../data/wx_data.txt | grep -i -B 1 -A 7 "${1}" | grep -i -A 6 "${2}" | egrep -i "storm_distance" | uniq); read -ra WX_MILE <<< "$DATA_MILE"
fi

# Calculate the basic "Comfort Index"
DATA_COMF=$(bc -l <<< "((${WX_TEMP[1]}+${WX_HUMI[1]})/4)")
IFS='.'
read -ra WX_COMF <<< "$DATA_COMF"

# Friendly output
echo "[i] ${1} (${2})"
if [[ $DATA_MNTH -gt 10 || $DATA_MNTH -lt 3  ]]; then
echo "[i] HVAC Season      : Heating"
elif [[ $DATA_MNTH -gt 3 || $DATA_MNTH -lt 10  ]]; then
echo "[i] HVAC Season      : Cooling"
fi

if [[ "${WX_HUMI[1]}" -gt 39 && "${WX_HUMI[1]}" -lt 61 ]]; then
	WX_MOIS=$(echo "Good")
else
	if [[ "${WX_HUMI[1]}" -lt 40 ]]; then
		WX_MOIS=$(echo "Too Dry")
	else
		WX_MOIS=$(echo "Too Wet")
	fi
fi

echo "[-] Temperature      : ${WX_TEMP[1]}F"
echo "[-] Dew Point        : ${WX_DEWP}F"
echo "[-] Humidity         : ${WX_HUMI[1]}%"
echo "[-] Air Comfort      : ${WX_MOIS} (${WX_COMF[0]} Index)"

if [[ "$1" == "$RX_STORM" ]]; then

	DATA_CSV+="${1}-${2},${DATA_TIME},${WX_TEMP[1]},${WX_DEWP},${WX_HUMI[1]},${WX_COMF[0]},${WX_BOLT[1]},${WX_MILE[1]}"

	if [[ "${WX_MILE[1]}" -gt "30" ]]; then
		echo -e "[-] Stored Strikes   : ${WX_BOLT[1]}"
		echo -e "[-] No Storm Nearby"
	elif [[ "${WX_MILE[1]}" -lt "31" ]]; then
		echo -e "[\u26A0] Stored Strikes   : ${WX_BOLT[1]}"
        	echo -e "[\u26A0] Storm Distance   : ${WX_MILE[1]} Miles"
		DATA_STORM=$(echo "${DATA_CSV}" >> ../data/wx_storm.csv)
	else
		echo -e "[!] - NO STORM DATA"
	fi
else
	DATA_CSV+="${1}-${2},${DATA_TIME},${WX_TEMP[1]},${WX_DEWP},${WX_HUMI[1]},${WX_COMF[0]},0,0"
fi


DATA_FILE=$(echo "${DATA_CSV}" >> ../data/wx_data.csv)
else
echo "[!] ${1} (${2})"
echo "[!] NO DATA: Signal low, sensor out of range or scanning time too short"

fi

echo ""
