import os, subprocess, time
from datetime import datetime

import feedparser, pandas



# Change TN to your state for example KY
# Change Davison to your county for example Benton

# Documentation	: https://alerts.weather.gov/cap/pdf/CAP%20v12%20guide%20web%2006052013.pdf
# Other idea	: Backup data when Thunderstorm Watch issued for county/state combo
# Other idea	: Email upon trigger
# Other idea	: Set number of warnings threshold to between 1 and 5 if county is large or warning broad
# Other idea    : Fallback onto RTL_433 with Accurite-6045M Tower

cfg_state = "TN"
cfg_cname = "Davidson"
cfg_cwarn = "Severe Thunderstorm Warning"
cfg_timer = "25"
cfg_script= 'shutdown -h 00:05 "[!] Storm detected nearby. Shutdown scheduled to protect device against power disruption, please complete your work"'
cfg_go    = "no"


# Main script
feed_url = "https://alerts.weather.gov/cap/"+ cfg_state.lower() +".php?x=0"
feed_age = subprocess.check_output('find ./data.xml -mmin +' + cfg_timer, shell=True, universal_newlines=True)
if len(feed_age) > 0:
	os.system('wget --quiet -O "./data.xml" ' + feed_url + '');
	print("\n\n[-] Weather fetched from NWS [" + cfg_cname + ", " + cfg_state  + "]")
else:
	feed_now = float(time.time())
	feed_dif = float(feed_now + (float(cfg_timer) * 60))
	feed_nxt = datetime.fromtimestamp(feed_dif)
	print("[-] Weather threat monitoring (" + cfg_cname + ", " + cfg_state + " - Next update: " + feed_nxt.strftime('%H:%M:%S') + ")")
feed_xml = open("data.xml", "r")
feed_dat = feed_xml.read().replace("cap:", "cap_")
feed_xml.close()

blog_feed = feedparser.parse(feed_dat)

posts = blog_feed.entries
for post in posts:
        if "Tornado Watch" in post.title and cfg_cname in post.cap_areadesc:
                print("[!] A Tornado Watch is in effect for your area")
                cfg_go = "no"
for post in posts:
        if "High Wind Warning" in post.title and cfg_cname in post.cap_areadesc:
                print("[!] A High Wind Warning is in effect for your area")
                cfg_go = "no"
for post in posts:
	if "Wind Advisory" in post.title and cfg_cname in post.cap_areadesc:
		print("[!] A Wind Advisory is in effect for your area")
		cfg_go = "no"
for post in posts:
	if "Thunderstorm Watch" in post.title and cfg_cname in post.cap_areadesc:
		print("[!] A Storm Watch is in effect for your area")
		cfg_go = "no"

for post in posts:
	if (cfg_cwarn or "Tornado Warning") in post.title and cfg_cname in post.summary:
		print("[!] Severe Storm detected nearby ... (" + post.cap_areadesc + ")")
		cfg_go = "yes"

# Only run once, even if multiple warnings for the same county
if cfg_go == "yes":
	os.system("speaker-test -t sine -f 1000 -l 1")
	os.system(cfg_script)
