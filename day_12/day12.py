"""
Advent of Code 2019 Day 12.
https://adventofcode.com/2019/day/12

@author Ákos Valics
"""
import argparse
from math import gcd

import numpy as np


class Moons:

    def __init__(self, filename):
        """
        Initialization of Moons class. Loads coordinates from a file and creates and array which contains velocities.

        :param filename: Input file which contains the coordinate information.
        """
        self.coordinates = self.load_coordinates(filename=filename)
        self.velocities = np.zeros(self.coordinates.shape, dtype=int)

    @staticmethod
    def lcm(a, b):
        """
        Calculates the least common multiple of the two input values.

        :param a: Input 1.
        :param b: Input 2.

        :return: Least common multiple of a and b.
        """
        return (a * b) // gcd(a, b)

    @staticmethod
    def load_coordinates(filename):
        """
        Loads coordinate information from a given file to a numpy array.

        :param filename: Name of the file which contains the coordinate information.

        :return: Numpy array of the coordinates.
        """
        coordinates = np.array([], dtype=int)
        with open(filename) as f:
            for row in f.readlines():
                row = row.strip("\n<>").replace(" ", "").replace("=", ",").split(",")
                coordinates = np.append(coordinates, np.asarray(row[1::2]).astype(int))

        return np.reshape(coordinates, (int(coordinates.size/3), 3))

    def simulate_one_motion_step(self):
        """
        Simulates one motion step. First applies gravity and updates the velocities of the moons,
        then applies velocity and updates the coordinates of every moon.

        :return: None
        """
        checked_moons = []
        moon_1_counter = 0
        moon_2_counter = 0
        for moon_1 in self.coordinates:
            if moon_1_counter == 4:
                moon_1_counter = 0
            for moon_2 in self.coordinates:
                if moon_2_counter == 4:
                    moon_2_counter = 0
                if moon_1_counter == moon_2_counter or moon_2_counter in checked_moons:
                    moon_2_counter += 1
                else:
                    for i in range(moon_2.size):
                        if moon_1[i] > moon_2[i]:
                            self.velocities[moon_1_counter][i] -= 1
                            self.velocities[moon_2_counter][i] += 1
                        elif moon_1[i] < moon_2[i]:
                            self.velocities[moon_1_counter][i] += 1
                            self.velocities[moon_2_counter][i] -= 1
                    moon_2_counter += 1
            checked_moons.append(moon_1_counter)
            moon_1_counter += 1

        self.coordinates += self.velocities

    def calculate_energy(self):
        """
        Calculates the potential, kinetic and total energy of each moon.

        :return: Numpy array which contains potential, kinetic and total energy of each moon.
        """
        potential = np.sum(np.abs(self.coordinates), axis=1).reshape((4, 1))
        kinetic = np.sum(np.abs(self.velocities), axis=1).reshape((4, 1))
        total = potential * kinetic
        energy = np.concatenate((potential, kinetic, total), axis=1)

        return energy

    def determine_circulation_time(self):
        """
        Determines the circulation time of the moons in every axis and then calculates the least common multiple of them
        to get the number of steps (circulation time) after every moon returns to its initial state.

        :return: Circulation time.
        """
        init_x = tuple(self.coordinates[:, 0]) + tuple(self.velocities[:, 0])
        init_y = tuple(self.coordinates[:, 1]) + tuple(self.velocities[:, 1])
        init_z = tuple(self.coordinates[:, 2]) + tuple(self.velocities[:, 2])
        step = 1
        flags = [None, None, None]

        while True:
            self.simulate_one_motion_step()
            if init_x == (tuple(self.coordinates[:, 0]) + tuple(self.velocities[:, 0])) and flags[0] is None:
                flags[0] = step
            if init_y == tuple(self.coordinates[:, 1]) + tuple(self.velocities[:, 1]) and flags[1] is None:
                flags[1] = step
            if init_z == tuple(self.coordinates[:, 2]) + tuple(self.velocities[:, 2]) and flags[2] is None:
                flags[2] = step
            if None not in flags:
                break
            step += 1
        circulation_time = self.lcm(self.lcm(flags[0], flags[1]), flags[2])

        return circulation_time


def main(args):
    """
    Main function. Creates an instance of Moons class, then calls its functions to solve the tasks of
    Advent of Code Day 12.

    :param args: Arguments.

    :return: None.
    """
    moons = Moons(filename=args.input_file)

    if args.simulate_part_1:
        for i in range(args.simulation_steps):
            moons.simulate_one_motion_step()
        energy = moons.calculate_energy()
        energy_of_the_system = np.sum(energy, axis=0)[2]
        print(f"Total energy of the system is: {energy_of_the_system}\n")

    if args.simulate_part_2:
        print("Calculating circulation times ...\n")
        moons.__init__(filename=args.input_file)
        circulation_time = moons.determine_circulation_time()
        print(f"Steps after every planet returns to its initial state: {circulation_time}")


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', default="input_day12.txt",
                        help="Input file, which contains the coordinate information.")
    parser.add_argument('--simulation_steps', type=int, default=1000,
                        help="Number of steps in the first part of the task.")
    parser.add_argument('--simulate_part_1', type=bool, default=True,
                        help="Whether to simulate the first part of the task or not.")
    parser.add_argument('--simulate_part_2', type=bool, default=True,
                        help="Whether to simulate the second part of the task or not.")
    args = parser.parse_args()

    return args


if __name__ == '__main__':
    arguments = create_parser()
    main(args=arguments)
