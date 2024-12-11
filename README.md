# config_3
Гаврилюк Алексей ИКБО-42-23
# Задание (Вариант 6)
Разработать инструмент командной строки для учебного конфигурационного языка, синтаксис которого приведен далее.
Этот инструмент преобразует текст из входного формата в выходной.
Синтаксические ошибки выявляются с выдачей сообщений.
Входной текст на учебном конфигурационном языке принимается из стандартного ввода.
Выходной текст на языке xml попадает в стандартный вывод.
Однострочные комментарии:

\ Это однострочный комментарий. "\n"
Словари:
{
  имя = значение,
  имя = значение,
  имя = значение,
  ...
}
Имена:
 [_a-zA-Z]+
Значения:
  Числа.
  Словари.
Объявление константы на этапе трансляции:
  def имя = значение;
Вычисление константного выражения на этапе трансляции (инфиксная форма), пример:
  #(имя + 1)

Результатом вычисления константного выражения является значение.
Для константных вычислений определены операции и функции:
  1. Сложение.
  2. Вычитание.
  3. Умножение.
  4. sqrt().
  5. min().
Все конструкции учебного конфигурационного языка (с учетом их возможной вложенности) должны быть покрыты тестами.
Необходимо показать 3 примера описания конфигураций из разных предметных областей.
