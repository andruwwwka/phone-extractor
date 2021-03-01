import re
from typing import Iterator, Set


class PhoneExtractor:
    """Логика поиска телефонов в теле страницы."""

    russia_phone_pattern = re.compile(r'(\s)?((7|8|\+7)?[\- ]?)(\(?((3|4|8)\d{2,4})\)?[\- ]?)([\d\- ]{5,10})')
    moscow_phone_pattern = re.compile(r'((7|8|\+7)?[\- ]?)(\(?((3|4|8)\d{2,4})\)?[\- ]?)?(\d{3}-\d{2}-\d{2})|(\d{1}-\d{2}-\d{2}-\d{2})')
    clean_phone = re.compile(r'-| ')

    @staticmethod
    def phone_is_valid(phone: str) -> bool:
        """
        Проверка телефона на валидность.

        По идее метод в будущем может обрастать логикой, поэтому он и вынесен в отдельную реализацию.
        Сейчас условно считается, что регулярные выражения корректно отбирают телефоны по формату
        написания, но попадает мусор - числовые последовательности, которых выдает их длина."""
        return len(phone) == 11

    @classmethod
    def extract_russia_phone_numbers(cls, html_page: str) -> Iterator[str]:
        """
        Поиск российских номеров телефонов в произвольной строке.
        
        Дополнительно производится нормализация телефонов путем унификации кода страны и исключением
        из результата лишних символов, такие как скобки и пробелы.
        """
        for phone_parts in cls.russia_phone_pattern.findall(html_page):
            phone = cls.clean_phone.sub('', f'8{phone_parts[4]}{phone_parts[6]}')
            if cls.phone_is_valid(phone):
                yield phone

    @classmethod
    def extract_moscow_phone_numbers(cls, html_page: str, ignore_phones: Set[str]) -> Iterator[str]:
        """
        Поиск московских номеров телефонов.

        Московские номера телефонов уже могли попасть в поиск по паттерну российских телефонов,
        поэтому для того, чтобы не возвращать их повторно, методу передается множество с телефонами,
        которые были отобраны по паттерну российских телефонов
        """
        for phone_parts in cls.moscow_phone_pattern.findall(html_page):
            if not any(phone_parts[i] not in {'', ' '} for i in range(5)):
                phone = cls.clean_phone.sub('', f'8495{phone_parts[5] or phone_parts[6]}')
                if cls.phone_is_valid(phone) and phone not in ignore_phones:
                    yield phone

    @classmethod
    def extract(cls, html_page: str) -> Iterator[str]:
        """
        Поиск телефонов в произвольной строке.

        Сначала отбираются российские телефоны и сохраняются во множестве, затем ищутся московские
        номер телефонов без кода города. Номера, которые уже были отобраны по паттерну российских
        номеров отбрасываются.
        """
        already_extracted: Set[str] = set()
        for phone in cls.extract_russia_phone_numbers(html_page):
            already_extracted.add(phone)
            yield phone
        for phone in cls.extract_moscow_phone_numbers(html_page, already_extracted):
            yield phone
