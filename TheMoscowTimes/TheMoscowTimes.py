import requests
import time

from json import dumps
from pyquery import PyQuery
from requests import Response
from concurrent.futures import ThreadPoolExecutor

from TheMoscowTimes.helpers import Parser, logging

class TheMoscowTimes:
    def __init__(self) -> None:
        self.__BASE_URL: str = 'https://www.themoscowtimes.com'
        self.__parser: Parser = Parser()
        
        self.__result: dict = {}
        self.__result['data']: list = []

    def __get_urls(self, html: str) -> list:
        return [PyQuery(a).attr('href') for a in self.__parser.execute(html, 'a')]

    def __get_data_page(self, url: str) -> None:
        response: Response = requests.get(url)

        logging.info(url)

        parser: PyQuery = self.__parser.execute(response.text, 'html')

        article = parser('.article__block.article__block--html.article__block--column').text().replace('\n', '')

        self.__result['data'].append({
            "title": parser('h1').text(),
            "lang": parser.attr('lang'),
            "create_at": parser('.row-flex.gutter-2 .byline__datetime.timeago').attr('datetime'),
            "url": url,
            "url_thumbnail": parser('.row-flex.gutter-2 .article__featured-image.featured-image img').attr('src'),
            'autor': None if not parser('.row-flex.gutter-2 .byline__author__name').text() else parser('.row-flex.gutter-2 .byline__author__name').text(),
            "desc": article[:100] + '...',
            "article": article
        })

    def get_by_category(self, category: str, page: int) -> dict:
        response: Response = requests.get(f'{self.__BASE_URL}/{category}/{(page - 1) * 18}')

        urls: list = self.__get_urls(response.text)
        
        with ThreadPoolExecutor(len(urls)) as executor:
            executor.map(self.__get_data_page, urls)

        return self.__result


    def search(self, keyword: str, page: int) -> dict:
        response: Response = requests.get(f'https://www.themoscowtimes.com/api/search?query={keyword}')
        print(response)

if(__name__ == '__main__'):
    start = time.perf_counter()

    tmt: TheMoscowTimes = TheMoscowTimes()
    # data: dict = tmt.get_by_category(category='news', page=1)
    data: dict = tmt.search(keyword='news', page=1)

    # with open('test_data.json', 'w') as file:
    #     file.write(dumps(data, indent=2, ensure_ascii=False))

    logging.info(time.perf_counter() - start)