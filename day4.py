"""Problem statement: https://adventofcode.com/2019/day/4"""
import re

DAY4_INPUT = '206938-679128'


def is_password_valid_part1(password: str) -> bool:
    """Return whether a password has a valid form.

    Requirements:
    * 6-digit number
    * two adjacent digits are the same
    * going from left to right, digits do not decrease"""
    # is it exactly 6 digits?
    len_and_digits_re = r'\d\d\d\d\d\d'
    if not re.fullmatch(len_and_digits_re, password):
        return False
    # does some digit repeat at least once?
    repeated_digit_re = r'.*(1{2}|2{2}|3{2}|4{2}|5{2}|6{2}|7{2}|8{2}|9{2}|0{2}).*'
    if not re.fullmatch(repeated_digit_re, password):
        return False
    # do the digits never decrease?
    marker = 0
    for digit in password:
        if int(digit) < marker:
            return False
        marker = int(digit)
    return True


def is_password_valid_part2(password: str) -> bool:
    """Return whether a password has a valid form.

    Requirements:
    * simple validity criteria from problem part 1
    * additionally, the two adjacent matching digits must not be part of a larger group of matching
      digits"""
    # check simple validity criteria first
    if not is_password_valid_part1(password):
        return False
    # check extended validity
    found_double_digit = False
    for num in range(10):
        if str(num) * 2 in password and str(num) * 3 not in password:
            found_double_digit = True
    if not found_double_digit:
        return False
    return True


def solve_part1(num_range: str) -> int:
    """Return the number of valid passwords within num_range (given as a string 'XXXXXX-YYYYYY').

    Use the simple validity criteria from problem part 1."""
    start, stop = num_range.split('-')
    start = int(start)
    stop = int(stop)
    total = 0
    for password in range(start, stop+1):
        password = str(password)
        if is_password_valid_part1(password):
            total += 1
    return total


def solve_part2(num_range: str) -> int:
    """Return the number of valid passwords within num_range (given as a string 'XXXXXX-YYYYYY').

    Use the extended validity criteria from problem part 2."""
    start, stop = num_range.split('-')
    start = int(start)
    stop = int(stop)
    total = 0
    for password in range(start, stop + 1):
        password = str(password)
        if is_password_valid_part2(password):
            total += 1
    return total


if __name__ == '__main__':
    answer = solve_part1(DAY4_INPUT)
    print(f'{answer} different passwords within the range {DAY4_INPUT} meet the Part 1 criteria.')
    answer = solve_part2(DAY4_INPUT)
    print(f'{answer} different passwords within the range {DAY4_INPUT} meet the Part 2 criteria.')
