import re
import sys
import xml.etree.ElementTree as ET
from math import sqrt

# Шаблоны для парсинга
COMMENT_PATTERN = r"\\.*"  # Комментарии
DICT_PATTERN = r"\{([^}]*)\}"  # Словари
DEF_PATTERN = r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.*?);"  # Определения констант
EXPR_PATTERN = r"#\((.*?)\)"  # Выражения для вычисления констант


def clean_function_arguments(expr):
    """Удаляет лишние скобки вокруг аргументов функций (например, sqrt((25)) -> sqrt(25))"""
    # Регулярное выражение для нахождения функций с аргументами
    func_pattern = r"(\w+)\((.*)\)"

    # Находим все функции вида sqrt(что-то)
    matches = re.finditer(func_pattern, expr)

    # Для каждой найденной функции убираем лишние скобки вокруг аргументов
    for match in matches:
        func_name = match.group(1)
        argument = match.group(2)

        # Убираем лишние скобки вокруг аргумента
        argument = remove_extra_parentheses(argument)

        # Вставляем обратно исправленный аргумент
        expr = expr.replace(match.group(0), f"{func_name}({argument})")

    return expr


def remove_extra_parentheses(expr):
    """Удаляет лишние внешние скобки из выражения."""
    while expr.startswith('(') and expr.endswith(')'):
        inner_expr = expr[1:-1]
        if inner_expr.count('(') == inner_expr.count(')'):
            expr = inner_expr
        else:
            break
    return expr


def evaluate_expression(expr, context):
    """Вычисляет выражение, подставляя значения из контекста."""
    expr = expr.strip()

    # Подставляем значения переменных в выражение
    for key, value in context.items():
        expr = expr.replace(key, str(value))

    # Очищаем скобки вокруг функций
    expr = clean_function_arguments(expr)

    try:
        # Выполняем вычисление выражения
        result = eval(expr, {"__builtins__": None}, {"sqrt": sqrt, "min": min})
        return result
    except Exception as e:
        raise ValueError(f"Ошибка при вычислении выражения '{expr}': {e}")


def parse_dict(content, context):
    """Парсит строку словаря и возвращает XML элемент."""
    dict_elem = ET.Element("dict")

    # Разбираем строки внутри словаря
    entries = content.split(',')
    for entry in entries:
        entry = entry.strip()
        if '=' in entry:
            key, value = entry.split('=', 1)
            key = key.strip()
            value = value.strip()

            # Если значение — это выражение (например #(a + 5))
            if value.startswith("#(") and value.endswith(")"):
                value = evaluate_expression(value[2:-1], context)
            # Если это число
            elif value.isdigit():
                value = int(value)
            # Если это ссылка на константу
            elif value in context:
                value = context[value]

            # Добавляем элемент в XML
            entry_elem = ET.SubElement(dict_elem, "entry")
            ET.SubElement(entry_elem, "key").text = key
            ET.SubElement(entry_elem, "value").text = str(value)

    return dict_elem


def parse_definitions(text, context):
    """Парсит определения констант и сохраняет их в контексте."""
    for match in re.finditer(DEF_PATTERN, text):
        name = match.group(1)
        value = match.group(2).strip()

        # Если значение содержит выражение, вычисляем его
        if value.startswith("#(") and value.endswith(")"):
            value = evaluate_expression(value[2:-1], context)
        elif value.isdigit():
            value = int(value)

        context[name] = value


def parse_input(input_text):
    """Парсит входной текст и возвращает XML структуру."""
    context = {}  # Контекст для хранения значений констант
    root = ET.Element("config")

    # Удаляем комментарии
    input_text = re.sub(COMMENT_PATTERN, '', input_text)

    # Парсим определения констант
    parse_definitions(input_text, context)

    # Парсим все словари
    for match in re.finditer(DICT_PATTERN, input_text):
        dict_elem = parse_dict(match.group(1), context)
        root.append(dict_elem)

    return ET.ElementTree(root)


def main():
    """Основная функция программы."""
    # Чтение данных из стандартного ввода
    input_text = sys.stdin.read()

    try:
        # Парсим входной текст
        tree = parse_input(input_text)

        # Записываем результат в XML файл
        with open("output1.xml", "w", encoding="utf-8") as output_file:
            tree.write(output_file, encoding='unicode', xml_declaration=True)

        print("XML файл успешно сохранен как 'output1.xml'.")
    except Exception as e:
        print(f"Ошибка: {e}")  # Выводим ошибку, если она произошла


if __name__ == "__main__":
    main()