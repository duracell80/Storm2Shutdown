import os, subprocess

os.system('sudo powertop --csv=powertop.csv -q > /dev/null')
powertop_baseline = subprocess.getoutput('cat powertop.csv | grep "The system baseline power"')

print("[-] " + powertop_baseline.replace("  W;", "watts"))