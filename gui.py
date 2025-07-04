import tkinter as tk
# =======================
# Urban Dead RPG - Table of Contents
# =======================
# - Player
# - World
# - Location
# - Building
# - GameEngine
# - UrbanDeadGUI (Tkinter GUI)
# - main launcher
# =======================

import random, time
import tkinter as tk

# --- Player ---
class Player:
    def __init__(self, name, x=0, y=0):
        self.name = name
        self.HP = 50
        self.maxHP = 50  # added maxHP attribute
        self.AP = 50  # added AP attribute
        self.maxAP = 50  # added maxAP attribute
        self.x = x
        self.y = y
        self.Outside = False  # True if player is outside, False if inside a building
        self.Living = True
        self.Zombie = False
        self.infected = False
        self.XP = 0
        self.level = 1
        self.inventory = []
        self.skills = []
        self.equipment = []

    def set_position(self, x, y):
        self.x = x
        self.y = y

# --- World, Location, Building ---
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

# --- GameEngine ---
class GameEngine:
    def __init__(self):
        self.player = None
        self.world = None
        self.is_running = True
    def run(self):
        print("Welcome to Urban Dead RPG!")
        while self.is_running:
            self.display_status()
            self.handle_input()
    def display_status(self):
        if self.player and self.world:
            loc = self.world.get_location(self.player.x, self.player.y)
            print(f"\nYou are at: {loc.name} [{self.player.x},{self.player.y}]")
            print(loc.description)
            print(f"Tile type: {loc.tile_type}")
            print(f"HP: {self.player.HP}")
    def handle_input(self):
        command = input("> ").lower().strip()
        direction_map = {
            '8': (-1, 0),    # North
            '2': (1, 0),     # South
            '4': (0, -1),    # West
            '6': (0, 1),     # East
            '7': (-1, -1),   # NW
            '9': (-1, 1),    # NE
            '1': (1, -1),    # SW
            '3': (1, 1),     # SE
        }
        if command == "quit":
            print("Thanks for playing!")
            self.is_running = False
        elif command in direction_map:
            dx, dy = direction_map[command]
            new_x = self.player.x + dx
            new_y = self.player.y + dy
            if self.world.get_location(new_x, new_y):
                self.player.set_position(new_x, new_y)
                print(f"You move to [{new_x},{new_y}].")
            else:
                print("You can't move outside the suburb!")
        else:
            print("Unknown command. Use numpad directions (8,2,4,6,7,9,1,3) or 'quit'.")

class UrbanDeadGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Urban Dead RPG")

        # Set up game engine
        self.engine = GameEngine()
        self.world = World(width=10, height=10)
        px, py = self.world.get_random_empty_tile()
        self.player = Player("Survivor", x=px, y=py)
        self.engine.player = self.player
        self.engine.world = self.world

        # Map grid (3x3) - now buttons
        self.map_buttons = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                rel_dx = i - 1
                rel_dy = j - 1
                if rel_dx == 0 and rel_dy == 0:
                    # Center tile: display only, not clickable
                    btn = tk.Label(root, width=10, height=3, relief="ridge", borderwidth=2, font=("Consolas", 10), bg="yellow")
                else:
                    btn = tk.Button(root, width=10, height=3, relief="ridge", borderwidth=2, font=("Consolas", 10),
                                    command=lambda dx=rel_dx, dy=rel_dy: self.move(dx, dy))
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.map_buttons[i][j] = btn

        # Description panel (beside the map)
        self.desc_panel = tk.Label(root, text="", anchor="nw", justify="left", width=30, height=6, font=("Consolas", 10), relief="groove", borderwidth=2)
        self.desc_panel.grid(row=0, column=3, rowspan=3, padx=8, pady=2, sticky="n")

        # Interaction buttons (below description)
        # Add label above actions
        self.actions_label = tk.Label(root, text="Available Actions:", font=("Consolas", 10, "bold"))
        self.actions_label.grid(row=2, column=3, padx=8, pady=(10, 0), sticky="sw")

        self.action_frame = tk.Frame(root)
        self.action_frame.grid(row=3, column=3, padx=8, pady=2, sticky="nw")
        self.action_buttons = {}
        actions = [
            ("Open Door", self.open_door),
            ("Close Door", self.close_door),
            ("Barricade", self.barricade),
            ("Enter/Exit", self.enter_exit),
            ("Jump from Window", self.jump_window),
            ("Search", self.search),
            # Suggestions for future actions:
            # ("Smash Generator", self.smash_genny),
            # ("Refuel Generator", self.refuel_genny),
            # ("Repair", self.repair),
        ]
        for idx, (label, callback) in enumerate(actions):
            btn = tk.Button(self.action_frame, text=label, width=15, command=callback)
            btn.grid(row=idx, column=0, pady=2, sticky="w")
            self.action_buttons[label] = btn

        # Bind numpad keys for movement
        key_dir = {
            '1': (1, -1), '2': (1, 0), '3': (1, 1),
            '4': (0, -1),              '6': (0, 1),
            '7': (-1, -1), '8': (-1, 0), '9': (-1, 1)
        }
        for key, (dx, dy) in key_dir.items():
            self.root.bind(f'<Key-{key}>', lambda e, dx=dx, dy=dy: self.move(dx, dy))
            self.root.bind(f'<KP_{key}>', lambda e, dx=dx, dy=dy: self.move(dx, dy))

        # Status label
        self.status = tk.Label(root, text="", font=("Consolas", 10))
        self.status.grid(row=4, column=0, columnspan=3)

        # God mode toggle button (bottom right)
        self.god_mode = False
        self.god_btn = tk.Button(root, text="God Mode: OFF", command=self.toggle_god_mode, bg="lightgray")
        self.god_btn.grid(row=5, column=3, sticky="se", padx=8, pady=8)

        self.update_map()

    def update_description(self):
        loc = self.world.get_location(self.player.x, self.player.y)
        desc = loc.description
        if loc.tile_type == 'building':
            b = loc.building
            desc += f"\n{b.barricade_desc()} | {b.ruin_desc()}"
            desc += f"\nGenerator: {'on' if b.Genny else 'off'}, Fuelled: {'yes' if b.Fuelled else 'no'}"
            desc += f"\nYou are {'outside' if self.player.Outside else 'inside'} the building."
        self.desc_panel["text"] = desc

    def update_actions(self):
        loc = self.world.get_location(self.player.x, self.player.y)
        # Hide all action buttons by default
        for label, btn in self.action_buttons.items():
            btn.grid_remove()
        # Only show buttons for actions that are currently possible
        if loc.tile_type == 'building':
            b = loc.building
            if self.player.Outside:
                # Open Door: only if door is closed and not barricaded
                if not b.DoorsOpen and b.Barricaded == 0:
                    self.action_buttons["Open Door"].grid()
                # Close Door: only if door is open and not barricaded
                if b.DoorsOpen and b.Barricaded == 0:
                    self.action_buttons["Close Door"].grid()
                # Enter/Exit: only if doors open and not barricaded
                if b.DoorsOpen and b.Barricaded == 0:
                    self.action_buttons["Enter/Exit"].grid()
            else:
                # Barricade: only if not ruined and not at max barricade
                # must add condition:                 if b.Ruined == 0 and b.Barricaded < b.MAX_BARRICADE:
                self.action_buttons["Barricade"].grid()
                # Enter/Exit: only if doors open and not barricaded
                if b.DoorsOpen and b.Barricaded == 0:
                    self.action_buttons["Enter/Exit"].grid()
                # Jump from Window: only if barricaded and inside
                if self.player.Outside == False:
                    self.action_buttons["Jump from Window"].grid()
                self.action_buttons["Search"].grid()
        else:
            # Not a building: only Search is available
            self.action_buttons["Search"].grid()
        # Buttons are now only visible if the action is possible

    def open_door(self):
        loc = self.world.get_location(self.player.x, self.player.y)
        if loc.tile_type == 'building':
            b = loc.building
            if not b.DoorsOpen and b.Barricaded == 0:
                b.DoorsOpen = True
            elif b.Barricaded > 0:
                self.status["text"] = "The barricades prevent you from opening the door."
        self.update_map()

    def close_door(self):
        loc = self.world.get_location(self.player.x, self.player.y)
        if loc.tile_type == 'building':
            b = loc.building
            if b.DoorsOpen and b.Barricaded == 0:
                b.DoorsOpen = False
        self.update_map()

    def barricade(self):
        loc = self.world.get_location(self.player.x, self.player.y)
        if loc.tile_type == 'building':
            b = loc.building
            if not self.player.Outside and b.Ruined == 0 and b.Barricaded < b.MAX_BARRICADE:
                b.Barricaded += 1
                b.DoorsOpen = False  # Cading closes the doors
        self.update_map()

    def enter_exit(self):
        loc = self.world.get_location(self.player.x, self.player.y)
        if loc.tile_type == 'building':
            b = loc.building
            if self.player.Outside:
                if b.DoorsOpen and b.Barricaded == 0:
                    self.player.Outside = False
            else:
                if b.DoorsOpen and b.Barricaded == 0:
                    self.player.Outside = True
        self.update_map()

    def jump_window(self):
        import tkinter.messagebox as mb
        if not self.player.Living:
            self.status["text"] = "You are already dead."
            return
        if mb.askyesno("Jump from Window", "It will be fatal and the dev hasn't made any revive features yet! Are you sure?"):
            self.player.Outside = True
            self.player.Living = False
            self.status["text"] = "You leap from the window and plummet to the ground. Your vision fades as you hit the pavement."
            self.update_map()

    def search(self):
        # Placeholder for search logic
        self.status["text"] = "You search the area, but find nothing."

    def move(self, dx, dy):
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        loc = self.world.get_location(new_x, new_y)
        if loc:
            self.player.set_position(new_x, new_y)
            # If moving onto a building, player remains outside, 
            # except if moving building to building with freerunning(adding skills later)
            if loc.tile_type == 'building':
                self.player.Outside = True
            else:
                self.player.Outside = False
        self.update_map()

    def update_map(self):
        px, py = self.player.x, self.player.y
        for i in range(3):
            for j in range(3):
                wx = px + (i-1)
                wy = py + (j-1)
                loc = self.world.get_location(wx, wy)
                text = f"{loc.tile_type}" if loc else "---"
                btn = self.map_buttons[i][j]
                if isinstance(btn, tk.Label):
                    btn["text"] = text
                    btn["bg"] = "yellow"
                else:
                    btn["text"] = text
                    btn["state"] = tk.NORMAL if loc else tk.DISABLED
                    btn["bg"] = "white"
        # Only show vital stats, not coordinates
        status = f"HP: {self.player.HP}/{self.player.maxHP} | AP: {self.player.AP} | "
        status += f"Level: {self.player.level} | XP: {self.player.XP} | "
        status += "Alive" if self.player.Living else "Dead"
        if getattr(self, 'god_mode', False):
            status += " | GOD MODE"
        self.status["text"] = status
        # Update description panel
        self.update_description()
        # Update action buttons
        self.update_actions()

    def toggle_god_mode(self):
        self.god_mode = not self.god_mode
        self.god_btn["text"] = f"God Mode: {'ON' if self.god_mode else 'OFF'}"
        self.god_btn["bg"] = "lightgreen" if self.god_mode else "lightgray"
        #show
        self.update_map()

if __name__ == "__main__":
    root = tk.Tk()
    app = UrbanDeadGUI(root)
    root.mainloop()
