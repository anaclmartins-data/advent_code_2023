import os
import re
import itertools
from collections import namedtuple

def read_lines_from_file(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()

def extract_game_number(line):
    match = re.search(r'Game (\d+):', line)
    return int(match.group(1)) if match else None

def extract_cube_counts(comp):
    red_count = int(''.join(re.findall(r'(\d+) red', comp)) or 0)
    green_count = int(''.join(re.findall(r'(\d+) green', comp)) or 0)
    blue_count = int(''.join(re.findall(r'(\d+) blue', comp)) or 0)
    return red_count, green_count, blue_count

def sum_possible_ids(lines, red=12, green=13, blue=14):
    seen_plays = set()
    removed_games = set()
    game_results = []

    for line in lines:
        game_number = extract_game_number(line)
        if game_number is not None:
            seen_plays.add(game_number)
            line = re.sub(r'Game \d+:', '', line)

        for comp in line.split(';'):
            red_count, green_count, blue_count = extract_cube_counts(comp)

            if red_count > red or green_count > green or blue_count > blue:
                removed_games.add(game_number)
            
            game_results.append(GameResult(game_number, red_count, green_count, blue_count))

    possible_games = seen_plays - removed_games
    return sum(possible_games), game_results


def get_sum_power_sets(game_results):
    sum_power = 0

    # calculate the max for each color for each game
    for _, plays in itertools.groupby(sorted(game_results), key=lambda x: x.game_number):
        plays_list = list(plays)
        if plays_list:
            max_red = max(play.red_count for play in plays_list)
            max_green = max(play.green_count for play in plays_list)
            max_blue = max(play.blue_count for play in plays_list)

            sum_power += max_red * max_green * max_blue

    return sum_power


# Read lines from the file
file_path = os.path.join(os.path.dirname(__file__), 'doc.txt')
lines = read_lines_from_file(file_path)

# Part 1
# Define a named tuple to represent game results
GameResult = namedtuple('GameResult', ['game_number', 'red_count', 'green_count', 'blue_count'])
sum_games, game_results = sum_possible_ids(lines)
print('The sum is', sum_games)

# Part 2
# what is the fewest number of cubes of each color that could have been in the bag to make the game possible?
# What is the sum of the power of these sets?
sum_power = get_sum_power_sets(game_results)
print('The sum of the power of these sets is', sum_power)