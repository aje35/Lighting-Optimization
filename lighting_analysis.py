import matplotlib.pyplot as plt
import numpy as np
import random
import glob, os
import time 

popSize = 1000
tournSize = (popSize)*.15
numGens = 100
mutProb = 0.7
minLamps = 30
maxLamps = 50

# import required lighting
requiredLighting = np.genfromtxt('Examples/Test_LightData6.csv', delimiter=',')

# import lamps from local 'Lamps/' directory
file_list = glob.glob('Lamps/*.csv')
lamps = []
for file_path in file_list:
    lamps.append(
        np.genfromtxt(file_path, delimiter=','))

# fitness function that compares two arrays and scores with an under- or over-penalty
def fitness(compareArray):
	score = 0
	underPenalty = -0.1
	overPenalty = -0.0001
	evalArray = np.subtract(requiredLighting, compareArray)
	for elements in evalArray.flat:
		if elements < 0:
			score += abs(elements)*underPenalty
		if elements > 0:
			score += abs(elements)*overPenalty
	return score

# function to add sub-array (mat2) at a specific location (xycoor) in main array (mat1)
def addAtPos(mat1, mat2, xycoor):
    size_x, size_y = np.shape(mat2)
    coor_x, coor_y = xycoor
    end_x, end_y   = (coor_x + size_x), (coor_y + size_y)
    mat1[coor_x:end_x, coor_y:end_y] = mat1[coor_x:end_x, coor_y:end_y] + mat2
    return mat1

# heat map visualization of array
def plotHeatmap(array):
	im = plt.imshow(array, cmap='hot',  vmin = 0, vmax = 200)
	plt.axis('off')
	plt.colorbar(im, orientation='horizontal').set_label('Footcandles (fc)')
	plt.show()

def placeLamp():
	lampType = random.randint(0,len(lamps)-1)
	xmin = 0
	xmax = requiredLighting.shape[1] - lamps[lampType].shape[0]
	ymin = 0
	ymax = requiredLighting.shape[0] - lamps[lampType].shape[1]
	xrand = random.randint(xmin, xmax)
	yrand = random.randint(ymin, ymax)
	return [xrand,yrand,lampType]

def initFirstGen():
	population = []
	for n in range(0,popSize):
		individual = []
		totalLamps = random.randint(minLamps, maxLamps)
		for i in range(0,totalLamps):
			individual.append(placeLamp())
		population.append(individual)
	return population

def mutate(individual):
	individual[random.randint(0,len(individual)-1)] = placeLamp()
	return individual

def crossover(mom,dad):
	mommy = len(mom)
	daddy = len(dad)
	if mommy<daddy:
		reunion = random.randint(0,mommy)
		kid = mom[0:reunion]+dad[reunion:daddy+1]
	else:
		reunion = random.randint(0,daddy)
		kid = dad[0:reunion]+mom[reunion:mommy+1]
	return kid

def sortGen(generation):
	genScores = []
	for n in range(0,popSize):
		achievedLighting = np.zeros((requiredLighting.shape[0],requiredLighting.shape[1]))
		indSize = len(generation[n])
		for k in range(0,indSize):
			addAtPos(achievedLighting,lamps[generation[n][k][2]],(generation[n][k][1],generation[n][k][0]))
		genScores.append(fitness(achievedLighting))	
	genScores, generation = zip(*sorted(zip(genScores, generation),reverse = True))
	return generation, genScores[0]

def nextGen(currentGen):
	newGen = []
	for n in range(0,popSize):
		if n < tournSize:
			newGen.append(currentGen[n])
		else:
			if random.random() < mutProb:
				child = mutate(crossover(currentGen[random.randint(0,popSize-1)],currentGen[random.randint(0,popSize-1)]))
				newGen.append(child)
			else:
				child = crossover(currentGen[random.randint(0,popSize-1)],currentGen[random.randint(0,popSize-1)])
				newGen.append(child)
	return newGen
		
def childToLightingArray(child):
		solution = np.zeros((requiredLighting.shape[0],requiredLighting.shape[1]))
		indSize = len(child)
		for k in range(0,indSize):
			addAtPos(solution,lamps[child[k][2]],(child[k][1],child[k][0]))
		return solution
		
if __name__ == '__main__':
	start_time = time.time()	
	generation = initFirstGen()
	for gen in range(0,numGens):
		generation, highscore = sortGen(generation)
		generation = nextGen(generation)
		print("Generation: %s \t Top Score: %s" % (gen+1,highscore))
	
	print("--- %s seconds ---" % (time.time() - start_time))
	print generation[0]
	plotHeatmap(requiredLighting)
	plotHeatmap(childToLightingArray(generation[0]))

	