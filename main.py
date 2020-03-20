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
    window = pygame.display.set_mode((Config.Win.WIN_WIDTH, Config.Win.WIN_HEIGHT))
    pygame.display.set_caption(Config.Win.WIN_TITLE)
    gameDisplay = pygame.Surface((Config.Win.AREA_WIDTH, Config.Win.AREA_HEIGHT))
    pc = PhysicsController(1,  createBalls(20))
    run = True
    pc.switch = True
    while run:
        start = time.perf_counter()
        pc.drawBalls(gameDisplay)
        pc.createThreads()
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
        finish = time.perf_counter() - start
        print(int(1/finish))
        #clock.tick(FPS)
