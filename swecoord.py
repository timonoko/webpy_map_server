

import math


rt90_converter = None
sweref99tm_converter = None

def atanh(x):
 return math.log((1./x+1.) / (1./x-1.))/2.

def wgsToswe(lat, long):

    global sweref99tm_converter
    if (sweref99tm_converter == None):
        sweref99tm_converter = SwedishGeoPositionConverter("sweref_99_tm")
    return sweref99tm_converter.geodeticToGrid(lat, long)
    
def sweTowgs(n, e):
    global sweref99tm_converter
    if (sweref99tm_converter == None):
        sweref99tm_converter = SwedishGeoPositionConverter("sweref_99_tm")
    return sweref99tm_converter.gridToGeodetic(n, e)

class SwedishGeoPositionConverter(object):

    def __init__(self, projection = "sweref_99_tm"):
        self.__initialized = False
        self.__axis = 0.0 # Semi-major axis of the ellipsoid.
        self.__flattening = 0.0 # Flattening of the ellipsoid.
        self.__central_meridian = 0.0 # Central meridian for the projection.
        self.__lat_of_origin = 0.0 # Latitude of origin (not used).
        self.__scale = 0.0 # Scale on central meridian.
        self.__false_northing = 0.0 # Offset for origo.
        self.__false_easting = 0.0 # Offset for origo.
        self.__a_roof = 0.0
        self.__A = 0.0
        self.__B = 0.0
        self.__C = 0.0
        self.__D = 0.0
        self.__beta1 = 0.0
        self.__beta2 = 0.0
        self.__beta3 = 0.0
        self.__beta4 = 0.0
        self.__delta1 = 0.0
        self.__delta2 = 0.0
        self.__delta3 = 0.0
        self.__delta4 = 0.0
        self.__Astar = 0.0
        self.__Bstar = 0.0
        self.__Cstar = 0.0
        self.__Dstar = 0.0
        # Initial calculations.
        self.__setProjection(projection)
        self.__prepareEllipsoid()
    
    def geodeticToGrid(self, latitude, longitude):
        """
        Transformation from geodetic coordinates to grid coordinates.
        @param latitude
        @param longitude
        @return (north, east)
        (North corresponds to X in RT 90 and N in SWEREF 99.) 
        (East corresponds to Y in RT 90 and E in SWEREF 99.)
        """
        if (self.__initialized == False):
            return None
        deg_to_rad = math.pi / 180.0
        phi = latitude * deg_to_rad
        lambda_long = longitude * deg_to_rad
        lambda_zero = self.__central_meridian * deg_to_rad
        
        phi_star = phi - math.sin(phi) * math.cos(phi) * (self.__A + \
                self.__B*math.pow(math.sin(phi), 2) + \
                self.__C*math.pow(math.sin(phi), 4) + \
                self.__D*math.pow(math.sin(phi), 6))
        delta_lambda = lambda_long - lambda_zero
        xi_prim = math.atan(math.tan(phi_star) / math.cos(delta_lambda))
#        eta_prim = math.atan(math.cos(phi_star) * math.sin(delta_lambda))
        eta_prim = atanh(math.cos(phi_star) * math.sin(delta_lambda))
        north = self.__scale * self.__a_roof * (xi_prim + \
                self.__beta1 * math.sin(2.0*xi_prim) * math.cosh(2.0*eta_prim) + \
                self.__beta2 * math.sin(4.0*xi_prim) * math.cosh(4.0*eta_prim) + \
                self.__beta3 * math.sin(6.0*xi_prim) * math.cosh(6.0*eta_prim) + \
                self.__beta4 * math.sin(8.0*xi_prim) * math.cosh(8.0*eta_prim)) + \
                self.__false_northing
        east = self.__scale * self.__a_roof * (eta_prim + \
                self.__beta1 * math.cos(2.0*xi_prim) * math.sinh(2.0*eta_prim) + \
                self.__beta2 * math.cos(4.0*xi_prim) * math.sinh(4.0*eta_prim) + \
                self.__beta3 * math.cos(6.0*xi_prim) * math.sinh(6.0*eta_prim) + \
                self.__beta4 * math.cos(8.0*xi_prim) * math.sinh(8.0*eta_prim)) + \
                self.__false_easting
        north = round(north * 1000.0) / 1000.0
        east = round(east * 1000.0) / 1000.0
        return (north, east)
    
    def gridToGeodetic(self, north, east):

        if (self.__initialized == False):
            return None

        deg_to_rad = math.pi / 180
        lambda_zero = self.__central_meridian * deg_to_rad
        xi = (north - self.__false_northing) / (self.__scale * self.__a_roof)        
        eta = (east - self.__false_easting) / (self.__scale * self.__a_roof)
        xi_prim = xi - \
                self.__delta1*math.sin(2.0*xi) * math.cosh(2.0*eta) - \
                self.__delta2*math.sin(4.0*xi) * math.cosh(4.0*eta) - \
                self.__delta3*math.sin(6.0*xi) * math.cosh(6.0*eta) - \
                self.__delta4*math.sin(8.0*xi) * math.cosh(8.0*eta)
        eta_prim = eta - \
                self.__delta1*math.cos(2.0*xi) * math.sinh(2.0*eta) - \
                self.__delta2*math.cos(4.0*xi) * math.sinh(4.0*eta) - \
                self.__delta3*math.cos(6.0*xi) * math.sinh(6.0*eta) - \
                self.__delta4*math.cos(8.0*xi) * math.sinh(8.0*eta)
        phi_star = math.asin(math.sin(xi_prim) / math.cosh(eta_prim))
        delta_lambda = math.atan(math.sinh(eta_prim) / math.cos(xi_prim))
        lon_radian = lambda_zero + delta_lambda
        lat_radian = phi_star + math.sin(phi_star) * math.cos(phi_star) * \
                (self.__Astar + \
                 self.__Bstar*math.pow(math.sin(phi_star), 2) + \
                 self.__Cstar*math.pow(math.sin(phi_star), 4) + \
                 self.__Dstar*math.pow(math.sin(phi_star), 6))      
        lat = lat_radian * 180.0 / math.pi
        lon = lon_radian * 180.0 / math.pi
        return (lat, lon)
    
    def __prepareEllipsoid(self):
        """ Prepare calculations only related to the choosen ellipsoid. """
        if (self.__initialized == False):
            return None
        
        e2 = self.__flattening * (2.0 - self.__flattening)
        n = self.__flattening / (2.0 - self.__flattening)
        self.__a_roof = self.__axis / (1.0 + n) * (1.0 + n*n/4.0 + n*n*n*n/64.0)
        # Prepare ellipsoid-based stuff for geodetic_to_grid.
        self.__A = e2
        self.__B = (5.0*e2*e2 - e2*e2*e2) / 6.0
        self.__C = (104.0*e2*e2*e2 - 45.0*e2*e2*e2*e2) / 120.0
        self.__D = (1237.0*e2*e2*e2*e2) / 1260.0
        self.__beta1 = n/2.0 - 2.0*n*n/3.0 + 5.0*n*n*n/16.0 + 41.0*n*n*n*n/180.0
        self.__beta2 = 13.0*n*n/48.0 - 3.0*n*n*n/5.0 + 557.0*n*n*n*n/1440.0
        self.__beta3 = 61.0*n*n*n/240.0 - 103.0*n*n*n*n/140.0
        self.__beta4 = 49561.0*n*n*n*n/161280.0
        # Prepare ellipsoid-based stuff for grid_to_geodetic.
        self.__delta1 = n/2.0 - 2.0*n*n/3.0 + 37.0*n*n*n/96.0 - n*n*n*n/360.0
        self.__delta2 = n*n/48.0 + n*n*n/15.0 - 437.0*n*n*n*n/1440.0
        self.__delta3 = 17.0*n*n*n/480.0 - 37*n*n*n*n/840.0
        self.__delta4 = 4397.0*n*n*n*n/161280.0
        self.__Astar = e2 + e2*e2 + e2*e2*e2 + e2*e2*e2*e2
        self.__Bstar = -(7.0*e2*e2 + 17.0*e2*e2*e2 + 30.0*e2*e2*e2*e2) / 6.0
        self.__Cstar = (224.0*e2*e2*e2 + 889.0*e2*e2*e2*e2) / 120.0
        self.__Dstar = -(4279.0*e2*e2*e2*e2) / 1260.0

    def __setProjection(self, projection):
        if (projection == "sweref_99_tm"):
            self.__sweref99()
            self.__central_meridian = 15.00
            self.__lat_of_origin = 0.0
            self.__scale = 0.9996
            self.__false_northing = 0.0
            self.__false_easting = 500000.0
            self.__initialized = True
        elif (projection == "sweref_99_1200"):
            self.__sweref99()
            self.__central_meridian = 12.00
            self.__initialized = True
        elif (projection == "sweref_99_1330"):
            self.__sweref99()
            self.__central_meridian = 13.50
            self.__initialized = True
        elif (projection == "sweref_99_1500"):
            self.__sweref99()
            self.__central_meridian = 15.00
            self.__initialized = True
        elif (projection == "sweref_99_1630"):
            self.__sweref99()
            self.__central_meridian = 16.50
            self.__initialized = True
        elif (projection == "sweref_99_1800"):
            self.__sweref99()
            self.__central_meridian = 18.00
            self.__initialized = True
        elif (projection == "sweref_99_1415"):
            self.__sweref99()
            self.__central_meridian = 14.25
            self.__initialized = True
        elif (projection == "sweref_99_1545"):
            self.__sweref99()
            self.__central_meridian = 15.75
            self.__initialized = True
        elif (projection == "sweref_99_1715"):
            self.__sweref99()
            self.__central_meridian = 17.25
            self.__initialized = True
        elif (projection == "sweref_99_1845"):
            self.__sweref99()
            self.__central_meridian = 18.75
            self.__initialized = True
        elif (projection == "sweref_99_2015"):
            self.__sweref99()
            self.__central_meridian = 20.25
            self.__initialized = True
        elif (projection == "sweref_99_2145"):
            self.__sweref99()
            self.__central_meridian = 21.75
            self.__initialized = True
        elif (projection == "sweref_99_2315"):
            self.__sweref99()
            self.__central_meridian = 23.25
            self.__initialized = True
        # For testing.
        elif (projection == "test_case"):
            # Test-case:
            #    Lat: 66 0'0", long: 24 0'0".
            #    X:1135809.413803 Y:555304.016555.
            self.__axis = 6378137.0
            self.__flattening = 1.0 / 298.257222101
            self.__central_meridian = 13.0 + 35.0/60.0 + 7.692000/3600.0
            self.__lat_of_origin = 0.0
            self.__scale = 1.000002540000
            self.__false_northing = -6226307.8640
            self.__false_easting = 84182.8790
            self.__initialized = True
        else:
            self.__initialized = False
    
    def __grs80(self):
        """ Default parameters for the GRS80 ellipsoid. """
        self.__axis = 6378137.0
        self.__flattening = 1.0 / 298.257222101
        self.__lat_of_origin = 0.0

    def __bessel(self):
        """ Default parameters for the Bessel 1841 ellipsoid. """
        self.__axis = 6377397.155
        self.__flattening = 1.0 / 299.1528128
        self.__lat_of_origin = 0.0
        self.__scale = 1.0
        self.__false_northing = 0.0
        self.__false_easting = 1500000.0

    def __sweref99(self):
        """ Default parameters for the SWEREF 99 ellipsoid. """
        self.__axis = 6378137.0
        self.__flattening = 1.0 / 298.257222101
        self.__lat_of_origin = 0.0
        self.__scale = 1.0
        self.__false_northing = 0.0
        self.__false_easting = 150000.0
