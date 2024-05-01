import numpy as np
from sympy import *
import matplotlib.pyplot as plt
import math
from functools import reduce
import operator
import matplotlib.ticker as ticker
import pyautocad as pyA
from pyautocad import Autocad, APoint, ACAD


def get_deviation(arr1, arr2):
    dev_sum=0
    for i in arr1:
        dev=100
        for j in arr2:
            dev_current = sqrt((i[0]**2-j[0])**2+(i[1]**2-j[1])**2)

            if dev_current<dev:
                dev=dev_current
        dev_sum=dev_sum+dev
    return dev

def get_tuple(arrX, arrY):
    i=1
    tuple=[]
    #print(arrX)
    while i<len(arrX):
        tuple.append([arrX[i], arrY[i]])
        i=i+1
    return  tuple
# Задаю рисунок размером 7 на 7 и оси
fig, ax = plt.subplots(figsize=(7, 7))
a = 2
ax.set_xlim(-16, 1)
ax.set_ylim(-16, 1)
# Точки с опытов Пейджа
T = np.genfromtxt('Page_0.csv', delimiter=',')
# Точки с кривой, которую записал точками
WV = np.genfromtxt('points.csv', delimiter=',')
# Точки с критерия прочности Гениева
G = np.genfromtxt('points_G_0.csv', delimiter=',')
pointsX = T[:, 0] * -1  # Меняю х и у местами потому что у Пейджа СИГМА2 (по y) равно СИГМА1 у Поздеева
pointsY = T[:, 1] * -1
ax.scatter(pointsY, pointsX, marker="x", color="black", linewidths=1)
pageArr=get_tuple(pointsX, pointsY)
print(T)

pointsX = WV[:, 0] * -1  # Меняю х и у местами потому что у Пейджа СИГМА2 (по y) равно СИГМА1 у Поздеева
pointsY = WV[:, 1] * -1
ax.scatter(pointsY, pointsX, marker=".", color="red", linewidths=0.01)
mwArr=get_tuple(pointsX, pointsY)

pointsX = G[:, 1] * 1
pointsY = G[:, 0] * 1
genArr=get_tuple(pointsX, pointsY)
pointsX = pointsX.tolist()
pointsY = pointsY.tolist()
# Сгущаю точки с критерия Гениева, добавив одну точку между существующими
j = 0


while j < 10:
    i = 0
    while i < len(pointsX) - 1:
        if (sqrt((pointsX[i + 1] - pointsX[i]) ** 2 + (pointsY[i + 1] - pointsY[i]) ** 2) >= 0.2):
            newX = (pointsX[i] + pointsX[i + 1]) / 2
            newY = (pointsY[i] + pointsY[i + 1]) / 2
            pointsX.insert(i + 1, newX)
            pointsY.insert(i + 1, newY)
            i = i + 2
        else:
            i = i + 1
    j = j + 1
ax.scatter(pointsY, pointsX, marker=".", color="blue", linewidths=0.01)
# ax.plot(pointsY, pointsX, color="blue")

# ax.scatter(pointsY, pointsX, marker=".", color="blue", linewidths=0.01)
# plt.scatter( x_solve[1] * math.tan(math.radians(95)), x_solve[1])
# acad = Autocad()
# acad.prompt("Hello, Autocad from Python\n")
# print(acad.doc.Name)
# i=0
# APints=[]
# while i<len(pointsX):
#     p=APoint(pointsX[i], pointsY[i])
#     APints.append(p)
#     Mark = acad.model.AddPoint(p)
#     i=i+1
# ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
# ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
# ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
# ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))

ax.grid(which='major',
        color='k')
ax.minorticks_on()
ax.grid(which='minor',
        color='gray',
        linestyle=':')

print(get_deviation(pageArr, genArr))
print(get_deviation(pageArr, mwArr))

plt.show()
