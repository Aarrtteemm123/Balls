from config import Config
from pygame.threads import Thread
import math, random


class PhysicsController(object):
    def __init__(self, numThreads, ballsList):
        self.numThreads = numThreads
        self.threadList = []
        self.ballsList = ballsList
        self.degreeX = 0
        self.degreeY = 0
        self.switch = False
        self.counter = 0
        self.flRun = True
        if len(self.ballsList) % self.numThreads != 0:
            self.groupSize = (len(self.ballsList) // self.numThreads) + 1
        else:
            self.groupSize = (len(self.ballsList) // self.numThreads)
        self.createThreads()

    def createThreads(self):
        self.threadList = [Thread(target=self.calculatePhysics, args=(i,)) for i in range(self.numThreads)]

    def startThreads(self):
        self.flRun = True
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
            friction = ball.mass * Config.Physics.GRAVITY * \
                   math.cos(abs(degree) * 180 / math.pi) * Config.Physics.FRICTION
            if speed == 0 and mg > friction:
                speed += direction * abs(mg - friction) / ball.mass
            else:
                speed += direction * abs(mg - friction) / ball.mass

        elif degree == 0:
            if speed > 0:
                speed -= Config.Physics.FRICTION * Config.Physics.GRAVITY
                if speed < 0: speed = 0
            if speed < 0:
                speed += Config.Physics.FRICTION * Config.Physics.GRAVITY
                if speed > 0: speed = 0

        if axis == 'X':
            if ball.x + ball.radius > Config.Win.AREA_WIDTH:
                speed *= -(1 - Config.Physics.COLLISION_ENERGY_LOSS)
            if ball.x < ball.radius:
                speed *= -(1 - Config.Physics.COLLISION_ENERGY_LOSS)
        elif axis == 'Y':
            if ball.y + ball.radius > Config.Win.AREA_HEIGHT:
                speed *= -(1 - Config.Physics.COLLISION_ENERGY_LOSS)
            if ball.y < ball.radius:
                speed *= -(1 - Config.Physics.COLLISION_ENERGY_LOSS)

        return speed

    def distance(self,ball1,ball2):
        return math.sqrt((ball1.x - ball2.x)**2 + (ball1.y - ball2.y)**2)

    def caclulateWallCollision(self,ball):
        if ball.x + ball.radius > Config.Win.AREA_WIDTH:
            ball.x = Config.Win.AREA_WIDTH - ball.radius

        if ball.x - ball.radius < 0:
            ball.x = ball.radius

        if ball.y + ball.radius > Config.Win.AREA_HEIGHT:
            ball.y = Config.Win.AREA_HEIGHT - ball.radius

        if ball.y - ball.radius < 0:
            ball.y = ball.radius


    def caclulateStaticCollision(self,ball1,ball2):
        overlap = ball1.radius + ball2.radius - self.distance(ball1, ball2)
        smallBall = ball1
        bigBall = ball2
        if smallBall.radius > bigBall.radius:
            self.caclulateStaticCollision(ball2,ball1)
        else:
            while overlap<0:
                theta = math.atan2((bigBall.y - smallBall.y), (bigBall.x - smallBall.x))
                smallBall.x -= overlap * math.cos(theta)
                smallBall.y -= overlap * math.sin(theta)

    def caclulateBallCollision(self):
            for i in range(len(self.ballsList)):
                for j in range(i,len(self.ballsList)):
                    ball1 = self.ballsList[i]
                    ball2 = self.ballsList[j]
                    if self.distance(ball1, ball2) < ball1.radius + ball2.radius:
                        phi = math.atan2((ball2.y - ball1.y), (ball2.x - ball1.x))
                        theta1 = ball1.angleBetweenSpeedXY()
                        theta2 = ball2.angleBetweenSpeedXY()
                        speed1 = ball1.speed()
                        speed2 = ball2.speed()

                        newSpeedX1 = (speed1 * math.cos(theta1 - phi) * (ball1.mass - ball2.mass) + 2 * ball2.mass * speed2 * math.cos(theta2 - phi)) / (
                                    ball1.mass + ball2.mass) * math.cos(phi) + speed1 * math.sin(theta1 - phi) * math.cos(phi + math.pi / 2)

                        newSpeedY1 = (speed1 * math.cos(theta1 - phi) * (ball1.mass - ball2.mass) + 2 * ball2.mass * speed2 * math.cos(theta2 - phi)) / (
                                    ball1.mass + ball2.mass) * math.sin(phi) + speed1 * math.sin(theta1 - phi) * math.sin(phi + math.pi / 2)

                        newSpeedX2 = (speed2 * math.cos(theta2 - phi) * (ball2.mass - ball1.mass) + 2 * ball1.mass * speed1 * math.cos(theta1 - phi)) / (
                                    ball1.mass + ball2.mass) * math.cos(phi) + speed2 * math.sin(theta2 - phi) * math.cos(phi + math.pi / 2)

                        newSpeedY2 = (speed2 * math.cos(theta2 - phi) * (ball2.mass - ball1.mass) + 2 * ball1.mass * speed1 * math.cos(theta1 - phi)) / (
                                    ball1.mass + ball2.mass) * math.sin(phi) + speed2 * math.sin(theta2 - phi) * math.sin(phi + math.pi / 2)

                        ball1.speedX = newSpeedX1
                        ball1.speedY = newSpeedY1
                        ball2.speedX = newSpeedX2
                        ball2.speedY = newSpeedY2

                        self.caclulateStaticCollision(ball1,ball2)

    def calculatePhysics(self, indexThread):
        for i in range(self.groupSize * indexThread,
                       self.groupSize * (indexThread + 1)):
            if i < len(self.ballsList):
                self.ballsList[i].speedX = self.caclulateSpeed(self.ballsList[i], self.degreeX, 'X')
                self.ballsList[i].speedY = self.caclulateSpeed(self.ballsList[i], self.degreeY, 'Y')

                if indexThread == 0:
                    self.caclulateBallCollision()
                    self.flRun = False

                while self.flRun: pass # wait other threads on first (indexThread = 0)

                self.caclulateWallCollision(self.ballsList[i])
                self.ballsList[i].x += self.ballsList[i].speedX * Config.Physics.DELTA_TIME
                self.ballsList[i].y += self.ballsList[i].speedY * Config.Physics.DELTA_TIME


    def autoControl(self):
        if self.switch:
            if self.counter == 0:
                degree = random.randint(-90, 90)
                self.counter = random.randint(0, 50)
                if random.randint(0, 1) == 0:
                    self.degreeX = degree
                else:
                    self.degreeY = degree
            else:
                self.counter -= 1


    def drawBalls(self, gameDisplay):
        for ball in self.ballsList: ball.drawBall(gameDisplay)
