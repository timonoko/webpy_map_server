# webpy_map_server

Messy web.py map-server, which remembers every page ever fetched and connects to all known tile providers in nordic countries, legal or not.

The name is "osm.py", because it started as osm-mapper.

When run inside Linux-for-Android, the paikka.py (Py4A) reads the GPS for you. I had some weird problems when running Py4A only and roaming in Norway.

Swedes (and Normen) changed their tile-provider format to something else, so phuck you.

Main operating enviroment is now Termux, Qpython fails at urlretrieve.

Opera is the best client. Shortcut to http://0.0.0.0:8080 goes fullscreen.

Interface is weird, but wet-finger friendly. It was originally made for python-for-symbian and E52 buttons.

<img src="Screenshot_2019-04-24-08-18-34.png" >

