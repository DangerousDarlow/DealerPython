import json
import random

def get_count(card):
    if 'count' in card:
        return card['count']
    else:
        card['count'] = 1
        return 1


def get_total(cards):
    total = 0
    for card in cards:
        total += get_count(card)

    return total


def calculate_probabilities(cards):
    total = get_total(cards)
    for card in cards:
        count = get_count(card)
        card['probability'] = count / total


def draw_card(cards, random):
    cumulative_probability = 0
    for card in cards:
        cumulative_probability += card['probability']
        if cumulative_probability >= random:
            return card


def random_values(n):
    values = []
    for _ in range(n):
        values.append(random.random())

    return values


if __name__ == "__main__":
    cards = {}
    with open('cards.json') as cards_file:
        cards = json.load(cards_file)

    players = {}
    with open('players.json') as players_file:
        players = json.load(players_file)

    randoms = random_values(len(players))

    for index in range(len(players)):
        print('index', index, 'random', randoms[index])

        player = players[index]
        calculate_probabilities(cards)
        print(json.dumps(cards, indent=2))

        card = draw_card(cards, randoms[index])
        player['card'] = card
        print(json.dumps(player, indent=2))

        count = get_count(card)
        card['count'] = count -1
        print()
        print()