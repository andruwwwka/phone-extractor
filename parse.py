import concurrent.futures
import logging
import urllib.request
from typing import List

from data_provider import JSONFileData
from phone_extractor import PhoneExtractor


logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
_data_provider = JSONFileData()


class ParserRunner:
    """Реализация взаимодействия со страницами."""

    @staticmethod
    def parse_phones(page_url: str) -> List[str]:
        """Получение страниц и передача их контента для поиска телефонов."""
        with urllib.request.urlopen(page_url, timeout=15) as response:
            response = response.read().decode(response.headers.get_content_charset())
            return [phone for phone in PhoneExtractor.extract(response)]

    @classmethod
    def run(cls) -> None:
        """Запуск процесса парсинга."""
        phone_numbers: List[str] = []
        logging.info('Start processing')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(cls.parse_phones, page_url): page_url for page_url in _data_provider.get_pages()}
            for future in concurrent.futures.as_completed(futures):
                page_url = futures[future]
                try:
                    phones_for_url = future.result()
                    logging.info(f'For url {page_url} was founded phones: {phones_for_url}')
                    phone_numbers.extend(phones_for_url)
                except BaseException:
                    logging.exception(f'Error while processing url: {page_url}')
        _data_provider.process_phone_numbers(phone_numbers)
        logging.info('See results in file ./json_data/phone.json')


if __name__ == '__main__':
    ParserRunner.run() 
