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
        self.dodge_cooldown     = 0
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
        dist = direction.length()
        if dist > self.radius + entity.radius and dist != 0:
            self.pos += direction / dist * self.speed * dt

            
    def take_damage(self, dmg):
        self.health -= dmg
        return self.health <= 0
    
    def collides(self, dt, entity):
        if self.collision_cooldown > 0:
            self.collision_cooldown = max(0, self.collision_cooldown - dt)
            return False
        
        if (self.pos - entity.pos).length_squared() < (self.radius + entity.radius) ** 2:
            self.collision_cooldown = 0.5
            return True

        return False
    
    def die(self):
        drops = []

        if random.random() < self.drop_chance:  # chance to even drop
            # weight items by enemy strength and item value
            item_types = list(ItemType)
            weights = [max(1, item.worth * self.type.health / 100) for item in item_types]
            item = random.choices(item_types, weights=weights, k=1)[0]

            drops.append(Item(self.pos, item))

        return drops
    
def try_dodge(self, projectile, dt):
    if self.dodge_cooldown > 0:
        self.dodge_cooldown = max(0, self.dodge_cooldown - dt)
        return False
    
    # Smaller and faster enemies dodge more easily
    speed_factor = self.speed / 200 # the faster the enemy, the easier to dodge
    size_factor = max(0, (25 - self.radius) / 25)  # the smaller the enemy, the easier to dodge
    dodge_chance = min(0.6, speed_factor * 0.5 + size_factor * 0.3)  # cap at 60%

    if random.random() < dodge_chance:
        direction = projectile.pos - self.pos
        if direction.length() != 0:
            # randomly choose left or right dodge
            perp = pygame.Vector2(-direction.y, direction.x) if random.random() < 0.5 else pygame.Vector2(direction.y, -direction.x)
            perp = perp.normalize()

            # dodge distance scaled by enemy size
            size_multiplier = max(0.5, 25 / self.radius)  # smaller enemies dodge further
            self.pos += perp * self.speed * projectile.radius * 0.1 * size_multiplier # dodge distance
 
            # cooldown to avoid spamming dodge
            self.dodge_cooldown = 0.3

        return True

    return False