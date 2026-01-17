import pygame
from resource_path import resource_path


class Player:
    def __init__(self, screen_width, screen_height, use_png=True):
        self.screen_width   = screen_width
        self.screen_height  = screen_height
        self.pos           = pygame.Vector2(0, 0)
        self.radius        = 20
        self.pickup_radius = self.radius + 5
        self.max_health    = 100
        self.health        = 100
        self.base_speed    = 100
        self.speed         = 100

        # projectile stuff
        self.damage        = 20
        self.damage_mult   = 1.0
        self.attack_speed  = 0.2
        self.attack_timer  = 0.0
        self.proj_spd      = 250
        self.proj_life     = 2
        self.proj_radius   = 5
        
        #movement
        self.blink_timer    = 0  #s
        self.blink_regen    = 1  #s
        self.blink_count    = 1
        
        self.stamina        = 100
        self.stamina_max    = 100
        self.stamina_regen  = 25
        self.stamina_drain  = 50
        self.sprinting      = False
        self.sprint_mult    = 1.5
        
        self.drawImage      = False
        if not use_png:
            self.drawImage      = True
            try:
                self.image      = pygame.image.load(resource_path("assets/player.png")).convert_alpha()
                self.image      = pygame.transform.smoothscale(self.image, (self.radius*2, self.radius*2))
            except:
                self.drawImage  = False
            
        

    def take_damage(self, dmg):
        self.health -= dmg
        return self.health > 0
        
    def TickTimers(self, dt):
        if self.blink_timer > 0:
            self.blink_timer -= dt
            if self.blink_timer < 0:
                self.blink_timer = 0
        
        if self.attack_timer > 0:
            self.attack_timer -= dt
            
        if self.sprinting:
            self.stamina -= dt * self.stamina_drain
            
            if self.stamina <= 0:
                self.stamina = 0
                self.toggle_sprinting()
        
        if not self.sprinting and self.stamina < self.stamina_max:
            self.stamina += dt * self.stamina_regen
            if self.stamina > self.stamina_max:
                self.stamina = self.stamina_max
        
        
    def UpdateScreenSize(self, screen_width, screen_height):
        self.screen_width  = screen_width
        self.screen_height = screen_height

    def move(self, dt, keys):                                   
        if keys[pygame.K_w]:
            self.pos.y -= self.speed * dt
        if keys[pygame.K_s]:
            self.pos.y += self.speed * dt
        if keys[pygame.K_a]:
            self.pos.x -= self.speed * dt
        if keys[pygame.K_d]:
            self.pos.x += self.speed * dt

    def draw(self, screen, drawHealth=False, drawPlayer=False, drawBlinkCooldown=False, drawStamina=False):
        if drawPlayer:
            if not self.drawImage:
                pygame.draw.circle(
                    screen, "purple",
                    (self.screen_width // 2,
                    self.screen_height // 2),
                    self.radius
                )
            
            if self.drawImage:
                screen.blit(self.image, (self.screen_width // 2 - self.radius, self.screen_height // 2 - self.radius))
                
        if drawHealth:
            pygame.draw.rect(
                screen, "white",
                rect=(pygame.Rect(self.screen_width // 2 - self.max_health // 2,
                    self.screen_height // 2 - self.radius - 20,
                    self.max_health,
                    self.radius / 2)
                ),
            )
            
            pygame.draw.rect(
                screen, "red",
                rect=(pygame.Rect(self.screen_width // 2 - self.max_health // 2,
                    self.screen_height // 2 - self.radius - 20,
                    self.health,
                    self.radius / 2)
                ),
            )
            
        if drawStamina:
            # background
            pygame.draw.rect(
                screen, "white",
                rect=pygame.Rect(
                    self.screen_width // 2 - 25,               
                    self.screen_height // 2 + self.radius + 5,
                    50,                                        
                    10                                         
                )
            )

            # filled bar
            pygame.draw.rect(
                screen, "blue",
                rect=pygame.Rect(
                    self.screen_width // 2 - 25,
                    self.screen_height // 2 + self.radius + 5,
                    int(50 * (self.stamina / self.stamina_max if self.stamina_max else 0)),
                    10
                )
            )
            
        if self.blink_timer > 0 and drawBlinkCooldown:
            y = 50 * (self.blink_timer / self.blink_regen) if self.blink_regen else 0
            pygame.draw.rect(
                screen, "gray",
                rect=(pygame.Rect(  
                    10, 
                    self.screen_height - 10 - y, 
                    50,
                    y)
                ),
            )
        
    
    def toggle_sprinting(self):
        if self.sprinting:
            # always allow stopping
            self.sprinting = False
            self.speed = self.base_speed
        else:
            # only start sprint if enough stamina
            if self.stamina > 0:
                self.sprinting = True
                self.speed = self.base_speed * self.sprint_mult
                
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
            "STAMINA":      self.stamina,
            "MAX_STAMINA":  self.stamina_max,
            "SPRINTING":    self.sprinting,
            "BLINK_TIMER": self.blink_timer,
            "BLINK_REGEN": self.blink_regen,
            "BLINK_COUNT": self.blink_count,
            "ATTACK_TIMER": self.attack_timer,
            "ATTACK_SPEED": self.attack_speed,
            "DAMAGE":      self.damage,
            "SPRINT_MULT": self.sprint_mult,
            "STAMINA_DRAIN": self.stamina_drain,
            "STAMINA_REGEN": self.stamina_regen,
        }
        

