import os
import pickle


class Config(object):
    def __init__(self):
        self.win = self.Win()
        self.physics = self.Physics()
        self.app = self.App()

    class Win(object):
        def __init__(self):
            self.WIN_WIDTH = 950
            self.WIN_HEIGHT = 600
            self.WIN_TITLE = "Balls"
            self.AREA_WIDTH = 600
            self.AREA_HEIGHT = 600
            self.AREA_X = 350
            self.AREA_Y = 0
            self.AREA_COLOR = (255, 255, 255)
            self.WIN_COLOR = (0, 0, 0)
            self.AREA_ALPHA = 0.0

    class Physics(object):
        def __init__(self):
            self.NUMBER_BALLS = 30
            self.MIN_RADIUS = 3
            self.MAX_RADIUS = 20
            self.GRAVITY = 9.8
            self.FRICTION = 0.1
            self.COLLISION_ENERGY_LOSS = 0.25
            self.DELTA_TIME = 0.001
            self.COLLISION = False

    class App(object):
        def __init__(self):
            self.NUMBER_THREADS = os.cpu_count() * 2