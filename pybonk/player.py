import pygame

class Player:
    def __init__(self, screen_width, screen_height):
        self.screen_width   = screen_width
        self.screen_height  = screen_height
        self.pos           = pygame.Vector2(0, 0)
        self.radius        = 20
        self.pickup_radius = self.radius + 5
        self.max_health    = 100
        self.health        = 100
        self.speed         = 100
        self.damage        = 10
        self.damage_mult   = 1.0
        self.proj_spd      = 250
        self.proj_life     = 2
        self.proj_radius   = 5
        self.dash_cooldown = 100
        self.dash_distance = 100
        
        
    def take_damage(self, dmg):
        self.health -= dmg
        return self.health > 0

    def stats(self):
        return {
            "HEALTH":        self.health,
            "MAX_HEALTH":    self.max_health,
            "SPEED":         self.speed,
            "DAMAGE_MULT":   self.damage_mult,
            "BASE_DAMAGE":   self.damage,
            "RADIUS":        self.radius,
            "PICKUP_RADIUS": self.pickup_radius,
            "PROJ_SPD":      self.proj_spd,
            "PROJ_RADIUS":   self.proj_radius,
            "PROJ_LIFE":     self.proj_life,
        }
        
    def UpdateScreenSize(self, screen_width, screen_height):
        self.screen_width  = screen_width
        self.screen_height = screen_height

    def update(self, dt, keys):
        if keys[pygame.K_w]:
            self.pos.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.pos.y += self.speed * dt
        if keys[pygame.K_a]:
            self.pos.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.pos.x += self.speed * dt

    def draw(self, screen, drawHealth=False, drawPlayer=False, drawDashCooldown=False):
        if drawPlayer:
            pygame.draw.circle(
                screen, "purple",
                (self.screen_width // 2, self.screen_height // 2),
                self.radius
            )
            
        if drawHealth:
            pygame.draw.rect(
                screen, "white",
                rect=(pygame.Rect(self.screen_width // 2 - self.max_health // 2, self.screen_height // 2 - self.radius - 20, self.max_health, self.radius / 2)),
            )
            
            pygame.draw.rect(
                screen, "red",
                rect=(pygame.Rect(self.screen_width // 2 - self.max_health // 2, self.screen_height // 2 - self.radius - 20, self.health, self.radius / 2)),
            )
        
        if self.dash_cooldown > 0 and drawDashCooldown:
            pygame.draw.rect(
                screen, "white",
                rect=(pygame.Rect(self.screen_width // 2 - self.dash_cooldown // 4, self.screen_height // 2 + self.radius + 10, self.dash_cooldown // 2, self.radius // 3)),
            )
        
    def dash(self):
        
        pass

