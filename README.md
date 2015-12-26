# whoip
Automated IP geolocation and identification using reverse DNS and folium.

![Example Map](viz/README.png?raw=true "Example Map")

## What it does
whoip reveals the identities and locations of the IP addresses that your connection is traveling through, on an interactive map enabled by [folium](https://github.com/python-visualization/folium). Attach a listfile of IPs, or perform a traceroute on a domain (eg. 'google.com').

## Usage
```
whoip.py -f <LISTFILE>
whoip.py -t <TARGET IP ADDRESS>
-f, --list-file     :     Upload a list of IPs for processing
-t, --traceroute    :     Perform traceroute on target IP
-h, --help          :     Assistance
```

## To-Do
- [viz] Better starting zoomed view of map to show all waypoints
- [viz] Toggle-able lines between traceroute hops on map
- [viz] Better styling for IP info on map
- [code] More usage options
- [code] Clean and caption

## Contribute
Feel free to contribute and try the tool for yourself!
