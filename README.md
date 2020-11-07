# WildixEnum
Wildix user enumeration and show current location


## Wildix
Wildix is a PBX with build-in call, chat and video chat functionality.

## What is this?
This script enumerates users via the Public Kite API and shows their Name and Location. In fact, you can chat with everyone on the PBX.

## How did you make this?
First, if you don't trust it, don't execute it. It's a compiled python script that brute forces the API with internal extentions, from 200 to 700.
If the API returns 200 OK, it reads and displays the data. This data contains live location.

I would add a map with location markers, but python folium is broken on Windows v2004, so.. no map.

# Disclaimer
I am not responsible for any damage you might cause with this tool. I made it to only make people aware of endpoints that show sensetive data about the users. Also, the developers don't think this is an issue.
