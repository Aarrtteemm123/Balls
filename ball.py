import random

import pygame, math
from pygame import gfxdraw
from config import Config


class Ball(object):
    def __init__(self,config):
        self.config = config
        self.radius = 10
        self.x = 0
        self.y = 0
        self.speedX = 0
        self.speedY = 0
        self.mass = 1
        self.red = 0
        self.green = 0
        self.blue = 0

    def setRandomParameters(self):
        self.radius = random.randint(self.config.physics.MIN_RADIUS, self.config.physics.MAX_RADIUS)
        self.x = random.randint(self.radius, self.config.win.AREA_WIDTH - self.radius)
        self.y = random.randint(self.radius, self.config.win.AREA_HEIGHT - self.radius)
        self.speedX = 0
        self.speedY = 0
        self.mass = 4 / 3 * math.pi * self.radius ** 3
        self.red = random.randrange(0, 255)
        self.green = random.randrange(0, 255)
        self.blue = random.randrange(0, 255)

    def speed(self):
        return math.sqrt(self.speedX ** 2 + self.speedY ** 2)

    def angleBetweenSpeedXY(self):
        return math.atan2(self.speedY, self.speedX)

    def drawBall(self, surface):
        pygame.gfxdraw.filled_circle(surface, int(self.x), int(self.y),
                                     self.radius, (self.red, self.green, self.blue))
