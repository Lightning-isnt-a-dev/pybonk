import pygame
import random
from settings import PLAYER_PNG_PATH, TOGGLE_SPRINT, WIDTH, HEIGHT, FPS, AUTOFIRE, FULLSCREEN, SPRINT, BLINK, SHOOT, USE_PLAYER_PNG
from player import Player
from enemies import Enemy
from projectiles import Projectile
from enum import Enum
from blink import Blink
from ui import *

class GameStateType(Enum):
    MAIN_MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3

# --- Pygame setup ---
flags = pygame.FULLSCREEN if FULLSCREEN else pygame.RESIZABLE
if FULLSCREEN:
    pygame.display.init()
    screen_width, screen_height = pygame.display.get_desktop_sizes()[0]
    screen = pygame.display.set_mode((screen_width, screen_height), flags)
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)

screen_width, screen_height = screen.get_size()
clock = pygame.time.Clock()
pygame.display.set_caption("pybonk")
pygame.font.init()

# --- Game objects ---
player = Player(screen_width, screen_height, USE_PLAYER_PNG, PLAYER_PNG_PATH)
enemies = []
items = []
projectiles = []

enemy_spawn_timer = 0.0
enemy_spawn_rate = 1.0 
enemy_spawn_chance = 0.2
enemy_spawn_increase = 0.001

running = True
GameState = GameStateType.MAIN_MENU
selected_index = 0  # For main menu

# --- Main game loop ---
while running:
    dt = clock.tick(FPS) / 1000
    keys = pygame.key.get_pressed()

    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE and not FULLSCREEN:
            screen_width, screen_height = event.w, event.h
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            player.UpdateScreenSize(screen_width, screen_height)

        elif event.type == pygame.KEYDOWN:
            # --- MAIN MENU ---
            if GameState == GameStateType.MAIN_MENU:
                if event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(MAIN_MENU_OPTIONS)
                elif event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(MAIN_MENU_OPTIONS)
                elif event.key == pygame.K_RETURN:
                    if selected_index == 0:  # Start Game
                        GameState = GameStateType.PLAYING
                    elif selected_index == 1:  # Settings (not implemented)
                        print("Open Settings menu (not implemented)")
                    elif selected_index == 2:  # Quit
                        running = False

            # --- In-game keys ---
            if GameState == GameStateType.PLAYING:
                if event.key == BLINK:
                    Blink(player, keys)
                if event.key == SPRINT:
                    player.toggle_sprinting()
                if event.key == pygame.K_F11:
                    FULLSCREEN = not FULLSCREEN
                    flags = pygame.FULLSCREEN if FULLSCREEN else pygame.RESIZABLE
                    screen = pygame.display.set_mode((0, 0) if FULLSCREEN else (WIDTH, HEIGHT), flags)
                    screen_width, screen_height = screen.get_size()
                    player.UpdateScreenSize(screen_width, screen_height)
                elif event.key == pygame.K_ESCAPE:
                    GameState = GameStateType.PAUSED

            # --- Pause / Game over keys ---
            elif GameState == GameStateType.PAUSED:
                if event.key == pygame.K_ESCAPE:
                    GameState = GameStateType.PLAYING
            elif GameState == GameStateType.GAME_OVER:
                if event.key == pygame.K_r:
                    # reset game
                    player = Player(screen_width, screen_height, USE_PLAYER_PNG, PLAYER_PNG_PATH)
                    enemies.clear()
                    items.clear()
                    projectiles.clear()
                    enemy_spawn_timer = 0.0
                    enemy_spawn_rate = 1.0
                    enemy_spawn_chance = 0.2
                    GameState = GameStateType.PLAYING
                elif event.key == pygame.K_ESCAPE:
                    GameState = GameStateType.MAIN_MENU

        elif event.type == pygame.KEYUP:
            if event.key == SPRINT and not TOGGLE_SPRINT:
                if player.sprinting:
                    player.toggle_sprinting()

    # --- Game logic ---
    if GameState == GameStateType.PLAYING:
        # --- Player stuff ---
        player.TickTimers(dt)
        player.move(dt, keys)

        camera = player.pos - pygame.Vector2(screen_width // 2, screen_height // 2)
        
        # --- Mouse direction ---
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) + camera
        direction = mouse_pos - player.pos

        # --- Enemy spawning ---
        if enemy_spawn_timer <= 0:
            enemy_spawn_timer = enemy_spawn_rate
            for _ in range(random.randint(1, 5)):
                if random.random() < enemy_spawn_chance:
                    enemies.append(Enemy(player, screen_width, screen_height))
            enemy_spawn_chance = min(enemy_spawn_chance + enemy_spawn_increase, 0.8)
            enemy_spawn_rate = max(0.2, enemy_spawn_rate - 0.0005)
        else:
            enemy_spawn_timer -= dt

        # --- Shooting ---
        if player.attack_timer <= 0 and (AUTOFIRE or keys[SHOOT]):
            player.attack_timer = player.attack_speed
            if direction.length() != 0:
                direction = direction.normalize()
            spawn_pos = player.pos + direction * (player.radius + player.proj_radius + 2)
            projectiles.append(Projectile(spawn_pos, direction, player)) 

        # --- Enemy logic ---
        for enemy in enemies[:]:
            enemy.move(dt, player)
            if enemy.collides(dt, player):
                if not player.take_damage(enemy.damage):
                    GameState = GameStateType.GAME_OVER

        # --- Projectiles ---
        for projectile in projectiles[:]:
            projectile.update(dt)
            if projectile.life <= 0:
                projectiles.remove(projectile)
                continue
            for enemy in enemies[:]:
                if projectile.hits(enemy):
                    if enemy.try_dodge(projectile, dt):
                        continue  # projectile missed due to dodge
                    projectiles.remove(projectile)
                    if enemy.take_damage(projectile.damage):
                        items.extend(enemy.die())
                        enemies.remove(enemy)
                    break

        # --- Item collisions ---
        for item in items[:]:
            if player.pos.distance_to(item.pos) < player.pickup_radius + item.radius:
                item.apply(player)
                items.remove(item)

    # --- Drawing ---
    screen.fill("black")

    if GameState == GameStateType.PLAYING or GameState == GameStateType.PAUSED:
        player.draw(screen, drawPlayer=True)
        for item in items:
            item.draw(screen, camera, mouse_pos)
        for enemy in enemies:
            enemy.draw(screen, camera)
        for projectile in projectiles:
            projectile.draw(screen, camera)
        player.draw(screen, drawHealth=True, drawBlinkCooldown=True, drawStamina=True)

        # Draw pause overlay if paused
        if GameState == GameStateType.PAUSED:
            draw_overlay(screen, screen_width, screen_height, "PAUSED", "Press ESC to resume")

    elif GameState == GameStateType.GAME_OVER:
        draw_overlay(screen, screen_width, screen_height, "GAME OVER", "Press R to restart or ESC to return to main menu", color="red")

    elif GameState == GameStateType.MAIN_MENU:
        draw_main_menu(screen, screen_width, screen_height, selected_index, pygame.mouse.get_pos())

    pygame.display.flip()

pygame.quit()
