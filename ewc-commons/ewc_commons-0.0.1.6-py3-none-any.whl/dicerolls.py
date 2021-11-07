# Import the base Dice module to add some convenience
# objects & functions for dice rolling
from ewccommons.dice import _Die_Faces_, Dice

# Define the common die set
D3: Dice = Dice(3, name="D3", val=None)
D4: Dice = Dice(4, name="D4", val=None)
D6: Dice = Dice(6, name="D6", val=None)
D8: Dice = Dice(8, name="D8", val=None)
D10: Dice = Dice(10, name="D10", val=None)
D12: Dice = Dice(12, name="D12", val=None)
D20: Dice = Dice(20, name="D20", val=None)
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


def main(*args) -> None:
    """Main function to run the application"""
    # Check if any args were supplied
    if not len(args):
        # Import the sys to get any argv used
        import sys

        # Convert the values to lower case for ease
        args = [str(_).lower() for _ in sys.argv[1:]]
    # Check for die rolls in the supplied arguments list
    if "d3" in args:
        print("D3 Rolls...", roll_d3())
    if "d4" in args:
        print("D4 Rolls...", roll_d4())
    if "d6" in args:
        print("D6 Rolls...", roll_d6())
    if "d8" in args:
        print("D8 Rolls...", roll_d8())
    if "d10" in args:
        print("D10 Rolls...", D10.roll())
    if "d12" in args:
        print("D12 Rolls...", D12.roll())
    if "d20" in args:
        print("D20 Rolls...", D20.roll())
    if "d100" in args:
        print("D100 Rolls...", roll_d100())


# Make sure the script is being called as a script & not being imported into
# another module file
if __name__ == "__main__":
    # Call the main function
    main()
