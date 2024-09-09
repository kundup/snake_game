import pygame as pg
import random

pg.init()

# initializing
screen = pg.display.set_mode((500, 500))
pg.display.set_caption("snake_game")
clock = pg.time.Clock()
FPS = 60

# Bait class
class Bait():
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("coin.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, 400)
        self.rect.y = random.randint(50, 400)

    def update(self):
        screen.blit(self.image, self.rect)


bait = Bait()

run = True
while run:
    screen.fill("grey")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    bait.update()

    pg.display.update()
    clock.tick(FPS)

pg.quit()
