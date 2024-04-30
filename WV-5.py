import numpy as np
from sympy import *
import matplotlib.pyplot as plt
import math
import matplotlib.ticker as ticker
import pyautocad as pyA
from pyautocad import Autocad, APoint, ACAD

T = np.genfromtxt('Page_90.csv', delimiter=',')

pointsX = T[:, 0] * -1  # Меняю х и у местами потому что у Пейджа СИГМА2 (по y) равно СИГМА1 у Поздеева
pointsY = T[:, 1] * -1
# DEGREES = np.radians(0) #Угол отличается от углов Пейджа на 90 градусов по принятым формулам
# Задаю рисунок размером 7 на 7 и оси
fig, ax = plt.subplots(figsize=(7, 7))
a = 2
ax.set_xlim(-a, a)
ax.set_ylim(-a, a)
# ax.scatter(pointsY, pointsX, color="black", linewidths=0.1)

ft = 1.01
fcu = 1
fcb = 1
alpha_z = ft / fcu
alpha_u = fcb / fcu

x, y = symbols('x y')
cos_theta = (x + y) / (sqrt(2) * sqrt((x - y) ** 2 + y ** 2 + x ** 2))
tau_a = sqrt(1 / 15) * ((x - y) ** 2 + x ** 2 + y ** 2) ** 0.5
sigma_a = 1 / 3 * (x + y)

ksi = -sigma_a / fcu
ro1 = tau_a / fcu
ro2 = tau_a / fcu
a2 = (sqrt(6 / 5) * ksi * (alpha_z - alpha_u) - sqrt(6 / 5) * alpha_z * alpha_u + ro1 * (2 * alpha_u + alpha_z)) / (
        (2 * alpha_u + alpha_z) * (
        ksi ** 2 - 2 / 3 * alpha_u * ksi + 1 / 3 * alpha_z * ksi - 2 / 9 * alpha_z * alpha_u))
a1 = 1 / 3 * (2 * alpha_u - alpha_z) * a2 + sqrt(6 / 5) * (alpha_z - alpha_u) / (2 * alpha_u + alpha_z)
a0 = 2 / 3 * alpha_u * a1 - 4 / 9 * alpha_u ** 2 * alpha_z + sqrt(2 / 15) * alpha_u
ksi0 = (-a1 - sqrt(a1 ** 2 - 4 * a0 * a2)) / (2 * a2)
b2 = (ro2 * (ksi0 + 1 / 3) - sqrt(2 / 15) * (ksi0 + ksi)) / ((ksi + ksi0) * (ksi - 1 / 3) * (ksi0 + 1 / 3))
b1 = (ksi + 1 / 3)
b2 + (sqrt(6 / 5) - 3 * ro2) / (3 * ksi - 1)
b0 = -ksi0 * b1 - ksi0 ** 2 * b2

r1 = a0 + a1 * sigma_a / fcu + a2 * sigma_a ** 2 / fcu ** 2
r2 = b0 + b1 * sigma_a / fcu + b2 * sigma_a ** 2 / fcu ** 2
r = (2 * r2 * (r2 ** 2 - r1 ** 2) * cos_theta + r2 * (2 * r1 - r2) * sqrt(
    4 * (r2 ** 2 - r1 ** 2) * cos_theta ** 2 + 5 * r1 ** 2 - 4 * r1 * r2)) / \
    (4 * (r2 ** 2 - r1 ** 2) * cos_theta ** 2 + (r2 - 2 * r1) ** 2)

crit = 1 / r * tau_a / fcu - 1
# print(r1)
print(crit.subs(y, x))
x_solve = solve(crit.subs(y, 0 * x))
print(x_solve)
points = []
i = 1
while i < 180:
    print("i=", i, ":")
    # print(math.tan(math.radians(i)))
    x_solve = solve(crit.subs(y, math.tan(math.radians(i)) * x))
    # print(x_solve)
    # print(x_solve[0], x_solve[0] * math.tan(math.radians(i)))
    # plt.scatter(x_solve[0], x_solve[0] * math.tan(math.radians(i)))
    #
    # if(len(x_solve)>1):
    #     print(x_solve[1] , x_solve[1]* math.tan(math.radians(i)))
    #     plt.scatter(x_solve[1] , x_solve[1]* math.tan(math.radians(i)))
    for j in x_solve:
        try:
            plt.scatter(j, j * math.tan(math.radians(i)))
        except:
            print("что то тут было не так")
    i = i + 10

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

plt.show()
