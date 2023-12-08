# Advent of Code - Day 1 - Part 1
# On each lin'e', the calibration value = first digit + last digit (in that order) to form a single two-digit number
# What is the sum of all of the calibration values?

import os
import re

def read_lines_from_file(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()

def calculate_calibration_value(line):
    first_digit_match = re.search(r'\d', line)
    last_digit_match = re.search(r'\d(?=\D*$)', line)
    if last_digit_match:
        return int(str(first_digit_match.group()) + str(last_digit_match.group()))
    return 0

def apply_word_digit_mapping(line, word_digit_mapping):
    for word, replacement in word_digit_mapping.items():
        line = line.replace(word, replacement)
    return line

file_path = os.path.join(os.path.dirname(__file__), 'doc.txt')
lines = read_lines_from_file(file_path)

# Part 1
sum_digits_part1 = sum(calculate_calibration_value(line) for line in lines)
print('Part 1: The sum of all the calibration values is {}'.format(sum_digits_part1))

# Part 2
word_digit_mapping = {'one': 'o1e', 'two': 't2o', 'three': 't3e', 'four': 'f4r', 'five': 'f5e', 'six': 's6x',
                      'seven': 's7n', 'eight': 'e8t', 'nine': 'n9e'}

sum_digits_part2 = sum(calculate_calibration_value(apply_word_digit_mapping(line, word_digit_mapping)) for line in lines)
print('Part 2: The correct sum of all the calibration values is {}'.format(sum_digits_part2))