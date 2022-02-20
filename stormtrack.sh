#!/bin/bash
clear
echo -e "StormTrack - Looping mode"

echo -e "\n \nWeather data obtained from The Accurite Lightning Tower every 5 minutes"
echo -e "- Press [CTRL+Z] to stop \n\n"


while true
do
 rm stormtrack.txt
 usbreset 0bda:2838
 rtl_433 -T 60 > stormtrack.txt
 clear

 DATA_COUNT=$(sort stormtrack.txt | uniq | grep "strike_count")
 DATA_DIST=$(sort stormtrack.txt | uniq | grep "storm_distance")
 DATA_TEMP=$(sort stormtrack.txt | uniq | grep "temperature")
 DATA_HUMID=$(sort stormtrack.txt | uniq | grep "humidity")
 DATA_TIME=$(sort stormtrack.txt | uniq | grep "time")
 STRIKES_PREV=$(cat strikecount.txt)

 # Get storm distance as number
 IFS=': '
 read -ra STORM_DIST <<< "$DATA_DIST"
 read -ra STORM_TEMP <<< "$DATA_TEMP"
 read -ra STORM_HUMID <<< "$DATA_HUMID"
 read -ra STORM_COUNT <<< "$DATA_COUNT"


 IFS=' '
 read -ra STORM_TIME <<< "$DATA_TIME"
 DATA_TIME=${STORM_TIME[2]}
 DATA_TIME+=" "
 DATA_TIME+=${STORM_TIME[3]}

 STORM_TIME=$(date -d "$DATA_TIME" +%s)

 echo "Time [$DATA_TIME] Temp [${STORM_TEMP[1]}F] Humidity [${STORM_HUMID[1]}%]"
 if [ ${STORM_COUNT[1]} -gt $STRIKES_PREV ];
 then
  echo "New Strike Detected: Total ${STORM_COUNT[1]} [!] - ${STORM_DIST} miles]"
  rm strikecount.txt
  speaker-test -t sine -f 1000 -l 1
  echo ${STORM_COUNT[1]} > strikecount.txt
 else

  DATE_STRIKES=$(stat -c %Y -- strikecount.txt)
  DATE_NOW=$(date +%s)
  DATE_DIF=$(($DATE_NOW - $DATE_STRIKES))

  if [ $DATE_DIF -gt 1800 ];
  then
   echo "Stored Strike Count: ${STORM_COUNT[1]} [o]"
   echo ""
   echo ""
   echo "The storm may have passed"
   echo "The tower contains data for about 2 hours"
  else
   echo "Stored Strike Count: ${STORM_COUNT[1]} [-]"
   # Test how close the storm is
   if [ ${STORM_DIST[1]} -lt 30 ];
   then
    echo ""
    echo ""
    echo "The storm was about ${STORM_DIST[1]} miles away"
   fi

  fi
 fi
 sleep 240
done
