import math
import os
import android
import time
import urllib
droid=android.Android()
diri='/storage/extSdCard/karttoja/'
paikka=diri+'paikka.txt'
while True:
    while os.path.isfile(paikka):
        print time.asctime()
        time.sleep(10)
    droid.startLocating()
    loc = {}
    while loc == {}:
        loc = droid.readLocation().result
        print loc
        if loc <> {}:
            try:
                n = loc['gps']
            except:
                n = loc['network']
        else:
            time.sleep(2)
    la = n['latitude']
    lo = n['longitude']
    droid.stopLocating()
    print la, lo
    f=open(paikka,'w')
    f.write(' %f, %f ' % (la,lo))
    f.close()

