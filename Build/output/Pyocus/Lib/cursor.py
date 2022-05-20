import pygame
import os

from Lib import settings



class Cursor:
  def __init__(self):
    self.x, self.y = pygame.mouse.get_pos()
    self.image = pygame.image.load(os.path.join('Assets', 'cursor-sprite-inactive.png'))


  def get_pos(self, x, y):
    self.x, self.y = x, y


  def sniper_ready_sprite(self):
    self.image = pygame.image.load(os.path.join('Assets', 'cursor-sprite-sniper-ready.png'))


  def active_sprite(self):
    self.image = pygame.image.load(os.path.join('Assets', 'cursor-sprite-active.png'))


  def inactive_sprite(self):
    self.image = pygame.image.load(os.path.join('Assets', 'cursor-sprite-inactive.png'))


  def draw_sprite(self):
    settings.SCREEN.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2))
    self.pos = (self.x, self.y)