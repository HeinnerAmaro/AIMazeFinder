

from copy import deepcopy   # In order to deep copy the Maze object for reutilization https://docs.python.org/3/library/copy.html
from queue import PriorityQueue   #Need this import for Astar search  
import sys                      
from math import sqrt #for euclidian



#class to create the maze, we are going to read the 
#file input by the user and then assign the states 
#https://runestone.academy/runestone/books/published/pythonds/Recursion/ExploringaMaze.html
#Rune academy class maze helped me with this, their class is for a Python turtle whick will explore the whole graph and create it 
class Maze:
    #We are going to store the text file on an array using the MazeLines 
	def mazeArray(self, num, mazeFile):
		MazeLines = [] 
		someFile = open(mazeFile,"r") # Read File 
        # take out new Line characters to print out maze
		for i in someFile: 
			MazeLines.append(i.rstrip('\n'))

		columns = -1 
		rows = -1 
		for i in MazeLines: 
			temporary2DArray = [] 
			rows += 1 
			columns = -1 
			for char in i: 
				columns += 1 
				if char == "S": 
					self.stateInitialPosition = (rows,columns) # Initial State from where the search will start 
				elif char == "G":
					self.initialGoalStatePosition = (rows,columns) # Goal State where the search will stop 
				temporary2DArray.append(char)
			num.append(temporary2DArray)

		self.numRows = rows + 1 
		self.numCols = columns + 1 


	# How to print out the Maze object
	def __str__(self):
		mazeFile = '' 
		for i in self.plots: 
			mazeFile += ''.join(i) 
			mazeFile += "\n"
		return mazeFile


	def __init__(self, mazeFile):
		self.plots = []
		self.stateInitialPosition = (-1,-1)
		self.initialGoalStatePosition = (-1,-1)
		self.numRows = -1
		self.numCols = -1
		self.mazeArray(self.plots, mazeFile)

	# #https://runestone.academy/runestone/books/published/pythonds/Recursion/ExploringaMaze.html
    #This method helps locate the position of agent when it is not on an obstacle 
	def getPosition(self, rows,columns):
		if columns >= 0 and columns < self.numCols:
			if rows >= 0 and rows < self.numRows:
				if self.plots[rows][columns] != "%":
					
					return (rows,columns)
		else:
			return None

	# Helps the agent move by getting adjance nodes on the grid https://www.codementor.io/blog/basic-pathfinding-explained-with-python-5pil8767c1
	def getAdjacent(self,rows,columns):
		neighborsArray = [] # list of neighborsArray to return

		neighborsArray.append(self.getPosition(rows-1,columns)) # Goes up 
		neighborsArray.append(self.getPosition(rows,columns+1)) # Right
		neighborsArray.append(self.getPosition(rows+1,columns)) #Down
		neighborsArray.append(self.getPosition(rows,columns-1)) # Left

		return neighborsArray 
# euclidan for A*
def euclidan_distance(n1, n2):
	 return sqrt((n1[0] - n2[0])**2 + (n1[1] - n2[1])**2)


#Backtrack to calculate cost
def backtrack(parentNode, initial, goal):
	path = [] # initialize path
	path.clear() # clear the path
	path.append(goal) # goal is first element

	# gets the path
	while path[-1] != initial:
		path.append(parentNode[path[-1]])

	path.reverse() 
	print("Cost: " + str(len(path)))
	return path 

#Path cost
def path_cost(parentNode, initial, node):
	pathArray = [] 
	pathArray.clear() 
	pathArray.append(node) 

	
	while pathArray[-1] != initial:
		pathArray.append(parentNode[pathArray[-1]])

	return len(pathArray) 


#Depth First search https://www.annytab.com/depth-first-search-algorithm-in-python/
def dfsSearch(maze):
	#First element just like queue 
	NodeStack = [maze.stateInitialPosition]

	#Create Array
	numberOfNodesVisitedArray = [[0 for i in range(maze.numCols)] for j in range(maze.numRows)]
	counter = 0 

	parentNode = {} 

	
	numberOfNodesVisitedArray[maze.stateInitialPosition[0]][maze.stateInitialPosition[1]] = 1

	
	while NodeStack:
		currentNode = NodeStack.pop() 
		counter += 1 

		if(currentNode == maze.initialGoalStatePosition): # Goal
			print("DFS:Data")
			print("Nodes: " + str(counter)) 

			# Path
			return(backtrack(parentNode, maze.stateInitialPosition, maze.initialGoalStatePosition))

		
		for nodes in maze.getAdjacent(currentNode[0], currentNode[1]):
			if nodes == None: 
				continue
			elif numberOfNodesVisitedArray[nodes[0]][nodes[1]] == False: 
				if nodes not in NodeStack: 
					parentNode[nodes] = currentNode
				
				NodeStack.append(nodes)

				numberOfNodesVisitedArray[nodes[0]][nodes[1]] = True 


#Searches
#https://www.redblobgames.com/pathfinding/a-star/implementation.html
def bfsSearch(maze):
	# Get initial Position
	queue = [maze.stateInitialPosition] 

	# Array
	numberOfNodesVisitedArray = [[0 for i in range(maze.numCols)] for j in range(maze.numRows)]
	counter = 0 

	parentNode = {} 

	# Get First node
	numberOfNodesVisitedArray[maze.stateInitialPosition[0]][maze.stateInitialPosition[1]] = 1


	while queue:
		currentNode = queue.pop(0) 
		counter += 1 # Increment Array

		if(currentNode == maze.initialGoalStatePosition): # If Goal
			print("Data for BFS") 
			print("Nodes : " + str(counter)) 

			# Path
			return(backtrack(parentNode, maze.stateInitialPosition, maze.initialGoalStatePosition))

		# Add the up,down,south,east,west nodes 
		for nodes in maze.getAdjacent(currentNode[0], currentNode[1]):
			if nodes == None: # If no node but obstacle
				continue
			elif numberOfNodesVisitedArray[nodes[0]][nodes[1]] == False: 
				if nodes not in queue: 
					parentNode[nodes] = currentNode 
				
				queue.append(nodes) 

				numberOfNodesVisitedArray[nodes[0]][nodes[1]] = True 
	

		


   
#Astar Search https://www.redblobgames.com/pathfinding/a-star/implementation.html
def aStarSearch(maze):
	# PriorityQueue
	aStarSearchQueue = PriorityQueue() 
    #Array
	numberOfNodesVisitedArray = [[0 for i in range(maze.numCols)] for j in range(maze.numRows)]
	counter = 0 
	parentNode = {} 

	aStarSearchQueue.put((1, maze.stateInitialPosition))

	# First Node
	numberOfNodesVisitedArray[maze.stateInitialPosition[0]][maze.stateInitialPosition[1]] = 1

	
	while aStarSearchQueue:
		currentNode = aStarSearchQueue.get() 
		currentNode = currentNode[1] 
		counter += 1 

		if(currentNode == maze.initialGoalStatePosition): 
			print("AstarSearch Data:")
			print("Nodes: " + str(counter)) 

			return(backtrack(parentNode, maze.stateInitialPosition, maze.initialGoalStatePosition))
			

		for nodes in maze.getAdjacent(currentNode[0], currentNode[1]):
			if nodes == None: 
				continue
			elif numberOfNodesVisitedArray[nodes[0]][nodes[1]] == False: 
				parentNode[nodes] = currentNode
				
				
				aStarSearchQueue.put((euclidan_distance(nodes, maze.initialGoalStatePosition) + path_cost(parentNode, maze.stateInitialPosition, nodes), nodes))
		

				numberOfNodesVisitedArray[nodes[0]][nodes[1]] = True 


	

def searchedMaze(maze, path):
	temporary2DArray = deepcopy(maze) 

	for node in path:
		if temporary2DArray.plots[node[0]][node[1]] != "G": # Not the goal state
			temporary2DArray.plots[node[0]][node[1]] = "'" #Pathing

	temporary2DArray.plots[temporary2DArray.stateInitialPosition[0]][temporary2DArray.stateInitialPosition[1]] = "S"

	print(temporary2DArray) 

def main():
	mazeFile = Maze(sys.argv[2]) #Get File

	if sys.argv[1] == "breadth":
		searchedMaze(mazeFile, bfsSearch(mazeFile))
	elif sys.argv[1] == "depth":
		searchedMaze(mazeFile, dfsSearch(mazeFile))
	elif sys.argv[1] == "astar":
		searchedMaze(mazeFile, aStarSearch(mazeFile))


main() 

