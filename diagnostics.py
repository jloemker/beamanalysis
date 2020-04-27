
import numpy as np
import scipy.io as sc
import math
import matplotlib.pyplot as plt

def normData(data):
    maxVal = np.max(data)
    return [i/maxVal for i in data]



def transformation(posX, posY):
    pX = 0.02841
    pY = 0.02841
    posMMX = -14.66 + posX * pX
    posMMY = -11.02 + posY * pY  # change the initial value
    return posMMX,posMMY

def mean (weight):
    sum = 0
    sumWeight = 0
    i = 0
    while i < len(weight):
        sum = sum + i*weight[i]
        sumWeight = sumWeight + weight[i]
        i = i + 1
    return sum/sumWeight


def normMean (pixels):
    return sum(pixels)/len(pixels)

#TODO: check how to calculate sigma
def sigma (normmean, weights):
    summ = 0
    for i in range(0, len(weights),1):
        if weights[i] == 0:
            continue
        summ = summ + weights[i] * (i - normmean)*(i - normmean)

    return math.sqrt(summ/np.sum(weights))

mat = sc.loadmat("/Users/sonachitchyan/Downloads/01.10.2019_12_10_37")
matrix = mat.get("profiledata")
cleanedmatrix = matrix[:]
cleanedmatrix[cleanedmatrix < np.max(cleanedmatrix) * 0.3] = 0
weightsX = normData(np.sum(matrix, 0))
weightsY = normData(np.sum(matrix, 1))
dataX = np.linspace(0, len(weightsX), len(weightsX))
dataY = np.linspace(0, len(weightsY), len(weightsY))

cleanedweightsX = normData(np.sum(cleanedmatrix, 0))
cleanedweightsY = normData(np.sum(cleanedmatrix,1))


positionX = mean(cleanedweightsX)
positionY = mean(cleanedweightsY)
print(transformation(positionX, positionY))
sigmaX = 0.02841 * sigma(positionX, cleanedweightsX)
sigmaY = 0.02841 * sigma(positionY, cleanedweightsY)
print (sigmaX, sigmaY)


fig = plt.figure()
plt.imshow(cleanedmatrix)
plt.colorbar()
plt.show()
