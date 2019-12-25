import json
import random

def get_value(obj, key):
    if key in obj:
        return obj[key]
    else:
        obj[key] = 0
        return 0


def change_value(obj, key, change):
    initial = get_value(obj, key)
    obj[key] = initial + change


def inc_value(obj, key):
    change_value(obj, key, 1)


def dec_value(obj, key):
    change_value(obj, key, -1)
    

def get_count(card):
    return get_value(card, 'count')


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


def get_random_values(n):
    values = []
    for _ in range(n):
        values.append(random.random())

    return values


if __name__ == "__main__":
    players = {}
    with open('players.json') as players_file:
        players = json.load(players_file)

    cards = {}
    with open('cards.json') as cards_file:
        cards = json.load(cards_file)

    for player in players:
        for card in cards:
            player[card['name']] = 0

    for iteration in range(10000):
        cards = {}
        with open('cards.json') as cards_file:
            cards = json.load(cards_file)

        random_values = get_random_values(len(players))

        for player_index in range(len(players)):
            player = players[player_index]
            calculate_probabilities(cards)

            card = draw_card(cards, random_values[player_index])
            inc_value(player, card['name'])
            dec_value(card, 'count')

    print(json.dumps(players, indent=2))