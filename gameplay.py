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
        self.image = loadImage("baller02.png",True)
        self.rect = self.image.get_rect()
        self.rect.center = (0.15*SCREEN_WIDTH, 0.75*SCREEN_HEIGHT)
        self.x_velocity = 0
        self.y_velocity = 0

    def update(self):
        self.rect.move_ip((self.x_velocity, self.y_velocity))

        if self.rect.left < 70:
            self.rect.left = 70
        elif self.rect.right > 1120:
            self.rect.right = 1120

        if self.rect.top <= SCREEN_HEIGHT/2: #tylko dolna połowa ekranu
            self.rect.top = SCREEN_HEIGHT/2
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


#-----------------------------------------------------------------------------
# Proper program
#-----------------------------------------------------------------------------


# create game window
screen = pygame.display.set_mode((SCREEN_SIZE))
pygame.display.set_caption("Basket League")

# load backgroud file
background_image = loadImage("court130.jpg")
screen.blit(background_image,(0,0))

# initialize player
myplayerSprite = pygame.sprite.RenderClear()    #container box
myplayer = MyPlayer()                           #create player
myplayerSprite.add(myplayer)                    #add player



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT:
                myplayer.x_velocity = -1
            elif event.key == K_RIGHT:
                myplayer.x_velocity = 1
            elif event.key == K_UP:
                pass
            elif event.key == K_DOWN:
                pass
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                myplayer.x_velocity = 0 
            elif event.key == K_RIGHT:
                myplayer.x_velocity = 0
            elif event.key == K_UP:
                myplayer.y_velocity = 0
            elif event.key == K_DOWN:
                myplayer.y_velocity = 0
        
    myplayerSprite.update()     #update player sprite
    myplayerSprite.clear(screen,background_image) #clean screen
    myplayerSprite.draw(screen) #draw player sprite

    pygame.display.flip() #update the display
    