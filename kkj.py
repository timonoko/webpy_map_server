import math

def KKJxy_to_KKJlalo(KKJ, ZoneNumber):
    MinLa = math.radians(59.0)
    MaxLa = math.radians(70.5)
    MinLo = math.radians(18.5)
    MaxLo = math.radians(32.0)

    for i in range(1, 35):
        DeltaLa = MaxLa - MinLa
        DeltaLo = MaxLo - MinLo
        LALO = {'La':MinLa + 0.5 * DeltaLa, 'Lo':MinLo + 0.5 * DeltaLo}

        kkjx,kkjy  = _kkj_latlon_to_kkj_xy((LALO['La'],LALO['Lo']), ZoneNumber)
        KKJt = {'X':kkjx, 'Y':kkjy}

        if KKJt['X'] < KKJ['X']:
            MinLa = MinLa + 0.45 * DeltaLa
        else:
            MaxLa = MinLa + 0.55 * DeltaLa

        if KKJt['Y'] < KKJ['Y']:
            MinLo = MinLo + 0.45 * DeltaLo
        else:
            MaxLo = MinLo + 0.55 * DeltaLo;
    return LALO


def KKJlalo_to_WGSlalo(KKJ):
    La = math.degrees(KKJ['La'])
    Lo = math.degrees(KKJ['Lo'])

    dLa = math.radians(  0.124867E+01       +
                     -0.269982E+00 * La +
                     0.191330E+00 * Lo +
                     0.356119E-02 * La * La +
                     -0.122312E-02 * La * Lo +
                     -0.335514E-03 * Lo * Lo ) / 3600.0
    dLo = math.radians( -0.286111E+02       +
                    0.114183E+01 * La +
                    -0.581428E+00 * Lo +
                    -0.152421E-01 * La * La +
                    0.118177E-01 * La * Lo +
                    0.826646E-03 * Lo * Lo ) / 3600.0

    WGS = {}
    WGS['La'] = KKJ['La'] + dLa
    WGS['Lo'] = KKJ['Lo'] + dLo

    return WGS

def KKJ2WGS(KKJ, zoneNumber):
    """KKJ = (x,y)"""
    x,y = KKJ
    KKJdict = {'X':x, 'Y':y}
    KKJ = KKJxy_to_KKJlalo(KKJdict, zoneNumber)
    WGSdict = KKJlalo_to_WGSlalo(KKJ)
    return WGSdict['La'],WGSdict['Lo']


def WGS2KKJ(coordinate_latlon):
    lat,lon = coordinate_latlon

    dla = math.radians(-0.124766E+01 + 0.269941E+00 * lat + \
                       -0.191342E+00 * lon + -0.356086E-02 * lat * lat + \
                        0.122353E-02 * lat * lon +
                        0.335456E-03 * lon * lon ) / 3600.0

    dlo = math.radians(0.286008E+02 + -0.114139E+01 * lat + \
                       0.581329E+00 * lon + 0.152376E-01 * lat * lat + \
                      -0.118166E-01 * lat * lon + \
                      -0.826201E-03 * lon * lon ) / 3600.0
    #print dla,dlo
           
    kkj_lat = math.radians(lat) + dla
    kkj_lon = math.radians(lon) + dlo   
    #print 'KKJ lat lon: %f, %f' % (kkj_lat,kkj_lon)
    return _kkj_latlon_to_kkj_xy((kkj_lat,kkj_lon),2)


def _kkj_latlon_to_kkj_xy(kkj_latlon, zone_number):
    kkj_lat, kkj_lon = kkj_latlon
    lon0 = math.radians(zone_number * 3.0 + 18.0)
    #print lon0
    lon = kkj_lon - lon0
    
    a  = 6378388.0            # Hayford ellipsoid
    f  = 1/297.0
    
    b  = (1.0 - f) * a
    bb = b * b   
    c  = (a / b) * a
    ee = (a * a - bb) / bb
    n = (a - b)/(a + b)
    nn = n * n
    
    cosLa = math.cos(kkj_lat)
    NN = ee * cosLa * cosLa
    
    LaF = math.atan(math.tan(kkj_lat) / math.cos(lon * math.sqrt(1 + NN)))
    cosLaF = math.cos(LaF)
    
    t   = (math.tan(lon) * cosLaF) / math.sqrt(1 + ee * cosLaF * cosLaF)

    A   = a / ( 1 + n )

    A1  = A * (1 + nn / 4 + nn * nn / 64)

    A2  = A * 1.5 * n * (1 - nn / 8)

    A3  = A * 0.9375 * nn * (1 - nn / 4)

    A4  = A * 35/48.0 * nn * n
    
    kkj_x = A1 * LaF - A2 * math.sin(2*LaF) + A3 * math.sin(4*LaF) - \
            A4 * math.sin(6*LaF)
    kkj_y = c * math.log(t + math.sqrt(1+t*t)) \
            + 500000.0 + zone_number * 1000000.0
    return kkj_x,kkj_y    
