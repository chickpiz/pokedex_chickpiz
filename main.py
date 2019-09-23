# coding=UTF-8
# main.py
import requests
from pokemon import Pokemon
from bs4 import BeautifulSoup
from html_table_parser import parser_functions
from constants.TYPES import TYPES
from constants.ABILITIES import ABILITIES


class PokemonBuilder:

    def __init__(self):
        self.pokemon = Pokemon()

    def crawl_basics(self):
        text = get_html("https://pokemon.fandom.com/ko/wiki/파르셀_(포켓몬)")
        soup = BeautifulSoup(text, features="html.parser")

        body = []
        body_table = [[], []]

        for div in soup("div"):
            if "class" in div.attrs:
                # 포켓몬의 이름
                if "name-ko" in div["class"]:
                    self.pokemon.Basic.name = div.text.strip()

                # 도감 번호
                if "index" in div["class"]:
                    self.pokemon.Basic.number = div.text[3:]  # No. 제거

        # 기본 정보가 담긴 표(body_table) 추출
        tables = soup.find_all("table")
        for table in tables:
            if "class" in table.attrs:
                if "body" in table.attrs["class"]:
                    body = parser_functions.make2d(table)
                    print(body)

        type_i = 0
        j = 1
        for item in body:
            if type_i % 2 == j % 2:
                for values in item:
                    if "도감 번호" in values:
                        body_table[0].append(values)
                        j += 0.5
                    else:
                        body_table[1].append(values)
            else:
                for columns in item:
                    body_table[0].append(columns)
            type_i += 1

        print(body_table)

        # 표에서 정보 추출
        for key in body_table[0]:
            index = body_table[0].index(key)
            if key == "타입":
                type_i = 0
                while True:
                    type_i += 1
                    if body_table[1][index][0:type_i] in TYPES:
                        self.pokemon.Basic.types.append(body_table[1][index][0:type_i])
                        self.pokemon.Basic.types.append(body_table[1][index][type_i:])
                        break
            elif key == "분류":
                self.pokemon.Basic.species = body_table[1][index]
            elif key == "특성":
                abilities_i = 0
                while True:
                    abilities_i += 1
                    if body_table[1][index][0:abilities_i] in ABILITIES:
                        self.pokemon.Battle.ord_abilities.append(body_table[1][index][0:abilities_i])
                        self.pokemon.Battle.ord_abilities.append(body_table[1][index][abilities_i:])
                        break
        print(self.pokemon.Basic.types)
        print(self.pokemon.Battle.ord_abilities)

    def dump_to_json(self, filename):
        pass


def get_html(url):
    html = ""
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text

    return html


if __name__ == "__main__":
    builder = PokemonBuilder()
    builder.crawl_basics()

