import unittest

from phone_extractor import PhoneExtractor


class TestPhoneExtractor(unittest.TestCase):
    """Тесты функционала извлечения телефона изкода страницы (произвольного текста)."""

    def test_phone_validator_with_correct_phone(self):
        """Позитивный тест метода проверки телефона на валидность."""
        self.assertTrue(PhoneExtractor.phone_is_valid('84956237070'))

    def test_phone_validator_with_incorrect_phone(self):
        """Негативный тест метода проверки телефона на валидность."""
        self.assertFalse(PhoneExtractor.phone_is_valid('849562370701'))

    def test_russian_phone_with_7(self):
        """Тест российских номеров телефонов, начинающихся с 7."""
        html_string = 'Звонить по телефону 74950210211, 7(495)0210212, , а также 7 (495) 021-02-13'
        result = [phone for phone in PhoneExtractor.extract_russia_phone_numbers(html_string)]
        expected = ['84950210211', '84950210212', '84950210213']
        self.assertListEqual(result, expected)

    def test_russian_phone_with_plust_7(self):
        """Тест российских номеров телефонов, начинающихся с +7."""
        html_string = 'Звонить по телефону +74950210211, +7(495)0210212, , а также +7 (495) 021-02-13'
        result = [phone for phone in PhoneExtractor.extract_russia_phone_numbers(html_string)]
        expected = ['84950210211', '84950210212', '84950210213']
        self.assertListEqual(result, expected)

    def test_russian_phone_with_8(self):
        """Тест российских номеров телефонов, начинающихся с 8."""
        html_string = 'Звонить по телефону 84950210211, 8(495)0210212, , а также 8 (495) 021-02-13'
        result = [phone for phone in PhoneExtractor.extract_russia_phone_numbers(html_string)]
        expected = ['84950210211', '84950210212', '84950210213']
        self.assertListEqual(result, expected)

    def test_russian_phone_without_country_code(self):
        """Тест российских телефонов без кода страны."""
        html_string = 'Звонить по телефону 4950210211, (895)0210212, , а также (395) 021-02-13'
        result = [phone for phone in PhoneExtractor.extract_russia_phone_numbers(html_string)]
        expected = ['84950210211', '88950210212', '83950210213']
        self.assertListEqual(result, expected)

    def test_russian_phone_with_invalid_region_code(self):
        """
        Тест россиских телефонов с невалидным кодом региона.
        
        Вспоминаем из справочной информации в ReadMe.md, что коды регионов доступны в форматах:
        3xx, 4xx и 8xxx.
        """
        html_string = 'Звонить по телефону 87950210211, 8(595)0210212, , а также 8 (995) 021-02-13'
        result = [phone for phone in PhoneExtractor.extract_russia_phone_numbers(html_string)]
        expected = []
        self.assertListEqual(result, expected)

    def test_moscow_phone_without_city_code(self):
        """Тест для московских номеров (без кода города)."""
        html_string = 'Звонить по телефону 456-33-22, 4-55-55-33, , а также 021-02-13'
        result = [phone for phone in PhoneExtractor.extract_moscow_phone_numbers(html_string, {})]
        expected = ['84954563322', '84954555533', '84950210213']
        self.assertListEqual(result, expected)

    def test_mixed_russian_and_moscow_numbers(self):
        """Тест на распознавание в тексте разных телефонов: москва без кода и формат российского телефона."""
        html_string = 'Звонить по телефону 7488456-33-22, 4-55-55-33, , а также 021-02-13'
        result = [phone for phone in PhoneExtractor.extract(html_string)]
        expected = ['84884563322', '84954555533', '84950210213']
        self.assertListEqual(result, expected)

    def test_mixed_russian_and_moscow_numbers_with_intersection(self):
        """Тест на распознавание в тексте разных форматов при условии, что имеются два одинаковых московских номера."""
        html_string = 'Звонить по телефону 7(495)455-55-33, 4-55-55-33, , а также 021-02-13'
        result = [phone for phone in PhoneExtractor.extract(html_string)]
        expected = ['84954555533', '84950210213']
        self.assertListEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
