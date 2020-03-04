from config import Config
from pygame.threads import Thread
import math,random

class PhysicsController(object):
    def __init__(self, numProc, ballsList):
        self.numProc = numProc
        self.threadList = []
        self.ballsList = ballsList
        self.degreeX = 0
        self.degreeY = 0
        self.switch = False
        self.counter = 0
        if len(self.ballsList) % self.numProc != 0:
            self.groupSize = (len(self.ballsList) // self.numProc) + 1
        else:
            self.groupSize = (len(self.ballsList) // self.numProc)
        self.createThreads()

    def createThreads(self):
        self.threadList = [Thread(target=self.calculatePhysics, args=(i,)) for i in range(self.numProc)]

    def startThreads(self):
        for thread in self.threadList: thread.start()
        for thread in self.threadList: thread.join()

    def caclulateSpeed(self, ball, degree, axis):
        speed = 0
        if axis == 'X':
            speed = ball.speedX
        elif axis == 'Y':
            speed = ball.speedY
        else:
            return speed
        direction = 1
        if degree < 0: direction = -1
        if degree != 0:
            mg = ball.mass * Config.Physics.GRAVITY * \
                 math.sin(abs(degree) * 180 / math.pi)
            fric = ball.mass * Config.Physics.GRAVITY * \
                   math.cos(abs(degree) * 180 / math.pi) * Config.Physics.FRICTION
            if speed == 0 and mg > fric:
                speed += direction * abs(mg - fric) / ball.mass
            else:
                speed += direction * abs(mg - fric) / ball.mass

        elif degree == 0:
            if speed > 0:
                speed -= Config.Physics.FRICTION * Config.Physics.GRAVITY
                if speed < 0: speed = 0
            if speed < 0:
                speed += Config.Physics.FRICTION * Config.Physics.GRAVITY
                if speed > 0: speed = 0

        if axis == 'X':
            if ball.x + ball.radius > Config.Win.AREA_WIDTH:
                ball.x = Config.Win.AREA_WIDTH - ball.radius
                speed *= -(1 - Config.Physics.COLLISION_ENERGY_LOSS)
            if ball.x < ball.radius:
                ball.x = ball.radius
                speed *= -(1 - Config.Physics.COLLISION_ENERGY_LOSS)
        elif axis == 'Y':
            if ball.y + ball.radius > Config.Win.AREA_HEIGHT:
                ball.y = Config.Win.AREA_HEIGHT - ball.radius
                speed *= -(1 - Config.Physics.COLLISION_ENERGY_LOSS)
            if ball.y < ball.radius:
                ball.y = ball.radius
                speed *= -(1 - Config.Physics.COLLISION_ENERGY_LOSS)

        return speed

    def caclulateCollision(self):
        pass

    def calculatePhysics(self, indexThread):
        for i in range(self.groupSize * indexThread,
                       self.groupSize * (indexThread + 1)):
            if i < len(self.ballsList):
                self.ballsList[i].speedX = self.caclulateSpeed(self.ballsList[i], self.degreeX, 'X')
                self.ballsList[i].speedY = self.caclulateSpeed(self.ballsList[i], self.degreeY, 'Y')
                self.ballsList[i].x += self.ballsList[i].speedX / 100
                self.ballsList[i].y += self.ballsList[i].speedY / 100

    def autoControl(self):
        if self.switch:
            if self.counter == 0:
                degree = random.randint(-90,90)
                self.counter = random.randint(0,100)
                if random.randint(0, 1) == 0:
                    self.degreeX = degree
                else: self.degreeY = degree
            else: self.counter-=1

    def drawBalls(self, gameDisplay):
        for ball in self.ballsList: ball.drawBall(gameDisplay)
