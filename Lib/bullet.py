import pygame
import math as m
import random as rd

from Lib import settings


class Bullet:
  def __init__(self, ingame_player_pos, ingame_cursor_pos):
    self.type = 'normal'
    self.pos = (ingame_player_pos[0], ingame_player_pos[1])
    mx, my = ingame_cursor_pos
    self.dir = (mx - self.pos[0], my - self.pos[1])
    length = m.hypot(*self.dir)
    if length == 0.0:
      self.dir = (0, -1)
    else:
      self.dir = (self.dir[0] / length, self.dir[1] / length)
    angle = m.degrees(m.atan2(-self.dir[1], self.dir[0]))
    self.bullet = pygame.Surface((settings.BULLET_INGAME_WIDTH, settings.BULLET_INGAME_HEIGHT)).convert_alpha()
    self.bullet.fill(settings.WHITE)
    self.bullet = pygame.transform.rotate(self.bullet, angle)
    self.speed = settings.BULLET_INGAME_VEL

  def update(self):
    self.pos = (self.pos[0] + self.dir[0] * self.speed,
                self.pos[1] + self.dir[1] * self.speed)

  def draw(self, surf):
    bullet_rect = self.bullet.get_rect(center = self.pos)
    surf.blit(self.bullet, bullet_rect)


class SniperBullet(Bullet):
  def __init__(self, ingame_player_pos, ingame_cursor_pos):
    Bullet.__init__(self, ingame_player_pos, ingame_cursor_pos)
    self.type = 'sniper'
    angle = m.degrees(m.atan2(-self.dir[1], self.dir[0]))
    self.bullet = pygame.Surface((settings.BULLET_INGAME_WIDTH * 3, settings.BULLET_INGAME_HEIGHT * 2)).convert_alpha()
    self.bullet.fill(settings.WHITE)
    self.bullet = pygame.transform.rotate(self.bullet, angle)
    self.speed = settings.SNIPER_BULLET_VEL_INGAME


def shotgun_fires(bullets, ingame_player_pos, ingame_cursor_pos):
  mx, my = ingame_cursor_pos
  shotgun_bullet_number = settings.SHOTGUN_BULLET_NUMBER
  while shotgun_bullet_number > 0:
    bullet_dest_x = rd.randrange(mx - settings.SHOTGUN_BULLET_SPREAD, mx + settings.SHOTGUN_BULLET_SPREAD)
    bullet_dest_y = rd.randrange(my - settings.SHOTGUN_BULLET_SPREAD, my + settings.SHOTGUN_BULLET_SPREAD)
    bullets.append(Bullet(ingame_player_pos, (bullet_dest_x, bullet_dest_y)))
    shotgun_bullet_number -= 1