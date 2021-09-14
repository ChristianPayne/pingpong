import time
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull

pixel_pin = board.D24

p1_pin = DigitalInOut(board.D10)
p1_pin.direction = Direction.INPUT
p1_pin.pull = Pull.DOWN

p2_pin = DigitalInOut(board.D11)
p2_pin.direction = Direction.INPUT
p2_pin.pull = Pull.DOWN

# idle, play, gameOver
game_state = 'idle'

num_pixels = 30

center_pixels_color = (0, 0, 0, 255)
marker_color = (0, 0, 0, 255)

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.15, auto_write=False, pixel_order=(1, 0, 2, 3))

marker_pos = 1
marker_direction = 1

def setup () :
  # Clear all the pixels of color.
  pixels.fill((0, 0, 0))
  pixels.show()

def loop () :
  global game_state
  global marker_pos
  while True:
    if(game_state == 'idle'):
      pixels.fill((50,50,50))
      if(p1_pin.value):
        marker_pos = 1
        game_state = 'play'
      if(p2_pin.value):
        marker_pos = num_pixels - 2
        game_state = 'play'
      pixels.show()
    elif(game_state == 'play'):
      if(p1_pin.value):
        click(0)
      if(p2_pin.value):
        click(1)
      pixels.show()
      PixelRun()
      setCenterPixels()
    elif(game_state == 'gameOver'):
      time.sleep(3)
      game_state = 'idle'


# FUNCTIONS

def click(player):
  global marker_direction
  global marker_pos
  global side
  
  if(marker_pos - int(num_pixels / 2) < 0):
    side = 0
  else:
    side = 1

  if(player == 0 and side == 0):
    marker_direction = 1
  if(player == 1 and side == 1):
    marker_direction = -1

def setCenterPixels():
  global center_pixels
  if(num_pixels % 2 == 0):
    center_pixels = [int(num_pixels / 2), int(num_pixels / 2) - 1]
  else:
    center_pixels = [int(num_pixels / 2)]

  for i in range(0, len(center_pixels)):
    pixels[center_pixels[i]] = center_pixels_color

# Move an integer from 0 to the max number of pixels and back.
def PixelRun ():
  global marker_pos
  global marker_direction
  # Turn off all the pixels.
  pixels.fill((0, 0, 255))
  # Set the pixel at the current position to white.
  pixels[marker_pos] = marker_color
  # Increment the position of the pixel.

  # Bounce back if you hit a side.
  if(marker_pos == 0):
    gameOver(0)
  elif (marker_pos >= num_pixels - 1):
    gameOver(1)

  marker_pos += marker_direction
  time.sleep(0.005)

def gameOver(playerWhoLost):
  global game_state
  pixels.fill((0, 255, 0))
  if(playerWhoLost == 0):
    for i in range(0, int(num_pixels/2)):
      pixels[i] = (255, 0, 0)
  if(playerWhoLost == 1):
    for i in range(int(num_pixels/2), num_pixels):
      pixels[i] = (255, 0, 0)

  setCenterPixels()
  pixels.show()
  game_state = 'gameOver'




setup()
loop()