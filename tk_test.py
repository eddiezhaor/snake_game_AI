from tkinter import *
import time
import numpy as np
import pandas as pd
class snake:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.master = Tk()
        self.action_l = ['u', 'd', 'l', 'r']
        self.canvas = Canvas(self.master,width = self.width, height = self.height)
        self.x = 1
        self.y = 0
        self.z = None
        self.canvas.pack()
        self.initGame()
        # self.move_oval()
        # self.canvas.after(1,self.timer) 

    def initGame(self):
        margin = 10
        self.canvas.create_line(margin, margin, margin, self.height-10,fill='blue')
        self.canvas.create_line(margin, margin, self.height-10,margin, fill='blue')
        self.canvas.create_line(self.height-10, margin, self.height-10,self.height-10, fill='blue')
        self.canvas.create_line(margin, self.height-10, self.height-10,self.height-10, fill='blue')
        self.z = self.canvas.create_rectangle(10,10, 20, 20, fill = 'black')
        # num = np.random.randint(1,self.height-11,size=1)[0]
        # self.point = self.canvas.create_oval(num,num, num+10, num+10,fill='black')
        num =100
        self.point = self.canvas.create_oval(num,num, num+10, num+10,fill='black')  
    def go(self,action):
        s = self.canvas.coords(self.self.point)
        b_action = np.array([0,0])
        distance = 10
        if action == 0: #up
            if s[1] >10 :
                b_action[1] -= distance
        elif aciton == 1: #down
            if s[1] < self.height - 10:
                b_action[1] += distance
        elif aciton == 2: #left
            if s[0] > 10:
                b_action[0] -= 1
        elif action == 3: #right
            if s[3] < self.width-10:
                b_action[0] += distance
        self.canvas.move(self.z,b_action[0], b_action[1])
        s_ = self.canvas.coords()

    # def move_oval(self):
    #     self.canvas.move(self.z,self.x,self.y)
    #     # self.canvas.after(1,self.move_oval)
        
    # def move_left(self,event):
    #     # self.canvas.focus_set()
    #     self.x = -1
    #     self.y = 0
    #     self.move_oval()
    #     # self.move_oval()

    # def move_right(self,event):
    #     # self.canvas.focus_set()
    #     self.x = 1
    #     self.y = 0
    #     self.move_oval()
    #     # self.move_oval()

    # def move_up(self,event):
    #     # self.canvas.focus_set()
    #     self.x = 0
    #     self.y = -1
    #     self.move_oval()
    #     # self.move_oval()

    # def move_down(self,event):
    #     # self.canvas.focus_set()
    #     self.x = 0
    #     self.y = 1
    #     self.move_oval()
    #     # self.move_oval()

    def create_point(self):
        x1,x2,y1,y2 = self.canvas.coords(self.point)
        if len(self.canvas.find_overlapping(x1,x2,y1,y2)) !=1 :
            self.canvas.delete(self.point)
            num = np.random.randint(1,self.height-11,size=1)[0]
            self.point = self.canvas.create_oval(num,num, num+10, num+10,fill='black')

    # def timer(self):
    #     if True:
    #         self.create_point()
    #         # self.create_point()
    #         self.canvas.after(100,self.timer) 
    
    def reset(self):
        self.canvas.delete(self.z)
        self.z = self.canvas.create_rectangle(10,10, 20, 20, fill = 'black')
        self.canvas.delete(self.point)
        num = np.random.randint(1,self.height-11,size=1)[0]
        self.point = self.canvas.create_oval(num,num, num+10, num+10,fill='black')


if __name__ == "__main__": 
    p = snake(400,400)
    # p.master.bind('<KeyPress-Left>',p.move_left)
    # p.master.bind('<KeyPress-Right>',p.move_right)
    # p.master.bind('<KeyPress-Up>',p.move_up)
    # p.master.bind('<KeyPress-Down>',p.move_down)
    mainloop() 