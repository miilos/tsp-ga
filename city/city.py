from math import sqrt, radians, sin, cos, asin
from typing import Self


class City:
    def __init__(self, id: int, name: str, lat: float, lng: float):
        self.id = id
        self.name = name
        self.lat = lat
        self.lng = lng

    # calculates haversine distance to another city
    def distance_to(self, other_city: Self) -> float:
        R = 6372.8

        dLat = radians(other_city.lat - self.lat)
        dLng = radians(other_city.lng - self.lng)
        lat1 = radians(self.lat)
        lat2 = radians(other_city.lat)

        a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLng/2)**2
        c = 2 * asin(sqrt(a))

        return R * c