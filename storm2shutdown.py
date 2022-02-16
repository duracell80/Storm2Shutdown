import os, subprocess, time
import feedparser, pandas

#def measure_temp():
        #temp = os.popen("vcgencmd measure_temp").readline()
        #return (temp.replace("temp=",""))


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
cfg_timer = "10"
cfg_script= 'shutdown -h 00:05 "[!] Storm detected nearby. Shutdown scheduled to protect device against power disruption, please complete your work"'
cfg_go    = "no"

# Read EPA eGrid for Power Generation Data
# 2020 Data - https://www.epa.gov/egrid/summary-data

egrid = pandas.read_csv('egrid-2020.csv', sep='[;]', engine='python')

eidx = 1
while eidx < 50:
    eidx += 1
    if "TN" in egrid['State'][eidx]:
        # Calculate Delta Bewteen Carbon and Low Carbon
        power_dirty = round(float(egrid['Gas'][eidx].strip('%')) + float(egrid['Coal'][eidx].strip('%')) + float(egrid['Oil'][eidx].strip('%')) + float(egrid['Biomass'][eidx].strip('%')), 2)
        
        power_nuclear   = egrid['Nuclear'][eidx]
        power_hydro     = egrid['Hydro'][eidx]
        power_wind      = egrid['Wind'][eidx]
        power_solar     = egrid['Solar'][eidx]
        power_geo       = egrid['Geo- thermal'][eidx]
        
        print("\n\nState progress on energy transition \n * Source - EPA eGrid 2020 \n")
        print("Dirty Generation: \n[Carbon  = " + str(power_dirty) + "%] \n[Nuclear = " + power_nuclear + "] \n")
        print("Clean Generation: \n[Solar = " + power_solar + "] [Wind = " + power_wind + "] [Hydro = " + power_hydro + "] [GeoThermal = " + power_geo + "] \n\n")

# Main script
feed_url = "https://alerts.weather.gov/cap/"+ cfg_state.lower() +".php?x=0"
feed_age = subprocess.check_output('find ./data.xml -mmin +' + cfg_timer, shell=True, universal_newlines=True)
if len(feed_age) > 0:
	os.system('wget --quiet -O "./data.xml" ' + feed_url + '');
	print("[i] Weather fetched from NWS (" + cfg_cname + ", " + cfg_state  + ")")
else:
	print("[i] Weather backoff active (" + cfg_timer  + " minutes)")
	#print("[i] System (" + measure_temp() + ")")    
    
    
feed_xml = open("data.xml", "r")
feed_dat = feed_xml.read().replace("cap:", "cap_")
feed_xml.close()

blog_feed = feedparser.parse(feed_dat)

posts = blog_feed.entries
for post in posts:
	if (cfg_cwarn or "Tornado Warning") in post.title and cfg_cname in post.summary:
		print("[?] Severe Storm detected nearby ... (" + post.cap_areadesc + ")")
		cfg_go = "yes"

# Only run once, even if multiple warnings for the same county
if cfg_go == "yes":
	os.system(cfg_script)