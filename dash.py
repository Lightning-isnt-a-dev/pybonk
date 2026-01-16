import pygame

def Dash(entity):
    if entity.dash_cooldown <= 0:
        entity.dash_cooldown = 3
        entity.dash_timer = 0.5
        entity.speed *= 5
        return