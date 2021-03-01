import json
from abc import ABCMeta, abstractmethod
from typing import List


class DataInterface(metaclass=ABCMeta):
    """
    Общий интерфейс для класса работы с данными.
    
    Подразумевается, что для изменения источника данных, откуда забирается список страниц для
    поиска телефонов и изменения поведения обработки полученных телефонов реализуется новый 
    класс провайдера данных и им подменяется реализованный в рамках данной задачи класс JSONFileData.
    """

    @abstractmethod
    def get_pages(self) -> List[str]:
        """Интерфейс метода для получения страниц, по которым будет вестить работа."""
        ...

    @abstractmethod
    def process_phone_numbers(self, phones: List[str]) -> None:
        """Интерфейс метода-обработчика списка полученных телефонов."""
        ...


class JSONFileData(DataInterface):
    """Провайдер данных из json-файла."""

    def get_pages(self) -> List[str]:
        """Реализация метода получения списка страниц из json-файла."""
        with open('json_data/pages.json') as pages:
            pages_list = json.load(pages)
        return pages_list

    def process_phone_numbers(self, phones: List[str]) -> None:
        """Реализация метода обработки телефонов, полученных в результате поиска."""
        with open('json_data/phones.json', 'w') as phones_file:
            json.dump(list(set(phones)), phones_file)
