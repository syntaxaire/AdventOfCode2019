"""Problem statement: https://adventofcode.com/2019/day/1"""
from typing import List


def fuel_required(mass: int) -> int:
    """Return the amount of fuel required to launch a module with the given mass."""
    fuel = mass // 3 - 2
    return fuel if fuel >= 0 else 0


def calc_modules_fuel(masses: List[int]) -> int:
    """Return the total amount of fuel required to launch the given module masses."""
    fuel = 0
    for module in masses:
        fuel += fuel_required(module)
    return fuel


def calc_modules_with_fuel(masses: List[int]) -> int:
    """Return the total amount of fuel required to launch the given module masses, taking the
    added mass of the fuel into account."""
    total_fuel = 0
    for module in masses:
        subtotal_fuel = 0
        continuing_mass = module
        while continuing_mass > 0:
            this_fuel = fuel_required(continuing_mass)
            subtotal_fuel += this_fuel
            continuing_mass = this_fuel
        total_fuel += subtotal_fuel
    return total_fuel


if __name__ == '__main__':
    with open('day1.input', 'r') as inputs:
        module_masses = [int(module) for module in inputs.readlines()]
    modules_fuel = calc_modules_fuel(module_masses)
    print(f'(Part 1): The total fuel needed for the modules is {modules_fuel}.')
    modules_fuel_fuel = calc_modules_with_fuel(module_masses)
    print(f'(Part 2) The actual fuel needed to launch the modules is {modules_fuel_fuel}.')
