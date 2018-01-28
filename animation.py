import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

import Backpacker
t=0
r=3.0
n=0
global data#

def startNew():
    global data
    data=[]
    for x in range(10):
        for y in range(10):
            data.append([random.uniform(0,100),random.uniform(0,100)])
    data = np.array(data).transpose()



def start(mindata):
    global data
    data=[[i[0],i[1]] for i in mindata]
    data = np.array(data)#.transpose()
    print( "Start",len(data))#,
    
    return data#one,two,three

startNew()
fig = plt.figure()
#linecentroids, = plt.plot(centroids[0],centroids[1], "ro", color="blue")
lineone, = plt.plot(data[0],data[1], "ro", color="green")

def update():
    while(True):
        #import pdb;pdb.set_trace()
        route = Backpacker.getNextRoute()
        #A[0],A[1] = np.array([d[0],d[1]])

        #mindata = start(d)
        #centroids[0],centroids[1] = np.array([c[0],c[1]])
        #data[0],data[1] = np.array([mindata[0],mindata[1]])

        for edge in route:
            data[0] = edge.fromNode.city.latitude
            data[1] = edge.fromNode.city.longitude
        yield data,#one,two,three
    #d = Clustering.getNextData()
    #for i in range(len(d[0])):
    #    A[0],A[1] = d[0][i],d[1][i]
    #for i in range(100):
    #    A[0], A[1] = r*A[0]*(1-A[0]), r*A[1]*(1-A[1])
    #    print A
    #    yield A

def draw(data):
    #print "Draw data",data
    #linecentroids.set_xdata(data[0][0])
    #linecentroids.set_ydata(data[0][1])
    print( "Draw",len(data[0]))
    #linecentroids.set_xdata([i[0] for i in data[0]])
    #linecentroids.set_ydata([i[1] for i in data[0]])
    lineone.set_xdata([i[0] for i in data[0]])
    lineone.set_ydata([i[1] for i in data[0]])
    #linetwo.set_xdata([i[0] for i in data[1]])
    #linetwo.set_ydata([i[1] for i in data[1]])
    #linethree.set_xdata([i[0] for i in data[2]])
    #linethree.set_ydata([i[1] for i in data[2]])
    return lineone,#linetwo,linethree

ani = animation.FuncAnimation(fig, draw, update, interval=10, blit=False)

plt.show()
