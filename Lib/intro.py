import pygame

from Lib import snake
from Lib import settings



def display_intro(ingame_player):
  clock = pygame.time.Clock()
  intro = True
  intro_snake = snake.Snake(ingame_player.enemy_no_spawn_area)

  while intro:
    clock.tick(settings.FPS)
    settings.SCREEN.fill(settings.GRAY)
    intro_background_text = settings.INTRO_PYOCUS_FONT.render('PYOCUS', True, settings.BLACK)
    intro_foreground_text = settings.INTRO_SCREEN_FONT.render('MỒI SĂN RẮN', True, settings.DARK_BLUE)
    intro_background_text_rect = intro_background_text.get_rect(center = pygame.display.get_surface().get_rect().center)
    intro_foreground_text_rect = intro_foreground_text.get_rect(center = pygame.display.get_surface().get_rect().center)
    settings.SCREEN.blit(intro_background_text, intro_background_text_rect)
    intro_snake.move(None)
    intro_snake.draw()
    settings.SCREEN.blit(intro_foreground_text, intro_foreground_text_rect)
    ingame_player.hitbox.x = settings.DISPLAY_WIDTH // 2
    ingame_player.hitbox.y = settings.DISPLAY_HEIGHT // 2
    ingame_player.handle_drawing()
    pygame.display.update()
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
        intro = False