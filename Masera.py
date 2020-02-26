import random
import threading
import time
import matplotlib; matplotlib.use("TkAgg")
from matplotlib.patches import Circle

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from itertools import combinations
import numpy as np
import logging
logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

class Agent(threading.Thread):
    def __init__(self,id,type,prodTime,initBudget,initFood,initFoodPrice,riskFactor,nbrRadius,x, y, vx, vy, radius):
        super().__init__()
        logging.debug("Initilizing Agent #%s", id)
        self.day = 0
        self.type = type
        self.id = id
        self.prodTime = prodTime
        self.money = initBudget
        self.food = initFood
        self.foodPrice = initFoodPrice
        self.risk = riskFactor
        self.nbrRadius = nbrRadius
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.r = np.array((x, y))
        self.v = np.array((vx, vy))
        self.radius = radius
        self.wait = False
        self.currentDay=0
        self.maxDays=0
        #edge color ,'edgecolor': types[(type+1)%len(types)]
        self.style={'linewidth': 2, 'facecolor': AGENTDATA.get(type)[2]}

    def run(self):
        logging.debug("Starting Agent %s",self.id)
        while self.day<self.maxDays:
            self.runDay()
            while self.wait:
                time.sleep(1)
        logging.debug("Ending Agent %s",self.id)
    def runDay(self):
        lenght = random.random() * 5
        time.sleep(lenght)
        logging.debug("Agent %s slept for %s", self.id, lenght)
        self.day+=1
        self.wait=True

    def clone(self):
        return Agent(self.id,self.type,self.prodTime,self.money,self.food,self.foodPrice,self.risk,self.nbrRadius,self.x,self.y,self.vx,self.vy,self.radius)
    def overlaps(self, other):
        return np.hypot(*(self.r - other.r)) < self.radius + other.radius

    def draw(self):
        return Circle((self.x,self.y), radius=self.radius,**self.style,label=self.type)

    def advance(self, dt):
        self.x += self.vx*dt
        self.y += self.vy*dt

        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx
        if self.x + self.radius > 1:
            self.x = 1-self.radius
            self.vx = -self.vx
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy
        if self.y + self.radius > 1:
            self.y = 1-self.radius
            self.vy = -self.vy
        self.r[0],self.r[1] = self.x, self.y
        self.v[0],self.v[1] = self.vx, self.vy


class MASERA:
    """
   •	 number of agents of each type
   •	 production times (per each agent type)
   •  	 initial budget (equally distributed)
   •	 initial free’ food (equally distributed)
   •	 food price at start
   •	 risk factor (range of random values)
   •	 neighborhood radius
   •	 size of the 2D Environment.
    """

    def __init__(self,days,initBudget,initFood,initFoodPrice,riskFactor,nbrRadius,enviromentSize):
        self.agents = []
        self.maxDays=days
        id = 0
        self.enviromentSize=np.array((enviromentSize[0],enviromentSize[1]))
        radius=min(enviromentSize)/50
        for key in AGENTDATA:
            for numAgents in range(AGENTDATA.get(key)[0]):
                x, y = radius + (self.enviromentSize-(2*radius)) * np.random.random(2)  # x,y in bounds
                #vx, vy = 1 * (np.random.random(2) - .5)
                vx, vy = 0, 0
                id += 1
                prodTime=AGENTDATA.get(key)[1]
                agent=Agent(id, key,prodTime,initBudget,initFood,initFoodPrice,random.uniform(riskFactor[0],riskFactor[1]),nbrRadius,x, y, vx, vy,radius)
                agent.setName(key+":"+str(id))
                self.agents.append(agent)
        self.initSimulation()
        self.anim = animation.FuncAnimation(self.fig, self.runDay, frames=days,interval=5000, blit=True,repeat=False)

        self.save()
    def initSimulation(self):
        print("Initializing Simulation")
        print(self.agents)
        self.fig, self.ax = plt.subplots()
        for s in ['top', 'bottom', 'left', 'right']:
            self.ax.spines[s].set_linewidth(2)
        self.ax.set_aspect('equal', 'box')
        self.ax.set_xlim(0, self.enviromentSize[0])
        self.ax.set_ylim(0, self.enviromentSize[1])
        self.ax.xaxis.set_ticks([])
        self.ax.yaxis.set_ticks([])
        self.circles = []
        for agent in self.agents:
            agent.maxDays=self.maxDays
            agent.start()
            circle=agent.draw()
            self.ax.add_patch(circle)
            self.circles.append(circle)
        return self.circles
    def runDay(self,i):
        print("Day:",i)
        for i, p in enumerate(self.agents):
            p.wait=False
            self.circles[i].center = (p.x,p.y)
        return self.circles
    def save(self,save=False):
        if save:
            Writer = animation.writers['imagemagick']
            writer = Writer(fps=100, bitrate=1800)
            self.anim.save('Masera.gif', writer=writer)
        else:
            plt.show()

def main():
    global AGENTDATA
    AGENTDATA={"Farmer": (2, 1, "seagreen"), "Miller": (1, 2, "orange")}
    sim = MASERA(10,1000,5,1,(0.0,0.5),100,(10,10))
if __name__ == '__main__':
    main()