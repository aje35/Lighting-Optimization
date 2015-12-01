import matplotlib.pyplot as plt
import numpy as np
import random
import glob, os

'''
from scipy import ndimage
a = np.arange(12.).reshape((4, 3))
print a
print ndimage.map_coordinates(a, [[0, 0], [4,3]], order=1)
'''

# import required lighting array and lamp array
requiredLighting = np.genfromtxt('Examples/Test_LightData2.csv', delimiter=',')

# Get folder path containing text files
file_list = glob.glob('Lamps/*.csv')
lamps = []
for file_path in file_list:
    lamps.append(
        np.genfromtxt(file_path, delimiter=','))


#lamp = np.genfromtxt('Lamp/Lamp02.csv', delimiter=',')

# fitness function that compares two arrays and scores with an under- or over-penalty
def fitness(inputArray,compareArray):
	totalScore = 0
	underPenalty = -0.1
	overPenalty = -0.001
	totalScore = 0
	evalArray = np.subtract(inputArray, compareArray)
	for elements in evalArray.flat:
		if elements < 0:
			totalScore += abs(elements)*underPenalty
		if elements > 0:
			totalScore += abs(elements)*overPenalty
	return totalScore

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


if __name__ == '__main__':
	# very basic randomized optimization (that's not working well)
	for individual in range(0,100000):
		achievedLighting = np.zeros((requiredLighting.shape[0],requiredLighting.shape[1]))
		totalLamps = random.randint(10, 30)
		for x in range(0,totalLamps):
			lampType = random.randint(0,len(lamps)-1)
			# design boundaries for lamp placement
			xmin = 0
			xmax = requiredLighting.shape[1] - lamps[lampType].shape[0]
			ymin = 0
			ymax = requiredLighting.shape[0] - lamps[lampType].shape[1]
			xrand = random.randint(xmin, xmax)
			yrand = random.randint(ymin, ymax)
			addAtPos(achievedLighting,lamps[lampType],(yrand,xrand))
		if individual==0:
			highScore = fitness(requiredLighting,achievedLighting)
			bestOf = achievedLighting
			first=0
		if fitness(requiredLighting,achievedLighting) > highScore:
			bestOf = achievedLighting
			highScore = fitness(requiredLighting,achievedLighting)
			print highScore
		
	plotHeatmap(bestOf)
	#plotHeatmap(requiredLighting)