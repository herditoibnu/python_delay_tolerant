# Getting distance between two points based on latitude/longitude

from math import sin, cos, sqrt, atan2, radians, floor

# approximate radius of earth in km
R = 6373.0

lat1 = radians(52.2296756) # 52
lon1 = radians(21.0122287) # 21
lat2 = radians(52.406374) # 52
lon2 = radians(16.9251681) # 16

dlon = lon2 - lon1
dlat = lat2 - lat1

a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))

distance = floor(R * c)
if distance == 278: # 342
    print "haha"

print("Result:", distance)
print("Should be:", 278.546, "km")