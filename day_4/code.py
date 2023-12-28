import os

# Read lines from the file and return a matrix
file_path = os.path.join(os.path.dirname(__file__), 'doc.txt')

def read_lines_from_file(file_path):
    winning_numbers = []
    selected_numbers = []
    with open(file_path, 'r') as infile:
        for line in infile:
            new_line = line.strip().rsplit(' ')[2:]
            separator_index = new_line.index('|')
            winning_numbers.append([value for value in new_line[:separator_index] if value])
            selected_numbers.append([value for value in new_line[separator_index+1:] if value])

    return winning_numbers, selected_numbers


def get_points(winning_numbers, selected_numbers):
    n_matching_numbers = [sum(selected_number in winning_numbers[pos] for selected_number in list_numbers) 
                            for pos, list_numbers in enumerate(selected_numbers)]
    points = sum(2**(n-1) for n in n_matching_numbers if n > 0)

    return n_matching_numbers, points


def get_final_number_of_cards(winning_numbers, n_matching_numbers):
    number_of_cards = [1] * len(winning_numbers)
    
    for game_number, matches in enumerate(n_matching_numbers):
        # if there is at least one matching number in that game
        if matches > 0:
            current_cards = number_of_cards[game_number]
            for i in range(game_number + 1, game_number + matches + 1):
                # to the existing number of cards add the copies from current observed game
                number_of_cards[i] += current_cards
    
    return number_of_cards


# Part 1 - answer 15205
# which of the numbers you have appear in the list of winning numbers
# The first match makes the card worth one point and each match after the first doubles the point value of that card.
# How many points are they worth in total?
winning_numbers, selected_numbers = read_lines_from_file(file_path)
n_matching_numbers, points = get_points(winning_numbers, selected_numbers)
print("Number of points: ", points)

# Part 2 - answer 6189740
# scratchcards only cause you to win more scratchcards equal to the number of winning numbers you have
# you win copies of the scratchcards below the winning card equal to the number of matches
# how many total scratchcards do you end up with?
final_number_of_cards = get_final_number_of_cards(winning_numbers, n_matching_numbers)
print("The total number of cards is:", sum(final_number_of_cards))