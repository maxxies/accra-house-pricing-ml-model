from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

locate = 'tema community 8'
# try:
#     geolocator = Nominatim(user_agent="maxmawube@gmail.com")
#     geocode = RateLimiter(geolocator.geocode, min_delay_seconds=2)
#     location_coordinates = geocode(location, timeout=10)
#     latitude = location_coordinates.latitude
#     longitude = location_coordinates.longitude
# except :
#     latitude = None
#     longitude = None

geolocator = Nominatim(user_agent="test")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
location = geocode(locate)

print((location.latitude, location.longitude))
