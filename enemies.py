import pygame
import random
from enemy_types import EnemyType
from item_types import ItemType
from items import Item

class Enemy:
    def __init__(self, entity, screen_width, screen_height):
        # Pick enemy type with weighting
        types = list(EnemyType)
        weights = [t.spawn_chance for t in types]
        self.type = random.choices(types, weights=weights, k=1)[0]

        # spawn relative to entity
        angle = random.uniform(0, 360)
        screen_radius = pygame.Vector2(screen_width//2, screen_height//2).length()
        distance = screen_radius + self.type.radius
        offset = pygame.Vector2(distance, 0).rotate(angle)
        self.pos = entity.pos + offset

        # stats from enemy type
        self.radius             = self.type.radius
        self.pickup_radius      = self.radius + 5
        self.damage             = self.type.damage
        self.health             = self.type.health
        self.speed              = self.type.speed
        self.drop_chance        = self.type.drop_chance
        self.collision_cooldown = 0

    def draw(self, screen, camera):
        screen_pos = self.pos - camera
        pygame.draw.circle(
            screen, self.type.color,
            (int(screen_pos.x), int(screen_pos.y)),
            self.radius
        )
    
    def move(self, dt, entity):
        direction = entity.pos - self.pos
        if direction.length() > self.radius + entity.radius:
            self.pos += direction.normalize() * self.speed * dt
            
    def take_damage(self, dmg):
        self.health -= dmg
        return self.health <= 0
    
    def collides(self, dt, entity):
        if self.collision_cooldown > 0:
            self.collision_cooldown -= dt
            return False
        
        if self.pos.distance_to(entity.pos) < self.radius + entity.radius:
            self.collision_cooldown = 0.5
            return True

        return False
    
    def die(self):
        drops = []

        if random.random() < self.drop_chance:  # chance to even drop
            # weight items by enemy strength and item value
            item_types = list(ItemType)
            weights = [item.worth * self.type.health/100 for item in item_types]
            item = random.choices(item_types, weights=weights, k=1)[0]

            drops.append(Item(self.pos, item))

        return drops