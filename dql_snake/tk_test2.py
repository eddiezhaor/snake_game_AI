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
        self.n_actions = len(self.action_l)
        self.canvas = Canvas(self.master,width = self.width, height = self.height)
        self.x = 1
        self.y = 0
        self.z = None
        self.canvas.pack()
        self.initGame()
        num =100
        self.margin = 10
        self.point = self.canvas.create_oval(num,num, num+10, num+10,fill='black') 
        self.z = self.canvas.create_rectangle(10,10, 20, 20,width=1, fill = 'black')
        # self.h = self.canvas.create_rectangle(10,20,20, 30,width=1, fill = 'black')
        # self.move_oval()
        self.l = [self.z]
        # self.canvas.after(1,self.timer) 

    def initGame(self):
        margin = 10
        self.canvas.create_line(margin, margin, margin, self.height-10,fill='blue')
        self.canvas.create_line(margin, margin, self.height-10,margin, fill='blue')
        self.canvas.create_line(self.height-10, margin, self.height-10,self.height-10, fill='blue')
        self.canvas.create_line(margin, self.height-10, self.height-10,self.height-10, fill='blue')
        
        # num = np.random.randint(1,self.height-11,size=1)[0]
        # self.point = self.canvas.create_oval(num,num, num+10, num+10,fill='black')
        
         
    def go(self,action):
        s = self.canvas.coords(self.z)
        b_action = np.array([0,0])
        distance = 10
        if action == 0: #up
            if s[1] >=10 :
                b_action[1] -= distance
        elif action == 1: #down
            if s[1] <= self.height - 20:
                b_action[1] += distance
        elif action == 2: #left
            if s[0] >= 10:
                b_action[0] -= distance
        elif action == 3: #right
            if s[0] <= self.width-20:
                b_action[0] += distance
        # self.canvas.move(self.z, b_action[0], b_action[1])
        self.x = b_action[0]
        self.y = b_action[1]
        x1,x2,y1,y2 = self.canvas.coords(self.point)
        reward = self.check_collsion()
        end = False
        s_ = self.canvas.coords(self.z)
        s_x1, s_x2, s_y1, s_y2 = s_ 
        # print(s_)
        
        a1,b1,a2,b2 = self.canvas.coords(self.l[-1])
        m1,n1,m2,n2 = self.canvas.coords(self.l[0])
        if self.canvas.coords(self.point) == self.canvas.coords(self.l[-1]) :
            self.create_body()
            self.canvas.delete(self.point)
            num = np.random.randint(1,(self.height-20)/10,size=1)[0]*10
            self.point = self.canvas.create_oval(num,num, num+10, num+10,fill='black')
            reward = 2
            relative_coords = [1,1,1,1,2,2,2,2]
            end = False
        # if len(self.canvas.find_overlapping(x1,x2,y1,y2)) !=1:
        #     reward = 2
        #     relative_coords = [1,1,1,1]
        #     end = True
        # else:
        #     reward = -0.1
        #     end = False
        if s_[1] < self.margin or s_[1] > self.height-20 or s_[0] < self.margin or s_[0] > self.width-20:
            reward = -1
            end = False
            self.reset()
        relative_coords = [x1-s_x1,x2-s_x2, y1-s_y1,y2-s_y2,x1-m1,x2-n1,y1-m2,y2-n2]
        # self.master.after(100,self.go)
        return relative_coords, reward, end


    def move_oval(self):
        i = 0
        while i < len(self.l)-1:
            c1 = self.canvas.coords(self.l[i])
            c2 = self.canvas.coords(self.l[i+1])
            self.canvas.move(self.l[i],c2[0]-c1[0],c2[1] - c1[1])
            i+=1
        self.canvas.move(self.l[-1],self.x,self.y)
        # self.canvas.after(1,self.move_oval)

    def check_collsion(self):
        if len(self.l)>1:
            a1, a2, a3, a4 = self.canvas.coords(self.l[-2])
            x1, x2, x3, x4 = self.canvas.coords(self.l[-1])
            # print(self.canvas.coords(self.l[-2]),self.canvas.coords(self.l[-1]),self.x,self.y)
            if [x1+self.x, x2+self.y, x3+self.x, x4+self.y]!=[a1,a2,a3,a4]:
                self.move_oval()
        else:
            self.move_oval()
        x1, x2, x3, x4 = self.canvas.coords(self.l[-1])
        t = [x1, x2, x3, x4]
        overlapping = self.canvas.find_overlapping(x1,x2,x3,x4)
        reward = -0.1
        end=False
        for item in overlapping:
            if item in self.l[::-1][3:]:
                if t ==self.canvas.coords(item):
                    self.reset() 
                    # x1,x2,y1,y2 = self.canvas.coords(self.point)
                    # s_ = self.canvas.coords(self.z)
                    # relative_coords = [x1-s_x1,x2-s_x2, y1-s_y1,y2-s_y2,xx1-s_x1,x2-s_x2, y1-s_y1,y2-s_y2]
                    reward = -1
        return  reward
        
         
         

    # def move_left(self,event):
    #     # self.canvas.focus_set()
        
    #     self.x = -10
    #     self.y = 0
    #     self.check_collsion(event)
    #     # self.move_oval()

    # def move_right(self,event):
    #     # self.canvas.focus_set()
        
    #     self.x = 10
    #     self.y = 0
    #     self.check_collsion(event)
    #     # self.move_oval()
    #     # self.move_oval()

    # def move_up(self,event):
        
    #     # self.canvas.focus_set()
    #     self.x = 0
    #     self.y = -10
    #     self.check_collsion(event)
    #     # self.move_oval()
    #     # self.move_oval()

    # def move_down(self,event):
        
    #     # self.canvas.focus_set()
    #     self.x = 0
    #     self.y = 10
    #     self.check_collsion(event)
    #     # self.move_oval()
    #     # self.move_oval()
    def create_body(self):
        x1,y1,x2,y2 = self.canvas.coords(self.point)
        new_body = self.canvas.create_rectangle(x1,y1,x2,y2,width=1, fill='black')
        self.l.insert(0,new_body)
    # def create_point(self):
    #     x1,x2,y1,y2 = self.canvas.coords(self.point)
    #     a1,b1,a2,b2 = self.canvas.coords(self.l[-1])
    #     if self.canvas.coords(self.point) == self.canvas.coords(self.l[-1]) :
    #         self.create_body()
    #         self.canvas.delete(self.point)
    #         num = np.random.randint(1,self.height/10,size=1)[0]*10
    #         self.point = self.canvas.create_oval(num,num, num+10, num+10,fill='black')

    # def timer(self):
    #     if True:
    #         self.create_point()
    #         # self.create_point()
    #         self.canvas.after(100,self.timer) 
    
    def reset(self):
        self.canvas.delete('all')
        self.initGame()
        self.z = self.canvas.create_rectangle(10,10, 20, 20, fill = 'black')
        self.l = [self.z]
        self.canvas.delete(self.point)
        # num = np.random.randint(1,self.height-11,size=1)[0]
        # num = 100
        # self.point = self.canvas.create_oval(num,num, num+10, num+10,fill='black')
        num = np.random.randint(1,(self.height-20)/10,size=1)[0]*10
        self.point = self.canvas.create_oval(num,num, num+10, num+10,fill='black')

# if __name__ == "__main__": 
#     p = snake(400,400)
#     p.master.bind('<KeyPress-Left>',p.move_left)
#     p.master.bind('<KeyPress-Right>',p.move_right)
#     p.master.bind('<KeyPress-Up>',p.move_up)
#     p.master.bind('<KeyPress-Down>',p.move_down)
#     mainloop() 