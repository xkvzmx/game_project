import pygame
from pygame.locals import *
import os.path

#-----------------------------------------------------------------------
# Program parameters
#-----------------------------------------------------------------------
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 500
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

#-----------------------------------------------------------------------
# Auxiliary functions
#-----------------------------------------------------------------------
def loadImage(name, useColorKey=False):
    """Upload an image and convert it to a surface. 
    The function loads an image from a file and converts its pixels to the pixel format of the screen.
    If the useColorKey flag is set to True, the color contained in the pixel (1,1) will be treated as transparent.
    @param name: (str) file name
    @param useColorKey: (bool) the transparency flag

    @return image: converted image
    """
    fullname = os.path.join("pictures",name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if useColorKey is True:
        colorkey = image.get_at((1,1)) #get color in the pixel (1,1)
        image.set_colorkey(colorkey,RLEACCEL) #set as transparent, increase performance with the RLEACCEL flag
    return image


#-----------------------------------------------------------------------------
# Object classes
#-----------------------------------------------------------------------------
class MyPlayer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("baller2.jpg",True)
        self.rect = self.image.get_rect()
        self.rect.center = (0.20*SCREEN_WIDTH, 0.5*SCREEN_HEIGHT)
        self.x_velocity = 0
        self.y_velocity = 0

    def update(self):
        pass


#-----------------------------------------------------------------------------
# Proper program
#-----------------------------------------------------------------------------


# create game window
screen = pygame.display.set_mode((SCREEN_SIZE))
pygame.display.set_caption("Basket League")

# load backgroud file
background_image = loadImage("court13.jpg")
screen.blit(background_image,(-115,-100))

# initialize player
myplayerSprite = pygame.sprite.RenderClear()    #container box
myplayer = MyPlayer()                           #create player
myplayerSprite.add(myplayer)                    #add player



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    myplayerSprite.draw(screen)

    pygame.display.flip() #update the display
    