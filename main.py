import pygame as pg
import random

pg.init()

# initializing
width = 500
height = 500
screen = pg.display.set_mode((width, height))
pg.display.set_caption("snake_game")
clock = pg.time.Clock()
FPS = 60
game_over = False
score = 0
black = (0, 0, 0)
accelaration_speed = 2


def all_text(text, color, x, y, size):
    font_surf = pg.font.Font("Pixeltype.ttf", size)
    font_render = font_surf.render(text, False, color)
    font_rect = font_render.get_rect(midbottom=(x, y))
    screen.blit(font_render, font_rect)

def accelaration(score, accelaration_speed):
    if score > accelaration_speed * 2:
        player.direction += 0.5
        accelaration_speed = score
    return accelaration_speed

# Bait class
class Bait(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load("coin.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, 200)
        self.rect.y = random.randint(50, 200)
        self.score = 0

    def update(self):
        if self.rect.colliderect(player.rect):
            self.score += 1
            self.rect.x = random.randint(10, 480)
            self.rect.y = random.randint(10, 480)

        screen.blit(self.image, self.rect)
        return self.score


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, vel):
        super().__init__()
        img = pg.image.load("block.jpg").convert_alpha()
        self.image = pg.transform.smoothscale(img, (15, 15))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = vel
        self.dx = self.direction
        self.dy = 0

    def update(self, game_over):

        if not game_over:

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

            if self.rect.y <= 0 or self.rect.bottom >= height or self.rect.x <= 0 or self.rect.right >= width:
                game_over: bool = True

        screen.blit(self.image, self.rect)
        return game_over


bait = Bait()
player = Player(50, 50, 1)

run = True
while run:
    screen.fill("grey")
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    game_over = player.update(game_over)
    score = bait.update()
    accelaration_speed = accelaration(score, accelaration_speed)

    if game_over:
        all_text("Game Over", black, 250, 250, 50)

    all_text(f"Points:{score}", black, 40, 20, 25)
    pg.display.update()
    clock.tick(FPS)

pg.quit()

# collision (done)
# boundary (done)
# score addition (done)
# opening and game_over screen
# acceleration
# enlarging size
# high score saving
