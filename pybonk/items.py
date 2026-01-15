import pygame
import random
from item_types import ItemType

class Item:
    def __init__(self, pos, item_type):
        self.type = random.choice(list(ItemType)) if not item_type else item_type
        self.pos = pos
        self.radius = 20

    def apply(self, player=None):
        if player:
            PlayerEffects = {
                ItemType.HEALTH: lambda player: setattr(
                    player, "health", min(player.max_health, player.health + 20)
                ),

                ItemType.MAX_HEALTH: lambda player: (
                    setattr(player, "max_health", player.max_health + 10),
                    setattr(player, "health", player.health + 10),
                ),

                ItemType.SPEED: lambda player: setattr(
                    player, "speed", round(player.speed * 1.03)
                ),

                ItemType.DAMAGE_MULT: lambda player: setattr(
                    player, "damage_mult", player.damage_mult + 0.03
                ),

                ItemType.BASE_DAMAGE: lambda player: setattr(
                    player, "damage", player.damage + 2
                ),

                ItemType.RADIUS: lambda player: (
                    setattr(player, "radius", player.radius + 2),
                    setattr(player, "pickup_radius", player.pickup_radius + 2),
                ),

                ItemType.PROJ_SPD: lambda player: setattr(
                    player, "proj_spd", round(player.proj_spd * 1.03)
                ),

                ItemType.PROJ_RADIUS: lambda player: setattr(
                    player, "proj_radius", player.proj_radius + 1
                ),

                ItemType.PROJ_LIFE: lambda player: setattr(
                    player, "proj_life", round(player.proj_life * 1.03)
                ),

                ItemType.PICKUP_RADIUS: lambda player: setattr(
                    player, "pickup_radius", player.pickup_radius + 3
                ),
            }

            PlayerEffects[self.type](player)
            

    def draw(self, screen, camera):
        screen_pos = self.pos - camera
        pygame.draw.circle(
            screen, self.type.color,
            (int(screen_pos.x), int(screen_pos.y)),
            self.radius
        )
