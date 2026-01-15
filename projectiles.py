import pygame

class Projectile:
    def __init__(self, pos, direction, entity):
        self.pos       = pos
        self.direction = direction
        self.speed     = entity.proj_spd
        self.radius    = entity.proj_radius
        self.life      = entity.proj_life
        self.damage    = entity.damage * entity.damage_mult
        self.owner     = entity

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.life -= dt

    def hits(self, enemy):
        return self.pos.distance_to(enemy.pos) < self.radius + enemy.radius

    def draw(self, screen, camera):
        screen_pos = self.pos - camera
        pygame.draw.circle(
            screen,
            "white",
            (int(screen_pos.x), int(screen_pos.y)),
            self.radius
        )
