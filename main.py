import pygame
import random
from pygame.locals import *
import const

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
GRAVITY = 1
SPEED = 10
GAME_SPEED = 20

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 120
PIPE_HEIGHT = 500

PIPE_GAT = 200

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load(const.BLUEBIRD_MID).convert_alpha(),
                      pygame.image.load(const.BLUEBIRD_TOP).convert_alpha(),
                      pygame.image.load(const.BLUEBIRD_BOT).convert_alpha()]

        self.current_image = 0
        self.image = self.images[self.current_image]

        self.speed = GRAVITY

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2



    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY
        self.rect[1] += self.speed


    def bump(self):
        self.speed = -self.speed

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xPos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(const.CANO).convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xPos

        if inverted:
            self.imagem = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED




class Ground(pygame.sprite.Sprite):

    def __init__(self, xPos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(const.BASE)
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xPos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xPos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xPos, size)
    pipe_inverted = Pipe(True, xPos,SCREEN_HEIGHT - size - PIPE_GAT)
    return(pipe, pipe_inverted)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load(const.BACKGROUND)
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i * 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()

    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        newGround = Ground(GROUND_WIDTH - 20)
        ground_group.add(newGround)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDTH * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
         pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask)):
        input()
        break

