# Storm2Shutdown
Useful for applications such as NAS or Headless Linux/Pi. To protect against data loss by monitoring the weather for threats to power supply. Checks US NWS for severe weather to issue a standard Linux scheduled shutdown command when storm deteced
- Configurable backoff from RSS pull
- Configurable state and county search
- Will only issue shutdown command once if county appears in multiple warnings
- Run via shell on loop or once with &

## NWS Documentation
https://alerts.weather.gov/cap/pdf/CAP%20v12%20guide%20web%2006052013.pdf

## Install
Use PIP to get the feedparser

```
$ cd ~/
$ mkdir git
$ cd git
$ git clone https://github.com/duracell80/Storm2Shutdown.git
$ cd Storm2Shutdown
$ chmod a+x *.sh
$ ./install.sh
```

## Configuration
Change the first few lines at the start of storm2shutdown.py

## Usage
Run as straight python:
`
$ python3 storm2shutdown.py
`

Run as bash loop:
`
$ ./s2s.sh
`

Run everything once for debugging/demo:
`
$ ./s2s_once.sh
`

Run just the weather and shutdown routine (on Chron etc):
`
$ ./s2s_chron.sh
`

## Notes and ToDo
- Backup data when Thunderstorm Watch issued for county/state combo
- Email upon trigger
- Set number of warnings threshold to between 1 and 5 if county is large or warning broad
