import pickle
import time
import pygame
from GUI import Interface
from ball import Ball
from physics import PhysicsController


class Application(object):
    def __init__(self):
        self.config = self.loadConfig()
        self.gui = Interface(self.config)
        self.DEFAULT_TEXT_COLOR = (0, 200, 200)
        self.pc = PhysicsController(self.config, self.createBalls(self.config.physics.NUMBER_BALLS))
        self.run = True
        self.stop = False
        self.frameTime = 0
        self.timeCounter = 0
        self.counterInfoUpdate = 20

    def loadConfig(self):
        with open('Config', 'rb') as f:
            return pickle.load(f)

    def start(self):
        font = pygame.font.Font('Michroma.ttf', 15)
        self.pc = PhysicsController(self.config, self.createBalls(self.config.physics.NUMBER_BALLS))
        while self.run:
            startTime = time.perf_counter()
            self.pc.drawBalls(self.gui.gameDisplay)
            if not self.stop:
                self.pc.createThreads()
                self.pc.startThreads()
                self.pc.autoControl()
            self.control()
            self.gui.updateGyroscope(self.pc.degreeX, self.pc.degreeY)
            self.gui.renderText()
            self.gui.renderGyroscope()
            self.gui.updateWindow()
            finishTime = time.perf_counter()
            self.frameTime = finishTime - startTime
            self.timeCounter += self.frameTime
            if self.timeCounter > 1:
                self.gui.txtNumCollision = font.render(
                    'Collision/sec:  ' + str(int(self.pc.numCollision / self.timeCounter)), True,
                    self.DEFAULT_TEXT_COLOR)
                self.pc.numCollision = 0
                self.timeCounter = 0
            self.pc.deltaTime = self.config.physics.DELTA_TIME * self.frameTime * 500
            self.counterInfoUpdate -= 1
            self.gui.txtDegreeX = font.render('Degree X:  ' + str(round(self.pc.degreeX, 2)), True,
                                              self.DEFAULT_TEXT_COLOR)
            self.gui.txtDegreeY = font.render('Degree Y:  ' + str(round(self.pc.degreeY, 2)), True,
                                              self.DEFAULT_TEXT_COLOR)
            if self.counterInfoUpdate == 0:
                self.counterInfoUpdate = 20
                self.gui.txtFrameTime = font.render('Frame time:  ' + str(int(1000 * self.frameTime)), True,
                                                    self.DEFAULT_TEXT_COLOR)
                self.gui.txtFPS = font.render('FPS:  ' + str(int(1 / self.frameTime)), True, self.DEFAULT_TEXT_COLOR)
                self.gui.txtNumThreads = font.render('Threads:  ' + str(self.config.app.NUMBER_THREADS), True,
                                                     self.DEFAULT_TEXT_COLOR)
                self.gui.txtNumBalls = font.render('Balls:  ' + str(self.config.physics.NUMBER_BALLS), True,
                                                   self.DEFAULT_TEXT_COLOR)
                self.gui.txtAvgSpeed = font.render('Avg speed:  ' + str(round(self.pc.getAvgSpeed(), 2)), True,
                                                   self.DEFAULT_TEXT_COLOR)

    def control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.pc.degreeX -= self.frameTime * 100
            if self.pc.degreeX < -90: self.pc.degreeX = -90
        if keys[pygame.K_d]:
            self.pc.degreeX += self.frameTime * 100
            if self.pc.degreeX > 90: self.pc.degreeX = 90
        if keys[pygame.K_w]:
            self.pc.degreeY -= self.frameTime * 100
            if self.pc.degreeY < -90: self.pc.degreeY = -90
        if keys[pygame.K_s]:
            self.pc.degreeY += self.frameTime * 100
            if self.pc.degreeY > 90: self.pc.degreeY = 90
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    self.stop = not self.stop
                elif e.key == pygame.K_r:
                    self.config = self.loadConfig()
                    self.pc = PhysicsController(self.config,self.createBalls(self.config.physics.NUMBER_BALLS))
                elif e.key == pygame.K_z:
                    self.config.physics.COLLISION = not self.config.physics.COLLISION
                elif e.key == pygame.K_x:
                    self.pc.flAutoControl = not self.pc.flAutoControl

    def createBalls(self, number):
        lst = []
        for i in range(number): lst.append(Ball(self.config))
        for ball in lst:
            numberCollision = 1
            while numberCollision != 0:
                numberCollision = 0
                ball.setRandomParameters()
                for otherBall in lst:
                    if ball != otherBall and abs(ball.x - otherBall.x) < \
                            (ball.radius + otherBall.radius) and \
                            abs(ball.y - otherBall.y) < (ball.radius + otherBall.radius):
                        numberCollision += 1
        return lst
