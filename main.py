import pygame
from pygame.locals import *
import const

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
GRAVITY = 1
SPEED = 10
GAME_SPEED = 20

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

class Ground(pygame.sprite.Sprite):

    def __init__(self, width, height, xPos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(const.BASE)
        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()
        self.rect[0] = xPos
        self.rect[1] = SCREEN_HEIGHT - height

    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load(const.BACKGROUND)
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(2 * SCREEN_WIDTH, 100, 2* SCREEN_WIDTH *i)
    ground_group.add(ground)

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

        newGround = Ground(2 * SCREEN_WIDTH)
        ground_group.add(newGround)

    bird_group.update()
    ground_group.update()

    bird_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()