import tkinter as tk
import customtkinter as ctk
from cities_provider import CitiesProvider
from projector import make_projector
from window_settings import WindowSettings

window_settings = WindowSettings("TSP",900,650,40, "System")

ctk.set_appearance_mode(window_settings.appearance_mode)

app = ctk.CTk()
app.geometry(f"{window_settings.width}x{window_settings.height}")
app.title(window_settings.title)

canvas = tk.Canvas(
    app,
    width=window_settings.width,
    height=window_settings.height,
    bg="#628717"
)
canvas.pack()

cities_provider = CitiesProvider()
cities = cities_provider.get_cities()

project = make_projector(cities, window_settings)

for city in cities:
    x, y = project(city.lat, city.lng)
    r = 5
    canvas.create_oval(x - r, y - r, x + r, y + r, fill="#000", outline="")
    canvas.create_text(x, y - 14, text=city.name, fill="#000")

app.mainloop()