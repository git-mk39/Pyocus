import pygame

from Lib import settings
from Lib import snake


ENEMY_NUMBER = settings.ENEMY_INIT_NUMBER
ENEMIES = []


# left, top, width, height
PF_00 = pygame.Rect(150, 490, 70, 55)
PF_01 = pygame.Rect(290, 430, 130, 30)
PF_02 = pygame.Rect(450, 430, 30, 30)
PF_03 = pygame.Rect(550, 430, 30, 30)
PF_04 = pygame.Rect(630, 350, 50, 50)
PF_05 = pygame.Rect(700, 520, 150, 50)
PF_06 = pygame.Rect(810, 410, 100, 30)
PF_07 = pygame.Rect(920, 330, 50, 20)
PF_08 = pygame.Rect(820, 270, 50, 20)
PF_09 = pygame.Rect(720, 210, 50, 20)
PF_10 = pygame.Rect(480, 210, 150, 30)
PLATFORM = [PF_00,
            PF_01,
            PF_02,
            PF_03,
            PF_04,
            PF_05,
            PF_06,
            PF_07,
            PF_08,
            PF_09,
            PF_10]


def init_enemy(no_spawn_area):
  for i in range(ENEMY_NUMBER):
    ENEMIES.append(snake.Snake(no_spawn_area))
  pygame.display.update()


def draw_platform():
  for pf in PLATFORM:
    pygame.draw.rect(settings.SCREEN, settings.DARK_BLUE, pf)
    pygame.draw.rect(settings.SCREEN, settings.BLACK, pf, settings.BORDER_THICKNESS * 2)


def draw_enemy():
  for enemy in ENEMIES:
    enemy.draw()