import os


class Config(object):
    class Win(object):
        WIN_WIDTH = 950
        WIN_HEIGHT = 600
        WIN_TITLE = "Balls"
        AREA_WIDTH = 600
        AREA_HEIGHT = 600
        AREA_X = 350
        AREA_Y = 0
        AREA_COLOR = (255, 255, 255)
        WIN_COLOR = (0, 0, 0)
        AREA_ALPHA = 0.0

    class Physics(object):
        NUMBER_BALLS = 1
        MIN_RADIUS = 3
        MAX_RADIUS = 20
        GRAVITY = 9.8
        FRICTION = 0.1
        COLLISION_ENERGY_LOSS = 0.25
        DELTA_TIME = 0.001
        COLLISION = False

    class App(object):
        NUMBER_THREADS = os.cpu_count() * 2
