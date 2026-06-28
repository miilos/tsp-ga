import threading

from city.cities_provider import CitiesProvider
from file.file_writer import FileWriter
from ga.ga import Ga
from gui.gui_handler import GuiHandler
from gui.window_settings import WindowSettings

provider = CitiesProvider()
window_settings = WindowSettings("TSP", 900, 650, 120, 40, "System")

gui = GuiHandler(provider, window_settings)

file_writer = FileWriter("run_log.txt")

ga = Ga(provider, generation_delay=0.3)
ga.subscribe(gui)
ga.subscribe(file_writer)

gui.create_window(on_ready=lambda: threading.Thread(target=ga.run, daemon=True).start())
