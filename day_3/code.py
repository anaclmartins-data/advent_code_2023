import os
from collections import namedtuple


def get_numbers_symbols(file_path):
    with open(file_path,"rt") as infile:
        number_coordinates = namedtuple('NumberCoordinates', ['x', 'y', 'number'])
        symbol_coordinates = namedtuple('SymbolCoordinates', ['x', 'y', 'symbol'])
        number_coordinates_list = []
        symbol_coordinates_list = []
        numbers = ''
        symbols = ''

        for y, line in enumerate(infile):
            for x, char in enumerate(line.rstrip('\n')):
                # if the previous char was a number/symbol but the current isn't then we want to add the number/symbol to our list of observed numbers/symbols
                if numbers and not char.isnumeric():
                    number_coordinates_list.append(number_coordinates(x - len(numbers), y, numbers))
                    numbers = ''
                elif symbols and (char == '.' or char.isnumeric()):
                    symbol_coordinates_list.append(symbol_coordinates(x - len(symbols), y, symbols))
                    symbols = ''

                # if the current char is a number/symbol then we want to add it to the number/symbol string
                if char.isnumeric():
                    numbers += char
                elif char != '.':
                    symbols += char

            # catch cases where either a number or a symbol are at the last position of a line
            if numbers != '':
                number_coordinates_list.append(number_coordinates(x - len(numbers), y, numbers))
            if symbols != '':
                symbol_coordinates_list.append(symbol_coordinates(x - len(symbols), y, symbols))

    return number_coordinates_list, symbol_coordinates_list


def get_part_numbers(number_coordinates_list, symbol_coordinates_list):
    part_numbers = []
    part_symbols = []

    for symbol_position in symbol_coordinates_list:
        pos = 0
        while pos < len(number_coordinates_list):
            if (
                number_coordinates_list[pos].x - 1 <= symbol_position.x <= number_coordinates_list[pos].x + len(str(number_coordinates_list[pos].number))
                    and number_coordinates_list[pos].y - 1 <= symbol_position.y <= number_coordinates_list[pos].y + 1
            ):
                # add numbers that are part numbers
                part_numbers.append(int(number_coordinates_list[pos].number))
                # remove the number from the list
                number_coordinates_list.remove(number_coordinates_list[pos])
                # add symbols that have numbers nearby
                part_symbols.append(symbol_position)
            else:
                pos += 1

    return part_numbers, part_symbols


def get_gear_numbers(part_numbers, part_symbols):
    gear_numbers = []

    for pos in range(len(part_symbols) - 1):
        # if we have * check if the next position is the same *. If so, take the two numbers in the same position and multiply them
        if (part_symbols[pos].symbol == '*' 
                and part_symbols[pos+1].symbol == '*'
                and part_symbols[pos].x == part_symbols[pos+1].x
                and part_symbols[pos].y == part_symbols[pos+1].y
            ):
            gear_numbers.append(part_numbers[pos]*part_numbers[pos+1])
    
    return gear_numbers


# Read lines from the file and return a matrix
file_path = os.path.join(os.path.dirname(__file__), 'doc.txt')

number_coordinates_list, symbol_coordinates_list = get_numbers_symbols(file_path)

# Part 1 - answer 553825
# any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. 
# What is the sum of all of the part numbers in the engine schematic?
part_numbers, part_symbols = get_part_numbers(number_coordinates_list, symbol_coordinates_list)
print("The sum of all part numbers is", sum(part_numbers))

# Part 2 - answer 93994191
# A gear is any * symbol that is adjacent to exactly two part numbers. 
# Its gear ratio is the result of multiplying those two numbers together.
# What is the sum of all of the gear ratios in your engine schematic?
gear_numbers = get_gear_numbers(part_numbers, part_symbols)
print("The sum of the gears is:", sum(gear_numbers))