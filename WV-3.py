import numpy as np
from sympy import *
import matplotlib.pyplot as plt
import math
import csv
import matplotlib.ticker as ticker
import pyautocad as pyA
from pyautocad import Autocad, APoint, ACAD

T = np.genfromtxt('Page_90.csv', delimiter=',')

pointsX = T[:, 0] * -1  # Меняю х и у местами потому что у Пейджа СИГМА2 (по y) равно СИГМА1 у Поздеева
pointsY = T[:, 1] * -1
# DEGREES = np.radians(0) #Угол отличается от углов Пейджа на 90 градусов по принятым формулам
# Задаю рисунок размером 7 на 7 и оси
fig, ax = plt.subplots(figsize=(7, 7))
a=4
ax.set_xlim(-a, 0.2)
ax.set_ylim(-a, 0.2)
# ax.scatter(pointsY, pointsX, color="black", linewidths=0.1)

ft = 2.01
fcu = 2
fcb = 2
alpha_z = ft / fcu
alpha_u = fcb / fcu
r1 = sqrt(6 / 5) * (alpha_u * alpha_z) / (2 * alpha_u + alpha_z)
r2 = sqrt(6 / 5) * (alpha_u * alpha_z) / (3 * alpha_u * alpha_z + alpha_u - alpha_z)
z = (alpha_u * alpha_z) / (alpha_u - alpha_z)
x, y = symbols('x y')
cos_theta = (x + y) / (sqrt(2) * sqrt((x - y) ** 2 + y ** 2 + x ** 2))
tau_a = sqrt(1 / 15) * ((x - y) ** 2 + x ** 2 + y ** 2) ** 0.5
sigma_a = 1 / 3 * (x + y)
r = (2 * r2 * (r2 ** 2 - r1 ** 2) * cos_theta + r2 * (2 * r1 - r2) * sqrt(
    4 * (r2 ** 2 - r1 ** 2) * cos_theta ** 2 + 5 * r1 ** 2 - 4 * r1 * r2)) / \
    (4 * (r2 ** 2 - r1 ** 2) * cos_theta**2 + (r2 - 2 * r1) ** 2)

# crit = tau_a / fcu - r * (1 - 1 / z * sigma_a / fcu)
crit = 1/z*sigma_a/fcu+1/r*tau_a/fcu-1
# print(r1)
print(crit.subs(y,  x))
print(crit.subs(x,  y))
points=[]
i=1
while i<180:
    print("i=",i,":")
    x_solve=solve(crit.subs(y, math.tan(math.radians(i))*x))
    for j in  x_solve:
        try:
            plt.scatter(j, j * math.tan(math.radians(i)))
            points.append([j, j * math.tan(math.radians(i))])
        except:
            print("что то тут было не так")
    i=i+0.5
with open('points.csv', 'w', newline='') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
    quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in points:
        filewriter.writerow([i[0], i[1]])

#plt.scatter( x_solve[1] * math.tan(math.radians(95)), x_solve[1])
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

plt.show()
