# Простые исключения для ошибок
class BaseTooSmall(Exception):
    pass

class ValueBiggerThanBase(Exception):
    pass

class IntegerIsSigned(Exception):
    pass

# Класс для положительных целых чисел
class UnsignedInt:
    def __init__(self, value: int) -> None:
        if value < 0:
            raise IntegerIsSigned()  # Ошибка, если число отрицательное
        self._value = value  # Сохраняем число

    @property
    def value(self) -> int:
        return self._value  # Возвращаем значение

# Класс для баз (основ) систем счисления
class ValidBase:
    def __init__(self, value: UnsignedInt) -> None:
        if value.value < 1:
            raise BaseTooSmall()  # Ошибка, если база меньше 1
        self._value = value  # Сохраняем базу

    @property
    def value(self) -> UnsignedInt:
        return self._value  # Возвращаем базу

    def increase(self, n: UnsignedInt):
        self._value._value += n.value  # Увеличиваем значение базы

# Класс для цифр с учетом их базы
class BasedDigit:
    def __init__(self, base: ValidBase, value: UnsignedInt) -> None:
        if base.value.value <= value.value:
            raise ValueBiggerThanBase()  # Ошибка, если цифра больше базы
        self._base = base
        self._value = value

    @property
    def base(self) -> ValidBase:
        return self._base

    @property
    def value(self) -> UnsignedInt:
        return self._value

    def increase(self, n: UnsignedInt):
        self._value._value += n.value  # Увеличиваем цифру
        self._base._value._value += n.value  # Увеличиваем базу

# Класс для работы с числами
class BasedNumber:
    def __init__(self) -> None:
        self._digits = []  # Список для цифр
        self._base = ValidBase(UnsignedInt(1))  # Начальная база

    def digits(self):
        return iter(self._digits)  # Возвращаем список цифр

    @property
    def base(self):
        return self._base  # Возвращаем текущую базу

    def convert(self, new_base: ValidBase):
        if new_base == self.base:
            return  # Ничего не делаем, если база не меняется
        self_as_number = 0

        # Преобразуем число в десятичную форму
        for index, digit in enumerate(self._digits[::-1]):
            self_as_number += self._base.value.value ** index * digit.value

        # Преобразуем число в новую базу
        reversed_digits = []
        while self_as_number:
            reversed_digits.append(UnsignedInt(self_as_number % new_base.value.value))
            self_as_number //= new_base.value.value

        self._base = new_base  # Меняем базу
        self._digits = reversed_digits[::-1]  # Сохраняем цифры

    def write(self, based_digit: BasedDigit):
        if len(self._digits) == 0 and based_digit.value.value == 0:
            return  # Не записываем нули, если число пустое
        self.convert(based_digit.base)  # Преобразуем в базу цифры
        self._digits.append(based_digit.value)  # Добавляем цифру

    def read_digit(self, base: ValidBase) -> UnsignedInt:
        self.convert(base)  # Преобразуем в нужную базу
        try:
            return self._digits.pop()  # Возвращаем последнюю цифру
        except IndexError:
            return UnsignedInt(0)  # Если цифр нет, возвращаем 0
