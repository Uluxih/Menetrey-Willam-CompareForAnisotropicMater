import numpy as np
from sympy import *
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pyautocad as pyA
from pyautocad import Autocad, APoint, ACAD

T = np.genfromtxt('T_675_Пейдж.csv', delimiter=',')

pointsX = T[:, 0] * -1 #Меняю х и у местами потому что у Пейджа СИГМА2 (по y) равно СИГМА1 у Поздеева
pointsY = T[:, 1] * -1
DEGREES = np.radians(0) #Угол отличается от углов Пейджа на 90 градусов по принятым формулам
#Задаю рисунок размером 7 на 7 и оси
fig, ax = plt.subplots(figsize=(7, 7))
ax.set_xlim(-20, 2)
ax.set_ylim(-20, 2)
ax.scatter(pointsY, pointsX, color="black", linewidths=0.1)
c_2=1
c_3=1
def MW(x,y,C,O,D,g,k):
    F =  (2 ** 0.5 * (x + y ) /3**0.5)+4*C

acad = Autocad()
acad.prompt("Hello, Autocad from Python\n")
print(acad.doc.Name)
i=0
APints=[]
while i<len(pointsX):
    p=APoint(pointsX[i], pointsY[i])
    APints.append(p)
    Mark = acad.model.AddPoint(p)
    i=i+1
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1))
ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(1))

ax.grid(which='major',
        color = 'k')
ax.minorticks_on()
ax.grid(which='minor',
        color = 'gray',
        linestyle = ':')

#plt.show()