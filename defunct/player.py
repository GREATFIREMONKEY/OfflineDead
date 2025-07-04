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

    def set_position(self, x, y):
        self.x = x
        self.y = y
