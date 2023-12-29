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


def get_new_seeds_mapped(seeds):
    new_seeds = []
    for s in range(0, len(seeds), 2):
        new_seeds.append([seeds[s], seeds[s+1]])
    
    return new_seeds


def get_minimum_location(new_seeds, mapping_indicators):
    min_mapped_seed = []
    for seed in new_seeds:
        new_mapped_ranges_list = [seed]
        for key, mapping in mapping_indicators.items():
            mapped_ranges_list = new_mapped_ranges_list
            new_mapped_ranges_list = []
            for map_range in mapped_ranges_list:
                new_mapped_values = []
                for m in mapping:
                    upper_seed_bound = map_range[0]+map_range[1]-1
                    map_conversion = m[2]-m[0]
                    # seed range falls within mapping
                    if map_range[0] >= m[0] and upper_seed_bound <= m[1]:
                        new_mapped_values.append([map_range[0]+map_conversion, map_range[1]])
                        break
                    # seed range has a lower bound outside mapping range, but an upper bound within mapping range
                    elif map_range[0] < m[0] and upper_seed_bound >= m[0] and upper_seed_bound <= m[1]:
                        new_mapped_values.append([map_range[0], m[0]-map_range[0]])
                        mapped_ranges_list.append([m[2], upper_seed_bound-m[0]])
                        break
                    # seed range has an upper bound outside mapping range, but a lower bound within mapping range
                    elif upper_seed_bound > m[1] and map_range[0] >= m[0] and map_range[0] <= m[1]:
                        new_mapped_values.append([map_range[0]+map_conversion, m[1]-map_range[0]+1])
                        mapped_ranges_list.append([m[1]+1,upper_seed_bound-m[1]])
                        break
                
                # seed range falls outside mapping bounds
                if new_mapped_values == []:
                    new_mapped_values.append([map_range[0], map_range[1]])
    
                new_mapped_ranges_list.extend(new_mapped_values)
    
        min_mapped_seed.append(min(new_mapped_ranges_list, key=lambda x: x[0])[0])

    return min(min_mapped_seed)



# Read lines from the file and return a matrix
file_path = os.path.join(os.path.dirname(__file__), 'doc.txt')

# Part 1 - answer 199602917
# find the lowest location number that corresponds to any of the initial seeds
seeds, mapping_indicators = get_seeds_and_mapping(file_path)
locations = get_mapped_locations(seeds, mapping_indicators)
print("The lowest location number is", min(locations))

# Part 2 - answer 2254686
# the seeds: line actually describes ranges of seed numbers
# Within each pair, the first value is the start of the range and the second value is the length of the range
new_seeds = get_new_seeds_mapped(seeds)
absolute_min_location = get_minimum_location(new_seeds, mapping_indicators)
print("absolute min mapped", absolute_min_location)