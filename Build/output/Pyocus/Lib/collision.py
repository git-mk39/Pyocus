import pygame

from Lib import settings


def handle_bullet_collision_wall(bullets):
  for bl in bullets[:]:
    if not pygame.Rect(0, 0, settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT).collidepoint(bl.pos):
      bullets.remove(bl)


def handle_bullet_collision_platform(bullets, PLATFORM):
  for pf in PLATFORM:
    for bl in bullets[:]:
      if pf.collidepoint(bl.pos):
        settings.BULLET_HIT_SOUND.play()
        bullets.remove(bl)


def handle_bullet_collision_enemy(bullets, ENEMIES):
  for enemy in ENEMIES:
    for bl in bullets[:]:
      if enemy.handle_bullet_collision(bl):
        settings.BULLET_HIT_ENEMY.play()
        settings.SCORE_INGAME += settings.SCORE_STEP
        settings.ENEMY_HIT += 1
        if bl.type == 'normal':
          bullets.remove(bl)


def handle_player_collision_enemy(player, ENEMIES):
  for enemy in ENEMIES:
    if enemy.contact_player(player):
      return True