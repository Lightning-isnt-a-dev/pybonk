from enum import Enum
from item_types import ItemType

class EnemyType(Enum):
    #enemy_type = (description, color, radius, health, damage, speed, spawn_chance, drop_chance)
    BASIC            = ("BASIC"      , "red"     , 15, 50,  5 , 100, 60, 0.2)
    
    SPEEDSTER       = ("SPEEDSTER"  , "darkblue", 20, 100, 10, 125, 30, 0.35)
    
    BRUTE           = ("BRUTE"      , "yellow"  , 25, 200, 20, 75, 10, 0.5)
    
    SWARMER         = ("SWARMER"    , "orange"  , 10, 30,  3 , 150, 80, 0.1)
    
    TANK            = ("TANK"       , "darkred" , 30, 300, 15, 50, 5, 0.8)

    def __init__(self, description, color, radius, health, damage, speed, spawn_chance, drop_chance):
        self.label            = description
        self.color            = color
        self.radius           = radius
        self.health           = health
        self.damage           = damage
        self.speed            = speed
        self.spawn_chance     = spawn_chance
        self.drop_chance      = drop_chance
