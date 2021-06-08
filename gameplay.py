import pygame
from pygame.locals import *
import os.path
import random
import math

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

#-----------------------------------
# MyPlayer class
#-----------------------------------
class MyPlayer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("baller02.png",True)
        self.rect = self.image.get_rect()
        self.rect.center = (0.15*SCREEN_WIDTH, 0.75*SCREEN_HEIGHT)
        self.x_velocity = 0
        self.y_velocity = 0
        self.jumped = False

    def update(self):
        self.rect.move_ip((self.x_velocity, self.y_velocity))

        if self.rect.left < 70:
            self.rect.left = 70
        elif self.rect.right > 1120:
            self.rect.right = 1120

        if self.rect.top <= 250:
            self.rect.top = 250
            self.y_velocity = 5
        elif self.rect.bottom >= 450:
            self.rect.bottom = 450

#-----------------------------------
# Ball class
#-----------------------------------
class Ball(pygame.sprite.Sprite):
    def __init__(self,other):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("ball03.jpg",True)
        self.rect = self.image.get_rect()
        self.rect.center = (other.rect.center)
        self.isdribble = True
        self.shoot = False
        self.x_velocity = 0
        self.y_velocity = 0
        self.dy = 0

    def update(self):
        if self.isdribble == False:
            self.kill()
        elif self.shoot == True:
            #add gravity
            self.dy += 0.1
            if self.dy >= 20:
                self.dy = 20
            self.y_velocity += self.dy
            self.rect.move_ip((self.x_velocity,self.y_velocity))
            if 968 < self.rect.left < 988 and 993 < self.rect.right < 1013 and 223 < self.rect.top < 243 and 248 < self.rect.bottom < 268 and 0.1 < math.tan(self.x_velocity/self.y_velocity) < 1.0:
                print("POINT !")
                
        else:
            self.rect.move_ip((self.x_velocity,self.y_velocity))

            if self.rect.left < 133:
                self.rect.left = 133
            elif self.rect.right > 1060:
                self.rect.right = 1060

            if self.rect.top <= 365:
                self.rect.top = 365
                self.y_velocity = 5
            elif self.rect.bottom >= 450:
                self.rect.bottom = 450
                self.y_velocity = -5



#-----------------------------------------------------------------------------
# Proper program
#-----------------------------------------------------------------------------
pygame.init()

# create game window
screen = pygame.display.set_mode((SCREEN_SIZE))
pygame.display.set_caption("Basket League")

# load backgroud file
background_image = loadImage("court130.jpg")
screen.blit(background_image,(0,0))

# initialize player
myplayerSprite = pygame.sprite.RenderClear()    #player container
myplayer = MyPlayer()                           #create player
myplayerSprite.add(myplayer)                    #add player

# initialize ball
myballSprite = pygame.sprite.RenderClear()      #ball container
myball = Ball(myplayer)                         #create ball
myballSprite.add(myball)                        #add ball

# initialize time and running status
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(40)  # up to 40 frames per second
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT and myball.shoot == False:
                myplayer.x_velocity = -4
                myball.x_velocity = -4
            elif event.key == K_RIGHT and myball.shoot == False:
                myplayer.x_velocity = 4
                myball.x_velocity = 4
            elif event.key == K_UP and myplayer.jumped == False and myplayer.rect.bottom == 450 and myball.isdribble == False:
                myplayer.y_velocity = -12
                #myball.y_velocity = -12
                myplayer.jumped = True
            elif event.key == K_DOWN and myplayer.rect.bottom==450:
                myplayer.x_velocity = 0
                myplayer.y_velocity = 0
                myball.isdribble = False
                #myballSprite = pygame.sprite.RenderClear()      #ball container
                myball = Ball(myplayer)                         #create ball
                myballSprite.add(myball)                        #add ball
            elif event.key == K_r:
                myball.isdribble = False
            elif event.key == K_SPACE and myplayer.jumped == False and myplayer.rect.bottom == 450 and myball.isdribble==True:
                myball.kill()
                myball = Ball(myplayer)                         #create ball
                myballSprite.add(myball) 
                myball.rect.center = (myplayer.rect.midtop)
                myball.shoot = True
                myplayer.y_velocity = -12
                myplayer.jumped = True
                myball.x_velocity = random.randrange(15,17)
                myball.y_velocity = random.randrange(-18,-14)


        elif event.type == KEYUP:
            if event.key == K_LEFT:
                myplayer.x_velocity = 0 
                myball.x_velocity = 0 
            elif event.key == K_RIGHT:
                myplayer.x_velocity = 0
                myball.x_velocity = 0
            elif event.key == K_UP:
                myplayer.y_velocity = 5
                #myball.y_velocity = 5
                myplayer.jumped = False
            elif event.key == K_DOWN:
                pass
            elif event.key == K_SPACE:
                myplayer.y_velocity = 5
                myplayer.jumped = False
        
    myplayerSprite.update()     #update player sprite
    myballSprite.update()       #update ball sprite

    myplayerSprite.clear(screen,background_image) #clean screen
    myballSprite.clear(screen,background_image)
    
    myplayerSprite.draw(screen) #draw player sprite
    myballSprite.draw(screen)   #draw ball sprite

    pygame.display.flip() #update the display
    