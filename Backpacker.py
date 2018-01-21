#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 12:47:02 2018

@author: eivind
"""
import random
import math

#Country,City,AccentCity,Region,Population,Latitude,Longitude
class City:
    def __init__(self, line):
        self.countryCode = self.getPart(line, 0)
        self.city = self.getPart(line, 1)
        self.accentCity = self.getPart(line, 2)
        self.region = self.getPart(line, 3)
        self.latitude = float(self.getPart(line, 5))
        self.longitude = float(self.getPart(line, 6))
        
    def getPart(self, line, n):
        parts = line.split(",")
        return parts[n]
    # Simplified. Should use great circle.
    def getDistance(self, otherCity):
        dx = self.longitude - otherCity.longitude
        dy = self.latitude - otherCity.latitude
        return math.sqrt((dx)**2 + (dy)**2)
    
    def getName(self):
        return self.city
        

class Node:
    def __init__(self, city):
        self.city = city
        self.name = city.getName()
        self.edges = []
        self.isEndNode = False

    def rouletteWheelSimple(self):
        if len(self.edges) == 0:
            return None
        return random.choice(self.edges)

    def rouletteWheel(self, visitedEdges, startNode):
        visitedNodes = [oneEdge.toNode for oneEdge in visitedEdges]
        viableEdges = [oneEdge for oneEdge in self.edges if
                       not oneEdge.toNode in visitedNodes and oneEdge.toNode != startNode]
        if not viableEdges:
            viableEdges = [oneEdge for oneEdge in self.edges if not oneEdge.toNode in visitedNodes]

        allPheromones = sum([oneEdge.pheromones for oneEdge in viableEdges])
        num = random.uniform(0, allPheromones)
        #print("num:", num)
        s = 0
        i = 0
        if len(viableEdges) == 0:
            return None
        selectedEdge = viableEdges[0]
        while s <= num:
            selectedEdge = viableEdges[i]
            s += selectedEdge.pheromones
            i += 1
        return selectedEdge

    def getCity(self):
        return self.city

    def __repr__(self):
        return self.name



class Edge:
    def __init__(self,fromNode,toNode):
       self.fromNode = fromNode
       self.toNode = toNode
       self.cost = fromNode.getCity().getDistance(toNode.getCity())
       self.pheromones = 1

    def getCost(self):
        return self.cost

    def __repr__(self):
       return self.fromNode.name + "--(" + str(self.cost) + ")--" + self.toNode.name

class Ant:
    def __init__(self):
        self.visitedEdges = []


    def walk(self,startNode):
        currentNode = startNode
        currentEdge = None
        prevEdge = None
        ntries=0
        while(not self.checkAllNodesPresent(self.visitedEdges)):
            #currentEdge = currentNode.rouletteWheelSimple()
            currentEdge = currentNode.rouletteWheel(self.visitedEdges, startNode)

            #print("currentEdge", currentEdge)
            if currentEdge == None:
                # End node returns None. If end node is selected before all all edges are visited, try again.
                # Otherwise we may select the end node too early
                self.visitedEdges.remove(prevEdge)
                currentNode = prevEdge.fromNode
                if ntries>5:
                    #Not a valid path, did not walk all nodes.
                    return False
                ntries += 1
                #currentEdge = self.visitedEdges[len(self.visitedEdges)-1]
            else:
                currentNode = currentEdge.toNode
                self.visitedEdges.append(currentEdge)
                prevEdge = currentEdge
        return True



    def pheromones(self):
        currentCost = getSum(self.visitedEdges)
        if currentCost<MAXCOST:
            global minCost
            if currentCost<minCost:
                minCost = currentCost
                global bestVisits
                bestVisits = self.visitedEdges
            score = 1/(float(currentCost)/MAXCOST)
            #score = 10**(1-float(currentCost)/MAXCOST)
            print("score:", score, currentCost, MAXCOST)
            for oneEdge in self.visitedEdges:
                oneEdge.pheromones += score


    def checkAllNodesPresent(self, edges):
        visitedNodes = [edge.toNode for edge in edges]
        visitedNodes.append(nodes[0])
        return set(nodes).issubset(visitedNodes)

    def printEdges(self):
        for edge in self.visitedEdges:
            print(edge, edge.pheromones)


minCost = 10000000
'''
def checkAllNodesPresent( edges):
    visitedNodes = [edge.toNode for edge in edges]
    visitedNodes.append(nodes[0])
    return set(nodes).issubset(visitedNodes)
'''


def getCities(filename):
    cities = dict()
    in_handle = open(filename, "rt", encoding = "iso-8859-1")
    for line in in_handle:
        city = City(line)
        cities[city.getName()] = city
            
    in_handle.close()        
    return cities       


def getRandomCities(cityList, startCity, endCity, count):
    _selectedList = random.sample(cityList, count)
    _selectedList.remove(startCity)
    _selectedList.remove(endCity)

    _selectedList.insert(0, startCity)
    _selectedList.append(endCity)
    return _selectedList


def getEdges(nodeList):
    _edges = list()
    p = 1 # helper variable to prevent edge from start to end node.
    for n in range(0, len(nodeList) - 1):
        _fromNode = nodeList[n]
        for k in range(1, len(nodeList) - p):
            _toNode = nodeList[k]
            #Ensure no edge from self to self
            if _fromNode != _toNode:
                _edges.append(Edge(_fromNode, _toNode))
        p=0
    return _edges

#Cost function
def getSum(edges):
    return sum([e.getCost() for e in edges])

filename = "./tencities.txt"
allCities = getCities(filename)
cityList = list(allCities.values())
cityCount = len(allCities)

print("No of cities:", len(allCities))
startCity = allCities.get("oslo")
endCity = allCities.get("bergen")

dist = startCity.getDistance(endCity)
print("Dist: ", dist)
'''
sampleCities = getRandomCities(cityList, startCity, endCity, 8)

for city in sampleCities:
    print(city.getName())

nodes = list()

for city in sampleCities:
    nodes.append(Node(city))
nodes[len(nodes)-1].isEndNode = True

edges = getEdges(nodes)
MAXCOST = getSum(edges)
'''

#Make symetrical
'''
for oneEdge in edges[:]:
   edges.append(Edge(oneEdge.toNode,oneEdge.fromNode))
'''
edges = []
nodes = list()
MAXCOST=0


#print(getSum(edges))
#sampleCities = getRandomCities(cityList, startCity, endCity, 10)

# for city in sampleCities:
#    print(city.getName())

nodes = list()
cityList.remove(startCity)
cityList.remove(endCity)
nodes.append(Node(startCity))
for city in cityList:
    nodes.append(Node(city))
nodes.append(Node(endCity))

edges = getEdges(nodes)

# Assign to nodes
for oneEdge in edges:
    for oneNode in nodes:
        if (oneEdge.fromNode == oneNode):
            oneNode.edges.append(oneEdge)

#list of ant's walks. One entry consist of a list of edges, the best result should be stored.
bestVisits = []

def walkRandomPaths(max):
    for n in range(0, max):
        global MAXCOST
        MAXCOST = getSum(edges)

        startNode = nodes[0]
        ant = Ant()

        #print("walk...")
        isValid = ant.walk(startNode)
        if isValid:
            #ant.printEdges()
            #print("pheromones...")
            ant.pheromones()
            print("n", n, "Cost",  getSum(ant.visitedEdges))

walkRandomPaths(100000)

print("The best result: ", minCost)
for e in bestVisits:
    print(e)

#for key, value in allCities.items():
#    print(key, value.getName())