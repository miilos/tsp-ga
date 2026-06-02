from city import City

class CitiesProvider:
    CITIES_LIST = (
        City("Belgrade", 44.7866, 20.4489),
        City("Budapest", 47.4979, 19.0402),
        City("Paris", 48.8566, 2.3522),
        City("Rome", 41.9028, 12.4964),
        City("Madrid", 40.4168, -3.7038),
        City("Amsterdam", 52.3676, 4.9041),
        City("Vienna", 48.21, 16.37),
        City("London", 51.51, -0.13),
    )

    def get_cities(self):
        return self.CITIES_LIST