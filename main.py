import random
import numpy as np
from matplotlib import pyplot as plt
import time
import math

start_time = time.time()
# The script was really slow to begin with. It was because every element in the list containing the coordinates was of
# type ndarray, and it took the function check_monomer_distance forever to iterate over all the elements. Eventually
# I figured it out and fixed it.


# Function that simulate a single polymer and returns the Radius (end to end distance) of said polymer
def single_polymer_sim(pol_len, d):
    if d == 2:  # Simulating a polymer using the 2D model

        d_theta_range = np.arange(0.0, 2 * np.pi, d_angle)  # Setting up discrete angle intervals

        list_coo = [[0, 0]]  # A list containing the coordinates of every monomer
        last_coordinates = [0, 0]  # Initializing point of origin

        for n_m in range(0, pol_len):  # Creating n_m (number of monomers) monomers

            theta = random.choice(d_theta_range)  # Randomly choose an angle from the discrete angle interval list
            l = monomer_length  # A dummy variable so the next line will be shorter and more readable

            next_coordinates = [last_coordinates[0] + (l * math.cos(theta)),  # Building the next monomer using polar
                                last_coordinates[1] + (l * math.sin(theta))]  # coordinates

            while not check_monomer_distance(list_coo, next_coordinates):  # Repeat until monomers do not collide
                # The exact same process
                theta = random.choice(d_theta_range)
                l = monomer_length

                next_coordinates = [last_coordinates[0] + (l * math.cos(theta)),
                                    last_coordinates[1] + (l * math.sin(theta))]

            last_coordinates = next_coordinates
            list_coo.append(next_coordinates)

        with open('coordinates.txt', 'w') as coordinates:  # Writing the coordinates from the list to a txt file,
            coordinates.write('X COOR\tY COOR\n')          # which is overwritten with every new polymer simulated.
            for point1 in list_coo:
                coordinates.write(f'{point1[0]:+.5f}\t{point1[1]:+.5f}\n')

        return math.dist(list_coo[-1], list_coo[0])  # Calculating and returning the Radius as end to end distance

    elif d == 3:  # The same process with minor adjustments for the 3D model

        d_theta_range = np.arange(0.0, 2 * np.pi, d_angle)  # Setting up discrete angle intervals for both theta and phi
        d_phi_range = np.arange(0.0, np.pi, d_angle)

        list_coo = [[0, 0, 0]]
        last_coordinates = [0, 0, 0]

        for n_m in range(0, pol_len):

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

        with open('coordinates.txt', 'w') as coordinates:
            coordinates.write('X COOR\tY COOR\tZ COOR\n')
            for point2 in list_coo:
                coordinates.write(f'{point2[0]:+.5f}\t{point2[1]:+.5f}\t{point2[2]:+.5f}\n')

        return math.dist(list_coo[-1], list_coo[0])


# Function that returns True if monomers do NOT collide
def check_monomer_distance(list_coo, next_coordinates):
    for coo in list_coo[:-1]:  # Goes through every monomer that had already been simulated except the last one
        if math.dist(next_coordinates, coo) < edge_diameter:  # If the distance between the monomer that
            return False                                      # would be created and the current monomer
    return True                                               # is smaller then edge_diameter return false


def plot_linear():
    plt.style.use('fivethirtyeight')

    plt.figure()
    plt.plot(polymer_lengths, mean_radius_list, marker='x', linestyle='-', lw=0.75, ms=10, color='#12639f')

    plt.title(f'Mean Radius Vs. Polymer Length with Monomer Length of {int(monomer_length)}, in {int(dim)}D')
    plt.xlabel('Polymer Length')
    plt.ylabel('Mean Radius')


def plot_hist():
    total_radii = len(well_done_radii)
    mean_radius1 = np.mean(well_done_radii)

    plt.style.use('fivethirtyeight')

    cm = plt.cm.get_cmap('plasma')

    plt.figure()  # Plotting the histogram

    n, bins, patches = plt.hist(well_done_radii, edgecolor='black', bins=50)
    col = (n - n.min()) / (n.max() - n.min())

    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))

    plt.axvline(mean_radius1, color='b', label='Mean Radius', linewidth=1.75)

    plt.legend()
    plt.title(
        f'Histogram for Polymers with {polymer_length} monomers, each has the length of {int(monomer_length)}, in {int(dim)}D')
    plt.xlabel('Radius ')
    plt.ylabel(f'Number of Radii [Total Number of Radii: {total_radii}]')

    plt.tight_layout()


def plot_std():
    plt.style.use('fivethirtyeight')

    plt.figure()
    plt.plot(polymer_lengths, std_list, marker='x', linestyle='-', lw=0.75, ms=10, color='#12639f')

    plt.title(f'Standard deviation Vs. Polymer Length with Monomer Length of {int(monomer_length)}, in {int(dim)}D')
    plt.xlabel('Polymer Length')
    plt.ylabel('Standard deviation')


with open('input.txt') as input_parameters:  # Reading input file as a list of lines
    list_parameters = input_parameters.read().splitlines()

# Converting input from txt to variables

for i1 in range(len(list_parameters)):
    list_parameters[i1] = list_parameters[i1][list_parameters[i1].index('=') + 1:].strip()  # Stripping everything left of '=' sign
    if list_parameters[i1][-1].isdigit():  # Converting strings to numbers, if needed
        list_parameters[i1] = float(list_parameters[i1])

list_parameters[0] = list_parameters[0][1:-1].split(', ')  # Converting PolymerLengths into a list

for i2 in range(len(list_parameters[0])):  # Converting PolymerLengths's elements to integers
    list_parameters[0][i2] = int(list_parameters[0][i2])

# Assigning variables
polymer_lengths = sorted(list_parameters[0])
monomer_length = list_parameters[1]
edge_diameter = list_parameters[2]
dim = list_parameters[3]
angle_interval = list_parameters[4]
mean_error = list_parameters[5]
max_tries = list_parameters[6]

d_angle = math.radians(angle_interval)  # Converting angle to radians

mean_radius_list = []  # A list that would be used to plot the linear graph
std_list = []  # A list that would be used to plot linear graph of Standard deviation Vs. polymer length

# Main program, for every length of polymer given
for polymer_length in polymer_lengths:

    radii = []  # A list that contains the radius of every polymer simulated
    last_mean_radius = 0

    print(f'Simulating polymers with {polymer_length} monomers. Please wait.\n')

    valid = False
    start_conv = time.time()
    while not valid:  # Repeat until the condition is met

        radius = single_polymer_sim(polymer_length, dim)  # Simulating a single polymer and returning the radius to the variable
        radii.append(radius)
        mean_radius = np.mean(radii)  # Calculating the arithmetic mean of all radii calculated
        condition = abs((mean_radius - last_mean_radius) / mean_radius)

        if condition < mean_error or len(radii) > max_tries:  # We could also stop if there have been more than max_tries Radii calculated
            valid = True
            if len(radii) > max_tries:
                print(
                    f'Warning: The Radius for polymer length {polymer_length} did not converge in {max_tries} tries\n')

        last_mean_radius = mean_radius

    print(f'Number of Radii calculated for polymer length {polymer_length} in this run: {len(radii)}')
    print(f'The Mean Radius of polymer length {polymer_length} took {time.time() - start_conv:.2f} seconds to converge\n')

    mean_radius_list.append(last_mean_radius)

    #  Writing to a txt file every radius that had been calculated in this run
    with open(f'radii_{int(dim)}d_N{polymer_length}_l{int(monomer_length)}.txt', 'a+') as radii_file:
        radii_file.seek(0)
        if radii_file.readline(5) != 'Radii':  # If it's a brand new file add a title
            radii_file.write('Radii\n')
        for item in radii:
            radii_file.write(f'{item:.5f}\n')

    # Getting all the Radii that have ever been calculated from txt file into a list
    well_done_radii = []

    with open(f'radii_{int(dim)}d_N{polymer_length}_l{int(monomer_length)}.txt') as radii_file:
        radii_raw = radii_file.readlines()

    for ele in radii_raw[1:]:
        well_done_radii.append(float(ele))

    std_list.append(np.std(well_done_radii))

    plot_hist()  # Plotting Histogram


plot_linear()  # Plotting Linear Graph

plot_std()  # Plotting a graph of std Vs. polymer length

print(f'Total execution time: {time.time() - start_time:.2f} seconds')