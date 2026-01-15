from enum import Enum

class ItemType(Enum):
    HEALTH        = ("Restores 20 HP", "green", 1)
    MAX_HEALTH    = ("Increase max HP", "darkgreen", 5)
    SPEED         = ("Increase speed", "cyan", 2)
    DAMAGE_MULT   = ("Increase damage", "crimson", 4)
    BASE_DAMAGE   = ("Increase base damage", "violetred", 3)
    RADIUS        = ("Increase size", "orange", 2)
    PROJ_SPD      = ("Projectile speed", "darkcyan", 3)
    PROJ_RADIUS   = ("Projectile size", "darkorange", 2)
    PROJ_LIFE     = ("Projectile life", "darkred", 2)
    PICKUP_RADIUS = ("Pickup radius", "brown", 1)

    def __init__(self, description, color, worth):
        self.description = description
        self.color = color
        self.worth = worth