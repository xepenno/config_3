import unittest
import xml.etree.ElementTree as ET


class ConfigToXMLTests(unittest.TestCase):
    def normalize_xml(self, xml_string):
        """
        Преобразует строку XML в отформатированное дерево для унификации.
        """
        try:
            root = ET.fromstring(xml_string)
            return ET.tostring(root, encoding="unicode")
        except ET.ParseError as e:
            raise ValueError(f"Ошибка парсинга XML: {e}")

    def compare_xml_files(self, xml_file, expected_content):
        """
        Сравнивает содержимое XML-файла с ожидаемым XML.
        """
        # Читаем содержимое файла
        with open(xml_file, "r", encoding="utf-8") as file:
            actual_content = file.read().strip()

        # Нормализуем оба XML для сравнения
        normalized_actual = self.normalize_xml(actual_content)
        normalized_expected = self.normalize_xml(expected_content)

        # Сравниваем нормализованные строки
        self.assertEqual(
            normalized_actual,
            normalized_expected,
            f"Файл {xml_file} не совпал с ожидаемым содержимым!"
        )

    def test_case_1(self):
        xml_file = r"C:\Users\Алексей\PycharmProjects\config_3\output1.xml"
        expected_content = """<config>
    <dict>
        <entry>
            <key>x</key>
            <value>10</value>
        </entry>
        <entry>
            <key>y</key>
            <value>30</value>
        </entry>
        <entry>
            <key>z</key>
            <value>5.0</value>
        </entry>
    </dict>
</config>"""
        self.compare_xml_files(xml_file, expected_content)

    def test_case_2(self):
        xml_file = r"C:\Users\Алексей\PycharmProjects\config_3\output2.xml"
        expected_content = """<config>
    <dict>
        <entry>
            <key>key1</key>
            <value>14.0</value>
        </entry>
        <entry>
            <key>key2</key>
            <value>-10</value>
        </entry>
        <entry>
            <key>key3</key>
            <value>410</value>
        </entry>
        <entry>
            <key>key4</key>
            <value>14.142135623730951</value>
        </entry>
        <entry>
            <key>key5</key>
            <value>#(min(x</value>
        </entry>
    </dict>
</config>"""
        self.compare_xml_files(xml_file, expected_content)

    def test_case_3(self):
        xml_file = r"C:\Users\Алексей\PycharmProjects\config_3\output3.xml"
        expected_content = """<config>
    <dict>
        <entry>
            <key>x</key>
            <value>25</value>
        </entry>
        <entry>
            <key>y</key>
            <value>6.0</value>
        </entry>
        <entry>
            <key>z</key>
            <value>50</value>
        </entry>
    </dict>
</config>"""
        self.compare_xml_files(xml_file, expected_content)


if __name__ == "__main__":
    unittest.main()
