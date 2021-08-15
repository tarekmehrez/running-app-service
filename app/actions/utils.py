from math import radians, cos, sin, asin, sqrt


async def haversine_distance_km(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:

    radius = 6372.8
    diff_lat = radians(lat2 - lat1)
    diff_lon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(diff_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(diff_lon / 2) ** 2
    c = 2 * asin(sqrt(a))

    return radius * c
