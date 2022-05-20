import pygame
import random as rd

from Lib import settings
from Data import level_0



class Snake:
  def __init__(self, no_spawn_area):
    self.body_block_width = settings.SNAKE_INGAME_BODY_BLOCK_WIDTH
    self.body_block_height = settings.SNAKE_INGAME_BODY_BLOCK_HEIGHT
    spawn_x = rd.randrange(1, (settings.DISPLAY_WIDTH // 10)) * 10
    spawn_y = rd.randrange(1, (settings.DISPLAY_HEIGHT // 10)) * 10
    spawn_rect = pygame.Rect(spawn_x, spawn_y, self.body_block_width, self.body_block_height)
    while spawn_rect.colliderect(no_spawn_area):
      spawn_x = rd.randrange(1, (settings.DISPLAY_WIDTH // 10)) * 10
      spawn_y = rd.randrange(1, (settings.DISPLAY_HEIGHT // 10)) * 10
      spawn_rect = pygame.Rect(spawn_x, spawn_y, self.body_block_width, self.body_block_height)
    self.position_x = spawn_x
    self.position_y = spawn_y
    self.position = [self.position_x, self.position_y]
    self.body = []
    self.body_hitbox = []
    if settings.SNAKE_INTRO_BODY_LENGTH > 0:
      self.body_length = settings.SNAKE_INTRO_BODY_LENGTH
      settings.SNAKE_INTRO_BODY_LENGTH = 0
    else:
      self.body_length = rd.randrange(settings.SNAKE_BODY_LENGTH_MIN, settings.SNAKE_BODY_LENGTH_MAX)
    for i in range(self.body_length):
      block_hitbox = pygame.Rect(0, 0, self.body_block_width, self.body_block_height)
      self.body.insert(i, [0, 0])
      self.body_hitbox.insert(i, block_hitbox)

    self.move_vel = settings.SNAKE_INGAME_MOVE_VEL
    self.move_interval = settings.SNAKE_MOVE_INTERVAL
    self.direction_list = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    self.direction = self.direction_list[rd.randrange(4)]
    self.change_to = self.direction
    
    self.head_color = settings.WHITE
    self.body_color = settings.DARK_BLUE
    self.tail_color = settings.BLACK


  def move(self, platforms):
    if self.move_interval > 0:
      self.move_interval -= 1
    else:
      self.move_interval = settings.SNAKE_MOVE_INTERVAL
      if self.position[1] <= 0:
        self.direction = 'DOWN'
      elif self.position[0] >= settings.DISPLAY_WIDTH:
        self.direction = 'LEFT'
      elif self.position[1] >= settings.DISPLAY_HEIGHT:
        self.direction = 'UP'
      elif self.position[0] <= 0:
        self.direction = 'RIGHT'
      else:
        self.direction_list = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.change_to = self.direction_list[rd.randrange(len(self.direction_list))]
        if platforms:
          tmp_rect = pygame.Rect(0, 0, self.body_block_width, self.body_block_height)
          if self.change_to == 'UP':
            tmp_rect.x = self.position[0]
            tmp_rect.y = self.position[1] - self.move_vel * 3
            for pf in platforms:
              if pf.colliderect(tmp_rect):
                self.direction = 'DOWN'
                break
          if self.change_to == 'DOWN':
            tmp_rect.x = self.position[0]
            tmp_rect.y = self.position[1] + self.move_vel * 3
            for pf in platforms:
              if pf.colliderect(tmp_rect):
                self.direction = 'UP'
                break
          if self.change_to == 'LEFT':
            tmp_rect.x = self.position[0] - self.move_vel * 3
            tmp_rect.y = self.position[1]
            for pf in platforms:
              if pf.colliderect(tmp_rect):
                self.direction = 'RIGHT'
                break
          if self.change_to == 'RIGHT':
            tmp_rect.x = self.position[0] + self.move_vel * 3
            tmp_rect.y = self.position[1]
            for pf in platforms:
              if pf.colliderect(tmp_rect):
                self.direction = 'LEFT'
                break

      if self.change_to == 'UP' and self.direction != 'DOWN':
        self.direction = 'UP'
      if self.change_to == 'DOWN' and self.direction != 'UP':
        self.direction = 'DOWN'
      if self.change_to == 'LEFT' and self.direction != 'RIGHT':
        self.direction = 'LEFT'
      if self.change_to == 'RIGHT' and self.direction != 'LEFT':
        self.direction = 'RIGHT'

      if self.direction == 'UP':
        self.position[1] -= self.move_vel
      if self.direction == 'DOWN':
        self.position[1] += self.move_vel
      if self.direction == 'LEFT':
        self.position[0] -= self.move_vel
      if self.direction == 'RIGHT':
        self.position[0] += self.move_vel

      self.body.insert(0, list(self.position))
      self.body.pop()
      self.body_hitbox.insert(0, pygame.Rect(self.position[0], self.position[1], self.body_block_width, self.body_block_height))
      self.body_hitbox.pop()



  def draw(self):
    current_block_index = 0
    for block in self.body:
      if current_block_index < 2:
        pygame.draw.rect(settings.SCREEN, self.head_color,
        pygame.Rect(block[0], block[1], self.body_block_width, self.body_block_height))
        pygame.draw.rect(settings.SCREEN, settings.BLACK,
        pygame.Rect(block[0], block[1], self.body_block_width, self.body_block_height), settings.BORDER_INGAME_THICKNESS)

      elif current_block_index < len(self.body) - 4:
        pygame.draw.rect(settings.SCREEN, self.body_color,
        pygame.Rect(block[0], block[1], self.body_block_width, self.body_block_height))
        pygame.draw.rect(settings.SCREEN, settings.BLACK,
        pygame.Rect(block[0], block[1], self.body_block_width, self.body_block_height), settings.BORDER_INGAME_THICKNESS)

      else:
        pygame.draw.rect(settings.SCREEN, self.tail_color,
        pygame.Rect(block[0], block[1], self.body_block_width, self.body_block_height))

      current_block_index += 1
    self.head_color = settings.WHITE
    self.body_color = settings.DARK_BLUE
    self.tail_color = settings.BLACK


  def handle_scaling(self, display_mode):
    if display_mode & pygame.FULLSCREEN:
      self.position[0] //= 2
      self.position[1] //= 2
      settings.SNAKE_INGAME_BODY_BLOCK_WIDTH = settings.SNAKE_BODY_BLOCK_WIDTH
      settings.SNAKE_INGAME_BODY_BLOCK_HEIGHT = settings.SNAKE_BODY_BLOCK_HEIGHT
      settings.SNAKE_INGAME_MOVE_VEL = settings.SNAKE_MOVE_VEL
    else:
      self.position[0] *= 2
      self.position[1] *= 2
      settings.SNAKE_INGAME_BODY_BLOCK_WIDTH = settings.SNAKE_BODY_BLOCK_WIDTH * 2
      settings.SNAKE_INGAME_BODY_BLOCK_HEIGHT = settings.SNAKE_BODY_BLOCK_HEIGHT * 2
      settings.SNAKE_INGAME_MOVE_VEL = settings.SNAKE_MOVE_VEL * 2
    self.body_block_width = settings.SNAKE_INGAME_BODY_BLOCK_WIDTH
    self.body_block_height = settings.SNAKE_INGAME_BODY_BLOCK_HEIGHT
    self.move_vel = settings.SNAKE_INGAME_MOVE_VEL


  def handle_bullet_collision(self, bullet):
    for block in self.body_hitbox:
      if block.collidepoint(bullet.pos):
        if len(self.body) <= 3 or bullet.type == 'sniper':
          if settings.ENEMY_KILLED < level_0.ENEMY_NUMBER - 1:
            settings.ENEMY_DEAD_SOUND.play()
          settings.SCORE_INGAME += settings.SCORE_KILL_STEP
          settings.ENEMY_KILLED += 1
          settings.ENEMY_KILLED_TOTAL += 1
          self.body = []
          self.body_hitbox = []
        else:
          del self.body[:3]
          del self.body_hitbox[:3]
          self.head_color = self.body_color = self.tail_color = settings.DARK_RED
        return True