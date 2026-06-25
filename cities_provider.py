from city import City

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
    )

    def get_cities(self):
        return self.CITIES_LIST

    def get_city_by_id(self, city_id: int)-> City|None:
        for city in self.CITIES_LIST:
            if city.id == city_id:
                return city

        return None