# Import the typing library so variables can be type cast
from typing import List

# Import the sys for args
import sys

# Import the Sophie launcher system needed
from ewccommons.sophie import (
    _TNGN_,
    _CLI_Arg_Handled_,
    SophieLauncher,
    CLIUsageHandler,
    launcher,
)

# Import the collection of available modules
from ewccommons import dice
from ewccommons import dicerolls
from ewccommons import carddeck

# Define the current library/module version
VERSION: str = "0.0.1.6"


def cli_argument_handler(
    opts: List,
    args: List,
    show_usage_help: _TNGN_,
    show_version: _TNGN_,
) -> _CLI_Arg_Handled_:
    """Handle the processing of the cli arguments"""
    enquiry: str = None
    opt: str
    arg: str
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            # Just show the usage help & halt
            show_version()
            show_usage_help()
        elif opt in ("-v", "--version"):
            # Just show the version & halt
            show_version()
            sys.exit()
        elif opt == "--dice":
            # Run the dice main module function
            dice.main()
        elif opt == "--dicerolls":
            # Convert the value to lower, split on space & use as args for dicerolls
            dicerolls.main(*arg.lower().split())
        elif opt == "--carddeck":
            # Run the carddeck main module function
            carddeck.main()
        elif opt in ("-q", "--enquiry"):
            # Assign the enquiry value
            enquiry = arg
    return enquiry, args


def help_text() -> str:
    """Generate the help text to display"""
    return "\n".join(
        [
            "  -h --help (Show this help)",
            "  -v --version (Show library version)",
            "  --dice (Run the dice module)",
            "  --dicerolls Optional[d6 ...] (Run the dicerolls module)",
            "  --carddeck (Run the carddeck module)",
            "  -q <enquiry> (Make an enquiry)",
        ]
    )


def main() -> None:
    sophie: SophieLauncher
    usage: CLIUsageHandler
    sophie, usage = launcher(
        _usage=CLIUsageHandler,
        app_name="EWC Commons Library",
        version=VERSION,
        short_options="hvq:",
        long_options=["help", "version", "dice", "dicerolls=", "carddeck", "enquiry="],
        help_text=help_text,
    )
    # Let's have a look at what we got
    print(
        "Let's have a look:",
        "Sophie",
        sophie,
        "Usage",
        usage,
        "#############",
        sep="\n",
    )
    # Define the usage & types of variables to be used in this scope
    enquiry: str
    enquiry, args = sophie.launch(cli_argument_handler)
    print(enquiry, args)
    # sophie.show_usage_help()


# Make sure the script is being called as a script & not being imported into
# another module file
if __name__ == "__main__":
    # Call the main function
    main()
