from bs4 import BeautifulSoup
import requests
import sqlite3
from datetime import date
import os

cur_dir = os.getcwd()

conn = sqlite3.connect('chess_rating.db')

c = conn.cursor()

# c.execute("""CREATE TABLE rating (
#             Name text,
#             Bullet text,
#             Blitz text,
#             Rapid text,
#             Date text
#             )""")

Jack_link = 'https://lichess.org/@/Evgeniy1989'
Ivan_link = 'https://lichess.org/@/Pyrog_Ivan'

Jack_nick = Jack_link.split('/')[-1]
Ivan_nink = Ivan_link.split('/')[-1]



source_jack = requests.get(Jack_link).text
source_ivan = requests.get(Ivan_link).text


def get_rating(source, name):

    soup = BeautifulSoup(source, 'lxml')

    article = soup.find_all('span')
    nickname = name
    name = {}
    for art in article:
        if art.span:
            try:
                rating = (art.rating.strong.text).replace('?', '')
                name[f'{(art.h3.text)}'] = f'{rating}'
            except Exception as e:
                print(e)
    name['nickname'] = f'{nickname}'
    return name


Jack = get_rating(source_jack, Jack_nick)
Ivan = get_rating(source_ivan, Ivan_nink)

def insert_data(name):
    with conn:
        c.execute(f'INSERT INTO rating VALUES (:Name, :Bullet, :Blitz, :Rapid, :Date)',
           {'Name': name['nickname'], 'Bullet': name['Bullet'], 'Blitz': name['Blitz'],'Rapid': name['Rapid'], 'Date': date.today()})


insert_data(Jack)
insert_data(Ivan)

conn.close()