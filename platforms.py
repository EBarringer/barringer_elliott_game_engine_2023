# content from kids can code: http://kidscancode.org/blog/

# import libraries and modules
import pygame as pg
from pygame.sprite import Sprite
import random
import os
from settings import *
from threading import Timer

vec = pg.math.Vector2

# setup asset folders here - images sounds etc.
game_folder = os.path.dirname(__file__)
img_folder = game_folder
snd_folder = game_folder

global RUNNING 
RUNNING = True

# game settings 
WIDTH = 360
HEIGHT = 480
FPS = 30
SCORE = 0

# player settings
PLAYER_JUMP = 30
PLAYER_GRAV = 1.5
PLAYER_FRIC = -0.3

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKYBLUE = (150, 200, 255)

def draw_text(text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    screen.blit(text_surface, text_rect)

class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        # self.image = pg.Surface((50, 50))
        # self.image.fill(GREEN)
        # use an image for player sprite...
        self.image = pg.image.load(os.path.join(img_folder, 'theBell.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.hitpoints = 3
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.x = 5
        if keys[pg.K_SPACE]:
            self.jump()
    def jump(self):
        hits = pg.sprite.spritecollide(self, all_platforms, False)
        if hits:
            print("i can jump")
            self.vel.y = -PLAYER_JUMP
    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        self.controls()
        # friction for side to side 
        self.acc.x += self.vel.x * PLAYER_FRIC

        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

        # checks if player is no longer on the screen, resets pos
        if self.rect.y > HEIGHT or self.rect.x > WIDTH:
            
            self.pos = vec(WIDTH/2, HEIGHT/2)
        
        #checks if player has no more hitpoints
        if player.hitpoints <= 0:

            print("The player has no more hitpoints.")
            pg.quit()
            

# x plat

class XPlatform(Sprite):
    def __init__(self, x, y, w, h, category):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        print(self.rect.center)
        self.category = category
        self.speed = 10
    def update(self):
        if self.category == "moving":
            self.rect.x += self.speed
            if self.rect.x + self.rect.w > WIDTH or self.rect.x < 0:
                self.speed = -self.speed

# y plat

class YPlatform(Sprite):

    def __init__(self, x, y, w, h, category):

        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        print(self.rect.center)
        self.category = category
        self.speed = 5
    
    def update(self):

        if self.category == "moving":

            self.rect.y += self.speed

            if self.rect.y + self.rect.h > HEIGHT or self.rect.y < 0:

                self.speed = -self.speed
                
class Mob(Sprite):

    def __init__(self, x, y, w, h, category):

        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.category = category
        self.speed = random.randint(10, 15)

    def reset(self):

        self.category == "alive"
    
    def update(self):

        if self.category == "alive":

            self.rect.x += self.speed

            if (self.rect.y + self.rect.h > HEIGHT or self.rect.y < 0) or (self.rect.x + self.rect.w > WIDTH or self.rect.x < 0):
                
                self.speed = -self.speed
                self.rect.y += 25

        if self.category == "dead":

            self.rect.x = self.rect.x

            # resets mob position upon leaving the screen
            if self.rect.y > HEIGHT or self.rect.x > WIDTH:

                self.rect.x = 50
                self.rect.y = 50
        
        

            


# init pygame and create a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()

# create a group for all sprites
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
all_mobs = pg.sprite.Group()

# instantiate classes
player = Player()

for plat in PLATFORM_LIST:

    p = XPlatform(*plat)
    all_sprites.add(p)
    all_platforms.add(p)


Creature = Mob(50, 50, 50, 50, "alive")

# create group of random platforms

'''def RandPlat(int):

    for i in range(int):

        plat = XPlatform(random.randint(100, 300), random.randint(100, 300), random.randint(100, 300), random.randint(20, 50), "moving")
        all_sprites.add(plat)
        all_platforms.add(plat)'''

#RandPlat(3)

# add instances to groups
all_sprites.add(player)
all_sprites.add(plat)
all_sprites.add(plat1)
all_sprites.add(newplat)
all_sprites.add(Creature)
all_platforms.add(plat)
all_platforms.add(plat1)
all_platforms.add(newplat)
all_mobs.add(Creature)


# Game loop
while RUNNING:
    # keep the loop running using clock
    currentfps = clock.tick(FPS)
        
    for event in pg.event.get():
        # check for closed window
        if event.type == pg.QUIT:
            RUNNING = False
    
    ############ Update ##############
    # update all sprites
    # (the player controls or input happen in player update method)
    all_sprites.update()

    # this is what prevents the player from falling through the platform when falling down...
    if player.vel.y > 0:
            hits = pg.sprite.spritecollide(player, all_platforms, False)
            if hits:
                player.pos.y = hits[0].rect.top
                player.vel.y = 0
                
    # this prevents the player from jumping up through a platform
    if player.vel.y < 0:
        hits = pg.sprite.spritecollide(player, all_platforms, False)
        if hits:
            print("ouch")
            SCORE -= 1
            if player.rect.bottom >= hits[0].rect.top - 5:
                player.rect.top = hits[0].rect.bottom
                player.acc.y = 5
                player.vel.y = 0

    # interaction for when player touches the mob:
    m_collide = pg.sprite.spritecollide(player, all_mobs, False)

    if m_collide:

        #check for collision with the player
        collision = pg.sprite.spritecollide(player, all_mobs, False)

        if collision:

            all_mobs.category == "dead"

            t = Timer(3, all_mobs.reset)
            t.start()
        
    ############ Draw ################
    # draw the background screen
    # draw all sprites
    screen.fill(SKYBLUE)
    all_sprites.draw(screen)
    draw_text("FPS: " + str(currentfps), 22, WHITE, WIDTH/2, HEIGHT/10)
    draw_text("Health: " + str(player.hitpoints), 22, WHITE, (WIDTH / 2), (HEIGHT / 10) + 50)

    # buffer - after drawing everything, flip display
    pg.display.flip()

if not RUNNING:
    pg.quit()
