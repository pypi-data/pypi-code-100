# pylint: disable=eval-used, broad-except

# module-level docstring
__doc__='''
Command line user interface
===========================

Implements convenience function for CLI user interaction.
Useful when you need to ask the user what to do, or select one
of many options.

API:
    - choose_from_list
    - user_input
    - select_action

See elements' docstrings for further explanations.
'''

from typing import Iterable, Union, Any, Callable, Dict, Optional
import sys
from .banner import one_line_banner

KBI_msg = "A KEYBOARDINTERRUPT WAS RAISED. THE PROGRAM WILL EXIT NOW."

def __input_KBI( message: str, exit_on_KBI: bool = True ) -> str:
    ''' Handles `KeyboardInterrupts` on `input` calls, used by other more complex functions.
    '''
    if exit_on_KBI:
        try:
            return input( message )
        except KeyboardInterrupt:
            print( KBI_msg )
            sys.exit(0)
    return input( message )


def user_input( prompt: str, accepted: Union[Iterable[Union[str,int]],Callable], default: Any = None ) -> str:
    ''' Asks user for input, with restrictions on accpetable values.
    `prompt`: appropriate text asking the user for input. Should be straightforward and informative about the kind of data that is asked
    `accepted`: either a function testing if the user input is acceptable, or an iterable containing all acceptable values
    `default`: When given, if the user input is not acceptes, default is returned. When abscent, the user will be prompted again until either
    an accepted value is entered or a KeyboardInterrupt is raised.
    Note: this is only designed to retrieve values of the following types: str, int, float
    '''
    if default is not None:
        prompt += f"[default:{default}] "
        
    while True:
        _user_input = __input_KBI( prompt )
        
        # check whether _user_input (and variations) matches an item in `accepted`
        if callable(accepted) and accepted(_user_input):
            return _user_input
        elif _user_input in accepted:
            return _user_input

        variations = [ 'int(_user_input)', 'float(_user_input)', '_user_input.lower()' ]
        for variation in variations:
            try:
                __user_input = eval( variation )
                if __user_input in accepted:
                    return __user_input
            except Exception:
                pass
                
        if default is not None:
            return default
        
        print(f"Input {_user_input} not recognized. Please choose one of : {accepted}")


def choose_from_list( choices: list, default: int ) -> Any:
    ''' Prints then asks the user to choose an item from a list
    ``default` '''
    # Print choices
    print( "Choices:\n  " + '\n  '.join([
        f"[{idx}] {choice}"
        for idx, choice in enumerate(choices)
    ]) + '\n' )

    # Get user selection
    idx = user_input( "Selection : ", accepted=list(range(len(choices))), default=default )

    # Return choice
    return choices[idx]


def select_action( choices: Dict[str,Callable], no_banner: bool = False, default: str = None, execute: bool = False ) -> Optional[Callable]:
    ''' Asks the user to choose an action amongst a list of labeled actions. Returns a callable
    corresponding to the chosen action if `execute` is False, executes it otherwise.
    
    Example of `choices`:
    choices = {
        'q': {
            'explanation': 'quit the program'
            'action': <function that exits the program:Callable>
        }
        ...
    }
    ''' 

    # Print banner
    if not no_banner:
        banner = one_line_banner( "Selection menu" )
        print(banner)

    accepted_inputs = choices.keys()

    # Print choices
    choice_formatter = lambda choice: choice + ( f" - {choices[choice]['explanation']}" if 'explanation' in choices[choice] else '' )
    print( "Choices:\n  " + '\n  '.join([
        choice_formatter( choice )
        for choice in accepted_inputs
    ]) + '\n' )
    
    # Get user choice
    _user_input = user_input( "Selection : ", accepted=accepted_inputs, default=default )

    # Return or execute corresponding callable
    if execute:
        choices[_user_input]['action']()
    else:
        return choices[_user_input]['action']
