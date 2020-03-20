class Config(object):

    class Win(object):
        WIN_WIDTH = 800
        WIN_HEIGHT = 500
        WIN_TITLE = "Balls"
        AREA_WIDTH = 600
        AREA_HEIGHT = 500
        AREA_X = 200
        AREA_Y = 0
        AREA_COLOR = (255, 255, 255)
        AREA_ALPHA = 0.0

    class Physics(object):
        NUMBER_BALLS = 50
        MIN_MASS = 9
        MAX_MASS = 10
        RADIUS = 15
        GRAVITY = 9.8
        FRICTION = 0.0
        COLLISION_ENERGY_LOSS = 0.0
        DELTA_TIME = 0.001
        COLLISION = False

    class App(object):
        FPS_LIMIT = 60
        NUMBER_THREADS = 4
