__all__=['write', 'printerr', 'service', 'set_logfile', 'set_markup_keywords', 'set_markup_usage', 'flush_service', 'markup_codes']
import sys, io

terminal_codes={'':'\033[0m', 'red':'\033[31m', 'green':'\033[32m',
                'black':'\033[30m', 'yellow':'\033[33m', 'blue':'\033[34m',
                'magenta':'\033[35m', 'cyan':'\033[36m', 'white':'\033[37m',
                'bright':'\033[1m', 'dim':'\033[2m', 'underscore':'\033[4m',
                'blink':'\033[5m', 'reverse':'\033[7m', 'hidden':'\033[8m'}
markup_codes=set(terminal_codes.keys())
logfile=None
markup_keywords={}
printed_rchar=0
no_colors=False
    
def flush_service():
    """ Clears up the "sticky" messages printed with the service function

    Returns
    =======
    None
        None
    
    See Also
    ========
    service : print temporary messages to screen

    """
    global printed_rchar
    if printed_rchar:
        sys.stderr.write('\r'+printed_rchar*' '+'\r' )
        printed_rchar=0    
    
def write(text, end='\n', how='', keywords={}, is_service=False, is_stderror=False):
    """Prints a message to stdout, optionally using colors
    
    Wraps the builtin print() with convenient options.
    If a log file is defined, it prints to the logfile too (see set_logfile).

    Parameters
    ----------
    text : str | any
        text to be printed. If not str, it is converted to str

    end : str
        by default, a newline is added to each input text. 
        Provide end='' to avoid it, or another character to use a different end of line character

    how : str        
        any number of comma-separated termcodes to markup your text, among:
        black blink blue bright cyan dim green hidden magenta red reverse underscore white yellow

    keywords : dict
        use this to automatically highlight all occurrences of certain words.
        dictionary structured like word:termcode, so that all occurrences of word in text is marked with termcode(s)
        Note: using many keywords makes the function slower

    Returns
    -------
    None
        None
    """  
    if not keywords and markup_keywords:
        keywords=markup_keywords
    msg=str(text)
    if end:
        msg=msg+end

    if not is_service and not logfile is None:
        no_color_msg=msg
        
    # colors and other markup
    if (how or keywords) and sys.stdout.isatty() and not no_colors:
        if how:
            for c in how.split(','): 
                if not c in terminal_codes:
                    raise Exception(f"ERROR option 'how' for write was not recognized: {c} ; possible values are: {','.join([i for i in terminal_codes if i])}")
                msg=terminal_codes[c]+msg+terminal_codes['']
        for word in keywords:
            code=''
            for c in keywords[word].split(','):
                code+=terminal_codes[c]
            msg=msg.replace(word, code+word+terminal_codes[''])

    # flushing rchars
    flush_service()
        
    if is_stderror or is_service:
        sys.stderr.write(msg)
    else: 
        sys.stdout.write(msg)
        
    if not is_service and not logfile is None:
        print(str(no_color_msg), end='', file=logfile)

        
def service(text, **kwargs):
    """ Print a temporary message to screen (stderr) meant to be flushed out and re-printed again modified, e.g. in a progress bar style.
    
    Parameters
    ----------
    text : str
        message to be printed
    how : str
        termcodes for markup. See write() 

    Returns
    -------
    None
        None
    """
    if not sys.stdout.isatty(): return
    global printed_rchar
    write("\r"+text, end='', is_service=True, **kwargs)
    printed_rchar=len(text)

    
def printerr(text, *args, **kwargs):
    """Prints a message to stderr, optionally using colors
    
    Wraps the builtin print() with convenient options.
    If a log file is defined, it prints to the logfile too (see set_logfile).

    Parameters
    ----------
    text : str | any
        text to be printed. If not str, it is converted to str

    end : str
        by default, a newline is added to each input text. 
        Provide end='' to avoid it, or another character to use a different end of line character

    how : str        
        any number of comma-separated termcodes to markup your text, among:
        black blink blue bright cyan dim green hidden magenta red reverse underscore white yellow

    keywords : dict
        use this to automatically highlight all occurrences of certain words.
        dictionary structured like word:termcode, so that all occurrences of word in text is marked with termcode(s)
        Note: using many keywords makes the function slower

    Returns
    -------
    None
        None
    """
    write(text, *args, **kwargs, is_stderror=True)

    
def set_logfile(fileh_or_path):
    """Sets a logfile where all messages printed with printed with write() or printerr() are also sent.

    Parameters
    ----------
    fileh_or_path : file | str
        file path specification or buffer of desired logfile

    Returns
    -------
    None
        None
    """
    global logfile
    if type(fileh_or_path) is str:
        logfile=open(fileh_or_path, 'w')
    elif isinstance(fileh_or_path, io.IOBase):
        logfile=fileh_or_path
    else:
        raise Exception(f"set_logfile ERROR expected string or file, got this instead: {type(fileh_or_path)} {fileh_or_path}")
    
def set_markup_keywords(kwords):
    """Set a syntax to always print certain words using a specific markup (when using write or printerr)
    
    Parameters
    ----------
    kwords : dict
        dictionary like key:termcode, where key is any string, and termcode any comma-separated combination of these:
        black blink blue bright cyan dim green hidden magenta red reverse underscore white yellow
    
    Note
    ----
        Using many keywords makes printing slower, so beware

    
    Returns
    -------
    None
        None
    """
    
    global markup_keywords
    markup_keywords=kwords


def set_markup_usage(setting):
    """ Turns off or on the usage of colors and other terminal markup
    
    Parameters
    ----------
    setting : bool
          new setting, use False to turn off markup, True to turn back on

    Returns
    -------
    None
        None
    """
    global no_colors
    no_colors= not setting
