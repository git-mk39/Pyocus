import os
import pygame

from Lib import settings

def handle_scaling(display_mode, ingame_player, PLATFORM, ENEMIES):
  if display_mode & pygame.FULLSCREEN:
    settings.SCREEN = pygame.display.set_mode(settings.WINDOW_SIZE)
    settings.DISPLAY_WIDTH = settings.WINDOW_WIDTH
    settings.DISPLAY_HEIGHT = settings.WINDOW_HEIGHT
    settings.BACKGROUND_INGAME = settings.BACKGROUND

    ingame_player.handle_scaling(display_mode)

    settings.BORDER_INGAME_THICKNESS = settings.BORDER_THICKNESS
    for pf in PLATFORM:
      pf.x //= 2
      pf.y //= 2
      pf.width //= 2
      pf.height //= 2

    for enemy in ENEMIES:
      enemy.handle_scaling(display_mode)

    settings.BULLET_INGAME_WIDTH = settings.BULLET_WIDTH
    settings.BULLET_INGAME_HEIGHT = settings.BULLET_HEIGHT
    settings.BULLET_INGAME_VEL = settings.BULLET_VEL
    settings.SHOTGUN_BULLET_SPREAD_INGAME = settings.SHOTGUN_BULLET_SPREAD
    settings.SNIPER_BULLET_VEL_INGAME = settings.SNIPER_BULLET_VEL

    settings.FONT_SIZE_INGAME = settings.FONT_SIZE
    settings.END_SCREEN_FONT_SIZE_INGAME = settings.END_SCREEN_FONT_SIZE
    settings.PAUSE_SCREEN_FONT_SIZE_INGAME = settings.PAUSE_SCREEN_FONT_SIZE



  else:
    settings.SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    settings.DISPLAY_WIDTH = settings.FULLSCREEN_WIDTH
    settings.DISPLAY_HEIGHT = settings.FULLSCREEN_HEIGHT
    settings.BACKGROUND_INGAME = pygame.image.load(os.path.join('Assets', 'background.jpg'))
    
    ingame_player.handle_scaling(display_mode)

    settings.BORDER_INGAME_THICKNESS = settings.BORDER_THICKNESS * 2
    for pf in PLATFORM:
      pf.x *= 2
      pf.y *= 2
      pf.width *= 2
      pf.height *= 2

    for enemy in ENEMIES:
      enemy.handle_scaling(display_mode)

    settings.BULLET_INGAME_WIDTH = settings.BULLET_WIDTH * 2
    settings.BULLET_INGAME_HEIGHT = settings.BULLET_HEIGHT * 2
    settings.BULLET_INGAME_VEL = settings.BULLET_VEL * 2
    settings.SHOTGUN_BULLET_SPREAD_INGAME = settings.SHOTGUN_BULLET_SPREAD * 2
    settings.SNIPER_BULLET_VEL_INGAME = settings.SNIPER_BULLET_VEL * 2

    settings.FONT_SIZE_INGAME = settings.FONT_SIZE * 2
    settings.END_SCREEN_FONT_SIZE_INGAME = settings.END_SCREEN_FONT_SIZE * 2
    settings.PAUSE_SCREEN_FONT_SIZE_INGAME = settings.PAUSE_SCREEN_FONT_SIZE * 2

  settings.INGAME_FONT = pygame.font.Font(os.path.join('Assets', 'gomarice-no-continue-font.ttf'), settings.FONT_SIZE_INGAME)
  settings.END_SCREEN_FONT = pygame.font.Font(os.path.join('Assets', 'gomarice-no-continue-font.ttf'), settings.END_SCREEN_FONT_SIZE_INGAME)
  settings.PAUSE_SCREEN_FONT = pygame.font.Font(os.path.join('Assets', 'gomarice-no-continue-font.ttf'), settings.PAUSE_SCREEN_FONT_SIZE_INGAME)