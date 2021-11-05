# Import the base Dice module to add some convenience
# objects & functions for dice rolling
from ewccommons.dice import _Die_Faces_, Dice

# Define the common die set
D3: Dice = Dice(name="D3", sides=3)
D4: Dice = Dice(name="D4", sides=4)
D6: Dice = Dice(name="D6", sides=6)
D8: Dice = Dice(name="D8", sides=8)
D10: Dice = Dice(name="D10", sides=10)
D12: Dice = Dice(name="D12", sides=12)
D20: Dice = Dice(name="D20", sides=20)
# Define the common die set face values lists
_D3: _Die_Faces_ = D3.faces
_D4: _Die_Faces_ = D4.faces
_D6: _Die_Faces_ = D6.faces
_D8: _Die_Faces_ = D8.faces
_D10: _Die_Faces_ = D10.faces
_D12: _Die_Faces_ = D12.faces
_D20: _Die_Faces_ = D20.faces


def roll_d3() -> int:
    """Randomly choose a number from the 3 sided die"""
    return D3.roll()


def roll_d4() -> int:
    """Randomly choose a number from the 4 sided die"""
    return D4.roll()


def roll_d6() -> int:
    """Randomly choose a number from the 6 sided die"""
    return D6.roll()


def roll_d8() -> int:
    """Randomly choose a number from the 8 sided die"""
    return D8.roll()


def roll_d10() -> int:
    """Randomly choose a number from the 10 sided die"""
    return D10.roll()


def roll_d12() -> int:
    """Randomly choose a number from the 12 sided die"""
    return D12.roll()


def roll_d20() -> int:
    """Randomly choose a number from the 20 sided die"""
    return D20.roll()


def roll_d100() -> int:
    """Randomly choose a number from the 2 10 sided dice"""
    # Roll a ten sided die as the 10s die value
    # Removing 1 from the tens value allows the multiplier to work
    tens: int = D10.roll() - 1
    # Roll the units & return the sum
    units: int = D10.roll()
    return (tens * 10) + units


def main() -> None:
    """Main function to run the application"""
    # Just run a few dice rolls
    print("D100 Rolls...", roll_d100())
    print("D6 Rolls...", roll_d6())


# Make sure the script is being called as a script & not being imported into
# another module file
if __name__ == "__main__":
    # Call the main function
    main()
