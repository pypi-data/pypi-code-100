# Import the typing library so variables can be type cast
from typing import Any, Callable, List, Tuple

# Import the use of abstract classes
from abc import ABC, abstractmethod

# Import the system & get options to process command line arguments
import getopt
import sys

_CLI_Arg_Handled_ = Tuple[Any, ...]
"""Define the return type of the callback handler function"""

_TNGN_ = Callable[[], None]
"""Define a Takes Nothing, Gives Nothing function signature"""

_CLI_Arg_Handler_ = Callable[[List, List, _TNGN_, _TNGN_], _CLI_Arg_Handled_]
"""Define the callback handler function signature"""


class CLIUsage(ABC):
    """Define how a CLI Usage handler should look"""

    @property
    @abstractmethod
    def short_options(self) -> str:
        """Get the command line short version option"""

    @property
    @abstractmethod
    def long_options(self) -> List:
        """Get the command line long version option"""

    @property
    @abstractmethod
    def used(self) -> List:
        """Get a list of all the cli arguments used at runtime"""

    @abstractmethod
    def help(self) -> str:
        """Get the command line usage help"""


class CLArgsProcessor:
    """Processor class to extract the CLI arguments used"""

    def __init__(self, argv, usage: CLIUsage) -> None:
        """Initialize the class instance & set the instance properties"""
        self.__error: bool = False
        try:
            # Extract the options & arguments specified from the supplied arguments
            opts, args = getopt.getopt(argv, usage.short_options, usage.long_options)
        except getopt.GetoptError:
            # Hello there
            self.__error = True
            return
        # Set the options & arguments to process later
        self.__opts = opts
        self.__args = args

    def process(
        self,
        handler: _CLI_Arg_Handler_,
        show_usage_help: _TNGN_,
        show_version: _TNGN_,
    ) -> _CLI_Arg_Handled_:
        """process the command line arguments & return the corresponding data"""
        return handler(self.__opts, self.__args, show_usage_help, show_version)

    @property
    def has_error(self) -> bool:
        """Check if the processor encountered an error"""
        return self.__error


class CLIUsageHandler(CLIUsage):
    """Create a CLI argument usage handler"""

    def __init__(self, short_options: str, long_options: List, help_text) -> None:
        """Set the usage details"""
        self.__short_options: str = short_options
        self.__long_options: List = long_options
        self.arg_processor: CLArgsProcessor = None
        # Initialise the list of CLI arguments used at runtime
        self.__used: List = list()
        # If the help text specified is not a callable function, wrap it in a lambda
        self._help_text: Callable[[], str] = (
            help_text if callable(help_text) else lambda: str(help_text)
        )

    @property
    def short_options(self) -> str:
        """Get all the cli one character options available"""
        return self.__short_options

    @property
    def long_options(self) -> List:
        """Get a list of all the cli long options available"""
        return self.__long_options

    @property
    def used(self) -> List:
        """Get a list of all the cli arguments used at runtime"""
        return self.__used

    def using(self, arg_processor: CLArgsProcessor) -> None:
        """Provide a means of setting the CLI argument processor"""
        self.arg_processor = arg_processor

    def help(self) -> str:
        """Get the usage help for the options"""
        return self._help_text()

    def __str__(self) -> str:
        """Get the object as a human readable string"""
        return "\n".join([self._help_text()])


class SophieLauncher:
    """Define the main CLI script launcher"""

    def __init__(
        self, usage: CLIUsage, app_name: str = __name__, version: str = "0.0.1"
    ) -> None:
        """Initialize the class instance & set the instance properties"""
        self.__error: bool = False
        self.__app_name: str = app_name
        self.__version: str = version
        self.usage: CLIUsage = usage
        # Create a CLI argument processor
        self.arg_processor: CLArgsProcessor = CLArgsProcessor(
            argv=sys.argv[1:], usage=self.usage
        )
        # Check for processor errors
        if self.arg_processor.has_error:
            self.__error = True

    @property
    def has_error(self) -> bool:
        """Check if the launcher encountered an error"""
        return self.__error

    @property
    def app_name(self) -> str:
        """Get the name of the app instance"""
        return self.__app_name

    @property
    def app_version(self) -> str:
        """Get the app instance version"""
        return self.__version

    def show_usage_help(self) -> None:
        """Display the help text by constructing the app name with the usage help"""
        print(self.usage.help(), sep=" ")

    def show_version(self) -> None:
        """Display the version text by constructing the app name with the version"""
        print(self)

    def launch(
        self,
        handler: _CLI_Arg_Handler_,
    ) -> _CLI_Arg_Handled_:
        """Launch the module/script"""
        return self.arg_processor.process(
            handler=handler,
            show_usage_help=self.show_usage_help,
            show_version=self.show_version,
        )

    def __str__(self) -> str:
        """Get the object as a human readable string"""
        return "\n".join([self.app_name, f"Version - {self.app_version}"])


def launcher(
    _usage: CLIUsageHandler,
    app_name: str = __name__,
    version: str = "0.0.1",
    short_options: str = "hvq:",
    long_options: List = ["help", "version", "enquiry="],
    help_text="-q <enquiry>",
) -> Tuple[SophieLauncher, CLIUsageHandler]:
    """Shortcur method to create a SophieLauncher"""
    usage: CLIUsageHandler = _usage(
        short_options=short_options,
        long_options=long_options,
        help_text=help_text,
    )
    sophie: SophieLauncher = SophieLauncher(
        usage=usage,
        app_name=app_name,
        version=version,
    )
    # Check if something went wrong getting a processor
    if sophie.has_error:
        # Display the usage help & GTFO
        sophie.show_usage_help()
        sys.exit(2)
    return sophie, usage


def main() -> None:
    """Main function to run the module"""
    pass


# Make sure the script is being called as a script & not being imported into
# another module file
if __name__ == "__main__":
    # Call the main function
    main()
