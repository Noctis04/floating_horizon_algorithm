import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def visibility(x, y, top, bottom, t_flag):
    if bottom[x] < y < top[x]:
        t_flag[0] = 0
    if y >= top[x]:
        t_flag[0] = 1
    if y <= bottom[x]:
        t_flag[0] = -1

def edge_processing(x, y, x_edge, y_edge, bottom, top):
    if x_edge != -1:
        horizon(x_edge, y_edge, x, y, top, bottom)
    x_edge, y_edge = x, y

def horizon(x1, y1, x2, y2, bottom, top):
    if x2 - x1 == 0:
        top[x2] = max(top[x2], y2)
        bottom[x2] = min(bottom[x2], y2)
    else:
        m = (y2 - y1) / (x2 - x1)
        for x in range(x1, x2 + 1):
            y = m * (x - x1) + y1
            top[x] = max(top[x], y)
            bottom[x] = min(bottom[x], y)

def intersection(x1, y1, x2, y2, horizon):
    if x2 - x1 == 0:
        return x2, horizon[x2]
    else:
        m = (y2 - y1) / (x2 - x1)
        y_sign = (y1 + m - horizon[x1 + 1]) / abs(y1 + m - horizon[x1 + 1])
        c_sign = y_sign
        y_i = y1 + m
        x_i = x1 + 1

        while c_sign == y_sign:
            y_i = x_i + m
            x_i += 1
            c_sign = (y_i - horizon[x_i]) / abs(y_i - horizon[x_i])

        if abs(y_i - m - horizon[x_i - 1]) <= abs(y_i - horizon[x_i]):
            y_i -= m
            x_i -= 1

        return x_i, y_i

def floating_horizon_algorithm(ax, width, height, x_min, x_max, x_step, z_min, z_max, z_step):
    top = [0] * width
    bottom = [height] * width
    x_left, y_left = -1, -1
    x_right, y_right = -1, -1

    for x in range(width):
        top[x] = 0
        bottom[x] = height

    for z in range(z_max, z_min - 1, -z_step):
        x_pr = x_min
        y_pr = f(x_min, z)
        edge_processing(x_pr, y_pr, x_left, y_left, top, bottom)
        t_flag = [0]
        visibility(x_pr, y_pr, top, bottom, t_flag)

        for x in range(x_min, x_max + 1, x_step):
            y = f(x, z)
            visibility(x, y, top, bottom, t_flag)
            p_flag = t_flag[0]

            if t_flag[0] == p_flag:
                horizon(x_pr, y_pr, x, y, top, bottom)

            elif t_flag[0] == 0:
                if p_flag == 1:
                    x_i, y_i = intersection(x_pr, y_pr, x, y, top)
                else:
                    x_i, y_i = intersection(x_pr, y_pr, x, y, bottom)

                horizon(x_pr, y_pr, x_i, y_i, top, bottom)

            p_flag = t_flag[0]
            y_pr, x_pr = y, x
            edge_processing(x, y, x_right, y_right, top, bottom)

    # Plot the surface with a colormap
    x_values = np.linspace(x_min, x_max, width)
    z_values = np.linspace(z_min, z_max, int((z_max - z_min) / z_step) + 1)
    X, Z = np.meshgrid(x_values, z_values)

    # Use a colormap for the entire surface
    Y = f(X, Z)
    ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k', linewidth=0.5)

# Define the function f(x, z)
def f(x, z):
    return np.sin(np.sqrt(x ** 3 + z))

# Example usage
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
z_min, z_max = -10, 10
floating_horizon_algorithm(ax, width=800, height=600, x_min=-10, x_max=10, x_step=1, z_min=z_min, z_max=z_max, z_step=1)
plt.show()
