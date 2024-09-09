import pygame as pg
import random

import pygame.key

pg.init()

# initializing
screen = pg.display.set_mode((500, 500))
pg.display.set_caption("snake_game")
clock = pg.time.Clock()
FPS = 60


# Bait class
class Bait(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("coin.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, 400)
        self.rect.y = random.randint(50, 400)

    def update(self):
        screen.blit(self.image, self.rect)


class Player():
    def __init__(self, x, y):
        img = pg.image.load("block.jpg").convert_alpha()
        self.image = pg.transform.smoothscale(img, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.dx = self.direction
        self.dy = 0

    def update(self):

        pressed_key = pg.key.get_pressed()
        if pressed_key[pg.K_DOWN]:
            self.dx = 0 * self.direction
            self.dy = 1 * self.direction

        elif pressed_key[pg.K_LEFT]:
            self.dy = 0
            self.dx = -1 * self.direction

        elif pressed_key[pg.K_RIGHT]:
            self.dy = 0
            self.dx = self.direction

        elif pressed_key[pg.K_UP]:
            self.dy = -1 * self.direction
            self.dx = 0 * self.direction


        self.rect.x += self.dx
        self.rect.y += self.dy

        screen.blit(self.image, self.rect)


bait = Bait()
player = Player(50, 50)

run = True
while run:
    screen.fill("grey")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    bait.update()
    player.update()

    pg.display.update()
    clock.tick(FPS)

pg.quit()
