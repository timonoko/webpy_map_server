# webpy_map_server

Messy web.py map-server, which remembers every page ever fetched and connects to all known tile providers in nordic countries, legal or not.

The name is "osm.py", because it started as osm-mapper.

When run inside Linux-for-Android, the paikka.py (Py4A) reads the GPS for you. I had some weird problems when running Py4A only and roaming in Norway.

Swedes (and Normen) changed their tile-provider format to something else, so phuck you.

Main operating enviroment is now Termux, Qpython fails at urlretrieve.
