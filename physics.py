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
        if len(self.ballsList) % self.numThreads != 0:
            self.groupSize = (len(self.ballsList) // self.numThreads) + 1
        else:
            self.groupSize = (len(self.ballsList) // self.numThreads)
        self.createThreads()

    def createThreads(self):
        self.threadList = [Thread(target=self.calculatePhysics, args=(i,)) for i in range(self.numThreads)]

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

    def getIndexCollision(self, ball):
        for otherBall in self.ballsList:
            if ball != otherBall and abs(ball.x - otherBall.x) < \
                    (ball.radius + otherBall.radius) and \
                    abs(ball.y - otherBall.y) < (ball.radius + otherBall.radius):
                phi = 0
                try:
                    phi = math.atan((otherBall.y - ball.y) / (otherBall.x - ball.x))
                except:
                    phi = math.atan2((otherBall.y - ball.y), (otherBall.x - ball.x))
                ball.x -= (ball.radius + otherBall.radius) * math.cos(phi) - abs(ball.x - otherBall.x)
                ball.y -= (ball.radius + otherBall.radius) * math.sin(phi) - abs(ball.y - otherBall.y)
                return self.ballsList.index(otherBall)
        return -1

    def caclulateCollision(self):
        lstCollision = []
        for ball in self.ballsList:
            indexCollisionBall = self.getIndexCollision(ball)
            if indexCollisionBall != -1:
                ball2 = self.ballsList[indexCollisionBall]
                tmpCollLst = [[self.ballsList.index(ball), indexCollisionBall],
                              [indexCollisionBall, self.ballsList.index(ball)]]

                if ball2.y - ball.y == 0 and tmpCollLst[0] not in lstCollision:
                    newSpeedX1 = (1 - Config.Physics.COLLISION_ENERGY_LOSS) * (
                                (ball.mass - ball2.mass) * ball.speedX + 2 * ball2.mass * ball2.speedX) / (
                                             ball.mass + ball2.mass)
                    ball2.speedX = (1 - Config.Physics.COLLISION_ENERGY_LOSS) * (
                                (ball2.mass - ball.mass) * ball2.speedX + 2 * ball.mass * ball.speedX) / (
                                               ball.mass + ball2.mass)
                    ball.speedX = newSpeedX1
                if ball2.x - ball.x == 0 and tmpCollLst[0] not in lstCollision:
                    newSpeedY1 = (1 - Config.Physics.COLLISION_ENERGY_LOSS) * (
                            (ball.mass - ball2.mass) * ball.speedY + 2 * ball2.mass * ball2.speedY) / (
                                         ball.mass + ball2.mass)
                    ball2.speedY = (1 - Config.Physics.COLLISION_ENERGY_LOSS) * (
                            (ball2.mass - ball.mass) * ball2.speedY + 2 * ball.mass * ball.speedY) / (
                                           ball.mass + ball2.mass)
                    ball.speedY = newSpeedY1
                else:
                    '''
                    phi = math.atan((ball2.y - ball.y)/(ball2.x - ball.x))
                    theta1 = math.atan(ball.speedY/ball.speedX)
                    theta2 = math.atan(ball2.speedY/ball2.speedX)
                    speedXY = math.sqrt(ball.speedX*ball.speedX+ball.speedY*ball.speedY)
                    speedXY2 = math.sqrt(ball2.speedX*ball2.speedX+ball2.speedY*ball2.speedY)
                    ball.speedX = (speedXY*math.cos(theta1-phi)*(ball.mass - ball2.mass)+2*ball2.mass*speedXY2*math.cos(theta2-phi))/(ball.mass + ball2.mass)*math.cos(phi)+speedXY*math.sin(theta1-phi)*math.cos(phi+math.pi/2)
                    ball.speedY = (speedXY*math.cos(theta1-phi)*(ball.mass - ball2.mass)+2*ball2.mass*speedXY2*math.cos(theta2-phi))/(ball.mass + ball2.mass)*math.sin(phi)+speedXY*math.sin(theta1-phi)*math.sin(phi+math.pi/2)
                    '''
                if tmpCollLst not in lstCollision:
                    lstCollision.extend(tmpCollLst)

    def calculatePhysics(self, indexThread):
        for i in range(self.groupSize * indexThread,
                       self.groupSize * (indexThread + 1)):
            if i < len(self.ballsList):
                self.ballsList[i].speedX = self.caclulateSpeed(self.ballsList[i], self.degreeX, 'X')
                self.ballsList[i].speedY = self.caclulateSpeed(self.ballsList[i], self.degreeY, 'Y')
                self.ballsList[i].x += self.ballsList[i].speedX / 100
                self.ballsList[i].y += self.ballsList[i].speedY / 100
        if indexThread == 0:
            self.caclulateCollision()
            for i in range(len(self.ballsList)):
                self.ballsList[i].x += self.ballsList[i].speedX / 100
                self.ballsList[i].y += self.ballsList[i].speedY / 100

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
