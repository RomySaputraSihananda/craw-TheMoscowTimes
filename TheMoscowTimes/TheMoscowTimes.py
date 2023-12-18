import requests
import time

from hashlib import md5;
from json import dumps
from pyquery import PyQuery
from requests import Response
from concurrent.futures import ThreadPoolExecutor

from TheMoscowTimes.helpers import Parser, logging, Datetime

class TheMoscowTimes:
    def __init__(self) -> None:
        self.__BASE_URL: str = 'https://www.themoscowtimes.com'
        self.__parser: Parser = Parser()
        self.__datetime: Datetime = Datetime()
        
        self.__result: dict = {}
        self.__result['date_now']: str = None;
        self.__result['keyword']: str = None;
        self.__result['category']: str = None;
        self.__result['page']: int = None;
        self.__result['range_datetime']: dict = None;
        self.__result['data']: list = []

    def __get_urls(self, **kwargs) -> list:
        html = kwargs.get('html', None)
        if(html): return [PyQuery(a).attr('href') for a in self.__parser.execute(html, 'a')]

        json: dict = kwargs.get('json')

        return [json['data'][i]['url'] for i in range((json['page'] - 1) * 10, json['page'] * 10)]

    def __get_data_page(self, url: str) -> None:
        response: Response = requests.get(url)

        logging.info(url)

        parser: PyQuery = self.__parser.execute(response.text, 'html')

        article = parser('.article__block.article__block--html.article__block--column').text().replace('\n', '')
        title = parser('h1').text()

        self.__result['data'].append({
            'id': md5(title.encode()).hexdigest(),
            "title": title,
            "lang": parser.attr('lang'),
            "create_at": parser('.row-flex.gutter-2 .byline__datetime.timeago').attr('datetime'),
            "url": url,
            "url_thumbnail": parser('.article__featured-image.featured-image img').attr('src'),
            'autor': None if not parser('.row-flex.gutter-2 .byline__author__name').text() else parser('.row-flex.gutter-2 .byline__author__name').text(),
            "desc": article[:100] + '...',
            "article": article
        })

    def get_by_category(self, category: str, page: int) -> dict:
        response: Response = requests.get(f'{self.__BASE_URL}/{category}/{(page - 1) * 18}')

        urls: list = self.__get_urls(html=response.text)

        self.__result['date_now']: str = self.__datetime.now();
        self.__result['category']: str = category;
        self.__result['page']: int = page;
        
        with ThreadPoolExecutor(len(urls)) as executor:
            executor.map(self.__get_data_page, urls)

        return self.__result


    def search(self, keyword: str, page: int, **kwargs) -> dict:
        params: dict = {
            "query": keyword,
            "section": kwargs.get('category', None),
            "from": kwargs.get('from_date', None),
            "to": kwargs.get('to_date', None),
        }

        response: Response = requests.get(f'https://www.themoscowtimes.com/api/search', params=params)

        if(response.status_code != 200): return

        urls: list = self.__get_urls(json={'data': response.json(), 'page': page})

        self.__result['date_now']: str = self.__datetime.now();
        self.__result['keyword']: str = params['query'];
        self.__result['category']: str = params['section'];
        self.__result['page']: int = page;
        self.__result['range_datetime']: dict = {
            "from": params['from'],
            "to": params['to']
        };

        with ThreadPoolExecutor(len(urls)) as executor:
            executor.map(self.__get_data_page, urls)

        return self.__result

if(__name__ == '__main__'):
    start = time.perf_counter()

    tmt: TheMoscowTimes = TheMoscowTimes()
    data: dict = tmt.get_by_category(category='news', page=1)
    # data: dict = tmt.search(keyword='war', page=1, category='news', from_date='2023-12-01', to_date='2023-12-30')

    with open('test_data.json', 'w') as file:
        file.write(dumps(data, indent=2, ensure_ascii=False))

    logging.info(time.perf_counter() - start)