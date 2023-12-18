import requests
from requests import Response

class TheMoscowTimes:
    def __init__(self) -> None:
        self.__BASE_URL: str = 'https://www.themoscowtimes.com' 

    def get_by_category(self, category: str, page: int) -> dict:
        response: Response = requests.get(f'{self.__BASE_URL}/{category}/{(page - 1) * 18}')
        print(response.text)

    def search(self) -> dict:
        pass

if(__name__ == '__main__'):
    tmt: TheMoscowTimes = TheMoscowTimes()
    tmt.get_by_category(category='news', page=1)