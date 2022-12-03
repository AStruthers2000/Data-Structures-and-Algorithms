# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 16:43:24 2022

@author: Andrew Struthers
@honor-code: I pledge that I have neither given nor received help from anyone 
             other than the instructor or the TAs for all program components 
             included here.
"""

from timeit import default_timer as timer
import matplotlib.pyplot as plt
import numpy

class Rectangle:
    def __init__(self, xl, xh, yl, yh):
        self.xl = xl
        self.yl = yl
        self.xh = xh
        self.yh = yh
    
    def GetXBounds(self):
        return [self.xl, self.xh]
    
    def GetYBounds(self):
        return [self.yl, self.yh]
    
    def IsPointInRect(self, point):
        inXMin = numpy.all(point[0] > self.xl)
        inXMax = numpy.all(point[0] < self.xh)
        inYMin = numpy.all(point[1] > self.yl)
        inYMax = numpy.all(point[1] < self.yh)
        return inXMin and inXMax and inYMin and inYMax
        
        #if point[0] > self.GetXBounds()[0] and point[0] < self.GetXBounds()[1]:
        #    if point[1] > self.GetYBounds()[0] and point[1] < self.GetYBounds()[1]:
        #        return True
        #return False
    
    def OutsideXMin(self, x):
        return x <= self.xl
    
    def OutsideXMax(self, x):
        return x >= self.xh
    
    def OutsideYMin(self, y):
        return y <= self.yl
    
    def OutsideYMax(self, y):
        return y >= self.yh
        

def random_walk_2D(np, ns, rect, plot_step):
    particle_step = 0.01
    
    xpos = numpy.random.uniform(rect.GetXBounds()[0] + particle_step, rect.GetXBounds()[1]/2.0, np)
    ypos = numpy.random.uniform(rect.GetYBounds()[0] + particle_step, rect.GetXBounds()[1], np)
    
    moves = numpy.random.randint(1, 4+1, size = ns*np)
    moves.shape = (ns, np)
    
    plt.figure(1)
    
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    
    for step in range(ns):
        try:
            this_move = moves[step]
        except:
            print("This only happens because we are iterating from [0, ns+1] and we don't care about the ns+1 index, so we throw an error and quit")
            continue

        ypos += numpy.where(this_move == NORTH, particle_step, 0)
        ypos -= numpy.where(this_move == SOUTH, particle_step, 0)
        xpos += numpy.where(this_move == EAST,  particle_step, 0)
        xpos -= numpy.where(this_move == WEST,  particle_step, 0)
        
        ypos -= numpy.where(rect.OutsideYMax(ypos), particle_step, 0)
        ypos += numpy.where(rect.OutsideYMin(ypos), particle_step, 0)
        xpos -= numpy.where(rect.OutsideXMax(xpos), particle_step, 0)
        xpos += numpy.where(rect.OutsideXMin(xpos), particle_step, 0)
        
        
        valid_points = numpy.where(rect.IsPointInRect([xpos, ypos]), 1, 0)
        assert numpy.all(valid_points==1)
        
        if (step + 1) % plot_step == 0 or step == 0:            
            plt.scatter(xpos, ypos, s = 5)
            
            plt.ylim(rect.GetYBounds()[0] - 0.1, rect.GetYBounds()[1] + 0.1)
            plt.xlim(rect.GetXBounds()[0] - 0.1, rect.GetXBounds()[1] + 0.1)
            
            plt.hlines(rect.GetYBounds()[0], rect.GetXBounds()[0], rect.GetXBounds()[1], colors='black')
            plt.hlines(rect.GetYBounds()[1], rect.GetXBounds()[0], rect.GetXBounds()[1], colors='black')
            plt.vlines(rect.GetXBounds()[0], rect.GetYBounds()[0], rect.GetYBounds()[1], colors='black')
            plt.vlines(rect.GetXBounds()[1], rect.GetYBounds()[0], rect.GetYBounds()[1], colors='black')
            
            plt.title(f"{np} particles after {step+1} step"+("s" if step+1>1 else ""))
            plt.savefig(f'tmp_{step+1}.png')
            
            plt.clf()
            
    return xpos, ypos

#random.seed(10)

np = 10000
ns = 10000
plot_step = 50

start_total = timer()
x, y = random_walk_2D(np, ns, Rectangle(0, 1, 0, 1), plot_step)
end_total = timer()

print(f"Current total execution speed: {end_total-start_total}")