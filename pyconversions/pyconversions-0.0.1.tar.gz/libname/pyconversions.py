
"""For distances of certain lengths"""

"""For Inches including ranges
    for Meters, Kilometres etc"""


class Inches:
    def __init__(self, num):
        self.num = num

    def toFeet(self) -> float:
        return self.num/12

    def toYard(self) -> float:
        return self.num/36

    def toMillimeters(self) -> float:
        return self.num * 25.4

    def toCentimeter(self) -> float:
        return self.num * 2.54

    def toDecimeter(self) -> float:
        return self.num * 0.254

    def toDecameter(num: float) -> float:
        return num * 0.00254

    def toHectometer(self) -> float:
        return self.num * 0.000254

    def toMeter(self) -> float:
        return self.num * 0.0254

    def toKilometers(self) -> float:
        return self.num * 0.0000254


"""For Feet including ranges
    for Meters, Kilometers etc """


class Feet:
    def __init__(self, num):
        self.num = num

    def toInches(self):
        return self.num*12

    def toYard(self):
        return self.num / 3

    def toMillimeters(self):
        return self.num * 304.8

    def toCentimeter(self):
        return self.num * 30.48

    def toDecimeter(self):
        return self.num / 0.32808

    def toDecameter(self):
        return self.num * 0.03048

    def toHectometer(self):
        return self.num * 0.003048

    def toMeter(self):
        return self.num * 0.3048

    def toKilometer(self):
        return self.num * 0.0003048


"""For Yards including ranges
for Meters, Kilometers, etc."""


class Yard:
    def __init__(self, num):
        self.num = num

    def toInches(self):
        return self.num * 36

    def toFeet(self):
        return self.num * 3

    def toMillimeters(self):
        return self.num * 914.4

    def toCentimeter(self):
        return self.num * 91.44

    def toDecimeter(self):
        return self.num * 9.144

    def toDecameter(self):
        return self.num * 0.09144

    def toHectometer(self):
        return self.num * 0.009144

    def toMeter(self):
        return self.num * 0.9144

    def toKilometer(self):
        return self.num * 0.0009144


"""For Millimeters, including ranges
for Metres, Kilometers, etc"""


class Millimeter:
    def __init__(self, num):
        self.num = num

    def toInches(self):
        return self.num * 0.03937008

    def toFeet(self):
        return self.num * 0.00328084

    def toYard(self):
        return self.num * 0.001093613

    def toCentimeter(self):
        return self.num * 0.1

    def toDecimeter(self):
        return self.num * 0.01

    def toDecameter(self):
        return self.num * 0.0001

    def toHectometer(self):
        return self.num * 0.00001

    def toMeter(self):
        return self.num * 0.001

    def toKilometer(self):
        return self.num * 0.000001


"""For Centimeters, including ranges
from Meters, Kilometers, etc"""


class Centimeter:
    def __init__(self, num):
        self.num = num

    def toInches(self):
        return self.num * 0.3937008

    def toFeet(self):
        return self.num * 0.03280839993

    def toYard(self):
        return self.num * 0.01093613

    def toMillimeter(self):
        return self.num * 10

    def toDecimeter(self):
        return self.num * 0.1

    def toDecameter(self):
        return self.num * 0.001

    def toHectometer(self):
        return self.num * 0.0001

    def toMeter(self):
        return self.num * 0.01

    def toKilometer(self):
        return self.num * 0.00001


"""For Decimeter, including ranges
for Meter, Kilometer, etc"""


class Decimeter:
    def __init__(self, num):
        self.num = num

    def toInches(self):
        return self.num * 3.937008

    def toFeet(self):
        return self.num * 0.328084

    def toYard(self):
        return self.num * 0.1093613

    def toMillimeters(self):
        return self.num * 100

    def toCentimeter(self):
        return self.num * 10

    def toDekameter(self):
        return self.num * 0.01

    def toHectometer(self):
        return self.num * 0.001

    def toMeter(self):
        return self.num * 0.1

    def toKilometer(self):
        return self.num * 0.0001


"""For Decameter including ranges
for Meter, Kilometer, etc"""


class Decameter:
    def __init__(self, num):
        self.num = num

    def toInch(self):
        return self.num * 393.7008

    def toFeet(self):
        return self.num * 32.8084

    def toYard(self):
        return self.num * 10.93613

    def toMillimeter(self):
        return self.num * 10000

    def toCentimeter(self):
        return self.num * 1000

    def toDecimeter(self):
        return self.num * 100

    def toHectometer(self):
        return self.num * 0.1

    def toMeter(self):
        return self.num * 10

    def toKilometer(self):
        return self.num * 0.01


"""For Hectometer including ranges
for Meter, Kilometer, etc"""


class Hectometer:
    def __init__(self, num):
        self.num = num

    def toInches(self):
        return self.num * 3937.008

    def toFeet(self):
        return self.num * 328.084

    def toYard(self):
        return self.num * 109.3613

    def toMillimeters(self):
        return self.num * 100000

    def toCentimeter(self):
        return self.num * 10000

    def toDecimeter(self):
        return self.num * 1000

    def toDecameter(self):
        return self.num * 10

    def toMeter(self):
        return self.num * 100

    def toKilometer(self):
        return self.num * 0.1


class Meter:
    def __init__(self, num):
        self.num = num

    def toInches(self):
        return self.num * 39.37008

    def toFeet(self):
        return self.num * 3.28084

    def toYard(self):
        return self.num * 1.093613

    def toMillimeter(self):
        return self.num * 1000

    def toCentimeter(self):
        return self.num * 100

    def toDecimeter(self):
        return self.num * 10

    def toDecameter(self):
        return self.num * 0.1

    def toHectometer(self):
        return self.num * 0.01

    def toKilometer(self):
        return self.num * 0.001


class Kilometer:
    def __init__(self, num):
        self.num = num

    def toInches(self):
        return self.num * 39370.08

    def toFeet(self):
        return self.num * 3280.84

    def toYard(self):
        return self.num * 1.093613

    def toMillimeters(self):
        return self.num * 1000000

    def toCentimeter(self):
        return self.num * 100000

    def toDecimeter(self):
        return self.num * 10000

    def toDecameter(self):
        return self.num * 100

    def toMeter(self):
        return self.num * 1000


class Fahrenheit:
    def __init__(self, num):
        self.num = num

    def toCelsius(self):
        return (self.num-32) * (5/9)


class Celsius:
    def __init__(self, num):
        self.num = num

    def toFahrenheit(self):
        return self.num * (9/5) + 32


