import pickle
from tkinter import *
from config import Config


class GUIConfig(object):

    def __init__(self):
        self.root = Tk()
        self.root.title("Config")
        self.root.geometry('285x300+1050+200')
        self.butSetDefault = Button(self.root, bg='#c2c1c3', width=15, height=2, text='Set Default',
                                    command=self.butSetDefaultLogic)
        self.butSetDefault.place(x=10, y=250)
        self.butApply = Button(self.root, bg='#c2c1c3', width=15, height=2, text='Apply',
                               command=self.update)
        self.butApply.place(x=160, y=250)
        self.configNameValues = ['Balls', 'Min radius', 'Max radius', 'Gravity'
            , 'Friction', 'Collision energy loss']

        self.config = Config()
        self.entries = {}
        for i in range(len(self.configNameValues)):
            l = Label(self.root, font='Arial 10 bold',
                      text=self.configNameValues[i],
                      fg='Black')
            l.place(x=10, y=10 + i * 40)
            entry = Entry(self.root, width=15)
            entry.place(x=170, y=10 + i * 40)
            self.entries[self.configNameValues[i]] = entry

    def checkClose(self):
        config = self.loadConfig()
        if config.app.CLOSE_PROGRAM:
            self.root.destroy()
        self.root.after(10, self.checkClose)

    def isDigit(self, string):
        if string.isdigit():
            return True
        else:
            try:
                float(string)
                return True
            except ValueError:
                return False

    def toDigit(self, string):
        if string.isdigit():
            return int(string)
        else:
            try:
                return float(string)
            except ValueError:
                return None

    def validator(self):
        defaultConfig = Config()
        string = self.entries.get(self.configNameValues[0]).get()
        if string.isdigit() and self.toDigit(string) > 0:
            self.config.physics.NUMBER_BALLS = int(string)
        else:
            self.config.physics.NUMBER_BALLS = defaultConfig.physics.NUMBER_BALLS
        string = self.entries.get(self.configNameValues[1]).get()
        if string.isdigit() and self.toDigit(string) > 0 and self.toDigit(string) < self.config.physics.MAX_RADIUS:
            self.config.physics.MIN_RADIUS = int(string)
        else:
            self.config.physics.MIN_RADIUS = defaultConfig.physics.MIN_RADIUS
        string = self.entries.get(self.configNameValues[2]).get()
        if string.isdigit() and self.toDigit(string) > 0 and self.toDigit(string) > self.config.physics.MIN_RADIUS:
            self.config.physics.MAX_RADIUS = int(string)
        else:
            self.config.physics.MAX_RADIUS = defaultConfig.physics.MAX_RADIUS
        string = self.entries.get(self.configNameValues[3]).get()
        if string.isdigit() and self.toDigit(string) > 0:
            self.config.physics.MIN_RADIUS = float(string)
        else:
            self.config.physics.GRAVITY = defaultConfig.physics.GRAVITY
        string = self.entries.get(self.configNameValues[4]).get()
        if self.isDigit(string) and self.toDigit(string) >= 0:
            self.config.physics.FRICTION = float(string)
        else:
            self.config.physics.FRICTION = defaultConfig.physics.FRICTION
        string = self.entries.get(self.configNameValues[5]).get()
        if self.isDigit(string) and self.toDigit(string) >= 0 and self.toDigit(string) <= 1:
            self.config.physics.COLLISION_ENERGY_LOSS = float(string)
        else:
            self.config.physics.COLLISION_ENERGY_LOSS = defaultConfig.physics.COLLISION_ENERGY_LOSS

    def saveConfig(self, config):
        with open('Config', 'wb') as f:
            pickle.dump(config, f)

    def loadConfig(self):
        with open('Config', 'rb') as f:
            return pickle.load(f)

    def update(self):
        self.validator()
        self.saveConfig(self.config)
        self.showData()

    def showData(self):
        for i in range(len(self.entries)):
            self.entries.get(self.configNameValues[i]).delete(0, END)
        self.config = self.loadConfig()
        self.entries.get(self.configNameValues[0]).insert(0, self.config.physics.NUMBER_BALLS)
        self.entries.get(self.configNameValues[1]).insert(0, self.config.physics.MIN_RADIUS)
        self.entries.get(self.configNameValues[2]).insert(0, self.config.physics.MAX_RADIUS)
        self.entries.get(self.configNameValues[3]).insert(0, self.config.physics.GRAVITY)
        self.entries.get(self.configNameValues[4]).insert(0, self.config.physics.FRICTION)
        self.entries.get(self.configNameValues[5]).insert(0, self.config.physics.COLLISION_ENERGY_LOSS)

    def butSetDefaultLogic(self):
        self.config = Config()
        self.saveConfig(self.config)
        self.showData()

    def appRun(self):
        self.showData()
        self.update()
        self.checkClose()
        self.root.mainloop()


GUIConfig().appRun()
