import pygame

from Lib import settings

def handle_bullet_movement(bullets):
  for bl in bullets:
    bl.update()


def handle_enemy_movement(enemies, platforms):
  for enemy in enemies:
    enemy.move(platforms)