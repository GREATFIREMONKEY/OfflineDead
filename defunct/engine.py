class GameEngine:
    def __init__(self):
        self.player = None
        self.world = None
        self.is_running = True

    def run(self):
        """The main game loop."""
        print("Welcome to Urban Dead RPG!")
        
        while self.is_running:
            self.display_status()
            self.handle_input()

    def display_status(self):
        """Displays the player's current status and location."""
        if self.player and self.world:
            loc = self.world.get_location(self.player.x, self.player.y)
            print(f"\nYou are at: {loc.name} [{self.player.x},{self.player.y}]")
            print(loc.description)
            print(f"Tile type: {loc.tile_type}")
            print(f"HP: {self.player.hp}")

    def handle_input(self):
        """Handles player input."""
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

