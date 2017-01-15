# coding=iso-8859-1

import os
import math
import time
import urllib
import web,os

web.config.debug=False

if os.path.exists('/sdcard') and not os.path.exists('/external_sd'):
    androidi=True
#    os.chdir('/sdcard/sl4a/scripts')
else:
    androidi=False

if androidi:
    try:
        os.chdir('/sdcard/com.hipipal.qpyplus/scripts')
        import androidhelper as android
    except:    
        import android
    droid=android.Android()

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

tile_size=256

class datoja:
    urls=()
    bookmarks=[]
    bookmarks2=[]
    latti=60.0
    longi=25.0
    bearing=0.0
    prev_latti=60.19
    prev_longi=25.01
    tile_x=1
    tile_y=1
    zoomi=7
    korkeus=0.1
    leveys=0.1
    kartta=['osm','google','kapsi','ilma','eniro','sailm','bing','norja','norsjo','svesjo','gsat','cycle','viro','noka','orto','seamap']
    nykyinen=0
    online = "OFFLINE"
    seamap=False
    gps=[]
    lue_uudestaan=False

def savedatoja():
    if datoja.latti<>60.0:
        f=open("static/datoja","w")
        f.write('%f, %f, %d, %d\n'%(datoja.latti,datoja.longi,datoja.zoomi,datoja.nykyinen))
        f.close()
    if datoja.bookmarks<>[]:
        f=open("static/bookmarks","w")
        f.write(str(datoja.bookmarks))
        f.close()

def loaddatoja():
    if os.path.exists("static/datoja"):
        f=open("static/datoja","r")
        s=f.readline()
        y=s.split(",")
        if s<>'':
            y=s.split(",")
            datoja.latti=float(y[0])
            datoja.longi=float(y[1])
            datoja.zoomi=int(y[2])
            datoja.nykyinen=int(y[3])
        f.close()
    if os.path.exists("static/bookmarks"):
        f=open("static/bookmarks","r")
        datoja.bookmarks=eval(f.read())
        f.close()
    if os.path.exists("static/bookmarks.static"):
        f=open("static/bookmarks.static","r")
        datoja.bookmarks2=eval(f.read())
        f.close()

def google2kartta(x):
    if x==13:
        return 80000
    y= 2**(28-x)
    if y>100000:
        return 200000
    if y>50000:
        return 80000
    if y>30000:
        return 40000
    if y>10000:
        return 16000
    if y>5000:
        return 8000
    else:
        return 4000


def tiili(x,y,zoom,xo,yo,xd,yd):
    ny = datoja.kartta[datoja.nykyinen]
    if ny == "viro":
        return 'http://lbs.nutiteq.ee/topo/%d/%d/%d.jpg' % (zoom, x, y)
    if ny == "cycle":
        return 'http://b.tile.opencyclemap.org/cycle/%d/%d/%d.png' % (zoom, x, y)
    if ny == 'sailm': 
        y2=y
        if zoom==13:
            y2=2371-y+5820
        if zoom==14:
            y2=11639-y+4744
        return  'http://mapserver.sailmate.fi/fi/images/%d/%d/%d.png'%(zoom,x,y2)
    if ny == 'osm': 
        return  'http://b.tile.openstreetmap.org/%d/%d/%d.png'%(zoom,x,y)
    if ny == 'norja': 
        return  'http://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?layers=topo2&zoom=%d&x=%d&y=%d' % (zoom, x, y)
    if ny == 'google': 
        return 'http://mt.google.com/vt/v=w2.97&hl=en&x=%d&y=%d&z=%d' % (x, y, zoom)
    if ny == 'gsat':
        time.sleep(1)
        return 'http://khm.google.com/kh/v=113&x=%d&y=%d&z=%d' % (x, y, zoom)
    if ny == 'norsjo': 
        return 'http://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?layers=sjo_hovedkart2&zoom=%d&x=%d&y=%d' % (zoom, x, y)
    if ny == 'bing':
        import Tiles
        import random
        return 'http://a%d.ortho.tiles.virtualearth.net/tiles/a%s.jpeg?g=90' % (random.randint(0, 3),  Tiles.toMicrosoft(x,y,zoom))
    if ny == 'eniro':
	y2=math.pow(2,zoom)-y-1;
	return 'http://map.eniro.com/geowebcache/service/tms1.0.0/map/%d/%d/%d.png'%(zoom, x, y2)
    if ny == 'svesjo':
	y2=math.pow(2,zoom)-y-1;
	return 'http://map.eniro.com/geowebcache/service/tms1.0.0/nautical/%d/%d/%d.png'%(zoom, x, y2)
    if ny == 'kapsi':
        return 'http://tiles.kartat.kapsi.fi/peruskartta/%d/%d/%d.png'%(zoom, x, y)
#        if y % 2 == 0:
#           return 'https://tile1.kapsi.fi/mapcache/peruskartta_3067/%d/%d/%d.png'%(zoom, x, y)
#        else:
#           return 'https://tile2.kapsi.fi/mapcache/peruskartta_3067/%d/%d/%d.png'%(zoom, x, y)

    if ny == 'ilma':
        return 'http://tiles.kartat.kapsi.fi/ortokuva/%d/%d/%d.png'%(zoom, x, y)
    if ny == 'noka':
        import kkj
        bottomX,bottomY = kkj.WGS2KKJ(num2deg(x,y-2,zoom))
        topX,topY = kkj.WGS2KKJ(num2deg(x+3,y+1,zoom))
        return 'http://vanha.karttapaikka.fi/image?request=GetMap&bbox=%d,%d,%d,%d&scale=%d&width=800&height=800&srs=NLSFI:kkj&styles=normal&lang=FI&lmid=1179938105236' % (bottomY, bottomX, topY, topX, google2kartta(zoom))
    if ny == 'orto':
        import kkj
        bottomX,bottomY = kkj.WGS2KKJ(num2deg(x,y-2,zoom))
        topX,topY = kkj.WGS2KKJ(num2deg(x+3,y+1,zoom))
        return 'http://vanha.karttapaikka.fi/image?request=GetMap&bbox=%d,%d,%d,%d&scale=%d&width=800&height=800&srs=NLSFI:kkj&styles=normal&lang=FI&lmid=1179938105236&mode=orto' % (bottomY, bottomX, topY, topX, google2kartta(zoom))
    if ny in ['svedu','sveter']:
        import swecoord
        TILE_SIZE = 256
        lat,lon=num2deg(xo,yo,zoom)
        zoom1 = zoom
        zoom = 17 - zoom1
        if zoom<1:
            zoom =1
        yo,xo=swecoord.wgsToswe(lat,lon)
        s=int((TILE_SIZE*2**zoom)*20/33.5)
        xo=int(xo+xd*s)
        yo=int(yo-yd*s)
        yo2=int(yo-s)
        xo2=int(xo+s)
        if ny == 'svedu':
            return 'http://kso.lantmateriet.se/wmsproxy/wmsproxy?LAYERS=topowebbkartan&SERVICE=WMS&REQUEST=GetMap&FORMAT=image/jpeg&SRS=EPSG:3006&BBOX=%d,%d,%d,%d&WIDTH=%d&HEIGHT=%d' % ( xo, yo2, xo2 , yo, TILE_SIZE, TILE_SIZE ) 
        if ny == 'sveter':
            return 'http://kso.lantmateriet.se/wmsproxy/wmsproxy?LAYERS=terrangkartan&SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&STYLES=&EXCEPTIONS=application%%2Fvnd.ogc.se_inimage&FORMAT=image%%2Fjpeg&SRS=EPSG%%3A3006&BBOX=%d,%d,%d,%d&WIDTH=%d&HEIGHT=%d' % ( xo, yo2, xo2 , yo, TILE_SIZE, TILE_SIZE ) 
   

def nappi(f,osoite,kuvio,x,y):
    f.write('<div style="position: absolute; left:'+str(x)+'; top:'+str(y)+'">')
    f.write("<a href="+osoite+"><img src=static/"+kuvio+"></a>")
    f.write('</div>\n')

def html_encode(s):
    htmlCodes = (
        ("'", '&#39;'),
        ('"', '&quot;'),
        ('>', '&gt;'),
        ('<', '&lt;'),
        ('&', '&amp;'),
        ('ä', '&auml;'),
        ('Ä', '&Auml;'),       
        ('ö', '&ouml;'),
        ('Ö', '&ouml;'),        
        ('å', '&aring;'),        
        ('Å', '&Aring;'),        
        )
    for code in htmlCodes:
        s = s.replace(code[0], code[1])
    return s

def pelkka_teksti(f,teksti,x,y):
    f.write('<div style="position: absolute; left:'+str(x)+'; top:'+str(y)+'">\n')
    f.write(html_encode(teksti))
    f.write('\n</div>\n')

def ruudussa(lattiny,longiny):
    zoom=datoja.zoomi
    x = tile_size + int((longiny-num2deg(datoja.tile_x,datoja.tile_y,zoom)[1])/datoja.leveys*tile_size)
    y = tile_size - int((lattiny-num2deg(datoja.tile_x,datoja.tile_y,zoom)[0])/datoja.korkeus*tile_size)
    return (x, y)
            
def palauta_paska(refresh=False):
    print "palauta paska"
    savedatoja()
    zoom=datoja.zoomi
    datoja.tile_x,datoja.tile_y = deg2num(datoja.latti,datoja.longi,zoom)
    datoja.korkeus = num2deg(datoja.tile_x,datoja.tile_y-1,zoom)[0]-num2deg(datoja.tile_x,datoja.tile_y,zoom)[0]
    datoja.leveys = num2deg(datoja.tile_x,datoja.tile_y,zoom)[1]-num2deg(datoja.tile_x-1,datoja.tile_y,zoom)[1]
    tarkka_x, tarkka_y = ruudussa(datoja.latti,datoja.longi)
    f = open('static/paskaa.html','w')
    f.write('<html>')
    f.write('<head><title>http://localhost:8080/goto:%.4f,%.4f,%d</title>\n'%(datoja.latti,datoja.longi,datoja.zoomi))
    if refresh:
        f.write('<META HTTP-EQUIV="refresh" CONTENT="15">\n')
    f.write('</head>\n')
    for xd in [-1,0,1,2,3]:
        for yd in [5,4,3,2,1,0,-1]:
            x=datoja.tile_x+xd
            y=datoja.tile_y+yd
            jemma='static/%s/%d/%d/'%(datoja.kartta[datoja.nykyinen],zoom,x)
            if not os.path.exists(jemma):
                os.makedirs(jemma)
            if datoja.kartta[datoja.nykyinen] in ['svedu', 'sveter']:
                nimi = jemma+'%d%d%d.png'%(datoja.tile_y,yd,xd)
            else:    
                nimi = jemma+'%d.png'%y
            if  (not os.path.exists(nimi)) or datoja.lue_uudestaan:
                if datoja.online == 'online':
                    if (not (datoja.kartta[datoja.nykyinen] in ['noka','orto']) or (xd == -1 and yd == 1)) and abs(xd)<2 and abs(yd)<2:
                        print 'urlretrieve'
                        urllib.urlretrieve(tiili(x,y,zoom,datoja.tile_x,datoja.tile_y,xd,yd) , nimi )
            if datoja.seamap:
                jemma_sm='static/%s/%d/%d/'%('seamap',zoom,x)
                if not os.path.exists(jemma_sm):
                    os.makedirs(jemma_sm)
                nimi_sm = jemma_sm+'%d.png'%y
                if not os.path.exists(nimi_sm):
                    if datoja.online == 'online' and abs(xd)<2 and abs(yd)<2:
                        print 'urlretrieve'
                        urllib.urlretrieve('http://t1.openseamap.org/seamark/%d/%d/%d.png'%(zoom,x,y) , nimi_sm )
            if  os.path.exists(nimi):
                if datoja.kartta[datoja.nykyinen]=='gsat' and os.stat(nimi).st_size<2000:
                    os.remove(nimi)
                else:
                    if not (datoja.kartta[datoja.nykyinen] in ['noka','orto']):
                        f.write('<div style="position: absolute; left: %d ; top: %d ">'%(tile_size*(1+xd)+120,tile_size*(1+yd)+50))
                        f.write('%d %d %d'%(x, y, zoom))
                        f.write('</div>\n')
                        f.write('<div style="position: absolute; left: %d ; top: %d ">'%(tile_size*(1+xd),tile_size*(1+yd)))
#                        f.write('<img src="'+nimi+'?xxx=987878787">')
                        f.write('<img src="%s?xxx=%d">'%(nimi,int(10000*time.clock())))
                        f.write('</div>\n')
                    elif xd in [-1,2] and yd in [1,4]:
                        d = (3*256-800)/2
                        f.write('<div style="position: absolute; left: %d ; top: %d ">'%((xd+1)*256+d,(yd-1)*256+d))
                        f.write('<img src="'+nimi+'">')
                        f.write('</div>\n')
            if datoja.seamap and os.path.exists(nimi_sm) and  os.path.getsize(nimi_sm)>180:
                f.write('<div style="position: absolute; left: %d ; top: %d ">'%(tile_size*(1+xd),tile_size*(1+yd)))
                f.write('<img src="'+nimi_sm+'">')
                f.write('</div>\n')
    f.write('<div style="position: absolute; left: %d ; top: %d ">' % (tarkka_x-50, tarkka_y-50))
    f.write('<img src=static/kursori.png>')
    f.write('</div>\n')
    xr, yr = ruudussa(datoja.prev_latti, datoja.prev_longi)
    if 0 < xr < 3*tile_size and 0 < yr < 3*tile_size and not (tarkka_x == xr and tarkka_y == yr)  :
        f.write('<div style="position: absolute; left: %d ; top: %d ">' % (xr-10,yr-10))
        f.write('<img src=static/kurspieni.png>')
        f.write('</div>\n')
    kx=3*256/2
    ky=3*256/2
    vasen=0
    oikee=3*256-30
    yla=0
    ala=3*256-30
    keskix=kx-15
    keskiy=ky-15
    nappi(f,"kivia","kivia.png",vasen,yla)
    nappi(f,"taloja","taloja.png",(keskix+vasen)/4,yla)
    nappi(f,"haku","haku.png",(keskix+vasen)/2,yla)
    nappi(f,"zoomin","nothing.png",tarkka_x-15,tarkka_y-15)
    nappi(f,"zoomout","minus.png",oikee,yla)
    nappi(f,"left","left.png",vasen,keskiy)
    nappi(f,"right","right.png",oikee,keskiy)
    nappi(f,"up","up.png",keskix,yla)
    nappi(f,"down","down.png",keskix,ala)
    nappi(f,"minileft","nothing.png",tarkka_x-50,tarkka_y-15)
    nappi(f,"miniright","nothing.png",tarkka_x+50-30,tarkka_y-15)
    nappi(f,"miniup","nothing.png",tarkka_x-15,tarkka_y-50)
    nappi(f,"minidown","nothing.png",tarkka_x-15,tarkka_y+50-30)
    nappi(f,"gps","gps.png",(keskix+oikee)/2,yla)
    nappi(f,"bookmark","bee.png",(keskix+oikee)/2+80,yla)
    kamalaa=0
    for lat,lon in datoja.bookmarks:
        xr, yr = ruudussa(lat,lon)
        if 0 < xr < 3*tile_size and 0 < yr < 3*tile_size:
            nappi(f,"lippu_"+str(kamalaa),"lippu2.png",xr,yr-60)
        kamalaa+=1
    kamalaa=0
    for lat,lon,bteksti in datoja.bookmarks2:
        xr, yr = ruudussa(lat,lon)
        if 0 < xr < 3*tile_size and 0 < yr < 3*tile_size and datoja.zoomi>10:
            nappi(f,"lippu2_"+str(kamalaa),"lippu3.png",xr,yr-60)
            if  datoja.zoomi>13:
                pelkka_teksti(f,bteksti,xr+45,yr-55)
        kamalaa+=1

    f.write('<div style="position: absolute; left:'+str(10)+'; top:'+str(3*256+20)+'">')
    for k in range(0,len(datoja.kartta)):
        f.write('<a href="kartta_'+str(k)+'">'+datoja.kartta[k]+"</a>  ")
    f.write('<p>\n')
#    f.write('</div>\n')
#    f.write('<div style="position: absolute; left:'+str(10)+'; top:'+str(3*256+50)+'">')
    f.write('<a href=online><font color="red"> %s</font></a> : '%(datoja.online))
    if datoja.lue_uudestaan:
        f.write('<a href=uusi><font color="green"> FRESH</font></a> : ')
    else:
        f.write('<a href=uusi><font color="red"> rfrsh</font></a> : ')
    f.write('    %s'%(datoja.kartta[datoja.nykyinen]))
    if datoja.seamap:
        f.write('+seamap')
    wi=3*math.cos(math.radians(datoja.latti))*40000/(2**datoja.zoomi)
    f.write(' @ %.4f, %.4f, %d / %.2f km / %d m <p>\n'%(datoja.latti, datoja.longi, datoja.zoomi,\
	      wi, wi*1000/(3*256)*100))
    f.write(str(datoja.gps))
    f.write('</div>\n')
    f.write('</html>\n')
    f.close()
    f2=open("static/paskaa.html","r")
    s=f2.read(10000)
    f2.close()
    datoja.lue_uudestaan=False
    datoja.prev_latti = datoja.latti
    datoja.prev_longi = datoja.longi
    return s



datoja.urls=('/','index')
class index:
    def GET(self):
        loaddatoja()
        return palauta_paska()

datoja.urls+=('/goto:(.*)','goto')
class goto:
    def GET(self,s):
        y=s.split(",")
        datoja.latti=float(y[0])
        datoja.longi=float(y[1])
        datoja.zoomi=int(y[2])
        if datoja.zoomi>18:
            datoja.zoomi=14
        return palauta_paska()

datoja.urls+=('/kartta_(.*)','kartta')
class kartta:
    def GET(self,s):
        if datoja.kartta[int(s)]=='seamap':
	    datoja.seamap = not datoja.seamap
	else:
	    datoja.nykyinen=int(s)
	    if datoja.kartta[datoja.nykyinen]=='norsjo':
		if datoja.zoomi<9:
		    datoja.zoomi=7
		else:
		    datoja.zoomi=13
	    if datoja.kartta[datoja.nykyinen]=='sailm':
                datoja.zoomi=13
        return palauta_paska()

datoja.urls+=('/up','up')
class up:
    def GET(self):
        datoja.latti=datoja.latti+datoja.korkeus
        return palauta_paska()

datoja.urls+=('/down','down')
class down:
    def GET(self):
        datoja.latti=datoja.latti-datoja.korkeus
        return palauta_paska()

datoja.urls+=('/left','left')
class left:
    def GET(self):
        datoja.longi=datoja.longi-datoja.leveys
        return palauta_paska()

datoja.urls+=('/right','right')
class right:
    def GET(self):
        datoja.longi=datoja.longi+datoja.leveys
        return palauta_paska()

datoja.urls+=('/miniup','miniup')
class miniup:
    def GET(self):
        datoja.latti=datoja.latti+datoja.korkeus/5
        return palauta_paska()

datoja.urls+=('/minidown','minidown')
class minidown:
    def GET(self):
        datoja.latti=datoja.latti-datoja.korkeus/5
        return palauta_paska()

datoja.urls+=('/minileft','minileft')
class minileft:
    def GET(self):
        datoja.longi=datoja.longi-datoja.leveys/5
        return palauta_paska()

datoja.urls+=('/miniright','miniright')
class miniright:
    def GET(self):
        datoja.longi=datoja.longi+datoja.leveys/5
        return palauta_paska()

datoja.urls+=('/zoomin','zoomin')
class zoomin:
    def GET(self):
        if datoja.kartta[datoja.nykyinen]=='norsjo':
            datoja.zoomi = 13
        elif datoja.zoomi<18:
            datoja.zoomi = datoja.zoomi+1
        return palauta_paska()

datoja.urls+=('/zoomout','zoomout')
class zoomout:
    def GET(self):
        if datoja.kartta[datoja.nykyinen]=='norsjo':
            datoja.zoomi = 7
        elif datoja.zoomi>2:
            datoja.zoomi = datoja.zoomi-1
        return palauta_paska()

datoja.urls+=('/gps','gps')
class gps:
    def GET(self):
        print "GPS.."
        if androidi:
            droid.startLocating()
            time.sleep(5)
            loc = {}
            while loc == {}:
                loc = droid.readLocation().result
            try:
                n = loc['gps']
            except KeyError:
                n = loc['network']
	    datoja.gps = n
            datoja.latti = n['latitude']
            datoja.longi = n['longitude']
            droid.stopLocating()
        else:
            paikka='static/paikka.txt'
            if os.path.isfile(paikka):
                os.remove(paikka)
            while not os.path.isfile(paikka):
                time.sleep(2)
            f=open(paikka,'r')
            s=f.readline()
	    datoja.gps = s
            y=s.split(",")
            datoja.latti=float(y[0])
            datoja.longi=float(y[1])
            datoja.bearing=float(y[2])
            f.close()
        return palauta_paska(True)


datoja.urls+=('/bookmark','bookmark')
class bookmark:
    def GET(self):
        y = [round(datoja.latti,5),round(datoja.longi,5)]
        if y in datoja.bookmarks:
            datoja.bookmarks.remove(y)
        else:
            datoja.bookmarks+=[y]
        return palauta_paska()

datoja.urls+=('/lippu_(.*)','lippu')
class lippu:
    def GET(self,s):
        datoja.latti,datoja.longi=datoja.bookmarks[int(s)]
        return palauta_paska()

datoja.urls+=('/lippu2_(.*)','lippu2')
class lippu2:
    def GET(self,s):
        datoja.latti,datoja.longi,roina=datoja.bookmarks2[int(s)]
        return palauta_paska()


datoja.urls+=('/haku','haku')
class haku:
    def GET(self):
        datoja.zoomi = 10
        return palauta_paska()

datoja.urls+=('/taloja','taloja')
class taloja:
    def GET(self):
        datoja.zoomi = 13
        return palauta_paska()

datoja.urls+=('/kivia','kivia')
class kivia:
    def GET(self):
        datoja.zoomi = 15
        return palauta_paska()

datoja.urls+=('/online','online')
class online:
    def GET(self):
        if datoja.online == 'online':
            datoja.online = 'OFFLINE'
        else:
            datoja.online = 'online'
        return palauta_paska()

datoja.urls+=('/uusi','uusi')
class uusi:
    def GET(self):
        datoja.lue_uudestaan=True
        return palauta_paska()

def refresh_ei_toimi(s):
        return '<html> <head>\
        <meta http-equiv="refresh" content="0 %s "> </head> \
        <a href=%s>CLICK</a>\
        </html> '%(s,s)


if __name__ == "__main__":
    loaddatoja()
    app = web.application(datoja.urls, globals())
    app.run()
