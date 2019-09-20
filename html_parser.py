# html_parser.py
import requests
from bs4 import BeautifulSoup


def get_html(url):
    html = ""
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text

    return html

def crawl_basics():
    result = []
    text = get_html("https://pokemon.fandom.com/ko/wiki/%EC%9D%B4%EC%83%81%ED%95%B4%EC%94%A8_(%ED%8F%AC%EC%BC%93%EB%AA%AC)")
    soup = BeautifulSoup(text, features="html.parser")

    for div in soup('div'):
        if 'class' in div.attrs:
            # 포켓몬의 이름
            if 'name-ko' in div['class']:
                print(div.get_text())

            # 도감 번호
            if 'index' in div['class']:
                print(div.get_text()[3:]) # No. 제거


if __name__ == "__main__":
    crawl_basics()

