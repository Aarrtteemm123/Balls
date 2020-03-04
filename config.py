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
        AREA_ALPHA = 0

    class Physics(object):
        NUMBER_BALLS = 50
        MIN_MASS = 1
        MAX_MASS = 10
        MIN_RADIUS = 5
        MAX_RADIUS = 20
        GRAVITY = 9.8
        FRICTION = 0.2
        COLLISION_ENERGY_LOSS = 0.2
        COLLISION = False
