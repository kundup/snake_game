import pygame as pg
import random

# pygame initializing
pg.init()

# constants
width = 500
height = 500
FPS = 60
SIZE = 15
color = (0, 0, 0)
bg_color = (100,150,250)

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


def acceleration(score, acceleration_speed):
    if score > acceleration_speed * 2:
        player.direction += 1
        acceleration_speed = score
    return acceleration_speed


class Bait:
    def __init__(self):
        self.img = pg.image.load("coin.png")
        self.rect = self.img.get_rect()
        self.rect.x = random.randint(15, 485)
        self.rect.y = random.randint(15, 485)

    def update(self):
        screen.blit(self.img, self.rect)


class Player:
    def __init__(self, x, y, vel):
        img = pg.image.load("block.jpg").convert_alpha()
        self.image = pg.transform.smoothscale(img, (SIZE, SIZE))
        self.direction = vel
        self.dx = self.direction
        self.dy = 0
        self.list = [(x, y)]  # at first only one block

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


            for block in self.list:
                screen.blit(self.image, block)


        return game_over


player = Player(50, 50, 2)
bait = Bait()

run = True
while run:
    screen.fill(bg_color)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    game_over = player.update(game_over)
    acceleration_speed = acceleration(score, acceleration_speed)
    bait.update()

    # snake grows and scores
    if player.collision():
        score += 1
        player.grow()

    if game_over:
        all_text("Game Over", color, 250, 250, 50)

    all_text(f"Points:{score}", color, 40, 20, 25)

    pg.display.update()
    clock.tick(FPS)

pg.quit()
