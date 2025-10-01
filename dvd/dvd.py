import pygame
import random
import os

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
current = random.randint(0, 3)
dt = 0
dvd_logo = pygame.image.load(os.path.join('assets', 'dvd.png'))
dvd_logo = pygame.transform.scale(dvd_logo, (300, 100))

MIN_X = 0
MIN_Y = 0
MAX_X = 1280
MAX_Y = 720

player_pos = pygame.Vector2(random.randint(MIN_X, MAX_X), random.randint(MIN_Y, MAX_Y))

def move_up_right():
  player_pos.x += 200 * dt
  player_pos.y -= 100 * dt

def move_up_left():
  player_pos.x -= 200 * dt
  player_pos.y -= 100 * dt

def move_down_right():
  player_pos.x += 200 * dt
  player_pos.y += 100 * dt

def move_down_left():
  player_pos.x -= 200 * dt
  player_pos.y += 100 * dt

movements = [move_up_right, move_up_left, move_down_right, move_down_left]

direction = movements[current]

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  
  screen.fill('darkgrey')

  # RENDER HERE
  #pygame.draw.circle(screen, 'red', player_pos, CIRCLE_WIDTH)

  screen.blit(dvd_logo, player_pos)

  direction()

  if direction.__name__ == 'move_down_right' and int(player_pos.x) >= (MAX_X - 300):
    direction = move_down_left
    direction()

  if direction.__name__ == 'move_up_right' and int(player_pos.x) >= (MAX_X - 300):
    direction = move_up_left
    direction()

  if direction.__name__ == 'move_down_left' and int(player_pos.x) <= MIN_X:
    direction = move_down_right
    direction()

  if direction.__name__ == 'move_up_left' and int(player_pos.x) <= MIN_X:
    direction = move_up_right
    direction()

  if direction.__name__ == 'move_down_right' and int(player_pos.y) >= (MAX_Y - 100):
    direction = move_up_right
    direction()

  if direction.__name__ == 'move_up_right' and int(player_pos.y) <= MIN_Y:
    direction = move_down_right
    direction()

  if direction.__name__ == 'move_down_left' and int(player_pos.y) >= (MAX_Y - 100):
    direction = move_up_left
    direction()

  if direction.__name__ == 'move_up_left' and int(player_pos.y) <= MIN_Y:
    direction = move_down_left
    direction()

  pygame.display.flip()

  dt = clock.tick(60) / 1000

pygame.quit()
