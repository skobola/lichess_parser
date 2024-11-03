#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import date
from typing import Dict

conn = sqlite3.connect('chess_rating.db')

c = conn.cursor()

SQL_CREATE_TABLE = """CREATE TABLE IF NOT EXISTS rating (
                    Name text,
                    Bullet text,
                    Blitz text,
                    Rapid text,
                    Date text
                    )"""

c.execute(SQL_CREATE_TABLE)

players = ['Evgeniy1989', 'Pyrog_Ivan']


def get_rating(source, nick:str) -> Dict:
    """Parse lichess.com for 1 player and return data in dict"""
    name = {'nickname': nick, 'Bullet': None, 'Blitz': None, 'Rapid': None}
    soup = BeautifulSoup(source, 'lxml')
    article = soup.find_all('span')
    for art in article:
        if art.span:
            try:
                ratio = art.rating.strong.text.replace('?', "")
                ratio = int(ratio) if ratio else None
                name[f'{art.h3.text}'] = f'{ratio}'
            except Exception as e:
                print(e)
    return name


def insert_data(data: Dict):
    """Insert collected data to DB"""
    with conn:
        c.execute(
            'INSERT INTO rating VALUES (:Name, :Bullet, :Blitz, :Rapid, :Date)',
           {
               'Name': name_data['nickname'],
               'Bullet': name_data['Bullet'],
               'Blitz': name_data['Blitz'],
               'Rapid': name_data['Rapid'],
               'Date': date.today()
                        }
                        )


for player in players:
    url = f'https://lichess.org/@/{player}'
    r = requests.get(url).text
    name_data = get_rating(r, player)
    insert_data(name_data)

conn.close()
