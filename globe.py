import matplotlib.pyplot as plt
import numpy as np
import math

# создаю окно
fig = plt.figure()
# позиция графика
ax1 = fig.add_subplot(111)
# выравнивание
ax1.set_aspect(1)

# открываю файл с точками карты
file = open("HRESMAP.DAT.txt", 'r')

x = []
y = []

# перевожу данные из файла в списки
for line in file:
    if '.' in line:
        x.append(float(line[11:20]))
        y.append(float(line[0:10]))


# функция перевода географических координат в декартовы
def GeoVdek(r, phi, lmbd):
    phi = np.radians(phi)
    lmbd = np.radians(lmbd)
    X = r * np.cos(phi) * np.cos(lmbd)
    Y = r * np.cos(phi) * np.sin(lmbd)
    Z = r * np.sin(phi)
    return [X, Y, Z]


# функция перевода декартовых координат в географические
def DekVgeo(x, y, z):
    R = (x ** 2 + y ** 2 + z ** 2) ** 0.5
    phi = math.asin(z / R) * 180 / np.pi
    lmbd = math.atan2(y, x) * 180 / np.pi
    return [R, phi, lmbd]


# радиус глобуса
r = 1
alpha = np.pi / 4
# массив с проекциями
proek = []
# массивы с итоговыми координатами карты
x_map = []
y_map = []

# проецирую точки карты на поверхность шара
for i in range(len(x)):
    # проверка координаты точки на нахождение ее на светлой стороне земли
    if (x[i] * np.pi / 180 > -np.pi / 2) and (x[i] * np.pi / 180 < np.pi / 2):
        proek.append(GeoVdek(1, y[i], x[i]))
        # формула кабинетной проекции
        x_map.append(proek[-1][1] - proek[-1][0] * np.sin(alpha) / 2)
        y_map.append(proek[-1][2] - proek[-1][0] * np.cos(alpha) / 2)

# рисую карту на шаре
ax1.scatter(x_map, y_map, s=0.04, color='black')

# задаю шаги между меридианами и параллелями
stepLat = 8
stepLot = 8
# список координат точек параллелей
x_parallels = []
y_parallels = []
# список координат точек меридианов
x_meridians = []
y_meridians = []

# рисую горизонтальные параллели
for phi in np.arange(-np.pi / 2, np.pi / 2, stepLat * np.pi / 180):
    for lmbd in np.linspace(-np.pi / 2, np.pi / 2, 1000):
        X = r * np.cos(phi) * np.cos(lmbd)
        Y = r * np.cos(phi) * np.sin(lmbd)
        Z = r * np.sin(phi)

        # формула кабинетной проекции
        Xs = Y - X * np.sin(alpha) / 2
        Ys = Z - X * np.cos(alpha) / 2

        x_parallels.append(Xs)
        y_parallels.append(Ys)

# рисую параллели
ax1.scatter(x_parallels, y_parallels, s=0.005, color='grey')

# рисую меридианы
for lmbd in np.arange(-np.pi / 2, np.pi / 2, stepLot * np.pi / 180):
    for phi in np.linspace(-np.pi / 2, np.pi / 2, 1000):
        X = r * np.cos(phi) * np.cos(lmbd)
        Y = r * np.cos(phi) * np.sin(lmbd)
        Z = r * np.sin(phi)

        # кабинетная проекция
        Xs = Y - X * np.sin(alpha) / 2
        Ys = Z - X * np.cos(alpha) / 2

        x_meridians.append(Xs)
        y_meridians.append(Ys)

# рисую меридианы
ax1.scatter(x_meridians, y_meridians, s=0.005, color='grey')

plt.show()
