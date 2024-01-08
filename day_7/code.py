import os
from recordtype import recordtype


def read_hands(file_path, with_j=False):
    hands_details = []
    card_rankings_with_j = {'A':13, 'K':12, 'Q':11, 'J':0, 'T':9, '9':8, '8':7, '7':6, '6':5, '5':4, '4':3, '3':2, '2':1}
    card_rankings = {'A':13, 'K':12, 'Q':11, 'J':10, 'T':9, '9':8, '8':7, '7':6, '6':5, '5':4, '4':3, '3':2, '2':1}

    with open(file_path, 'r') as infile:
        for line in infile:
            cards = line.strip().rsplit(' ')[0]
            # transform a string like 'KK677' to [1,1,8,7,7]
            if not with_j:
                card_mapping = [card_rankings[char] for char in cards if char in card_rankings]
            else:
                card_mapping = [card_rankings_with_j[char] for char in cards if char in card_rankings_with_j]

            hands_details.append(hand_info(cards, card_mapping, int(line.strip().rsplit(' ')[1]), [], 1))
    
    return hands_details


def get_hands_strength(hands_details, with_j=False):

    for hand in hands_details:
        count_by_card = {'A':0, 'K':0, 'Q':0, 'J':0, 'T':0, '9':0, '8':0, '7':0, '6':0, '5':0, '4':0, '3':0, '2':0}

        for card in hand.cards:
            if card in count_by_card:
                count_by_card[card] += 1

        # take the values from the dict that are not 0
        if not with_j or count_by_card.get('J') == 5:
            hand.strength = [v for k,v in count_by_card.items() if v!= 0]
        else:
            hand.strength = [v for k,v in count_by_card.items() if v!= 0 and k!='J']

        hand.strength.sort(reverse=True)

        # if any 'J' exists then add the corresponding number of J's to the first element of the list
        if with_j and count_by_card.get('J') > 0 and count_by_card.get('J') != 5:
            hand.strength[0] = hand.strength[0] + count_by_card.get('J')

    hands_details.sort(key=lambda x: (x.strength[:2], x.card_mapping), reverse=True)

    return hands_details


def get_rank_total_winnings(hands_details):
    max_rank = len(hands_details)
    total_winnings = 0
    
    for i in range(max_rank):
        hands_details[i].rank = max_rank - i
        total_winnings += hands_details[i].rank * hands_details[i].bet

    return hands_details, total_winnings


file_path = os.path.join(os.path.dirname(__file__), 'doc.txt')
hand_info = recordtype('Hand', 'cards card_mapping bet strength rank')
# Part 1 - answer 250347426
# goal: order them based on the strength of each hand. If hands are tied, compare the first card in each hand. If tied, second card, etc
# hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2
# Each hand wins an amount equal to its bid multiplied by its rank (1 is the last player)
# What are the total winnings?
hands_details = read_hands(file_path)
hands_details = get_hands_strength(hands_details)
hands_details, total_winnings = get_rank_total_winnings(hands_details)

print('The total winnings is', total_winnings)

# Part 2 - answer 251224870
# J cards are now the weakest individual cards
# QJJQ2 is now considered four of a kind
# for the purpose of breaking ties between two hands of the same type, J is always treated as J
hands_details_j = read_hands(file_path, with_j=True)
hands_details_j = get_hands_strength(hands_details_j, with_j=True)
hands_details_j, total_winnings_j = get_rank_total_winnings(hands_details_j)
print('The total winnings with J as lowest is', total_winnings_j)