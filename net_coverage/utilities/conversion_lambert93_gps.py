# It takes care of conversion between lambert93 and GPS coordinates formats
from pyproj import Transformer


def lambert93_to_gps(x, y):
    transformer = Transformer.from_crs("+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 +x_0=700000 +y_0=6600000 "
                                       "+ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs",
                                       "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs")
    err_msg = ""
    if not x or not y:
        return None, None, f"Error in conversion from lambert93 to GPS: " \
                           f"please review the provided coordinates x {x} - y {y}"
    try:
        long, lat = transformer.transform(x, y)
    except TypeError as e:
        long = None
        lat = None
        err_msg = e
    return lat, long, err_msg  # to have it in the common Gmaps-like format (LAT,LONG)

