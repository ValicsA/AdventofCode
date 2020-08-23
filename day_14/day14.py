"""
Advent of Code 2019 Day 14.
https://adventofcode.com/2019/day/14

@author Ákos Valics
"""
import math


def load_input(filename):
    """
    Loads the equations from the given file to a dictionary.

    :param filename: Name of the file, which contains the equations.

    :return: Dictionary of the equations.
    """
    equations = {}
    with open(filename) as f:
        for row in f.readlines():
            row = row.strip("\n").split("=>")
            product = (int(row[1].strip().split(" ")[0]), row[1].strip().split(" ")[1])
            ingredients = [(int(a.strip().split(" ")[0]), a.strip().split(" ")[1]) for a in row[0].split(",")]
            equations[product[1]] = (product[0], ingredients)

    return equations


def ore_required_for_fuel(equations, fuel):
    """
    Calculates how much ore is needed to produce n fuel. n is defined in fuel input.

    :param equations: Dict of equations.
    :param fuel: Number of fuels.

    :return: Ore required to produce n fuel.
    """
    ore = 0
    chemicals_needed = {"FUEL": fuel}
    chemicals_remained = {}
    for c in equations.keys():
        chemicals_remained[c] = 0

    while len(chemicals_needed) > 0:
        element = list(chemicals_needed.keys())[0]
        if chemicals_needed[element] <= chemicals_remained[element]:
            chemicals_remained[element] -= chemicals_needed[element]
            del chemicals_needed[element]
            continue

        should_be_created = chemicals_needed[element] - chemicals_remained[element]
        chemicals_remained[element] = 0
        del chemicals_needed[element]
        produced = equations[element][0]

        if (should_be_created // produced) * produced == should_be_created:
            multiplier = should_be_created // produced
        else:
            multiplier = math.ceil(should_be_created / produced)

        chemicals_remained[element] += (multiplier * produced) - should_be_created

        for chemical in equations[element][1]:
            if chemical[1] == "ORE":
                ore += chemical[0] * multiplier
            else:
                if chemical[1] in chemicals_needed.keys():
                    chemicals_needed[chemical[1]] += chemical[0] * multiplier
                else:
                    chemicals_needed[chemical[1]] = chemical[0] * multiplier

    return ore


def maximum_fuel_from_ore(equations, ore, ore_for_one_fuel):
    """
    Calculates how much fuel can be produced from n ore. n is defined in ore input.

    :param equations: Dict of equations.
    :param ore: Number of ore.
    :param ore_for_one_fuel: Number from which exactly one fuel can be produced.

    :return: Maximum fuel, which can be produced from n ore.
    """
    minimal_fuel = math.ceil(ore / ore_for_one_fuel)
    ore_for_fuel = ore_required_for_fuel(equations=equations, fuel=minimal_fuel)
    fuel_produced = minimal_fuel
    fuel_can_be_created = minimal_fuel

    while fuel_can_be_created > 0:
        fuel_can_be_created = (ore - ore_for_fuel) // ore_for_one_fuel
        fuel_produced += fuel_can_be_created
        ore_for_fuel = ore_required_for_fuel(equations=equations, fuel=fuel_produced)

    return fuel_produced


def main():
    """
    Main function. Calls the functions to solve the tasks of Advent of Code 2019 Day 14.
    First calculates how much ore is needed to produce one fuel,
    then calculates how much fuel can be produced from 1000000000000 ores.

    :return: None.
    """
    equations = load_input(filename="input_day14.txt")
    ore_for_one_fuel = ore_required_for_fuel(equations=equations, fuel=1)
    print(f"Amount of ORE required to create 1 FUEL: {ore_for_one_fuel}")

    given_ore = 1000000000000
    fuel_produced = maximum_fuel_from_ore(equations=equations, ore=given_ore, ore_for_one_fuel=ore_for_one_fuel)
    print(f"Maximal amount of FUEL, which can be produced from {given_ore} ORE: {fuel_produced}")


if __name__ == '__main__':
    main()
