import pygame

def Blink(entity, keys):
    if entity.blink_timer <= 0:
        entity.blink_timer = entity.blink_regen 
        entity.move(1, keys)  