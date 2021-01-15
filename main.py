import logging
import collections
import requests
import bs4
import csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('sp')

ParseResult = collections.namedtuple(
    'ParseResult',
    (
        'brand_name',
        'url',
        'cate_name',
        'cena_name',
        'karta_name'
    ),
)

HEADERS = (
    'Товар',
    'Артикул',
    'Категория',
    'Цена без карты',
    'Цена с картой'
)


class Client:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0'
            'Accept-Language:' 'ru',
        }
        self.result = []

    def load_page(self):
        url = 'https://stroypark.su/catalog/sad-i-ogorod/setki-sadovyie-ukryivnoy-material/setki'
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def parse_page(self, text: str):
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select('div.c-good-item-content')
        for block in container:
            self.parse_block(block=block)

    def parse_block(self, block):

        url_block = block.select_one('div.c-good-item-code')
        if not url_block:
            logger.error('no url_block')
            return

        url = url_block.select_one('strong')
        if not url:
            logger.error('no href')
            return

        name_block = block.select_one('div.c-good-item-title')
        if not name_block:
            logger.error(f'no name_block on {url}')

        brand_name = name_block.select_one('a')
        if not brand_name:
            logger.error(f'no brand_name {url}')
            return

        url = url.text
        url = url.replace('<strong>  ', '</strong>').strip()
        brand_name = brand_name.text
        brand_name = brand_name.replace('<a href="/good/12922501">', '</a>').strip()

        cena_block = block.select_one('div.c-good-item-prices')
        if not cena_block:
            logger.error(f'no name_block on')

        cena_name = cena_block.select_one('strong')
        if not cena_name:
            logger.error(f'no brand_name')
            return
        cena_name = cena_name.text
        cena_name = cena_name.replace('<strong>  ', '</strong>').strip()

        karta_block = block.select_one('div.c-good-item-prices')
        if not karta_block:
            logger.error(f'no name_block on')

        karta_name = karta_block.select_one('strong.o-highlight')
        if not karta_name:
            logger.error(f'no brand_name')
            return
        karta_name = karta_name.text
        karta_name = karta_name.replace('<strong>  ', '</strong>').strip()

        self.result.append(ParseResult(
            url=url,
            cate_name='Сад и огород — Сетки садовые,укрывной материал — Сетки',
            brand_name=brand_name,
            cena_name=cena_name,
            karta_name=karta_name
        ))

        logger.debug('%s, %s, %s, %s, s%', brand_name, url, cena_name, karta_name)
        logger.debug('-' * 100)

    def save_result(self):
        path = '/media/mugichu/Transcend/pythonProject1/test.csv'
        with open(path, 'w') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADERS)
            for item in self.result:
                writer.writerow(item)

    def run(self):
        text = self.load_page()
        self.parse_page(text=text)
        logger.info(f'Получили{len(self.result)}элементов')
        self.save_result()


if __name__ == '__main__':
    parser = Client()
    parser.run()
