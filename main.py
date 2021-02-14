import pygame
import random
import const
import NeuralNetwork as neural
import json
from pygame.locals import *
from threading import Thread

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100
PIPE_WIDTH = 80
PIPE_HEIGHT = 700 

PIPE_GAP = 150

AMOUNT_HIDDEN = 3
AMOUNT_NEURON_INPUT = 4
AMOUNT_NEURON_HIDDEN = 6
AMOUNT_NEURON_OUTPUT = 1


class Game:

    def __init__(self):
        self.birds = []
        self.birdsCollision = []
        self.pipesList = []
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.age = 1

        self.BACKGROUND = pygame.image.load(const.BACKGROUND)
        self.BACKGROUND = pygame.transform.scale(self.BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.bird_group = pygame.sprite.Group()
        for n in range(0, 100):
            bird = Bird()
            self.birds.append(bird)
            self.bird_group.add(bird)
            loadWeights(bird)

        self.ground_group = pygame.sprite.Group()
        self.ceiling_group = pygame.sprite.Group()
        for i in range(2):
            ground = Ground(GROUND_WIDTH * i, SCREEN_HEIGHT - GROUND_HEIGHT)
            ceiling = Ground(GROUND_WIDTH * i, -(GROUND_HEIGHT-10))
            self.ground_group.add(ground)
            self.ceiling_group.add(ceiling)

        self.pipe_group = pygame.sprite.Group()

        pipes = get_random_pipes(600)
        self.pipe_group.add(pipes[0])
        self.pipe_group.add(pipes[1])

        listaPipe = [pipes[0], pipes[1]]
        self.pipesList.append(listaPipe)

        self.clock = pygame.time.Clock()

        pygame.font.init()
        self.fonte = pygame.font.get_default_font()
        self.fontesys=pygame.font.SysFont(self.fonte, 45)

    def newRound(self):
        self.age += 1
        self.pipe_group.empty()
        self.bird_group.empty()
        self.birds.clear()
        self.pipesList.clear()

        bird = getBestBird(self.birdsCollision)

        backupWeights = loadFromJson('weights.json')
        if bird.brain["score"] > backupWeights["score"]:
            saveWeights(bird)

        # Criar 100 novos passaros.
        self.bird_group = pygame.sprite.Group()
        for n in range(0, 40):
            bird = Bird()
            self.birds.append(bird)
            self.bird_group.add(bird)
            loadWeights(bird)
            neural.modifyWeights(bird.brain, random.randrange(3))

        self.ground_group = pygame.sprite.Group()
        self.ceiling_group = pygame.sprite.Group()
        for i in range(2):
            ground = Ground(GROUND_WIDTH * i, SCREEN_HEIGHT - GROUND_HEIGHT)
            ceiling = Ground(GROUND_WIDTH * i, -(GROUND_HEIGHT-10))
            self.ground_group.add(ground)
            self.ceiling_group.add(ceiling)

        self.pipe_group = pygame.sprite.Group()

        pipes = get_random_pipes(600)
        self.pipe_group.add(pipes[0])
        self.pipe_group.add(pipes[1])

        listaPipe = [pipes[0], pipes[1]]
        self.pipesList.append(listaPipe)

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load(const.BLUEBIRD_TOP).convert_alpha(),
                       pygame.image.load(const.BLUEBIRD_MID).convert_alpha(),
                       pygame.image.load(const.BLUEBIRD_BOT).convert_alpha()]

        self.speed = SPEED
        self.currentImage = 0
        self.image = pygame.image.load(const.BLUEBIRD_TOP).convert_alpha()

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = random.randrange(0, SCREEN_HEIGHT)

        self.brain = neural.createNeuralNetwork(AMOUNT_NEURON_INPUT, AMOUNT_HIDDEN, AMOUNT_NEURON_HIDDEN, AMOUNT_NEURON_OUTPUT)


    def update(self):
        self.currentImage = (self.currentImage + 1) % 3
        self.image = self.images[self.currentImage]

        self.speed += GRAVITY

        # Update height
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

    def getDistHorizontalPipe(self, game):
        return self.rect[0] - game.pipesList[0][0].rect[0]

    def getDistVerticalPipe(self, game):
        center = (game.pipesList[0][1].rect[1] + 700) + PIPE_GAP/2
        return self.rect[1] - center

    def getInputs(self, game):
        return [self.getDistHorizontalPipe(game), self.getDistVerticalPipe(game), GAME_SPEED, PIPE_GAP]


class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(const.CANO).convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED


class Ground(pygame.sprite.Sprite):

    def __init__(self, xPos, yPos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(const.BASE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xPos
        self.rect[1] = yPos

    def update(self):
        self.rect[0] -= GAME_SPEED


def is_off_screen(sprite):
    if sprite:
        return sprite.rect[0] < -(sprite.rect[2])
    return False


def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)


def getBestBird(birds):
    bestBird = birds[0]
    for bird in birds:
        if bestBird.brain["score"] < bird.brain["score"]:
            bestBird = bird

    return bestBird


def loadWeights(bird):
    bird.brain = loadFromJson('weights.json')


def saveWeights(bird):
    writeDictFromJson('weights.json', bird.brain)


def loadFromJson(file):
    with open(file, 'r') as archive:
        txt = archive.read()
        return json.loads(txt)


def writeDictFromJson(file, dict):
    with open(file, 'w') as arquivo:
        arquivo.write(json.dumps(dict, indent=2))


def notOnScreen(bird):
    return bird.rect[0] > SCREEN_WIDTH or bird.rect[0] < 0 or bird.rect[1] > SCREEN_HEIGHT or bird.rect[1] < 0


backupWeights = loadFromJson('weights.json')
game = Game()
while True:
    game.clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird = getBestBird(game.birds)
                saveWeights(bird)
                pygame.quit()
                quit()
                break

    # Executação Rede Neural
    for bird in game.birds:
        sensorList = bird.getInputs(game)

        neural.addInputs(bird.brain, sensorList)
        output = neural.getOutput(bird.brain)

        if output[0] == 0:
            bird.bump()

    game.screen.blit(game.BACKGROUND, (0, 0))

    if is_off_screen(game.ground_group.sprites()[0]):
        game.ground_group.remove(game.ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20, SCREEN_HEIGHT - GROUND_HEIGHT)
        game.ground_group.add(new_ground)

    if is_off_screen(game.ceiling_group.sprites()[0]):
        game.ceiling_group.remove(game.ceiling_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20, -(GROUND_HEIGHT - 10))
        game.ceiling_group.add(new_ground)

    # Criar novos Pipes quando melhor Bird passar por eles
    bird = getBestBird(game.birds)
    if bird.getDistHorizontalPipe(game) > 0:
        pipes = get_random_pipes(SCREEN_WIDTH + 100)
        game.pipe_group.add(pipes[0])
        game.pipe_group.add(pipes[1])

        game.pipesList.remove(game.pipesList[0])
        game.pipesList.append([pipes[0], pipes[1]])

    # Remover quando tiver fora da tela
    if is_off_screen(game.pipe_group.sprites()[0]):
        game.pipe_group.remove(game.pipe_group.sprites()[0])
        game.pipe_group.remove(game.pipe_group.sprites()[0])

    game.bird_group.update()
    game.ground_group.update()
    game.ceiling_group.update()
    game.pipe_group.update()

    game.bird_group.draw(game.screen)
    game.pipe_group.draw(game.screen)
    game.ceiling_group.draw(game.screen)
    game.ground_group.draw(game.screen)

    text = game.fontesys.render(f"Age: {game.age}, Score {bird.brain['score']}", 1, (0, 0, 0))
    game.screen.blit(text, (87,750))

    pygame.display.update()

    # Checa colisões remove do sprite.group e birds, adiciona em birdsCollision
    birdCollisionGround = pygame.sprite.groupcollide(game.bird_group, game.ground_group, True, False, pygame.sprite.collide_mask)
    if birdCollisionGround:
        birdsColl = birdCollisionGround.keys()
        for bird in birdsColl:
            game.birds.remove(bird)
            game.birdsCollision.append(bird)
    birdCollisionCeiling = pygame.sprite.groupcollide(game.bird_group, game.ceiling_group, True, False, pygame.sprite.collide_mask)
    if birdCollisionCeiling:
        birdsColl = birdCollisionCeiling.keys()
        for bird in birdsColl:
            game.birds.remove(bird)
            game.birdsCollision.append(bird)
    birdCollisionPipe = pygame.sprite.groupcollide(game.bird_group, game.pipe_group, True, False, pygame.sprite.collide_mask)
    if birdCollisionPipe:
        birdsColl = birdCollisionPipe.keys()
        for bird in birdsColl:
            game.birds.remove(bird)
            game.birdsCollision.append(bird)

    # Verifica se ainda tem passaros para começar novos
    if len(game.birds) == 0:
        game.newRound()
        continue
    else:
        if notOnScreen(bird):
            game.newRound()
            continue

    for bird in game.birds:
        bird.brain["score"] += 1