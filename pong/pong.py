'''
My own version of pong I will call "moog pong"
Expected Features:
 - Title and Game Over cards
 - Option to play with CPUs of varying difficulty or with a live player
 - Incrementally increasing ball speed (like tetris)
 - Option to choose colors of ball, bats
 - Score display
 - High score persistence

 This is a project I made for my own learning and is currently a simple MVP. Major changes are subject 
 to take place at any time.
'''

VERSION = "0.1"

### Imports
try:
  import pygame
  from pygame.locals import * # maybe don't use wildcard and just import what I need.
  import random
  import sys
except ImportError as e:
  print(f'Failed to load module: {e}')
  sys.exit(2)

### System functions

def terminate():
  print('Quitting...')
  sys.exit()

### Classes

class Ball: # Class for ball to appear on the screen which bats will volley back and forth
  def __init__(self):
    self.color = 'white'
    screen = pygame.display.get_surface()
    self.pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    self.score = 0
    self.last_score = 0
    self.speed = 300
    self.speed_factor = 1.2
    self.width = 20
    self.direction = self.still
    self.movement_choices = {'upright': self.upright, 'upleft': self.upleft, 'downright': self.downright, 'downleft': self.downleft}

  def draw_circle(self, surface, color, pos, width):
    pygame.draw.circle(surface, color, pos, width)

  ### Probably a better way to do this TODO Refactor
  def still(self, delta):
    self.pos.x += 0 * delta
    self.pos.y += 0 * delta
    self.state = 'still'

  def upright(self, delta):
    self.pos.x += self.speed * delta 
    self.pos.y -= self.speed / 2 * delta 
    self.state = 'upright'

  def downright(self, delta):
    self.pos.x += self.speed * delta
    self.pos.y += self.speed / 2 * delta
    self.state = 'downright'

  def upleft(self, delta):
    self.pos.x -= self.speed * delta
    self.pos.y -= self.speed / 2 * delta
    self.state = 'upleft'

  def downleft(self, delta):
    self.pos.x -= self.speed * delta
    self.pos.y += self.speed / 2 * delta
    self.state = 'downleft'

  ### Does this need to be here? Should I have a Game class with method start_game?
  def start_movement(self):
    self.state, self.direction = random.choice(list(self.movement_choices.items()))

class Bat: # Class for bat which player will use to volley ball
  def __init__(self, side):
    self.side = side
    self.width = 25
    self.height = 125
    self.speed = 10
    self.body = self.reinit()

  def reinit(self):
    screen = pygame.display.get_surface()
    self.center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    if self.side == 'left':
      self.center.x = 50
    if self.side == 'right':
      self.center.x = right - 50
    rect = pygame.Rect(self.center.x, self.center.y, self.width, self.height)
    rect.center = self.center
    return rect

  def draw_bat(self, surf, color):
    pygame.draw.rect(surf, color, self.body)

  def move_up(self, delta):
    self.center.y -= 500 * delta
    self.body.center = self.center

  def move_down(self, delta):
    self.center.y += 500 * delta
    self.body.center = self.center

class ScreenOverlay: # Class for title and game over cards. Also may use for "Options" screen
  def __init__(self, surf):
    self.surf = surf
    self.state = 'start'
    self.message = 'Press SPACE to Start'
    self.display_message()

  def show_start(self):
    self.state = 'start'
    self.message = 'Press SPACE to Start'

  def show_score(self, count):
    self.state = 'score'
    self.message = count

  def show_game_over(self):
    self.state = 'game over'
    self.message = 'GAME OVER'

  def display_message(self):
    self.font = pygame.font.Font(None, 64)
    self.text = self.font.render(self.message, False, (255, 255, 255))
    self.textpos = self.text.get_rect(centerx=self.surf.get_width() / 2, y=100)
    self.surf.blit(self.text, self.textpos)

### Main function
def main():
  pygame.init() # Initialize pygame
  global top, left, bottom, right
  top, left, bottom, right = 0, 0, 580, 920
  screen = pygame.display.set_mode((920, 580))
  clock = pygame.time.Clock()
  center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
  dt = 0

  # Initialize ball
  ball = Ball()
  player1 = Bat('left')
  player2 = Bat('right')
  screen_overlay = ScreenOverlay(screen)

  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        terminate()
      elif event.type == KEYDOWN:
        if event.key == K_SPACE and ball.state == 'still':
          ball.start_movement()

    screen.fill((0, 0, 0))

    # Render here vvv

    ball.draw_circle(screen, ball.color, ball.pos, ball.width)  
    player1.draw_bat(screen, 'teal')
    player2.draw_bat(screen, 'pink')

    ### BAT MOVEMENT ###
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.body.top >= top:
      player1.move_up(dt)
    if keys[pygame.K_s] and player1.body.bottom <= bottom:
      player1.move_down(dt)
    if keys[pygame.K_UP] and player2.body.top >= top:
      player2.move_up(dt)
    if keys[pygame.K_DOWN] and player2.body.bottom <= bottom:
      player2.move_down(dt)

    ### BALL MOVEMENT ###
    ball.direction(dt) # Initialize Ball direction

    collision_left = (ball.pos.y <= player1.body.bottom and ball.pos.y >= player1.body.top and ball.pos.x <= player1.body.right # Left paddle collide
      or ball.pos.y <= player1.body.bottom and ball.pos.y >= player1.body.top and ball.pos.x <= player1.body.right)

    collision_right = (ball.pos.y <= player2.body.bottom and ball.pos.y >= player2.body.top and ball.pos.x >= player2.body.left # Right paddle collide
      or ball.pos.y <= player2.body.bottom and ball.pos.y >= player2.body.top and ball.pos.x >= player2.body.left)

    if collision_left or collision_right:
      ball.score += 1
    
    if (collision_right and ball.state == 'downright' #right paddle collide 
      or ball.pos.y <= top + ball.width / 2 and ball.state == 'upleft'): # top
      ball.state = 'downleft'
      ball.direction = ball.downleft
      
    if (collision_right and ball.state == 'upright' #right paddle collide
      or ball.pos.y >= bottom - ball.width / 2 and ball.state == 'downleft'): # bottom
      ball.state = 'upleft'
      ball.direction = ball.upleft

    if (collision_left and ball.state == 'downleft' # left paddle collide
      or ball.pos.y <= top + ball.width / 2 and ball.state == 'upright'): # top
      ball.state = 'downright'
      ball.direction = ball.downright

    if (collision_left and ball.state == 'upleft' # left paddle collide
      or ball.pos.y >= bottom - ball.width / 2 and ball.state == 'downright'): # bottom
      ball.state = 'upright'
      ball.direction = ball.upright

    if ball.pos.x <= left or ball.pos.x >= right:
      ball.direction = ball.still
      screen_overlay.show_game_over()

    if ball.state != 'still':
      screen_overlay.show_score(str(ball.score))

    if ball.score > ball.last_score:
      ball.speed *= ball.speed_factor
      ball.last_score += 5

    screen_overlay.display_message()

    # Render here ^^^
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

    clock.tick(60)

  pygame.quit()

### Call main method

if __name__ == '__main__':
  main()
