# Import the typing library so variables can be type cast
from typing import List

# Import the random library
import random

# Define the dice sides variable type
_Dice_ = List[int]

# Define the common die set
D3: _Dice_ = [*range(1, 4)]
D4: _Dice_ = [*range(1, 5)]
D6: _Dice_ = [*range(1, 7)]
D8: _Dice_ = [*range(1, 9)]
D10: _Dice_ = [*range(1, 11)]
D12: _Dice_ = [*range(1, 13)]
D20: _Dice_ = [*range(1, 21)]


def roll_die(d: _Dice_) -> int:
    """Randomly choose a number from the x sided die"""
    return random.choice(d)


def roll_d3() -> int:
    """Randomly choose a number from the 3 sided die"""
    return random.choice(D3)


def roll_d4() -> int:
    """Randomly choose a number from the 4 sided die"""
    return random.choice(D4)


def roll_d6() -> int:
    """Randomly choose a number from the 6 sided die"""
    return random.choice(D6)


def roll_d8() -> int:
    """Randomly choose a number from the 8 sided die"""
    return random.choice(D8)


def roll_d10() -> int:
    """Randomly choose a number from the 10 sided die"""
    return random.choice(D10)


def roll_d12() -> int:
    """Randomly choose a number from the 12 sided die"""
    return random.choice(D12)


def roll_d20() -> int:
    """Randomly choose a number from the 20 sided die"""
    return random.choice(D20)


def roll_d100() -> int:
    """Randomly choose a number from the 2 10 sided dice"""
    # Roll a ten sided die as the 10s die value
    # Removing 1 from the tens value allows the multiplier to work
    tens: int = random.choice(D10) - 1
    # Roll the units & return the sum
    units: int = random.choice(D10)
    return (tens * 10) + units


class Dice:
    """Define a Die object instance"""

    def __init__(self, name: str, sides: _Dice_, val: int = None) -> None:
        """Initial the Die object & set a face value"""
        # Set the die face value range
        self.__name: str = name
        self.__sides: _Dice_ = sides
        # Check if an initial die face value is set
        if val is None:
            # Generate a random starting face value
            val = roll_die(self.__sides)
        # Make sure the initial die face value is actually within the values on the die
        if val < min(self.__sides) or val > max(self.__sides):
            raise ValueError("Dice initial value out of bounds")
        # Set the initial starting face value of the die
        self.__val: int = val

    def roll(self) -> int:
        """Simulate rolling the die"""
        val: int = roll_die(self.__sides)
        self.__val = val
        return self.rolled()

    def rolled(self) -> int:
        """Get the rolled face value of the die"""
        return self.__val

    def __str__(self) -> str:
        """Get the Dice instance as a string"""
        return f"{self.__name} : {self.__val}"


def main() -> None:
    """Main function to run the application"""
    # Just run a few dice rolls
    print("D100 Rolls...")
    print(roll_d100())
    print("D6 Rolls...")
    print(roll_d6())
    print("Dice(D12)")
    d: Dice = Dice("D12", D12)
    print(d)
    print("Rolls...")
    print(d.roll())


# Make sure the script is being called as a script & not being imported into
# another module file
if __name__ == "__main__":
    # Call the main function
    main()
