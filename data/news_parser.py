import requests
from bs4 import BeautifulSoup


class NewsVillageParser(object):
    """Данный класс предназначен для поиска нужных новостей

    """

    def __init__(self):
        url = 'http://www.the-village.ru/news'

    # get_html(self):
        r = requests.get(url)
        self.html = r.text

    def news_in_business(self):
        """Первая новость от Village

        :return:
        """
        soup = BeautifulSoup(self.html, 'lxml')
        news = soup.find_all('div', class_='just-bl')
        i = 0
        d = {}
        for new in news:
            i += 1
            link_news ='http://www.the-village.ru' + new.find('a', class_='post-link').get('href')
            try:
                title = new.find('h2', class_='post-title').text
            except Exception:
                title = new.find('h3', class_='post-title').text
            d[link_news]=str(title)
            if i == 3:
                break
        return d


def main():
    n = NewsVillageParser()
    di = n.news_in_business()
    for d in di:
        print(d, di[d])


if __name__ == '__main__':
    main()