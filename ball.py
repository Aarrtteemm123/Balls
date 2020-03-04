import random

import pygame
from pygame import gfxdraw
from config import Config


class Ball(object):
    def __init__(self):
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
        self.radius = random.randint(Config.Physics.MIN_RADIUS, Config.Physics.MAX_RADIUS)
        self.x = random.randint(self.radius, Config.Win.AREA_WIDTH-self.radius)
        self.y = random.randint(self.radius, Config.Win.AREA_HEIGHT-self.radius)
        self.speedX = 0
        self.speedY = 0
        self.mass = random.randrange(Config.Physics.MIN_MASS, Config.Physics.MAX_MASS)
        self.red = random.randrange(0, 255)
        self.green = random.randrange(0, 255)
        self.blue = random.randrange(0, 255)

    def drawBall(self, surface):
        pygame.gfxdraw.filled_circle(surface, int(self.x), int(self.y),
                              self.radius, (self.red, self.green, self.blue))
