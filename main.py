import random
from scipy import interpolate
import numpy as np
import statistics as stat
from sklearn import preprocessing
import pygame
import matplotlib.pyplot as plt
import sys
import CellAuto as ca


def read_from_init_file(file_name):
    file_handler = open(file_name, mode='r')
    return file_handler.read().split(' ')


def display_cells(cells_to_disp, cell_size=1.75):
    pygame.init()
    surf_width = 500
    surf_height = 800
    cell_size = (surf_width / len(cells_to_disp[0])) * cell_size
    if cell_size < 1:
        cell_size = 2
    surface = pygame.display.set_mode((surf_width, surf_height))
    surface.fill((0, 0, 0))

    itr1 = 0
    for clls in cells_to_disp:
        itr = 0
        for c in clls:
            if c == '1':
                pygame.draw.rect(surface,
                                 (150, 170, 80),
                                 pygame.Rect(0 + itr, 0 + itr1,
                                             cell_size,
                                             cell_size),
                                 width=0)
            itr += cell_size
        itr1 += cell_size
    pygame.display.flip()

    run_loop = True
    while run_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_loop = False
    pygame.display.quit()
    pygame.quit()


def gen_cells(length, prob):
    if length == 0:
        print("Min. len.: 1, 0 passed")
        return
    if prob > 1.0:
        prob = 0.5
    cells = ""
    for idx in range(length):
        rand_var = random.randint(0, 100)
        if rand_var <= (prob * 100):
            cells += '1'
        else:
            cells += '0'
    return cells


def gen_middle_point_cells(mp_cells_len):
    if mp_cells_len == 0:
        print("Min. len.: 1, 0 passed")
        return

    mp_cells = ""
    for ri in range(mp_cells_len):
        if ri == int(mp_cells_len / 2):
            mp_cells += '1'
        else:
            mp_cells += '0'
    return mp_cells


def comp_error(data, extrap_data):
    d10_iter = 0
    error = []
    for d in data:
        divider = d
        if divider == 0:
            divider = 0.000001
        error.append(abs((d - extrap_data[d10_iter])) / divider)
        d10_iter += 1
    return stat.mean(error)


def check_const(data):
    for cc_idx in range(10):
        idx = int(len(data) / (cc_idx + 2))
        if data[idx] == data[idx + 1]:
            continue
        else:
            return False
    return True


def classify(error, data):
    if error == 0:
        if check_const(data):
            return '1'
        else:
            return '2'
    else:
        return "3/4"


args = [2, 100, 1000, 160, 0.6, 0]

init_file_name = ""
if len(sys.argv) >= 2:
    init_file_name = sys.argv[1]
else:
    init_file_name = "init.txt"

args_iter = 0
for i in read_from_init_file(init_file_name):
    args[args_iter] = i
    args_iter += 1

rule = int(args[0])
cells_len = int(args[1])
epochs = int(args[2])
pre_epochs_last_idx = int(args[3])
one_prob = float(args[4])
disp_clls = int(args[5])

cells_list = []
cells = ""
dec_cells = []

if one_prob != -1:
    cells = gen_cells(cells_len, one_prob)
else:
    cells = gen_middle_point_cells(cells_len)

cells_len = len(cells)

cell_auto = ca.CellAuto(rule, 0)
for i in range(epochs):
    dec_cells.append(int(cells, 2))
    cells = cell_auto.update_cells(cells)
    cells_list.append(cells)

cells_list = cells_list[pre_epochs_last_idx + 1:len(cells_list)]
dec_cells = dec_cells[pre_epochs_last_idx + 1:len(dec_cells)]

if disp_clls == 1:
    display_cells(cells_list, 1)

dec_cells = list(preprocessing.normalize([dec_cells])[0])

last_data_80_idx = int(len(dec_cells) * 0.8) - 1
data_80 = dec_cells[0:last_data_80_idx + 1]
data_20 = dec_cells[last_data_80_idx + 1:len(dec_cells)]

x = np.arange(0, len(data_80))
f = interpolate.CubicSpline(x, data_80, extrapolate="periodic")

extrapolated_data = []
add_factor = 0
error_mean = 0
errors_means = []
for err_idx in range(3):
    extrapolated_data.clear()
    place_holder = error_mean
    for exp_iter in range(len(data_20)):
        extrapolated_data.append(f(last_data_80_idx + add_factor + exp_iter))
    error_mean = comp_error(data_20, extrapolated_data)
    errors_means.append(error_mean)
    if error_mean > 1:
        if add_factor == -1:
            add_factor = 1
        else:
            add_factor = -1
    if err_idx == 0 or place_holder != error_mean:
        print(f"Rule {rule} error :", error_mean)

clss = classify(min(errors_means), data_20)
print(f"Rule {rule} is class:", clss)

if disp_clls == 1:
    x2 = np.arange(0, len(data_80))
    y2 = f(x2)
    plt.plot(x2, data_80, 'o', x2, y2, '-')
    plt.show()

    x2 = np.arange(last_data_80_idx + 1, len(dec_cells))
    y2 = f(x2)
    plt.plot(x2, data_20, 'o', x2, y2, '-')
    plt.show()
print("")
