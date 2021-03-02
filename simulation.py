import random
import numpy as np
from matplotlib import pyplot as plt
import math


# Function that returns True if monomers do NOT collide
def check_monomer_distance(list_coo, next_coordinates):
    for coo in list_coo[:-1]:  # Goes through every monomer that had already been simulated except the last one
        if math.dist(next_coordinates, coo) < edge_diameter:  # If the distance between the monomer that
            return False                                      # would be created and the current monomer
    return True


with open('input.txt') as f:  # Reading input file as a list of lines
    lines = f.read().splitlines()

polymer_lengths = [int(x) for x in lines[0].replace(" ", "").split("=")[1].strip("[]").split(",")]
monomer_length, edge_diameter, dim, angle_interval, mean_err, max_tries = [float(value.replace(" ", "").split("=")[1]) for value in lines[1:]]

d_angle = math.radians(angle_interval)  # Converting angle to radians

for length in polymer_lengths:

    list_coo = [[0, 0, 0]]
    last_coordinates = [0, 0, 0]  # Initializing point of origin

    for n_m in range(0, length):  # Creating n_m (number of monomers) monomers

        d_phi_range = np.arange(0.0, 2 * np.pi, d_angle)  # Setting up discrete angle intervals for both theta and phi
        d_theta_range = np.arange(0.0, np.pi, d_angle)

        theta = random.choice(d_theta_range)  # Randomly choose an angle from the discrete angle interval list
        phi = random.choice(d_phi_range)  # For both theta and phi
        l = monomer_length

        next_coordinates = [last_coordinates[0] + (l * math.sin(theta) * math.cos(phi)),
                            last_coordinates[1] + (l * math.sin(theta) * math.sin(phi)),
                            last_coordinates[2] + (l * math.cos(theta))]  # Building the next monomer
                                                                          # using spherical coordinates
        while not check_monomer_distance(list_coo, next_coordinates):
            # The exact same process
            theta = random.choice(d_theta_range)
            phi = random.choice(d_theta_range)
            l = monomer_length

            next_coordinates = [last_coordinates[0] + (l * math.sin(theta) * math.cos(phi)),
                                last_coordinates[1] + (l * math.sin(theta) * math.sin(phi)),
                                last_coordinates[2] + (l * math.cos(theta))]

        last_coordinates = next_coordinates
        list_coo.append(next_coordinates)

    x = []
    y = []
    z = []

    for i in range(len(list_coo)):
        x.append(list_coo[i][0])
        y.append(list_coo[i][1])
        z.append(list_coo[i][2])

    plt.figure()

    ax = plt.axes(projection='3d')

    ax.plot3D(x, y, z, marker='.', mec='k', ms=7, mew=0.4)

    plt.title(f'3D representation of a polymer with {length} monomers')

    plt.tight_layout()
