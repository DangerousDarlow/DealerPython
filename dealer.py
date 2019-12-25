import json
import random

def total_cards(cards):
    total = 0
    for card in cards:
        if 'count' in card:
            total += card['count']
        else:
            total += 1

    return total


def random_values(n):
    values = []
    for _ in range(n):
        values.append(random.random())

    return values


cards = {}
with open('cards.json') as cards_file:
    cards = json.load(cards_file)

players = {}
with open('players.json') as players_file:
    players = json.load(players_file)

print(random_values(5))