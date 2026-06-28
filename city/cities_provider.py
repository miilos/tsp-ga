from city.city import City

class CitiesProvider:
    CITIES_LIST = (
        City(0, "Belgrade", 44.7866, 20.4489),
        City(1, "Budapest", 47.4979, 19.0402),
        City(2, "Paris", 48.8566, 2.3522),
        City(3, "Rome", 41.9028, 12.4964),
        City(4, "Madrid", 40.4168, -3.7038),
        City(5, "Amsterdam", 52.3676, 4.9041),
        City(6, "Vienna", 48.21, 16.37),
        City(7, "London", 51.51, -0.13),
        City(8, "Brussels", 50.8503, 4.3517),
        City(9, "Nice", 43.7034, 7.2663),
        City(10, "Athens", 37.9838, 23.7275),
        City(11, "Lisbon", 38.725278, -9.15000),
        City(12, "Oslo", 59.9122, 10.7313),
        City(13, "Ljubljana", 46.0569, 14.5058),
        City(14, "Bern", 46.9480, 7.4474),
        City(15, "Dublin", 53.350140, -6.266155),
        City(16, "Reykjavik", 64.1470, -21.9408),
        City(17, "Copenhagen", 55.6761, 12.5683),
        # City(18, "Sydney", 33.8688, 151.2093)
    )

    def get_cities(self):
        return self.CITIES_LIST

    def get_city_by_id(self, city_id: int)-> City|None:
        for city in self.CITIES_LIST:
            if city.id == city_id:
                return city

        return None