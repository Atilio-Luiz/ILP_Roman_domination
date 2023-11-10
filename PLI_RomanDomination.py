# Implementation of the ILP model for Roman Domination extracted from article:
# ReVelle, Charles S., and Kenneth E. Rosing. 
# "Defendens Imperium Romanum: A Classical Problem in Military Strategy."
# The American Mathematical Monthly, vol. 107, no. 7, 2000, pp. 585-94. 
# JSTOR, Link: https://doi.org/10.2307/2589113. Accessed 10 Nov. 2023.

from ortools.linear_solver import pywraplp

# create a solver using GLOP backend
msolver = pywraplp.Solver('roman domination', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

# reads the first line of the file, which contains a list with all the edges of the graph
f = open('edges.txt','r')
line = f.readline().split()
f.close()

# creates the list of edges
edges = []
for i in range(0,len(line),2):
    edges.append([int(line[i]),int(line[i+1])])

# Creates the graph
G = dict()

for e in edges:
    if e[0] not in G:
        G[e[0]] = []
    if e[1] not in G:
        G[e[1]] = []
    G[e[0]].append(e[1])
    G[e[1]].append(e[0])

edges = []

#define two lists of variables for the vertices of the graph
x = []
y = []
for i in range(0, len(G)):
    x.append(msolver.IntVar(0, 1, f'x_{i}'))
    y.append(msolver.IntVar(0, 1, f'y_{i}'))

# add constraints
for i in range(0, len(G)):
    vector = []
    vector.append(x[i])
    for vertex in G[i]:
        vector.append(y[vertex])
    msolver.Add(sum(vector)>=1) # constraint for vertex i
    msolver.Add(y[i]<=x[i]) # constraint for vertex i 

# objective function
msolver.Minimize(sum(x)+sum(y))

# calculate the optimal solution
mstatus = msolver.Solve()

# if an optimal solution has been found, print results
if mstatus == pywraplp.Solver.OPTIMAL:
    print(f'Roman domination function for the graph')
    print(f'Optimal function weight = {msolver.Objective().Value()}')
    print('Vertex Labels:')
    for v in range(0,len(G)):
        if y[v].solution_value() >= 1:
            print(f'label of v_{v} = {2.0}')
        else:
            print(f'label of v_{v} = {x[v].solution_value()}')
else:
    print('The solver could not find an optimal solution')