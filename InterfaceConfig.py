import pickle
from tkinter import *
from config import Config


class GUIConfig(object):

    def __init__(self):
        self.root = Tk()
        self.root.title("Config")
        self.root.geometry('285x300+600+200')
        self.butSetDefault = Button(self.root, bg='#c2c1c3', width=30, height=2, text='Set Default',
                                    command=self.butSetDefaultLogic)
        self.butSetDefault.place(x=35, y=250)
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

    def validator(self):
        pass

    def update(self):
        self.config.physics.NUMBER_BALLS = int(self.entries.get(self.configNameValues[0]).get())
        self.config.physics.MIN_RADIUS = int(self.entries.get(self.configNameValues[1]).get())
        self.config.physics.MAX_RADIUS = int(self.entries.get(self.configNameValues[2]).get())
        self.config.physics.GRAVITY = float(self.entries.get(self.configNameValues[3]).get())
        self.config.physics.FRICTION = float(self.entries.get(self.configNameValues[4]).get())
        self.config.physics.COLLISION_ENERGY_LOSS = float(self.entries.get(self.configNameValues[5]).get())
        with open('Config', 'wb') as f:
            pickle.dump(self.config, f)
        self.root.after(100, self.update)

    def showData(self):
        with open('Config', 'rb') as f:
            self.config = pickle.load(f)
        self.entries.get(self.configNameValues[0]).insert(0, self.config.physics.NUMBER_BALLS)
        self.entries.get(self.configNameValues[1]).insert(0, self.config.physics.MIN_RADIUS)
        self.entries.get(self.configNameValues[2]).insert(0, self.config.physics.MAX_RADIUS)
        self.entries.get(self.configNameValues[3]).insert(0, self.config.physics.GRAVITY)
        self.entries.get(self.configNameValues[4]).insert(0, self.config.physics.FRICTION)
        self.entries.get(self.configNameValues[5]).insert(0, self.config.physics.COLLISION_ENERGY_LOSS)

    def butSetDefaultLogic(self):
        self.config = Config()
        with open('Config', 'wb') as f:
            pickle.dump(self.config, f)
        for i in range(len(self.entries)):
            self.entries.get(self.configNameValues[i]).delete(0, END)
        self.showData()

    def appRun(self):
        self.showData()
        self.update()
        self.root.mainloop()


GUIConfig().appRun()
