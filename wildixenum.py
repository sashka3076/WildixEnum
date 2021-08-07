#/usr/bin/env python
import os, sys, requests, folium, webbrowser
from folium.features import CustomIcon
from tqdm import tqdm

# Print banner
print('''
Made by:
  _____                           _
 |_   _|                         (_)
   | |  _ __   ___ ___  _ __ ___  _ _ __   __ _
   | | | '_ \\ / __/ _ \\| '_ ` _ \\| | '_ \\ / _` |
  _| |_| | | | (_| (_) | | | | | | | | | | (_| |
 |_____|_| |_|\\___\\___/|_| |_|_|_|_|_| |_|\\__, |
  / ____|                    (_) |         __/ |
 | (___   ___  ___ _   _ _ __ _| |_ _   _ |___/
  \\___ \\ / _ \\/ __| | | | '__| | __| | | |
  ____) |  __/ (__| |_| | |  | | |_| |_| |
 |_____/ \\___|\\___|\\__,_|_|  |_|\\__|\\__, |
                                     __/ |
                                    |___/

          Coded with <3 by Leon Voerman
                        Copyright © 2020 - IncSec

''')

org   = input('Organisation [Default: ucit]: ') or 'ucit' # Default org is ucit, wich is used on Wildix.com
start = input('Range start [Default 200]: ') or 200 # In NL, we start at 200 to avoid conflict with 112
end   = input('Range end [Default: 300]: ') or 300 # Max can be anything above the start range, but take longer to finish the scan.

c   = 0 # Total found users Counter
on  = 0 # Online users Counter
loc = [] # Store lat-lng here to genetrate map later

with tqdm(initial=int(start), total=int(end), desc='Progress') as bar: # define progress bar
    # Print header
    tqdm.write('\n%s %s %s %s %s %s' % ('PBX'.ljust(35), 'Ext'.ljust(10), 'Name'.ljust(40), 'Online'.ljust(10), 'Chat Link'.ljust(45), 'Location'))

    for i in range(int(start),int(end)): # start - end range defined earlier
        r    = requests.get('https://kite.wildix.com/' + org + '/' + str(i) + '/api/info') # Craft Kite link and connect
        data = r.json() # Read JSON data

        if r.status_code == 200: # page status 200 OK, do this:
            try:
                # Read data from JSON
                ext     = data['result']['extension']
                naam    = data['result']['name']
                status  = data['result']['presence']['online']
                adres   = data['result']['presence']['location']['address']
                lat     = data['result']['presence']['location']['lat']
                long    = data['result']['presence']['location']['lng']
                pbx     = data['result']['pbxDomain']
                chat    = 'https://kite.wildix.com/' + org + '/' + str(ext)

                loc.append('%s:%s:%s:%s:%s' % (naam, adres, ext, lat, long)) # Data for Map

                if status == True:
                    on += 1

                # Print found data
                tqdm.write('%s %s %s %s %s %s' % (pbx.ljust(35), ext.ljust(10), naam.ljust(40), str(status).ljust(10), chat.ljust(45), str(adres)))
                c += 1
            except Exception:
                pass
        else:
            # if page status not 200 OK, user not exist, skip and continue
            pass

        bar.update(1)

# Print Total users and online users
print('\nFound %i users of wich %i are online..' % (int(c), int(on)))

# Create World Map
print('\nGenerating Map...')
folium_map = folium.Map(location=[51.862890, 4.535700], zoom_start=8, tiles="OpenStreetMap") # Define Map

for gebr in loc:
    try:
        gebr = gebr.split(':')
        icon = CustomIcon('https://kite.wildix.com/' + org + '/' + gebr[2] +'/api/avatar' % (), icon_size=(45,45)) # Use Kite User's profile picture on map
        marker = folium.Marker(location=[gebr[3], gebr[4]], popup='<b>%s (%s)</b><br><br>%s' % (gebr[0], gebr[2], gebr[1]), tooltip=gebr[0], fill=True, icon=icon).add_to(folium_map) # Set marker
    except Exception:
        pass # If error, skip this users on map

folium_map.save("./user_map.html") # Save map in current folder
webbrowser.open_new_tab('file://' + os.path.realpath('user_map.html')) # Open map when generated

# Finished, Exiting...
print('\nDone...')

p =  input('Press Any Key to Exit...')
sys.exit(0)
