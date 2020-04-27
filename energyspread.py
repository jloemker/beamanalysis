
import numpy as np
import scipy.io as sc
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def normData(data):
    maxVal = np.max(data)
    return [i/maxVal for i in data]



def transformation(posX, posY):
    pX = 0.01889
    pY = 0.01889
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


def sigma (normmean, weights):
    summ = 0
    for i in range(0, len(weights), 1):
        if weights[i] == 0:
            continue
        summ = summ + weights[i] * (i - normmean)*(i - normmean)

    return math.sqrt(summ/np.sum(weights))

f = "02.10.2019-YAG2-energy_10_22_04"
bg = "02.10.2019-YAG2-energy_bg_10_22_04"
mat = sc.loadmat(f)
matbg = sc.loadmat(bg)
matrix = mat.get("profiledata")
background = matbg.get("beckgrounddata")
cleanmatrix = matrix[:]-background[:]


cleanmatrix[cleanmatrix < np.max(cleanmatrix) * 0.4] = 0
weightsX = normData(np.sum(cleanmatrix, 0))
weightsY = normData(np.sum(cleanmatrix, 1))
dataX = np.linspace(0, len(weightsX), len(weightsX))
dataY = np.linspace(0, len(weightsY), len(weightsY))

positionX = mean(weightsX)
positionY = mean(weightsY)
print(transformation(positionX, positionY))
sigmaX = 0.02841 * sigma(positionX, weightsX)
sigmaY = 0.02841 * sigma(positionY, weightsY)




fig = plt.figure()
plt.imshow(cleanmatrix)
plt.colorbar()
plt.show()
print(sigmaX)
