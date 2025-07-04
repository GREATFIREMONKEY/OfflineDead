import random

class World:
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.grid = []
        for x in range(width):
            row = []
            for y in range(height):
                if random.random() < 0.4:
                    row.append(Location(x, y, 'building', 'A large, derelict building.'))
                else:
                    row.append(Location(x, y, 'road', 'A cracked and empty road.'))
            self.grid.append(row)

    def get_location(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None

    def get_random_empty_tile(self):
        # Returns random (x, y) on a road tile
        candidates = [(x, y) for x in range(self.width) for y in range(self.height)
                      if self.grid[x][y].tile_type == 'road']
        return random.choice(candidates) if candidates else (0, 0)

class Location:
    def __init__(self, x, y, tile_type, description):
        self.x = x
        self.y = y
        self.tile_type = tile_type  # e.g., 'road', 'building'
        self.description = description
        self.building = Building() if tile_type == 'building' else None

    @property
    def name(self):
        return f"({self.x},{self.y}) {self.tile_type.title()}"

class Building:
    MAX_BARRICADE = 21  # Urban Dead max cades
    MAX_RUIN = 25       # Arbitrary for realism, can be tuned

    BARRICADE_DESCS = [
        (0, "Doors open"),
        (1, "Doors closed"),
        (2, "Loose Barricade"),
        (5, "Lightly Barricaded"),
        (10, "Very Strongly Barricaded"),
        (15, "Heavily Barricaded"),
        (20, "Very Heavily Barricaded"),
        (21, "Extremely Heavily Barricaded"),
    ]
    RUIN_DESCS = [
        (0, "Clean"),
        (5, "Light Ruin"),
        (15, "Heavy Ruin"),
        (25, "Completely Ruined"),
    ]

    def __init__(self, DoorsOpen=False, Barricaded=0, Genny=False, Fuelled=False, Ruined=0):
        self.DoorsOpen = DoorsOpen
        self.Barricaded = Barricaded
        self.Genny = Genny
        self.Fuelled = Fuelled
        self.Ruined = Ruined

    def barricade_desc(self):
        for level, desc in reversed(self.BARRICADE_DESCS):
            if self.Barricaded >= level:
                return desc
        return "Unbarricaded"

    def ruin_desc(self):
        for level, desc in reversed(self.RUIN_DESCS):
            if self.Ruined >= level:
                return desc
        return "This building is not yet showing any damage."
