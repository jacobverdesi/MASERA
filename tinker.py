import numpy as np
import matplotlib; matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib import animation
from itertools import combinations
class Agent:
    def __init__(self, x, y, vx, vy,id,type, radius):

        self.x,self.y,self.vx,self.vy=x,y,vx,vy
        self.r = np.array((x, y))
        self.v = np.array((vx, vy))
        self.radius = radius
        self.type = type
        self.id= id
        #edge color ,'edgecolor': types[(type+1)%len(types)]
        self.style={'linewidth': 2, 'facecolor': types.get(type)}

    def overlaps(self, other):
        return np.hypot(*(self.r - other.r)) < self.radius + other.radius

    def draw(self, ax):
        circle = Circle((self.x,self.y), radius=self.radius,**self.style,label=self.type)
        ax.add_patch(circle)
        return circle

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
class Simulation:
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
    def __init__(self,agentData):
        self.agents=[]
        for key in agentData:
            for numAgents in agentData.get(key)[0]:

                self.agents.append(key)

    def handle_collisions(self):
        def change_velocities(p1, p2):
            m1, m2 = p1.radius**2, p2.radius**2
            M = m1 + m2
            r1, r2 = p1.r,p2.r
            d = np.linalg.norm(r1 - r2)**2
            v1, v2 = p1.v,p2.v
            u1 = v1 - 2*m2 / M * np.dot(v1-v2, r1-r2) / d * (r1 - r2)
            u2 = v2 - 2*m1 / M * np.dot(v2-v1, r2-r1) / d * (r2 - r1)
            p1.vx,p1.vy = u1[0],u1[1]
            p2.vx,p2.vy = u2[0],u2[1]
        pairs = combinations(range(len(self.agents)), 2)
        for i,j in pairs:
            if self.agents[i].overlaps(self.agents[j]):
                change_velocities(self.agents[i], self.agents[j])

    def init(self):
        self.circles = []
        for agent in self.agents:
            self.circles.append(agent.draw(self.ax))
        return self.circles

    def animate(self, i):
        for i, p in enumerate(self.agents):
            p.advance(.01)
            self.circles[i].center = (p.x,p.y)
        #self.handle_collisions()
        return self.circles

    def do_animation(self, save=False):
        fig, self.ax = plt.subplots()
        for s in ['top','bottom','left','right']:
            self.ax.spines[s].set_linewidth(2)
        self.ax.set_aspect('equal', 'box')
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.xaxis.set_ticks([])
        self.ax.yaxis.set_ticks([])
        anim = animation.FuncAnimation(fig, self.animate, init_func=self.init,
                               frames=800, interval=2, blit=True)

        if save:
            Writer = animation.writers['imagemagick']
            writer = Writer(fps=100, bitrate=1800)
            anim.save('collision.gif', writer=writer)
        else:
            plt.show()

def genAgents(radius):
    global colors,types

    #types={"Farmer": "seagreen","Miller": "orange", "Baker":"tomato","Seller":"cornflowerblue"}

    agents=[]
    id=0
    for type in types:
        x, y = radius + (1 - 2 * radius) * np.random.random(2)  # x,y in bounds
        vx,vy=1*(np.random.random(2)-.5)
        vx,vy=0,0
        agent = Agent(x, y, vx, vy,id, type, radius)
        agents.append(agent)
        id+=1
            # id+=1
            # notoverlap=True
            # while notoverlap:
            #     x, y = radius + (1 - 2 * radius) * np.random.random(2)  # x
            #     agent = Agent(x, y, vx, vy, id, type, radius)
            #     notoverlap=False
            #     for p2 in agents:
            #         if p2.overlaps(agent):
            #             notoverlap=True
            #     if not notoverlap:
            #         agents.append(agent)

    return agents

if __name__ == '__main__':
    radius=.02
    sim = Simulation({"Farmer": (1,1,"seagreen"),"Miller": (1,2,"orange")})
    #sim.do_animation(save=False)