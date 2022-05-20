import pygame

from Lib import settings
from Data import level_0



clock = pygame.time.Clock()


def draw_screen(ingame_player, ingame_cursor, bullets):
  settings.SCREEN.blit(settings.BACKGROUND_INGAME, (0, 0))
  level_0.draw_platform()
  level_0.draw_enemy()
  ingame_player.handle_drawing()
  for bl in bullets:
    bl.draw(settings.SCREEN)
  settings.SCREEN.blit(settings.INGAME_FONT.render('Score: ' + str(settings.SCORE_INGAME), True, settings.WHITE), (10, 10))
  settings.SCREEN.blit(settings.INGAME_FONT.render('Enemy hit: ' + str(settings.ENEMY_HIT), True, settings.WHITE), (10, settings.FONT_SIZE_INGAME + 20))
  settings.SCREEN.blit(settings.INGAME_FONT.render('Enemy killed: ' + str(settings.ENEMY_KILLED), True, settings.WHITE), (10, settings.FONT_SIZE_INGAME * 2 + 30))
  settings.SCREEN.blit(settings.INGAME_FONT.render('Total killed: ' + str(settings.ENEMY_KILLED_TOTAL), True, settings.WHITE), (10, settings.FONT_SIZE_INGAME * 3 + 40))
  settings.SCREEN.blit(settings.INGAME_FONT.render('Player death: ' + str(ingame_player.death_count), True, settings.WHITE), (10, settings.FONT_SIZE_INGAME * 4 + 50))
  settings.SCREEN.blit(settings.INGAME_FONT.render('Stage: ' + str(settings.CURRENT_STAGE), True, settings.WHITE), (10, settings.FONT_SIZE_INGAME * 5 + 60))
  settings.SCREEN.blit(ingame_player.heart_sprite, (ingame_player.heart_sprite_x, ingame_player.heart_sprite_y))
  settings.SCREEN.blit(settings.INGAME_FONT.render(str(ingame_player.lives), True, settings.WHITE), ((ingame_player.heart_sprite_x // 100) * 103, ingame_player.heart_sprite_y))
  ingame_cursor.draw_sprite()
  pygame.display.update()


def draw_screen_pause():
  pause = True
  pause_title = settings.END_SCREEN_FONT.render('GAME PAUSED', True, settings.WHITE)
  pause_info_continue = settings.PAUSE_SCREEN_FONT.render('Press <Esc> to continue', True, settings.WHITE)
  pause_info_quit = settings.PAUSE_SCREEN_FONT.render('Press <q> to quit', True, settings.WHITE)
  display_center = pygame.display.get_surface().get_rect().center
  pause_title_rect = pause_title.get_rect(center = display_center)
  tmp_rect = list(display_center)
  tmp_rect[1] = (tmp_rect[1] // 100) * 160
  pause_info_continue_rect = pause_info_continue.get_rect(center = tuple(tmp_rect))
  tmp_rect = list(display_center)
  tmp_rect[1] = (tmp_rect[1] // 100) * 180
  pause_info_quit_rect = pause_info_quit.get_rect(center = tuple(tmp_rect))
  settings.SCREEN.blit(pause_title, pause_title_rect)
  settings.SCREEN.blit(pause_info_continue, pause_info_continue_rect)
  settings.SCREEN.blit(pause_info_quit, pause_info_quit_rect)
  pygame.display.update()
  while pause:
    clock.tick(settings.FPS)
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        pause = False
        return True
      elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        return False


def draw_screen_win():
  text = settings.END_SCREEN_FONT.render('STAGE CLEAR!' , True, settings.WHITE)
  text_rect = text.get_rect(center = pygame.display.get_surface().get_rect().center)
  settings.SCREEN.blit(text, text_rect)
  pygame.display.update()
  while settings.END_SCREEN_TIME_REMAINING > 0:
    clock.tick(settings.FPS)
    settings.END_SCREEN_TIME_REMAINING -= 1
  settings.END_SCREEN_TIME_REMAINING = settings.END_SCREEN_TIME_INTERVAL


def draw_screen_loose(ingame_player):
  if ingame_player.lives == 0:
    text = settings.END_SCREEN_FONT.render('ONE MORE HIT, YOU\'RE DONE!', True, settings.WHITE)
  else:
    text = settings.END_SCREEN_FONT.render('YOU LOST 1 LIFE', True, settings.WHITE)
  text_rect = text.get_rect(center = pygame.display.get_surface().get_rect().center)
  settings.SCREEN.blit(text, text_rect)
  pygame.display.update()
  while settings.END_SCREEN_TIME_REMAINING > 0:
    clock.tick(settings.FPS)
    settings.END_SCREEN_TIME_REMAINING -= 1
  settings.END_SCREEN_TIME_REMAINING = settings.END_SCREEN_TIME_INTERVAL


def draw_screen_game_over():
  text = settings.END_SCREEN_FONT.render('GAME OVER :|', True, settings.WHITE)
  text_rect = text.get_rect(center = pygame.display.get_surface().get_rect().center)
  settings.SCREEN.blit(text, text_rect)
  pygame.display.update()
  while settings.GAME_OVER_SCREEN_TIME_REMAINING > 0:
    clock.tick(settings.FPS)
    settings.GAME_OVER_SCREEN_TIME_REMAINING -= 1
  settings.GAME_OVER_SCREEN_TIME_REMAINING = settings.GAME_OVER_SCREEN_TIME_INTERVAL