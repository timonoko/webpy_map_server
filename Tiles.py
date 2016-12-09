
import math

octalStrings = ('000', '001', '010', '011', '100', '101', '110', '111')

def toBinaryString(i):
    """ Return a binary string for an integer.
    """
    return ''.join([octalStrings[int(c)]
                    for c
                    in oct(i)]).lstrip('0')

def fromBinaryString(s):
    """ Return an integer for a binary string.
    """
    s = list(s)
    e = 0
    i = 0
    while(len(s)):
        if(s[-1]) == '1':
            i += int(math.pow(2, e))
        e += 1
        s.pop()
    return i

def fromYahoo(x, y, z):
    """ Return column, row, zoom for Yahoo x, y, z.
    """
    zoom = 18 - z
    row = int(math.pow(2, zoom - 1) - y - 1)
    col = x
    return col, row, zoom

def toYahoo(col, row, zoom):
    """ Return x, y, z for Yahoo tile column, row, zoom.
    """
    x = col
    y = int(math.pow(2, zoom - 1) - row - 1)
    z = 18 - zoom
    return x, y, z

def fromYahooRoad(x, y, z):
    """ Return column, row, zoom for Yahoo Road tile x, y, z.
    """
    return fromYahoo(x, y, z)

def toYahooRoad(col, row, zoom):
    """ Return x, y, z for Yahoo Road tile column, row, zoom.
    """
    return toYahoo(col, row, zoom)

def fromYahooAerial(x, y, z):
    """ Return column, row, zoom for Yahoo Aerial tile x, y, z.
    """
    return fromYahoo(x, y, z)

def toYahooAerial(col, row, zoom):
    """ Return x, y, z for Yahoo Aerial tile column, row, zoom.
    """
    return toYahoo(col, row, zoom)

microsoftFromCorners = {'0': '00', '1': '01', '2': '10', '3': '11'}
microsoftToCorners = {'00': '0', '01': '1', '10': '2', '11': '3'}

def fromMicrosoft(s):
    """ Return column, row, zoom for Microsoft tile string.
    """
    row, col = map(fromBinaryString, zip(*[list(microsoftFromCorners[c]) for c in s]))
    zoom = len(s)
    return col, row, zoom

def toMicrosoft(col, row, zoom):
    """ Return string for Microsoft tile column, row, zoom.
    """
    x = col
    y = row
    y, x = toBinaryString(y).rjust(zoom, '0'), toBinaryString(x).rjust(zoom, '0')
    string = ''.join([microsoftToCorners[y[c]+x[c]] for c in range(zoom)])
    return string

def fromMicrosoftRoad(s):
    """ Return column, row, zoom for Microsoft Road tile string.
    """
    return fromMicrosoft(s)

def toMicrosoftRoad(col, row, zoom):
    """ Return x, y, z for Microsoft Road tile column, row, zoom.
    """
    return toMicrosoft(col, row, zoom)

def fromMicrosoftAerial(s):
    """ Return column, row, zoom for Microsoft Aerial tile string.
    """
    return fromMicrosoft(s)

def toMicrosoftAerial(col, row, zoom):
    """ Return x, y, z for Microsoft Aerial tile column, row, zoom.
    """
    return toMicrosoft(col, row, zoom)

