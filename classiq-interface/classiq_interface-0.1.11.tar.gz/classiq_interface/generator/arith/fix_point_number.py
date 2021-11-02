import math
from typing import Optional

import pydantic

MAX_FRACTION_PLACES = 5


class FixPointNumber(pydantic.BaseModel):
    float_value: float
    max_fraction_places: Optional[pydantic.conint(ge=0)] = MAX_FRACTION_PLACES
    is_signed: Optional[bool] = None
    _fraction_places: Optional[int] = pydantic.PrivateAttr(default=None)
    _int_val: Optional[int] = pydantic.PrivateAttr(default=None)
    _size: Optional[int] = pydantic.PrivateAttr(default=None)
    _integer_part_size: Optional[int] = pydantic.PrivateAttr(default=None)

    def set_int_representation(self):
        int_val = math.floor(self.float_value * 2 ** self.max_fraction_places)
        int_val = self.signed_int_to_unsigned(int_val)

        if int_val == 0:
            fraction_places = 0
        else:
            bin_val = bin(int_val)[2:]
            fraction_places = self.max_fraction_places
            for b in reversed(bin_val):
                if b == "1" or fraction_places == 0:
                    break
                fraction_places -= 1
            int_val = int_val >> (self.max_fraction_places - fraction_places)

        self._fraction_places = fraction_places
        self._int_val = int_val

    @staticmethod
    def signed_int_to_unsigned(number: int):
        """Return the integer value of a signed int if it would we read as un-signed in binary representation"""
        if number >= 0:
            return number

        not_power2 = abs(number) & (abs(number) - 1) != 0
        return number + 2 ** (number.bit_length() + 1 * not_power2)

    @staticmethod
    def binary_to_float(bin_rep: str, fraction_part_size: int, is_signed: bool = False):
        negative_offset = -(2 ** len(bin_rep)) * (bin_rep[0] == "1") * is_signed
        value = int(bin_rep, 2) + negative_offset
        if (
            fraction_part_size > 0
        ):  # separated the clause to so that the value remains int if there is no fraction part
            value = value / 2 ** fraction_part_size
        return value

    @pydantic.validator("max_fraction_places", always=True)
    def validate_max_fraction_places(cls, max_fraction_places):
        if max_fraction_places is None:
            max_fraction_places = MAX_FRACTION_PLACES
        return max_fraction_places

    @pydantic.validator("is_signed", always=True)
    def validate_is_signed(cls, is_signed: bool, values: dict):
        float_value = values.get("float_value")
        if is_signed is False and float_value < 0:
            raise ValueError("Not possible to define a negative number as not signed")
        elif is_signed is None:
            is_signed = float_value < 0

        return is_signed

    @property
    def fraction_places(self):
        if self._fraction_places is None:
            self.set_int_representation()
        return self._fraction_places

    def set_fraction_places(self, value: int):
        if value < self._fraction_places:
            raise ValueError("size cannot be lower than minimum number bits required")

        if value > self.max_fraction_places:
            self.max_fraction_places = value
            self.set_int_representation()

        self._int_val = math.floor(self.int_val * 2 ** (value - self.fraction_places))
        self._fraction_places = value
        self._size = self._integer_part_size + self._fraction_places

    @property
    def int_val(self):
        if self._int_val is None:
            self.set_int_representation()
        return self._int_val

    @property
    def integer_part_size(self):
        if self._integer_part_size is None:
            self._integer_part_size = self.int_val.bit_length() - self.fraction_places
        return self._integer_part_size

    def set_integer_part_size(self, value: int):
        if value < self.integer_part_size:
            raise ValueError("size cannot be lower than minimum number bits required")
        self._integer_part_size = value
        self._size = self._integer_part_size + self._fraction_places
        self._int_val = int(self.bin_val, 2)

    def bit_length(self):
        return 1 if self.int_val == 0 else self.int_val.bit_length()

    @property
    def size(self):
        if self._size is None:
            self._size = self.bit_length()
        return self._size

    @property
    def bin_val(self):
        if self._int_val is None:
            self.set_int_representation()

        bin_rep = bin(self._int_val)[2:]
        size_diff = self.size - len(bin_rep)
        if self.float_value >= 0:
            return "0" * size_diff + bin_rep
        else:
            return "1" * size_diff + bin_rep

    @property
    def actual_float_value(self):
        return self.binary_to_float(self.bin_val, self.fraction_places, self.is_signed)

    def __eq__(self, other):
        return self.actual_float_value == other

    def __ge__(self, other):
        return self.actual_float_value >= other

    def __gt__(self, other):
        return self.actual_float_value > other

    def __le__(self, other):
        return self.actual_float_value <= other

    def __lt__(self, other):
        return self.actual_float_value < other

    def __ne__(self, other):
        return self.actual_float_value != other

    def __getitem__(self, item):
        return [v for v in self.bin_val[::-1]][
            item
        ]  # follow qiskit convention that LSB is the top wire, bigendian

    def __neg__(self):
        return FixPointNumber(
            float_value=-self.float_value, max_fraction_places=self.max_fraction_places
        )

    class Config:
        extra = "forbid"
