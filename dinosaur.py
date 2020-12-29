import pygame
from pygame.locals import *
from itertools import cycle
import random

SCREENWIDTH = 822
SCREENHEIGHT = 260
FPS = 30


def mainGame():
    score = 0
    over = False
    global SCREEN, FPSCLOCK
    pygame.init()

    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('jumps dinosaur')

    bg1 = MyMap(0, 0)
    bg2 = MyMap(800, 0)
    dinosaur = Dinosaur()
    addObstacleTimer = 0
    obstacleList = []

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                if dinosaur.rect.y >= dinosaur.lowest_y:
                    dinosaur.jump()
                    dinosaur.jump_audio.play()
                if over:
                    mainGame()

        if not over:
            bg1.map_update()
            bg1.map_rolling()
            bg2.map_update()
            bg2.map_rolling()
            dinosaur.move()
            dinosaur.draw_dinosaur()

            if addObstacleTimer >= 1300:
                r = random.randint(0, 100)
                if r > 40:
                    obstacle = Obstacle()
                    obstacleList.append(obstacle)
                addObstacleTimer = 0
            for i in range(len(obstacleList)):
                obstacleList[i].obstacle_move()
                obstacleList[i].draw_obstacle()
                if pygame.sprite.collide_rect(dinosaur, obstacleList[i]):
                    over = True
                    game_over()
                elif (obstacleList[i].rect.x + obstacleList[i].rect.width) < dinosaur.rect.x:
                    score += obstacleList[i].getScore()
                obstacleList[i].showScore(score)

        addObstacleTimer += 20
        pygame.display.update()
        FPSCLOCK.tick(FPS)


class MyMap():
    def __init__(self, x, y):
        self.bg = pygame.image.load("image/bg.png").convert_alpha()
        self.x = x
        self.y = y

    def map_rolling(self):
        if self.x < -790:
            self.x = 800
        else:
            self.x -= 5

    def map_update(self):
        SCREEN.blit(self.bg, (self.x, self.y))


class Dinosaur():
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.jumpState = False
        self.jumpHeight = 130

        self.lowest_y = 140
        self.jumpValue = 0
        self.dinosaurIndex = 0
        self.dinosaurIndexGen = cycle([0, 1, 2])

        self.dinosaur_img = (
            pygame.image.load("image/dinosaur1.png").convert_alpha(),
            pygame.image.load("image/dinosaur2.png").convert_alpha(),
            pygame.image.load("image/dinosaur3.png").convert_alpha(),
        )

        self.jump_audio = pygame.mixer.Sound('audio/jump.wav')
        self.rect.size = self.dinosaur_img[0].get_size()
        self.x = 50
        self.y = self.lowest_y
        self.rect.topleft = (self.x, self.y)

    def jump(self):
        self.jumpState = True

    def move(self):
        if self.jumpState:
            if self.rect.y >= self.lowest_y:
                self.jumpValue = -5
            if self.rect.y <= self.lowest_y - self.jumpHeight:
                self.jumpValue = 5
            self.rect.y += self.jumpValue
            if self.rect.y >= self.lowest_y:
                self.jumpState = False

    def draw_dinosaur(self):
        dinosaurIndex = next(self.dinosaurIndexGen)
        SCREEN.blit(self.dinosaur_img[dinosaurIndex],
                    (self.x, self.rect.y))


class Obstacle():
    score = 1

    def __init__(self):
        self.rect = pygame.Rect(0, 0, 0, 0, )
        self.stone = pygame.image.load("image/stone.png").convert_alpha()
        self.cacti = pygame.image.load("image/cacti.png").convert_alpha()
        # self.numbers = (pygame.image.load("image/{}.png".format(i for i in range(0, 10))).convert_alpha(),)
        self.numbers = (pygame.image.load("image/0.png").convert_alpha(),
                        pygame.image.load("image/1.png").convert_alpha(),
                        pygame.image.load("image/2.png").convert_alpha(),
                        pygame.image.load("image/3.png").convert_alpha(),
                        pygame.image.load("image/4.png").convert_alpha(),
                        pygame.image.load("image/5.png").convert_alpha(),
                        pygame.image.load("image/6.png").convert_alpha(),
                        pygame.image.load("image/7.png").convert_alpha(),
                        pygame.image.load("image/8.png").convert_alpha(),
                        pygame.image.load("image/9.png").convert_alpha(),
                        )
        self.score_audio = pygame.mixer.Sound("audio/score.wav")
        r = random.randint(0, 1)
        if r == 0:
            self.image = self.stone
        else:
            self.image = self.cacti
        self.rect.size = self.image.get_size()
        self.width, self.height = self.rect.size
        self.x = 800
        self.y = 200 - (self.height / 2)
        self.rect.center = (self.x, self.y)

    def obstacle_move(self):
        self.rect.x -= 5

    def draw_obstacle(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

    def getScore(self):
        tmp = self.score
        if tmp == 1:
            self.score_audio.play()
        self.score = 0
        return tmp

    def showScore(self, score):
        self.scoreDigists = [int(x) for x in list(str(score))]
        totalWidth = 0
        for digit in self.scoreDigists:
            totalWidth += self.numbers[digit].get_width()
        Xoffset = (SCREENWIDTH - totalWidth) / 2
        for digit in self.scoreDigists:
            SCREEN.blit(self.numbers[digit], (Xoffset, SCREENHEIGHT * 0.1))
            Xoffset += self.numbers[digit].get_width()


def game_over():
    bump_audio = pygame.mixer.Sound("audio/bump.wav")
    bump_audio.play()
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h
    over_img = pygame.image.load("image/gameover.png").convert_alpha()
    SCREEN.blit(over_img, ((screen_w - over_img.get_width()) / 2, (screen_h - over_img.get_height()) / 2))


if __name__ == '__main__':
    mainGame()
