import argparse
import copy
import json
import random
import requests

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


def get_random_values_from_random_org(n):
    print(f'requesting {n} random numbers from random.org')

    response = requests.post(
        'https://api.random.org/json-rpc/2/invoke',
        json={
            "jsonrpc": "2.0",
            "method": "generateDecimalFractions",
            "params": {
                "apiKey": f"{args.api_key}",
                "n": n,
                "decimalPlaces": 4,
                "replacement": True
            },
            "id": 1
        }
    )

    if response.status_code != 200:
        raise f'Random.org returned response {response.status_code}, {response.content}'

    return response.json()['result']['random']['data']


def get_random_values(n):
    if args.api_key != None:
        return get_random_values_from_random_org(n)

    values = []
    for _ in range(n):
        values.append(random.random())

    return values


def initialise_player_data():
    for player in players:
        player['last'] = 'none'
        player['consecutive'] = 0

        # Cards are initialised with 0 value to ensure the same display order for all players
        for card in cards:
            player[card['name']] = 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser('draw cards for The Resistance: Avalon and show draw data')
    parser.add_argument('games', type=int, help='number of games per session')
    parser.add_argument('--iterations', metavar='itr', type=int, default=1, help='number of iterations, default 1')
    parser.add_argument('--api-key', metavar='key', type=str, help='API key for random.org. If not None then random values are obtained from random.org.')
    args = parser.parse_args()

    cards = {}
    with open('cards.json') as cards_file:
        cards = json.load(cards_file)

    players = {}
    with open('players.json') as players_file:
        players = json.load(players_file)

    initialise_player_data()

    random_values = get_random_values(len(players) * args.games * args.iterations)
    random_values_index = 0

    for game in range(args.games):
        iteration_cards = copy.deepcopy(cards)

        for player_index in range(len(players)):
            player = players[player_index]
            calculate_probabilities(iteration_cards)

            card = draw_card(iteration_cards, random_values[random_values_index])
            random_values_index += 1
            inc_value(player, card['name'])

            # track if drawn card for this player is the same as last draw
            last = player['last']
            if last == card['name']:
                inc_value(player, 'consecutive')
            else:
                player['last'] = card['name']

            dec_value(card, 'count')

    print(json.dumps(players, indent=2))
