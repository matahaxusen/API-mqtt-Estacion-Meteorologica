from geopy.geocoders import Nominatim

def gps_ll(direccion):
    geolocator = Nominatim(user_agent='myapplication')
    location = geolocator.geocode(direccion)
    lngltd = str(location.latitude) +', '+ str(location.longitude)
    return lngltd
