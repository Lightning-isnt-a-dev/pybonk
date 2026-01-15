import pygame
import random
from settings import WIDTH, HEIGHT, FPS, AUTOFIRE, FULLSCREEN
from player import Player
from enemies import Enemy
from projectiles import Projectile



flags = pygame.FULLSCREEN if FULLSCREEN else pygame.RESIZABLE
if FULLSCREEN:
    pygame.display.init()
    WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
    
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)

screen_width, screen_height = screen.get_size()
clock = pygame.time.Clock()
pygame.display.set_caption("pybonk")

player      = Player(screen_width, screen_height)
enemies     = []
items       = []
projectiles = []

shoot_cooldown          = 0.2
shoot_timer             = 0
enemy_spawn_cooldown    = 1.0
enemy_spawn_chance      = 0.2
running = True

while running:
    dt = clock.tick(FPS) / 1000
    enemy_spawn_cooldown -= dt
    shoot_timer -= dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            player.UpdateScreenSize(WIDTH, HEIGHT)
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                player.dash()
                
            if event.key == pygame.K_F11:
                FULLSCREEN = not FULLSCREEN
                flags = pygame.FULLSCREEN if FULLSCREEN else pygame.RESIZABLE
                if FULLSCREEN:
                    pygame.display.set_mode((0, 0), flags)
                    WIDTH, HEIGHT = pygame.display.get_desktop_sizes()[0]
                else:
                    pygame.display.set_mode((WIDTH, HEIGHT), flags)
                player.UpdateScreenSize(WIDTH, HEIGHT)
                
            if event.key == pygame.K_ESCAPE:
                running = False
                continue
            
    keys = pygame.key.get_pressed()
        
    player.update(dt, keys)

    camera = player.pos - pygame.Vector2(WIDTH // 2, HEIGHT // 2)
    
    if enemy_spawn_cooldown <= 0:
        enemy_spawn_cooldown = 1.0
        enemy_spawn_chance += 0.001
        for _ in range(random.randint(1, 10)):
            enemies.append(Enemy(player, screen_height, screen_width)) if random.random() < enemy_spawn_chance else None

    # shooting
    if shoot_timer <= 0 and (AUTOFIRE or keys[pygame.K_SPACE]):
        shoot_timer = shoot_cooldown
        mouse       = pygame.Vector2(pygame.mouse.get_pos()) + camera
        direction   = mouse - player.pos
        
        if direction.length() != 0:
            direction = direction.normalize()

        spawn_pos = player.pos + direction * (player.radius + player.proj_radius + 2)
        projectiles.append(Projectile(spawn_pos, direction, player)) 
        
    #enemy logic
    for enemy in enemies[:]:
        # move enemy
        enemy.move(dt, player)

        # enemy-player collisione
        if enemy.collides(dt, player):
            running = player.take_damage(enemy.damage)  
            
        
    for projectile in projectiles[:]:
        projectile.update(dt)
        
        if projectile.life <= 0:
            projectiles.remove(projectile)
            continue
            
        for enemy in enemies[:]:
            if projectile.hits(enemy):
                projectiles.remove(projectile)

                #method returns true if enemy dies
                if enemy.take_damage(projectile.damage):
                    items.extend(enemy.die())
                    enemies.remove(enemy)
                break

    # item collisions
    for item in items[:]:
        if player.pos.distance_to(item.pos) < player.pickup_radius + item.radius:
            item.apply(player)
            items.remove(item)

    #draw
    screen.fill("black")
    player.draw(screen, drawPlayer=True)

    for obj in items:
        obj.draw(screen, camera)

    for enemy in enemies:
        enemy.draw(screen, camera)

    for projectile in projectiles:
        projectile.draw(screen, camera)
        
    player.draw(screen, drawHealth=True, drawDashCooldown=True)

    pygame.display.flip()

pygame.quit()
