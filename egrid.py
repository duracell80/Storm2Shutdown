import os, time
import pandas

# Change TN to your state for example KY
cfg_state = "TN"

# Read EPA eGrid for Power Generation Data
# 2020 Data - https://www.epa.gov/egrid/summary-data

egrid = pandas.read_csv('egrid-2020.csv', sep='[;]', engine='python')

eidx = 0
while eidx < 52:
    if "U.S." in egrid['State'][eidx]:
        total_solar     = egrid['Solar'][eidx]
    eidx += 1
eidx = 0
while eidx < 52:
    if cfg_state in egrid['State'][eidx]:
        power_dirty = round(float(egrid['Gas'][eidx].strip('%')) + float(egrid['Coal'][eidx].strip('%')) + float(egrid['Oil'][eidx].strip('%')) + float(egrid['Biomass'][eidx].strip('%')), 2)

        power_nuclear   = egrid['Nuclear'][eidx]
        power_hydro     = egrid['Hydro'][eidx]
        power_wind      = egrid['Wind'][eidx]
        power_solar     = egrid['Solar'][eidx]
        power_geo       = egrid['Geo- thermal'][eidx]

        print("\n\nState progress on energy transition (" + egrid['State'][eidx] + ") \n")
        print("Dirty Generation: \n[Carbon  = " + str(power_dirty) + "% (inc Biomass)] \n[Nuclear = " + power_nuclear + "] \n")
        print("Clean Generation: \n[Solar = " + power_solar + " (National: " + total_solar + ")] [Wind = " + power_wind + "] [Hydro = " + power_hydro + "] [Tidal = N/A] [GeoThermal = " + power_geo + "] \n")
    eidx += 1
    #print("Clean Storage: \n[Hydrogen = N/A] [Other Gravity = N/A] [Compressed Air = N/A] \n\n")