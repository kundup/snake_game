import pygame
from random import randint

pygame.init()

screen = pygame.display.set_mode((400,400))
color = (randint(0,255),randint(0,255),randint(0,255))


class Block:
    def __init__(self, x, y):
        self.block = pygame.Surface((15, 15))
        self.block.fill(color)
        self.block_rect = self.block.get_rect(midbottom =(x, y))

    def draw_block(self):
        screen.blit(self.block, self.block_rect)

blockland = Block (50, 50)

def run():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        blockland.draw_block()

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    run()

