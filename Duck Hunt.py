import pygame
import sys
import random
from pygame import *
from pygame.sprite import *
from pygame.sysfont import *



# -----------------------------------------
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load('s-l500.png')
        self.rect = self.image.get_rect()
        self.rect.y = random.randint(100,400)

# bird move to the right
    def flee(self):
        self.rect.right += random.randint(1,5)*4



    def draw(self,screen):
        screen.blit(self.image, self.rect)

# ----------------------------------------

class Aim(pygame.sprite.Sprite):

    def __init__(self):
        Sprite.__init__(self)
        self.image = pygame.image.load('target_PNG8.png')
        self.rect = self.image.get_rect()

    def hit(self,target):
        return self.rect.colliderect(target)

    def update(self,pt):
        self.rect.center = pt

    def draw(self,screen):
        screen.blit(self.image, self.rect)

# ---------------------------------------
class Text_Menu(Sprite):
    def __init__(self,fontsize, fontstyle, text, xpos, ypos, R, G, B):
        Sprite.__init__(self)
        self.font = pygame.font.SysFont(fontstyle,fontsize)
        self.image = self.font.render(text, False, (R,G,B))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos


# ---------- Main -----------------------
pygame.init()
screen = pygame.display.set_mode((1080,729))
pygame.display.set_caption('Duck Hunt')
background = pygame.image.load('stage.png')
scrWidth, scrHeight = screen.get_size()
gun_snd = pygame.mixer.Sound('Duck Hunt SFX (13).wav')
gun_snd.set_volume(1)

# ---------------------------------------------------------
# Main program / How the game works
def main():

    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    mousepos = (scrWidth/2, scrHeight/2)
    bird_timer = pygame.time.get_ticks()
    bird_group = Group()
    aim = Aim()
    score = 0
    life = 5
    running = True


    while running:
        text_score = Text_Menu(40,'Times New Roman','Score :' + str(score), 0, 0, 255, 255, 255)
        text_life = Text_Menu(40,'Times New Roman','Life :' + str(life), 0,80 , 255, 255, 255)
        text_appear = Group(text_score,text_life)

        clock.tick(60)

# To summon the bird
        if pygame.time.get_ticks() - bird_timer >= 3000:
            bird = Bird()
            bird_group.add(bird)
            bird_timer = pygame.time.get_ticks()

# how the bird work in the game
        for bird in bird_group:
            bird.flee()
            if bird.rect.left >= 1200:
                bird_group.remove(bird)
                life -= 1
            if life == 0:
                running = False
                mouse.set_visible(True)
                continue_menu(score)

# condition in the game
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEMOTION:
                mousepos = pygame.mouse.get_pos()
            if event.type == MOUSEBUTTONDOWN:
                running = True
                gun_snd.play()
                if spritecollide(aim, bird_group, dokill=True):
                    score += 100

                else:
                    life -= 1
                    if life == 0:
                        running = False
                        mouse.set_visible(True)
                        continue_menu(score)


        aim.update(mousepos)


# draw / update the picture
        screen.blit(background, (0,0))
        bird_group.draw(screen)
        aim.draw(screen)
        text_appear.draw(screen)

        pygame.display.update()

# ----------------------------------------------------
# Continue Menu when the life = 0
def continue_menu(score):
    bg = pygame.image.load('stage.png')

    pygame.mouse.set_visible(True)
    screen = pygame.display.set_mode((1280,729))
    text = Text_Menu(100,"Times New Roman", "Continue",  450,200 , 255, 255, 255)
    text_yes = Text_Menu(80,'Times New Roman','Yes', 470,300,255,255,255)
    text_no = Text_Menu(80,'Times New Roman','No',700,300,255,255,255)
    text_score = Text_Menu(80,'Times New Roman','Total Score :'+ str(score),450,100,255,255,255)
    screen.blit(bg,(0,0))


    while True:

        screen.blit(bg,(0,0))

        text_appear = Group(text,text_yes,text_no,text_score)
        text_appear.draw(screen)



        e = event.wait()
        if text_yes.rect.collidepoint(mouse.get_pos()):
            if e.type == MOUSEBUTTONDOWN:
                main()
        if text_no.rect.collidepoint(mouse.get_pos()):
            if e.type == MOUSEBUTTONDOWN:
                menu()
                break
        if e.type == QUIT:
            sys.exit()

        display.update()


# ------------------------------------------
# Main Menu
def menu():
    bg = pygame.image.load('stage.png')

    pygame.mouse.set_visible(True)
    screen = pygame.display.set_mode((1280,729))
    pygame.display.set_caption('Duck Hunt')
    text_start = Text_Menu(40,"Times New Roman", "Play",  100, 100, 255, 255, 255)
    text_exit = Text_Menu(40,"Times New Roman",'Quit', 100, 200, 255, 255, 255)
    screen.blit(bg,(0,0))


    while True:

        screen.blit(bg,(0,0))

        text_appear = Group(text_start,text_exit)
        text_appear.draw(screen)
        title = pygame.image.load('Duck-Hunt.png')
        screen.blit(title,(500, 300))

        e = event.wait()
        if text_start.rect.collidepoint(mouse.get_pos()):
            if e.type == MOUSEBUTTONDOWN:
                main()
        if text_exit.rect.collidepoint(mouse.get_pos()):
            if e.type == MOUSEBUTTONDOWN:
                sys.exit()
        if e.type == QUIT:
            pygame.quit
            break
        display.update()

menu()

# Special Thanks to Dumac, Pier, Georgius, and Excelino
# Sound from https://www.sounds-resource.com/nes/duckhunt/sound/4233/
