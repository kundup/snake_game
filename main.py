import sys

import pygame as pg
import random
from blocks import *

# pygame initializing
pg.init()

# constants
width = 500
height = 500
FPS = 60
SIZE = 15
color = (0, 0, 0)
bg_color = (100,150,250)
color_hurdle = (randint(0,255),randint(0,255),randint(0,255))
hurdles = []
is_paused = False

#images
res_img = pg.image.load("restart_btn.png").convert_alpha()
rec_img = pg.Surface((SIZE, SIZE)).convert()
bait_img = pg.image.load("coin.png").convert_alpha()
ghost_img = pg.image.load("ghost.png").convert_alpha()
# definitions
screen = pg.display.set_mode((width, height))
pg.display.set_caption("snake_game")
clock = pg.time.Clock()

# variables
game_over = False
score = 0
acceleration_speed = 2

def all_text(text, color, x, y, size):
    font_surf = pg.font.Font("Pixeltype.ttf", size)
    font_render = font_surf.render(text, False, color)
    font_rect = font_render.get_rect(midbottom=(x, y))
    screen.blit(font_render, font_rect)

def pause_game():
    global is_paused
    is_paused = True
    while is_paused:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    is_paused = False

            if event.type == pg.QUIT:
                sys.exit()
                pg.quit()


def acceleration(score, acceleration_speed):
    if score > acceleration_speed * 2:
        player.direction += 1
        acceleration_speed = score
        new_hurdle = Hurdle()
        hurdles.append(new_hurdle)

    return acceleration_speed

class Restart:
    def __init__(self):
        self.image = pg.transform.smoothscale(res_img, (90,40))
        self.rect = self.image.get_rect()
        self.rect.x = 210
        self.rect.y = 270

    def update(self):
        global game_over, score, acceleration_speed
        pos = pg.mouse.get_pos()
        if self.rect.collidepoint(pos) and pg.mouse.get_pressed()[0]:
            player.reset(50, 50, 2)
            game_over = 0
            score = 0
            acceleration_speed = 2

        screen.blit(self.image, self.rect)

class Hurdle:
    def __init__(self):
        self.img = rec_img
        self.img.fill(color_hurdle)
        self.rect = self.img.get_rect()
        self.rect.x =randint(40, 480)
        self.rect.y = randint(40, 480)

    def update(self):
        screen.blit(self.img, self.rect)



class Bait:
    def __init__(self):
        self.img = bait_img
        self.rect = self.img.get_rect()
        self.rect.x = random.randint(15, 485)
        self.rect.y = random.randint(15, 485)

    def update(self):
        screen.blit(self.img, self.rect)


class Player:
    def __init__(self):
        self.reset(50 ,50, 2)
        self.ghost_rect = None
        self.ghost_image = ghost_img


    def grow(self):
        # new block place the last position of block
        last_x, last_y = self.list[-1]
        new_block = (last_x , last_y )  # new block starts the position
        self.list.append(new_block)

    def collision(self):
        # eat the bait by mounth
        head_rect = pg.Rect(self.list[0][0], self.list[0][1], SIZE, SIZE)
        if head_rect.colliderect(bait.rect):
            bait.rect.x = random.randint(15, 485)
            bait.rect.y = random.randint(15, 485)

            return True
        return False

    def collision_over(self):
        head_rect = pg.Rect(self.list[0][0], self.list[0][1], SIZE, SIZE)
        for i in hurdles:
            if head_rect.colliderect(i.rect):
                return True
        return False

    def update(self, game_over):
        if not game_over:
            pressed_key = pg.key.get_pressed()
            if pressed_key[pg.K_DOWN]:
                self.dx = 0
                self.dy = self.direction
            elif pressed_key[pg.K_LEFT]:
                self.dy = 0
                self.dx = -self.direction
            elif pressed_key[pg.K_RIGHT]:
                self.dy = 0
                self.dx = self.direction
            elif pressed_key[pg.K_UP]:
                self.dy = -self.direction
                self.dx = 0

            # updating the body
            if len(self.list) > 1:
                for i in range(len(self.list) - 1, 0, -1):
                    self.list[i] = self.list[i - 1]  # former position

            # update head of snake
            head_x, head_y = self.list[0]
            new_head_x = head_x + self.dx
            new_head_y = head_y + self.dy
            self.list[0] = (new_head_x, new_head_y)

            if self.list[0][0] <= 0 or self.list[0][0] >= width - SIZE or self.list[0][1] <= 0 or self.list[0][1] >= height - SIZE:
                game_over = 1



        else:
            if not self.ghost_rect:
                self.list = []
                self.image = pg.transform.smoothscale(self.ghost_image, (SIZE * 1.5, SIZE * 1.5))
                self.ghost_rect = self.image.get_rect()
                self.ghost_rect.x = 200
                self.ghost_rect.y = 180
                self.list.append(self.ghost_rect)

            self.ghost_rect.y -= 1
            if self.ghost_rect.y < 0:
                self.ghost_rect = None

        for block in self.list:
            screen.blit(self.image, block)

        return game_over

    def reset(self, x, y, vel):
        self.image = blockland.block
        self.direction = vel
        self.dx = self.direction
        self.dy = 0
        self.list = [(x, y)]  # at first only one block
        self.ghost_rect = None

player = Player()
bait = Bait()
restart = Restart()


run = True
while run:
    screen.fill(bg_color)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.KEYDOWN and not game_over:
            if event.key == pg.K_SPACE:
                pause_game()


    game_over = player.update(game_over)
    acceleration_speed = acceleration(score, acceleration_speed)
    bait.update()

    # snake grows and scores
    if player.collision():
        score += 1
        player.grow()

    for hurd in hurdles:
        hurd.update()

    if player.collision_over():
        game_over = 1

    if game_over:
        all_text("Game Over", color, 250, 250, 50)
        hurdles = []
        restart.update()



    all_text(f"Points:{score}", color, 40, 20, 25)

    pg.display.update()
    clock.tick(FPS)

pg.quit()
