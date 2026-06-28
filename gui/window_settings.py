class WindowSettings:
    def __init__(self, title, width, map_height, info_height, margin, appearance_mode):
        self.title = title
        # width is shared by both the map and the info box
        self.width = width
        self.map_height = map_height
        self.info_height = info_height
        self.margin = margin
        self.appearance_mode = appearance_mode
