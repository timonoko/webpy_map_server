# webpy_map_server_mostly_android

Messy web.py map-server, which remember every page ever fetched and connects to all tile providers in nordic countries, legal or not.

The name is "osm.py", because it started as osm-mapper.

Cannot do the Finnish National Grid to Google Tile translation, because I am stupid. So I use 3x3 tiles, which fill the phone screen adequatly most of time.

When run inside Linux-for-Android, the paikka.py (Py4A) reads the GPS for you. I had some weird problems when running Py4A only and roaming Norway.
