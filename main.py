import pygame

from Lib import settings
from Lib import player
from Lib import scaling
from Lib import drawing
from Lib import movement
from Lib import collision
from Lib import cursor
from Lib import bullet
from Lib import intro
from Data import level_0


pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption('Pyocus')
pygame.display.set_icon(settings.GAME_ICON)
pygame.mouse.set_visible(False)


def main():
  settings.BACKGROUND_MUSIC_CHANNEL.play(settings.BACKGROUND_MUSIC)
  clock = pygame.time.Clock()
  ingame_player = player.Player()

  intro.display_intro(ingame_player)

  ingame_player.pos_init()
  run = True

  while run:
    if not settings.BACKGROUND_MUSIC_CHANNEL.get_busy():
      settings.BACKGROUND_MUSIC_CHANNEL.play(settings.BACKGROUND_MUSIC)
    level_0.init_enemy(ingame_player.enemy_no_spawn_area)
    bullets = []
    shotgun_fire_interval_remaining = 0
    sniper_current_charge = 0
    ingame_cursor = cursor.Cursor()
    game_progress = True

    while game_progress:
      clock.tick(settings.FPS)
      ingame_player_pos = ingame_player.hitbox.center
      ingame_cursor_pos = pygame.mouse.get_pos()

      if shotgun_fire_interval_remaining > 0:
        shotgun_fire_interval_remaining -= 1

      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          run = False
          game_progress = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
          scaling.handle_scaling(settings.SCREEN.get_flags(), ingame_player, level_0.PLATFORM, level_0.ENEMIES)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_w:
          ingame_player.handle_jump()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          bullets.append(bullet.Bullet(ingame_player_pos, ingame_cursor_pos))
          settings.BULLET_FIRE_SOUND.play()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and shotgun_fire_interval_remaining == 0:
          settings.SHOTGUN_FIRE_SOUND.play()
          bullet.shotgun_fires(bullets, ingame_player_pos, ingame_cursor_pos)
          shotgun_fire_interval_remaining = settings.SHOTGUN_FIRE_INTERVAL
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
          settings.BACKGROUND_MUSIC.set_volume(25)
          game_progress = drawing.draw_screen_pause()
          if game_progress == False:
            run = False
            break
          settings.BACKGROUND_MUSIC.set_volume(100)

      if pygame.mouse.get_pressed()[0]:
        sniper_current_charge += 1
        if settings.SNIPER_CHARGING_SOUND_IS_PLAYING == False and sniper_current_charge > 10:
          settings.SNIPER_CHARGING_SOUND.play()
          settings.SNIPER_CHARGING_SOUND_IS_PLAYING = True
        if sniper_current_charge >= settings.SNIPER_CHARGE:
          ingame_cursor.sniper_ready_sprite()
        else:
          ingame_cursor.active_sprite()
      else:
        if settings.SNIPER_CHARGING_SOUND_IS_PLAYING:
          settings.SNIPER_CHARGING_SOUND.stop()
          settings.SNIPER_CHARGING_SOUND_IS_PLAYING = False
        if sniper_current_charge >= settings.SNIPER_CHARGE:
          settings.SNIPER_FIRE_SOUND.play()
          bullets.append(bullet.SniperBullet(ingame_player_pos, ingame_cursor_pos))
        sniper_current_charge = 0
        ingame_cursor.inactive_sprite()
      ingame_cursor.get_pos(*ingame_cursor_pos)

      ingame_player.handle_gravity()
      ingame_player.handle_move_left_right()
      movement.handle_bullet_movement(bullets)
      movement.handle_enemy_movement(level_0.ENEMIES, level_0.PLATFORM)
      ingame_player.handle_platform_collision(level_0.PLATFORM)
      collision.handle_bullet_collision_wall(bullets)
      collision.handle_bullet_collision_platform(bullets, level_0.PLATFORM)
      collision.handle_bullet_collision_enemy(bullets, level_0.ENEMIES)
      drawing.draw_screen(ingame_player, ingame_cursor, bullets)

      if settings.ENEMY_KILLED == level_0.ENEMY_NUMBER:
        settings.VICTORY_SOUND.play()
        drawing.draw_screen_win()
        level_0.ENEMY_NUMBER += 3
        settings.SNAKE_BODY_LENGTH_MIN += 5
        settings.SNAKE_BODY_LENGTH_MAX += 5
        settings.CURRENT_STAGE += 1
        game_progress = False
      elif ingame_player.handle_enemy_collision(level_0.ENEMIES):
        if ingame_player.lives < 0:
          settings.BACKGROUND_MUSIC.stop()
          settings.GAME_OVER_SOUND.play()
          drawing.draw_screen_game_over()
          settings.ENEMY_KILLED_TOTAL = 0
          ingame_player.lives = settings.PLAYER_LIVES
          ingame_player.death_count = 0
          settings.CURRENT_STAGE = 0
          level_0.ENEMY_NUMBER = settings.ENEMY_INIT_NUMBER
        else:
          drawing.draw_screen_loose(ingame_player)
          ingame_player.death_count + 1
        settings.SCORE_INGAME = 0
        game_progress = False


    level_0.ENEMIES.clear()
    bullets.clear()
    ingame_player.set_enemy_no_spawn_area()
    settings.ENEMY_KILLED = 0
    settings.ENEMY_HIT = 0

  pygame.quit()
  level_0.ENEMIES.clear()
  bullets.clear()


if __name__ == '__main__':
  main()