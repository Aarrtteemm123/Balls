import pygame

from config import Config
from physics import Gyroscope


class Interface(object):
    def __init__(self):
        self.window = pygame.display.set_mode((Config.Win.WIN_WIDTH, Config.Win.WIN_HEIGHT))
        pygame.display.set_caption(Config.Win.WIN_TITLE)
        self.gameDisplay = pygame.Surface((Config.Win.AREA_WIDTH, Config.Win.AREA_HEIGHT))
        self.DEFAULT_TEXT_COLOR = (0, 200, 200)
        self.font = pygame.font.Font('Michroma.ttf', 15)
        self.txtSimulation = self.font.render('                               Simulation', True,
                                              self.DEFAULT_TEXT_COLOR)
        self.txtFPS = self.font.render('FPS: 0', True, self.DEFAULT_TEXT_COLOR)
        self.txtFrameTime = self.font.render('Frame time: 0', True, self.DEFAULT_TEXT_COLOR)
        self.txtNumThreads = self.font.render('Threads: ' + str(Config.App.NUMBER_THREADS), True,
                                              self.DEFAULT_TEXT_COLOR)
        self.txtNumBalls = self.font.render('Balls: ' + str(Config.Physics.NUMBER_BALLS), True, self.DEFAULT_TEXT_COLOR)
        self.txtNumCollision = self.font.render('Collision/sec: 0', True,
                                                self.DEFAULT_TEXT_COLOR)
        self.txtControls = self.font.render('                               Controls', True, self.DEFAULT_TEXT_COLOR)
        self.txtStart = self.font.render('Start/Stop: space', True, self.DEFAULT_TEXT_COLOR)
        self.txtReset = self.font.render('Reset: R', True, self.DEFAULT_TEXT_COLOR)
        self.txtCollision = self.font.render('Enable/Disable Collision: Z', True, self.DEFAULT_TEXT_COLOR)
        self.txtAutoControl = self.font.render('Enable/Disable auto control: X', True, self.DEFAULT_TEXT_COLOR)
        self.txtD = self.font.render('Incline right: D', True, self.DEFAULT_TEXT_COLOR)
        self.txtA = self.font.render('Incline left: A', True, self.DEFAULT_TEXT_COLOR)
        self.txtW = self.font.render('Incline forward: W', True, self.DEFAULT_TEXT_COLOR)
        self.txtS = self.font.render('Incline back: S', True, self.DEFAULT_TEXT_COLOR)
        self.txtOrientation = self.font.render('                              Orientation', True,
                                               self.DEFAULT_TEXT_COLOR)
        self.txtDegreeX = self.font.render('Degree X: 0', True, self.DEFAULT_TEXT_COLOR)
        self.txtDegreeY = self.font.render('Degree Y: 0', True, self.DEFAULT_TEXT_COLOR)
        self.gyroscope = Gyroscope()

    def __updateText(self):
        self.txtList = [self.txtSimulation, self.txtFPS, self.txtFrameTime, self.txtNumThreads, self.txtNumBalls,
                        self.txtNumCollision, self.txtControls, self.txtStart, self.txtReset, self.txtCollision,
                        self.txtAutoControl, self.txtD, self.txtA, self.txtW,
                        self.txtS, self.txtOrientation, self.txtDegreeX, self.txtDegreeY]

    def updateGyroscope(self, degreeX, degreeY):
        self.gyroscope.calculateOrientation(degreeX, degreeY)

    def updateWindow(self):
        self.window.blit(self.gameDisplay, (Config.Win.AREA_X, Config.Win.AREA_Y))
        pygame.display.update()
        self.gameDisplay.fill(Config.Win.AREA_COLOR)
        self.window.fill(Config.Win.WIN_COLOR)

    def renderText(self):
        self.__updateText()
        locX = 30
        locY = 10
        lineHeight = 22
        for text in self.txtList:
            if text == self.txtControls or text == self.txtOrientation:
                locY += lineHeight
            self.window.blit(text, (locX, locY))
            locY += lineHeight

    def renderGyroscope(self):
        self.gyroscope.draw(self.window)
