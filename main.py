import time
import pygame
from ball import Ball
from config import Config
from physics import PhysicsController


def createBalls(number):
    lst = []
    for i in range(number): lst.append(Ball())
    for ball in lst:
        numberCollision = 1
        while numberCollision!=0:
            numberCollision = 0
            ball.setRandomParameters()
            for otherBall in lst:
                if ball != otherBall and abs(ball.x - otherBall.x) < \
                        (ball.radius + otherBall.radius) and \
                        abs(ball.y - otherBall.y) < (ball.radius + otherBall.radius):
                    numberCollision+=1
    return lst

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    FPS = 60
    window = pygame.display.set_mode((Config.Win.WIN_WIDTH, Config.Win.WIN_HEIGHT))
    pygame.display.set_caption(Config.Win.WIN_TITLE)
    gameDisplay = pygame.Surface((Config.Win.AREA_WIDTH, Config.Win.AREA_HEIGHT))
    ball1 = Ball()
    ball1.setRandomParameters()
    ball1.x = 200
    ball1.y = 100
    ball1.speedX = 0
    ball1.speedY = 100
    ball1.radius = 20
    ball1.mass = 10

    ball2 = Ball()
    ball2.setRandomParameters()
    ball2.x = 200
    ball2.y = 250
    ball2.speedX = 0
    ball2.speedY = -10
    ball2.radius = 20
    ball2.mass = 10
    pc = PhysicsController(4, [ball1,ball2])
    run = True
    pc.switch = True
    while run:
        pc.drawBalls(gameDisplay)
        pc.createThreads()
        start = time.clock()
        pc.startThreads()
        #pc.autoControl()
       # print(start - time.clock())
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_a:
                        pc.degreeX-=5
                        print("X: "+str(pc.degreeX))
                elif e.key == pygame.K_d:
                        pc.degreeX+=5
                        print("X: "+str(pc.degreeX))
                elif e.key == pygame.K_w:
                    pc.degreeY -= 5
                    print("Y: " + str(pc.degreeY))
                elif e.key == pygame.K_s:
                    pc.degreeY += 5
                    print("Y: " + str(pc.degreeY))
        window.blit(gameDisplay, (Config.Win.AREA_X, Config.Win.AREA_Y))
        pygame.display.update()
        gameDisplay.fill(Config.Win.AREA_COLOR)
        clock.tick(FPS)
