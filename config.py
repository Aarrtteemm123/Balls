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
        WIN_COLOR = (0,0,0)
        AREA_ALPHA = 0.0

    class Physics(object):
        NUMBER_BALLS = 5
        MIN_RADIUS = 3
        MAX_RADIUS = 20
        GRAVITY = 9.8
        FRICTION = 0.05
        COLLISION_ENERGY_LOSS = 0.2
        DELTA_TIME = 0.01
        COLLISION = False

    class App(object):
        FPS_LIMIT = 60
        NUMBER_THREADS = 4
