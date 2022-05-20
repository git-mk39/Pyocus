from re import I
import pygame

from Lib import settings



class Player:
  def __init__(self):
    self.hitbox = pygame.Rect(settings.PLAYER_INIT_POS_X, settings.PLAYER_INIT_POS_Y
    , settings.PLAYER_WIDTH, settings.PLAYER_HEIGHT)
    self.enemy_no_spawn_area = pygame.Rect(self.hitbox.center[0] - self.hitbox.width * 20, self.hitbox.center[1] - self.hitbox.height * 20
    , self.hitbox.width * 40, self.hitbox.height * 40)

    self.gravity = settings.GRAVITY
    self.is_falling = True
    self.is_in_midair = False
    self.jump_height = settings.PLAYER_JUMP_HEIGHT
    self.midair_jump_remaining = settings.PLAYER_MIDAIR_JUMP_REMAINING
    self.midair_jump_height = settings.PLAYER_MIDAIR_JUMP_HEIGHT
    self.fall_vel = settings.PLAYER_FALL_VEL
    self.max_fall_vel = settings.PLAYER_MAX_FALL_VEL
    self.downward_smash_vel = settings.PLAYER_DOWNWARD_SMASH_VEL
    self.move_vel = settings.PLAYER_MOVE_VEL
    self.can_move_left = True
    self.can_move_right = True
    self.dash_duration = settings.PLAYER_DASH_DURATION
    self.dash_duration_remaining = 0
    self.dash_interval = settings.PLAYER_DASH_INTERVAL
    self.dash_interval_remaining = 0
    self.dash_to_left = False

    self.collision_with_platform = False
    self.platform_collided_with = None

    self.lives = settings.PLAYER_LIVES
    self.death_count = 0

    self.sprite = pygame.transform.scale(settings.PLAYER_SPRITE
    , (self.hitbox.width, self.hitbox.height))
    self.heart_sprite = pygame.transform.scale(settings.PLAYER_HEART_SPRITE
    , (18, 18))
    self.heart_sprite_x = settings.PLAYER_HEART_SPRITE_X
    self.heart_sprite_y = settings.PLAYER_HEART_SPRITE_Y


  def pos_init(self):
    self.hitbox.x = settings.PLAYER_INIT_POS_X
    self.hitbox.y = settings.PLAYER_INIT_POS_Y


  def handle_scaling(self, display_mode):
    if display_mode & pygame.FULLSCREEN:
      self.hitbox.x //= 2
      self.hitbox.y //=2
      self.hitbox.width = settings.PLAYER_WIDTH
      self.hitbox.height = settings.PLAYER_HEIGHT
      self.jump_height = settings.PLAYER_JUMP_HEIGHT
      self.midair_jump_height = settings.PLAYER_MIDAIR_JUMP_HEIGHT
      self.max_fall_vel = settings.PLAYER_MAX_FALL_VEL
      self.downward_smash_vel = settings.PLAYER_DOWNWARD_SMASH_VEL
      self.fall_vel = settings.PLAYER_FALL_VEL
      self.move_vel = settings.PLAYER_MOVE_VEL
      self.gravity = settings.GRAVITY
      self.sprite = pygame.transform.scale(settings.PLAYER_SPRITE
      , (self.hitbox.width, self.hitbox.height))
      self.heart_sprite = pygame.transform.scale(settings.PLAYER_HEART_SPRITE
      , (18, 18))
      self.heart_sprite_x //= 2
      self.heart_sprite_y //= 2
    else:
      self.hitbox.x *= 2
      self.hitbox.y *= 2
      self.hitbox.width = settings.PLAYER_WIDTH * 2
      self.hitbox.height = settings.PLAYER_HEIGHT * 2
      self.jump_height = settings.PLAYER_JUMP_HEIGHT * 2
      self.midair_jump_height = settings.PLAYER_MIDAIR_JUMP_HEIGHT * 2
      self.max_fall_vel = settings.PLAYER_MAX_FALL_VEL * 2
      self.downward_smash_vel = settings.PLAYER_DOWNWARD_SMASH_VEL * 2
      self.fall_vel = settings.PLAYER_FALL_VEL * 2
      self.move_vel = settings.PLAYER_MOVE_VEL * 2
      self.gravity = settings.GRAVITY * 2
      self.sprite = settings.PLAYER_SPRITE
      self.heart_sprite = settings.PLAYER_HEART_SPRITE
      self.heart_sprite_x *= 2
      self.heart_sprite_y *= 2


  def set_enemy_no_spawn_area(self):
    self.enemy_no_spawn_area.x = self.hitbox.center[0] - self.hitbox.width * 20
    self.enemy_no_spawn_area.y = self.hitbox.center[1] - self.hitbox.height * 20


  def handle_gravity(self):
    if self.is_falling:
      if self.hitbox.y + self.hitbox.height + self.fall_vel <= settings.DISPLAY_HEIGHT:
        if self.fall_vel <= self.max_fall_vel:
          self.fall_vel += self.gravity
        self.hitbox.y += self.fall_vel
      else:
        self.hitbox.y = settings.DISPLAY_HEIGHT - self.hitbox.height
        self.is_falling = False
        self.midair_jump_remaining = settings.PLAYER_MIDAIR_JUMP_REMAINING
        self.is_in_midair = False


  def handle_jump(self):
    if self.is_in_midair and self.midair_jump_remaining > 0:
      self.fall_vel = -self.midair_jump_height
      self.midair_jump_remaining -= 1
    elif self.is_falling == False:
      self.fall_vel = -self.jump_height
      self.is_falling = True
      self.is_in_midair = True


  def handle_move_left_right(self):
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_a] and self.can_move_left:
      if self.hitbox.x > 0:
        self.hitbox.x -= self.move_vel
      else:
        self.hitbox.x = 0
    if keys_pressed[pygame.K_d] and self.can_move_right:
      if self.hitbox.x + self.move_vel + self.hitbox.width < settings.DISPLAY_WIDTH:
        self.hitbox.x += self.move_vel
      else:
        self.hitbox.x = settings.DISPLAY_WIDTH - self.hitbox.width
    if keys_pressed[pygame.K_s] and keys_pressed[pygame.K_SPACE]:
      self.fall_vel = self.downward_smash_vel

    if self.dash_interval_remaining > 0:
      self.dash_interval_remaining -= 1
    else:
      if self.dash_duration_remaining > 0:
        if self.dash_to_left and self.can_move_left:
          self.hitbox.x -= self.move_vel * 2
        elif self.can_move_right:
          self.hitbox.x += self.move_vel * 2
        self.dash_duration_remaining -= 1
        if self.dash_duration_remaining <= 0:
          self.dash_interval_remaining = settings.PLAYER_DASH_INTERVAL
      elif keys_pressed[pygame.K_LSHIFT] and keys_pressed[pygame.K_a] and self.can_move_left:
        self.dash_duration_remaining = settings.PLAYER_DASH_DURATION
        self.dash_to_left = True
      elif keys_pressed[pygame.K_LSHIFT] and keys_pressed[pygame.K_d] and self.can_move_right:
        self.dash_duration_remaining = settings.PLAYER_DASH_DURATION
        self.dash_to_left = False


  def handle_platform_collision(self, platforms):
    for pf in platforms:
      player_center_x = self.hitbox.center[0]
      player_center_y = self.hitbox.center[1]

      pf_topleft_x = pf.topleft[0]
      pf_topleft_y = pf.topleft[1]
      pf_topright_x = pf.topright[0]
      pf_topright_y = pf.topright[1]
      pf_bottomleft_x = pf.bottomleft[0]
      pf_bottomleft_y = pf.bottomleft[1]
      pf_bottomright_x = pf.bottomright[0]
      pf_bottomright_y = pf.bottomright[1]
      pf_center_x = pf.center[0]
      pf_center_y = pf.center[1]

      if self.hitbox.colliderect(pf):
        if player_center_y < pf_center_y and player_center_x > pf_topleft_x and player_center_x < pf_topright_x:
          self.hitbox.y = pf.y - self.hitbox.height
          self.is_falling = False
          self.fall_vel = 0
          self.midair_jump_remaining = settings.PLAYER_MIDAIR_JUMP_REMAINING
          self.is_in_midair = False

        elif player_center_y > pf_center_y and player_center_x > pf_bottomleft_x and player_center_x < pf_bottomright_x:
          self.hitbox.y = pf_bottomright_y
          self.fall_vel = -self.fall_vel

        elif player_center_x < pf_center_x and player_center_y > pf_topleft_y and player_center_y < pf_bottomleft_y:
          self.hitbox.x = pf.x - self.hitbox.width
          self.can_move_right = False
      
        elif player_center_x > pf_center_x and player_center_y > pf_topright_y and player_center_y < pf_bottomright_y:
          self.hitbox.x = pf_bottomright_x
          self.can_move_left = False

        self.collision_with_platform = True
        self.platform_collided_with = pf

    if self.collision_with_platform:
      cp = self.platform_collided_with
      if self.hitbox.x + self.hitbox.width < cp.x or self.hitbox.x > cp.x + cp.width or self.hitbox.y < cp.y - self.hitbox.height or self.hitbox.y > cp.y + cp.height:
        self.is_falling = True
        self.is_in_midair = True
        self.can_move_left = True
        self.can_move_right = True
        self.collision_with_platform = False


  def handle_enemy_collision(self, enemies):
    for enemy in enemies:
      for enemy_body_block in enemy.body_hitbox:
        if self.hitbox.colliderect(enemy_body_block):
          self.death_count += 1
          self.lives -= 1
          return True


  def handle_drawing(self):
    settings.SCREEN.blit(self.sprite, (self.hitbox.x, self.hitbox.y))