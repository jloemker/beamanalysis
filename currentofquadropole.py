
import numpy as np
import scipy.io as sc
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

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


def sigma (normmean, weights):
    summ = 0
    for i in range(0, len(weights), 1):
        if weights[i] == 0:
            continue
        summ = summ + weights[i] * (i - normmean)*(i - normmean)

    return math.sqrt(summ/np.sum(weights))

file_names = ["02.10.2019-0mA_09_56_31.mat", "02.10.2019-20mA_09_55_55", "02.10.2019-40mA_09_55_05",
              "02.10.2019_09_51_58", "02.10.2019-80mA_09_57_39", "02.10.2019-100mA_09_58_13",
              "02.10.2019-120mA_09_59_16"]
currents = [0,20,40,60,80,100,120]
index = 0
sigmas = currents[:]
for f in file_names:
    mat = sc.loadmat(f)
    matrix = mat.get("profiledata")

    cleanmatrix = matrix[:]
    cleanmatrix[cleanmatrix < np.max(cleanmatrix) * 0.3] = 0
    weightsX = normData(np.sum(cleanmatrix, 0))
    weightsY = normData(np.sum(cleanmatrix, 1))
    dataX = np.linspace(0, len(weightsX), len(weightsX))
    dataY = np.linspace(0, len(weightsY), len(weightsY))

    positionX = mean(weightsX)
    positionY = mean(weightsY)
    print(transformation(positionX, positionY))
    sigmaX = 0.02841 * sigma(positionX, weightsX)
    sigmaY = 0.02841 * sigma(positionY, weightsY)
    print (f, "Sigmas", sigmaX, sigmaY)
    sigmas[index] = math.sqrt(sigmaY**2 + sigmaX**2)
    index = index + 1

    #
    fig = plt.figure()
    plt.imshow(cleanmatrix)
    plt.colorbar()
    plt.show()
print(sigmas)
# figure = plt.figure()
# plt.plot(currents, sigmas)
# plt.show()
#
# f = np.polyfit(currents, sigmas, 2)
# plt.show()
# currents_new = list(range(0, 120))
# pp = currents_new[:]
# for index in range(0, len(currents_new)):
#     pp[index] = f[0] + f[1] * (currents_new[index]-60) + f[2] * (currents_new[index]-60) * (currents_new[index])
# print(len(currents_new))
# print (f)
# plt.plot(currents_new, pp)
# plt.show()