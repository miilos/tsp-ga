from collections.abc import Callable
from city import City
from window_settings import WindowSettings


def make_projector(cities: list[City], window_settings: WindowSettings)-> Callable:
    lats = [c.lat for c in cities]
    lngs = [c.lng for c in cities]
    min_lat, max_lat = min(lats), max(lats)
    min_lng, max_lng = min(lngs), max(lngs)

    # prevent division by 0 later if all the cities happen to be in one line
    span_lat = (max_lat - min_lat) or 1
    span_lng = (max_lng - min_lng) or 1

    # return a closure so that the above computations only need to run once,
    # and then only the closure can be called with those results in the draw loop
    def project(lat: float, lng: float):
        # normalize lat and lng to a [0,1] interval
        nx = (lng - min_lng) / span_lng
        ny = (lat - min_lat) / span_lat

        # map the normalized coordinates onto the canvas
        x = window_settings.margin + nx * (window_settings.width - 2 * window_settings.margin)
        y = window_settings.margin + (1 - ny) * (window_settings.height - 2 * window_settings.margin)
        return x, y

    return project
