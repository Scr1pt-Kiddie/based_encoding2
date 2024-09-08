class InvalidBase(Exception):
    pass

class InvalidDigit(Exception):
    pass

class UnsignedInt:
    def __init__(self, value: int):
        if value < 0:
            raise ValueError("Value must be non-negative")
        self.value = value

class BasedNumber:
    def __init__(self, base: int):
        if base < 1:
            raise InvalidBase("Base must be greater than 0")
        self.base = base
        self.digits = []

    def add_digit(self, digit: int):
        if digit >= self.base:
            raise InvalidDigit("Digit must be smaller than the base")
        self.digits.append(digit)

    def convert(self, new_base: int):
        number = sum(d * (self.base ** i) for i, d in enumerate(reversed(self.digits)))
        self.digits = []
        self.base = new_base
        while number:
            self.digits.insert(0, number % new_base)
            number //= new_base

    def read(self):
        return self.digits.pop() if self.digits else 0

# Пример использования
def main():
    number = BasedNumber(10)
    number.add_digit(2)
    number.add_digit(5)
    print("Current base 10 digits:", number.digits)
    
    number.convert(2)
    print("Converted to base 2 digits:", number.digits)
    
    print("Read from base 2:", number.read())

main()

