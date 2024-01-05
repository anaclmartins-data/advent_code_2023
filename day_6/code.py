import os
import numpy as np
from functools import reduce


def read_time_distance(file_path):
    with open(file_path, 'r') as infile:
        for line in infile:
            new_line = line.strip().rsplit(' ')
            if 'time' in new_line[0].lower():
                time = [int(s) for s in new_line[1:] if s]
            else:
                distance = [int(s) for s in new_line[1:] if s]
        
        games = [[t, d] for t, d in zip(time, distance)]
        
    return games, time, distance


def ways_to_beat_record(games):
    ways_to_win = []
    for i, value in enumerate(games):
        # looking at the logic we want to solve for n**2 -t*n + d = 0
        coeff = [1, -value[0], value[1]]
        roots = np.roots(coeff)
        # I want all integers between roots
        ways_to_win.append(len([x for x in range(1, value[0]+1) if x > roots[1] and x < roots[0]]))
    
    return ways_to_win, reduce(lambda x, y: x*y, ways_to_win)


file_path = os.path.join(os.path.dirname(__file__), 'doc.txt')
# Part 1 - answer 6209190
# list with the time and the best distance
# For each ms holding down the button, the boat's speed increases by 1mm/ms
# determine the number of ways you can beat the record in each race and multiply them
games, times, distances = read_time_distance(file_path)
ways_to_win, mult_ways_to_win = ways_to_beat_record(games)
print("Part 1: The number of ways to win are", ways_to_win, "and multiplying them we have", mult_ways_to_win)

# Part 2 - answer 28545089
# There's really only one race - ignore the spaces between the numbers on each line.
new_games = [[int(''.join(str(t) for t in times)), int(''.join(str(d) for d in distances))]]
ways_to_win, mult_ways_to_win = ways_to_beat_record(new_games)
print("Part 2: The number of ways to win are", ways_to_win, "and multiplying them we have", mult_ways_to_win)