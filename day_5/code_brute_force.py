import os
import re


def get_seeds_and_mapping(file_path):
    mapping_indicators = {}
    seeds = []
    indicator = ''
    with open(file_path, 'r') as infile:
        data = infile.read()

    sections = re.split(r'(.*)\n', data)

    for line in sections:
        if line:
            new_line = line.rsplit(' ')
            
            if new_line[0] == 'seeds:':
                seeds = [int(i) for i in new_line[1:]]
            else:
                if not new_line[0].isnumeric():
                    indicator = new_line[0]
                    mapping_list = []
                else:
                    # [lower_source, upper_source, lower_dest, lower_dest]
                    mapping_list.append([
                                            int(new_line[1]),
                                            int(new_line[1])+int(new_line[2])-1,
                                            int(new_line[0]),
                                            int(new_line[0])+int(new_line[2])-1
                                        ])
                    
                mapping_indicators[indicator] = sorted(mapping_list)

    return seeds, mapping_indicators


def get_mapped_locations(seeds, mapping_indicators):
    locations = []

    for seed in seeds:
        new_value = seed
        for key, mapping in mapping_indicators.items():
            for m in mapping:
                if new_value >= m[0] and new_value <= m[1]:
                    new_value = new_value - m[0] + m[2]
                    break
        locations.append(new_value)

    return locations


def get_new_seeds(seeds):
    new_seeds = set()
    for s in range(0, len(seeds), 2):
        new_seeds.update(range(seeds[s], seeds[s] + seeds[s + 1] - 1))

    return new_seeds



# Read lines from the file and return a matrix
file_path = os.path.join(os.path.dirname(__file__), 'doc.txt')

# Part 1 - answer 199602917
# find the lowest location number that corresponds to any of the initial seeds
seeds, mapping_indicators = get_seeds_and_mapping(file_path)
locations = get_mapped_locations(seeds, mapping_indicators)

print("The lowest location number is", min(locations))

# Part 2 - answer
# the seeds: line actually describes ranges of seed numbers
# Within each pair, the first value is the start of the range and the second value is the length of the range
# does not run in a timely manner...
new_seeds = get_new_seeds(seeds)
print(new_seeds)
new_locations = get_mapped_locations(new_seeds, mapping_indicators)

print(min(new_locations))