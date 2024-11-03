#!/usr/bin/env python3

import requests
from utils import get_rating, initialize_db, insert_rating, PLAYERS


def main():
    initialize_db()
    for player in PLAYERS:
        url = f'https://lichess.org/@/{player}'
        r = requests.get(url).text
        name_data = get_rating(r, player)
        insert_rating(name_data)


if __name__ == "__main__":
    main()
