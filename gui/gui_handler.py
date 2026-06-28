import tkinter as tk
import customtkinter as ctk
from city.cities_provider import CitiesProvider
from city.city import City
from ga.generation_info import GenerationInfo
from gui.projector import make_projector
from gui.window_settings import WindowSettings
from observer.subscriber_interface import SubscriberInterface


class GuiHandler(SubscriberInterface):
    MAP_BG = "#628717"
    TEXT_COLOR = "#000"

    MAP_POINT_RADIUS = 5
    MAP_POINT_TEXT_OFFSET = 14

    INFO_PADDING = 12
    INFO_TEMPLATE = (
        "Current best path: {path}\n"
        "Distance: {distance}\n"
        "Current generation: {generation}"
    )

    def __init__(self, cities_provider: CitiesProvider, window_settings: WindowSettings):
        self.window_settings = window_settings
        self.app = None
        self.map = None
        self.info_label = None

        self.cities_provider = cities_provider
        self.cities = self.cities_provider.get_cities()

        self.project = make_projector(self.cities, self.window_settings)

    def create_window(self, on_ready=None) -> None:
        ctk.set_appearance_mode(self.window_settings.appearance_mode)

        self.app = ctk.CTk()
        total_height = self.window_settings.map_height + self.window_settings.info_height
        self.app.geometry(f"{self.window_settings.width}x{total_height}")
        self.app.title(self.window_settings.title)

        self._create_map(self.app)
        self._create_info_box(self.app)

        if on_ready is not None:
            self.app.after(0, on_ready)

        self.app.mainloop()

    def _create_map(self, app) -> None:
        self.map = tk.Canvas(
            app,
            width=self.window_settings.width,
            height=self.window_settings.map_height,
            bg=self.MAP_BG
        )
        self.map.pack()
        self._draw_cities(self.cities)

    def _draw_cities(self, cities: list[City]) -> None:
        for city in cities:
            x, y = self.project(city.lat, city.lng)
            self.map.create_oval(x - self.MAP_POINT_RADIUS, y - self.MAP_POINT_RADIUS, x + self.MAP_POINT_RADIUS, y + self.MAP_POINT_RADIUS, fill=self.TEXT_COLOR, outline="")
            self.map.create_text(x, y - self.MAP_POINT_TEXT_OFFSET, text=city.name, fill=self.TEXT_COLOR)

    def draw_path(self, path: list[int]) -> None:
        self.map.delete("path")
        coords = { city.id: self.project(city.lat, city.lng) for city in self.cities }

        for i in range(len(path)):
            x1, y1 = coords[path[i]]
            x2, y2 = coords[path[(i + 1) % len(path)]]
            self.map.create_line(x1, y1, x2, y2, fill=self.TEXT_COLOR, width=2, tags="path")

    def _create_info_box(self, app) -> None:
        info_frame = ctk.CTkFrame(
            app,
            width=self.window_settings.width,
            height=self.window_settings.info_height,
            corner_radius=0,
        )
        info_frame.pack(fill="x")
        info_frame.pack_propagate(False)

        self.info_label = ctk.CTkLabel(
            info_frame,
            text=self._format_info(),
            justify="left",
            anchor="nw",
        )
        self.info_label.pack(fill="both", expand=True, padx=self.INFO_PADDING, pady=self.INFO_PADDING)

    def _format_info(self, best_path="", distance="", generation="") -> str:
        return self.INFO_TEMPLATE.format(path=best_path, distance=distance, generation=generation)

    def update_info(self, best_path: list[int], distance: float, generation: int) -> None:
        best_path_str = " - ".join([ self.cities_provider.get_city_by_id(city_id).name for city_id in best_path ])
        self.info_label.configure(text=self._format_info(
            best_path_str, str(distance), str(generation))
        )

    def update(self, generation_info: GenerationInfo) -> None:
        if self.app is None:
            return
        self.app.after(0, lambda: self._render(generation_info))

    def _render(self, generation_info: GenerationInfo) -> None:
        try:
            self.draw_path(generation_info.best_individual)
            self.update_info(
                generation_info.best_individual,
                generation_info.best_cost,
                generation_info.generation_num
            )
        except tk.TclError:
            pass
