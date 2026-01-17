from enum import Enum

class ItemType(Enum):
    HEALTH        = ("Restores 20 HP", "green", 1)
    MAX_HEALTH    = ("Increase max HP by 10", "darkgreen", 5)
    SPEED         = ("Increase speed by 3%", "cyan", 2)
    DAMAGE_MULT   = ("Increase damage multiplier by 3%", "crimson", 4)
    BASE_DAMAGE   = ("Increase base damage by 2", "violetred", 3)
    RADIUS        = ("Increase radius by 2", "orange", 2)
    PROJ_SPD      = ("Increases projectile speed by 3%", "darkcyan", 3)
    PROJ_RADIUS   = ("Increases projectile radius by 1", "darkorange", 2)
    PROJ_LIFE     = ("Increases projectile life by 3%", "darkred", 2)
    PICKUP_RADIUS = ("Increases pickup radius by 3", "brown", 1)

    def __init__(self, description, color, worth):
        self.description = description
        self.color = color
        self.worth = worth