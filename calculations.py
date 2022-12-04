import math


def get_bounds(latitude, longitude, km):
    bounds = {}

    # turns diagonal to x and y length (for example when km is 10km this variable will be "3.5355339059327378" the length of a single axis )
    diameter_to_x_y = math.sqrt(km**2 / 2) / 2
    # one degree of latittude is equal to 110.547 km
    one_latitude_in_km = 110.574
    # one degree of longitude is equal to cos(latitude) * 111.320
    one_longitude_in_km = abs(math.cos(math.radians(latitude)) * 111.320)

    bounds['lat_max'] = round(
        latitude + (diameter_to_x_y / one_latitude_in_km), 6)
    bounds['lat_min'] = round(
        latitude - (diameter_to_x_y / one_latitude_in_km), 6)
    bounds['long_max'] = round(
        longitude + (diameter_to_x_y / one_longitude_in_km), 6)
    bounds['long_min'] = round(
        longitude - (diameter_to_x_y / one_longitude_in_km), 6)

    return bounds


def angle_to_compass(angle):
    directions = ['N', 'NE', 'E', 'S', 'S', 'SW', 'W', 'NW', 'N']
    if angle < 0:
        angle += 360

    return directions[round(angle / 45)]


def calculate_flyby(angle, flight_lat, flight_long, your_lat, your_long):
    distance = get_distance_from_lat_lon_in_km(
        flight_lat, flight_long, your_lat, your_long)
    one_latitude_in_km = 110.574
    one_longitude_in_km = abs(math.cos(math.radians(your_lat)) * 111.320)
    lat_km = distance * math.cos(math.radians(angle))
    long_km = distance * math.sin(math.radians(angle))

    new_lat = round(flight_lat + (lat_km / one_latitude_in_km), 6)
    new_long = round(flight_long + (long_km / one_longitude_in_km), 6)

    return {'lat': new_lat, 'long': new_long}


def get_distance_from_lat_lon_in_km(lat1, lon1, lat2, lon2):
    earth_radius = 6371
    # Radius of the earth in km
    dLat = deg_2_rad(lat2-lat1)
    # deg2rad below
    dLon = deg_2_rad(lon2-lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg_2_rad(lat1)) * \
        math.cos(deg_2_rad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = earth_radius * c
    # Distance in km
    return dist


def deg_2_rad(deg):
    return deg * (math.pi/180)


def feet_to_meter(ft):
    return round(ft * 0.3048)


def kts_to_kmph(kts):
    return round(kts * 1.852)
