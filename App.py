import time
import pygame

from GUI import Interface
from ball import Ball
from config import Config
from physics import PhysicsController

class Application(object):
    def __init__(self):
        self.gui = Interface()
        self.DEFAULT_TEXT_COLOR = (0, 200, 200)
        self.pc = PhysicsController(10,  self.createBalls(Config.Physics.NUMBER_BALLS))
        self.run = True
        self.frameTime = 0
        self.counterInfoUpdate = 20

    def start(self):
        font = pygame.font.Font('Michroma.ttf', 15)
        self.pc = PhysicsController(15, self.createBalls(30))
        while self.run:
            startTime = time.perf_counter()
            self.pc.drawBalls(self.gui.gameDisplay)
            self.pc.createThreads()
            self.pc.startThreads()
            self.pc.autoControl()
            self.control()
            self.gui.updateGyroscope(self.pc.degreeX,self.pc.degreeY)
            self.gui.renderText()
            self.gui.renderGyroscope()
            self.gui.updateWindow()
            finishTime = time.perf_counter()
            self.frameTime = finishTime - startTime
            self.counterInfoUpdate-=1
            if self.counterInfoUpdate == 0:
                self.counterInfoUpdate = 20
                self.gui.txtFrameTime = font.render('Frame time: '+str(int(1000*self.frameTime)), True, self.DEFAULT_TEXT_COLOR)
                self.gui.txtFPS = font.render('FPS: '+str(int(1/self.frameTime)), True, self.DEFAULT_TEXT_COLOR)
                self.gui.txtNumThreads = font.render('Threads: ' + str(Config.App.NUMBER_THREADS), True,self.DEFAULT_TEXT_COLOR)
                self.gui.txtNumBalls = font.render('Balls: ' + str(Config.Physics.NUMBER_BALLS), True, self.DEFAULT_TEXT_COLOR)
                self.gui.txtNumCollision = font.render('Collision/frame: ' + str(self.pc.numCollision), True,self.DEFAULT_TEXT_COLOR)

    def control(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                    self.pc.degreeX -= 5
                elif e.key == pygame.K_d:
                    self.pc.degreeX += 5
                elif e.key == pygame.K_w:
                    self.pc.degreeY -= 5
                elif e.key == pygame.K_s:
                    self.pc.degreeY += 5
                elif e.key == pygame.K_s:
                    self.pc.degreeY += 5


    def createBalls(self,number):
        lst = []
        for i in range(number): lst.append(Ball())
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
