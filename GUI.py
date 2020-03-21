import pygame

from config import Config


class Interface(object):
    def __init__(self):
        self.DEFAULT_COLOR = (0, 200, 200)
        self.font = pygame.font.Font('Michroma.ttf', 15)
        self.txtSimulation = self.font.render('                               Simulation', True, self.DEFAULT_COLOR)
        self.txtFPS = self.font.render('FPS: 0', True, self.DEFAULT_COLOR)
        self.txtFrameTime = self.font.render('Frame time: 0', True, self.DEFAULT_COLOR)
        self.txtNumThreads = self.font.render('Threads: ' + str(Config.App.NUMBER_THREADS), True, self.DEFAULT_COLOR)
        self.txtNumBalls = self.font.render('Balls: ' + str(Config.Physics.NUMBER_BALLS), True, self.DEFAULT_COLOR)
        self.txtNumCollision = self.font.render('Collision/frame: ' + str(Config.App.NUMBER_THREADS), True,
                                                self.DEFAULT_COLOR)
        self.txtControls = self.font.render('                               Controls', True, self.DEFAULT_COLOR)
        self.txtStart = self.font.render('Start/Stop: space', True, self.DEFAULT_COLOR)
        self.txtReset = self.font.render('Reset: R', True, self.DEFAULT_COLOR)
        self.txtCollision = self.font.render('Enable/Disable Collision: Z', True, self.DEFAULT_COLOR)
        self.txtAutoControl = self.font.render('Enable/Disable auto control: X', True, self.DEFAULT_COLOR)
        self.txtD = self.font.render('Incline right: D', True, self.DEFAULT_COLOR)
        self.txtA = self.font.render('Incline left: A', True, self.DEFAULT_COLOR)
        self.txtW = self.font.render('Incline forward: W', True, self.DEFAULT_COLOR)
        self.txtS = self.font.render('Incline back: S', True, self.DEFAULT_COLOR)
        self.txtOrientation = self.font.render('                              Orientation', True, self.DEFAULT_COLOR)

    def update(self):
        self.txtList = [self.txtSimulation, self.txtFPS, self.txtFrameTime, self.txtNumThreads, self.txtNumBalls,
                        self.txtNumCollision, self.txtControls, self.txtStart, self.txtReset, self.txtCollision,
                        self.txtAutoControl, self.txtD, self.txtA, self.txtW,
                        self.txtS, self.txtOrientation]

    def renderText(self, x, y, lineHeight, window):
        locY = y
        for text in self.txtList:
            if text == self.txtControls or text == self.txtOrientation:
                locY += lineHeight
            window.blit(text, (x, locY))
            locY += lineHeight
