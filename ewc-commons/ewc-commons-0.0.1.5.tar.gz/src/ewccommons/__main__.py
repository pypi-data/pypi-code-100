# Import the collection of available modules
from ewccommons import dice
from ewccommons import dicerolls
from ewccommons import carddeck

# Define the current library/module version
VERSION: str = "0.0.1.5"


def main() -> None:
    print(f"EWC Commons Library v{VERSION}")


# Make sure the script is being called as a script & not being imported into
# another module file
if __name__ == "__main__":
    # Call the main function
    main()
