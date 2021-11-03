import sys, string, copy, re, os, warnings, io, shlex
from .colorprint import write 
__all__ = ["command_line_options", "read_config_file",  "NoTracebackError",  "set_up_no_traceback_error"]

# "CommandLineOptions", "CommandLineError" 

def custom_formatwarning(msg, *args, **kwargs):
    return str(msg) + '\n'
warnings.formatwarning = custom_formatwarning


class CommandLineOptions(dict):
    """ Subclass of dict designed to store options of the command line.

    Two differences with dict:
     - its representation looks good on screen
     - requesting a key which is absent returns None, instead of throwing an error
    """
    accepted_option_chars=set(string.ascii_uppercase + string.ascii_lowercase)
    accepted_option_types=set([bool, int, float, list, str])    

    def __repr__(self):
        max_charlen=max( [ len(k) for k in self] ) if self else 0
        return('\n'.join( [f"{k:<{max_charlen}} : {type(self[k]).__name__:<5} = {self[k]}" for k in sorted(self.keys())]) )
    
    def __getitem__(self, name):
        if name in self:            return dict.__getitem__(self, name)
        else:                       return None

    def write_config_file(self, fileh_or_path, sep='=', ordered_keys=None):
        """Write options into a format that can be later read with read_config_file"""
        with (fileh_or_path if isinstance(fileh_or_path, io.IOBase)
              else open(fileh_or_path, 'w')) as fhw:
            ordered_keys=ordered_keys if ordered_keys is not None else sorted(self.keys())
            for key in ordered_keys:
                value=self[key]
                if type(value) is list:
                    fhw.write(f'{key} {sep} {" ".join(value)}\n')
                else:
                    fhw.write(f'{key} {sep} {value}\n')
        
        
class NoTracebackError(Exception):
    """Exception class which, when raised, shows the error message only, without traceback.
    Its usage requires running set_up_no_traceback_error()
    """
    pass

class CommandLineError(NoTracebackError):
    """Exception class indicating an error occured while reading command line options."""

def set_up_no_traceback_error(set_on=True):
    """After this, raising NoTracebackError or its subclasses results in single error line, without traceback.
    Under the hood, replaces sys.excepthook
    
    Parameters
    ----------

    set_on : bool
        normally this is set to True when the module is loaded.
        Call this fn with set_on=False to restore the default sys.excepthook

    Returns
    -------
    None
        None
    """
    def excepthook_allowing_notraceback(type, value, traceback):
        if issubclass(type, NoTracebackError):              sys.exit(str(value))
        return(sys.__excepthook__(type, value, traceback))  
    if set_on:
        sys.excepthook=excepthook_allowing_notraceback
    else: 
        sys.excepthook=sys.__excepthook__
        
set_up_no_traceback_error()

def command_line_options(default_opt,
                         help_msg='Command line usage:...',
                         positional_keys='',
                         synonyms={},
                         tolerate_extra=False,
                         tolerated_regexp=[],
                         warning_extra=True,
                         advanced_help_msg={},
                         arglist=None,
                         add_defaults=True):
    """Reads command line arguments and returns them after filling with default values
    
    Here below, we refer to option names as *keys* (e.g. the "i" in "program.py -i inputfile" ),
    and *arguments* for their argument (e.g. "inputfile" above).
    
    Parameters
    ----------
    
    default_opt : dict
        defines default arguments for all command lines keys. 
        Their value types also define the typing enforced on command line arguments.
        Possible value types are int, float, str, bool (whose argument can be omitted), list (multiple args accepted)

    help_msg : str
        if any of -h | -help | --help are  provided, this help message is displayed and the script exits

    positional_keys : iterable
        these keys will be associated, in order, to argumentss with no explicit keys (e.g. script.py arg1 arg2)

    synonyms : dict
        add synonyms for keys; e.g. if you use {'input':'i', 'p':'param'} then using -input or -i in the command line will be equivalent
        note: the built-in {'help':'h'} is automatically added

    tolerate_extra : bool
        normally any key not found in default_opt raises an error; this allows to tolerate & accept unexpected keys

    tolerated_regexp : list
        define which unexpected keys to tolerate using regexp syntax, employed by module re

    warning_extra : bool
        when keys are tolerated (see two previous args), normally a warning is printed; set this to False to silence them
    
    advanced_help_msg : dict
        dictionary defining specialized help messages, which are displayed only when invoked as argument to ``-h``
        e.g. if you run on the command line `` -h map ``, and if within the script you had 
        ``advanced_help_msg={'map':'map message'}``, then 'map message' is displayed
        By default, the normal help_msg is also displayed before the specialized one. 
        Add None as key to ovveride. For example, ``advanced_help_msg={'map':'map message', None:''}`` 
        will result in only the specialized message printed when ``-h map`` is used

    arglist : list, optional
        normally options are read from sys.argv, which is automatically filled from command line arguments.
        Use arglist to provide an analogous list of strings instead

    add_defaults : bool
        normally those options not specified on the command line are taken from def_opt. 
        Set add_defaults=False to simply omit them from the output

    Returns
    -------
    opt : CommandLineOptions
        dictionary like object with structure key:arg, carrying command line options and, if not provided, default values

    Examples
    --------

    **Example 1**

    If you use this code in your python script:

    .. code-block:: python

        opt=command_line_options( default_opt={'i': 'input', 'o':'output', 'param':3} ) 

    Then, when your script is run with this command line (in bash or analogous):

    .. code-block:: bash

        script.py -i file1  -o file2   

    
    ... this will result in this dictionary returned by ``command_line_options``:

    .. code-block:: python

        {'i':'file1', 'o':'file2', 'param':3}

    Different command line and resulting dictionary returned:
    
    .. code-block:: bash

        script.py -i file1  -param -1  
    
    .. code-block:: python

        {'i':'file1', 'o':'output', 'param':-1}   # note param is cast to int


    **Example 2**

    With::

        opt=command_line_options( default_opt={'param':3, 'files':[]},  synonyms={'p':'param'})

    This command line:

    .. code-block:: bash

        script.py -files a b c d e -p 10

    Results in::
 
        {'files':['a', 'b', 'c', 'd', 'e'], 'param':10}  # note -p as synonym


    **Example 3**

    With::

        opt=command_line_options( default_opt={'i':'', 'o':'', 's':'', 'k':5.5},  positional_keys=['i', 'o'])

    This command line:

    .. code-block:: bash

        script.py -k 4.5 in1 out1    
    
    Results in::

        {'i':'in1', 'o':'out1', 's':'', 'k':4.5}   # positional args

    While this command line:

    .. code-block:: bash

        script.py in1 out1 -k 10      

    Results in::

        {'i':'in1', 'o':'out1', 's':'', 'k':10.0}  # this order also accepted  # note -k cast to float

    And this command line:

    .. code-block:: bash

        script.py in1 -s "multi word str"   

    Results in::

        {'i':'in1', 'o':'', 's':'multi char str', 'k':5.5}  # multiword string as arg

    Note that, while the object returned by command_line_options is a dictionary, it is subclassed
    and implements its own representation function, so that if you actually try to print it, you would get
    something like:
    
    >>> print( opt )
    i : str     = in1
    k : float   = 5.5
    o : str     = 
    s : str     = multi char str
    """
    
    default_opt=CommandLineOptions(default_opt)
    for builtin_opt in ['h', 'print_opt']:
        if not builtin_opt in default_opt:
            default_opt[builtin_opt]=False
        elif type(default_opt[builtin_opt]) is not bool:
            default_opt[builtin_opt]=(False
                                       if default_opt[builtin_opt] in ('', '0', 'F', 'False', 0, 0.0)
                                       else True)

    opt=CommandLineOptions()
    arglist=sys.argv[1:] if arglist is None else arglist
    for h in ('help', '-help'):
        synonyms[h]='h'                   # built-in synonym
        

    ## checking default_opt and positional_keys
    for opt_key in default_opt:
        expected_type=type(default_opt[opt_key])
        if not expected_type in CommandLineOptions.accepted_option_types:
            raise CommandLineError( (f"ERROR Only these value types are "
                                               f"accepted (default_opt): {CommandLineOptions.accepted_option_types} "
                                               f"-- Instead it was provided {expected_type} for -{opt_key}"))
        if expected_type is list and any( [not type(x) is str   for x in default_opt[opt_key]]  ):
            raise CommandLineError((f"ERROR default options: each list type option must "
                                              f"contain string values only! Instead this was "
                                              f"provided for -{opt_key} : {default_opt[opt_key]}"))        
    if len([pk for pk in positional_keys if not pk in default_opt]):
        raise CommandLineError((f"ERROR positional keys provided are absent from default option: "
                                f"{' '.join(['-'+pk for pk in positional_keys if not pk in default_opt])}"))

    
    ## below: identifying those bit which are an option, like '-k' or '-test' or '--char'
    opt_key_indices=[i     for i, bit in enumerate(arglist)   
                     if bit.startswith('-') and len(bit.split())==1 and 
                            len(bit)>1 and bit[1] in CommandLineOptions.accepted_option_chars]

    ## dealing with positional arguments, provided before explicit options (or with no options)
    positionals=None
    if len(arglist) and (not len(opt_key_indices) or opt_key_indices[0]!=0):
        positionals='before'
        from_here=0
        up_to=None if not len(opt_key_indices) else opt_key_indices[0]
        
    ## dealing with positional arguments, provided after explicit options
    if len(arglist) and len(opt_key_indices):
        last_ki=opt_key_indices[-1]
        last_k= arglist[last_ki].lstrip('-')        
        if ( last_ki < len(arglist)-2 and
               #(type(default_opt[last_k]) is bool and last_ki < len(arglist)-1) )
             not type(default_opt[last_k]) is list):
            if positionals=='before':
                raise CommandLineError(f"ERROR you can provide positional arguments before "
                                       f"OR after other options, not both! ")
            positionals='after'
            if type(default_opt[last_k]) is bool:
                if  len(arglist)>last_ki+1 and  arglist[last_ki+1] in ('0', '1'):
                    from_here=last_ki+2
                else:
                    from_here=last_ki+1
            else:
                from_here=last_ki+2
            up_to=None

    
            
    ## inserting implied positional option keys explicitly in arglist
    if positionals:
        if not positional_keys: positional_keys=[]  # will result in error below; just saving some code
        insert_these=[]
        for i, value in enumerate(arglist[from_here:up_to]):
            if len(positional_keys)<i+1:
                if tolerate_extra:
                    warnings.warn((f"command_line_options WARNING ignoring extra argument: "
                              f"{' '.join(arglist[from_here+1:up_to])}"))
                else:
                    raise CommandLineError((f"ERROR extra argument not accepted: "
                                            f"{' '.join(arglist[from_here+i:up_to])}"))
                break
            insert_these.append( [from_here+i, positional_keys[i]])
            if type(default_opt[ positional_keys[i] ]) is list: break

        for i, key_opt in insert_these[::-1]:
            arglist.insert(i, f"-{key_opt}")

        opt_key_indices=[i     for i, bit in enumerate(arglist)   
                                if bit.startswith('-') and len(bit.split())==1 and 
                                len(bit)>1 and bit[1] in CommandLineOptions.accepted_option_chars]


    ##### 
    ## main block: going one option at the time, parsing arglist
    for ni, i in enumerate(opt_key_indices):
        ## some internal bits are ignored: e.g.   -n 8 these are all ignored -k 7
        if (ni>0 and opt_key_indices[ni-1]+1 < i-1 and
            not type(default_opt[opt_key]) is list): # note here opt_key is the previous one
            if tolerate_extra:
                warnings.warn((f"command_line_options WARNING ignoring extra argument: "
                          f"{' '.join(arglist[opt_key_indices[ni-1]+2:i])}"))
            else:
                raise CommandLineError((f"ERROR extra argument not accepted: "
                                        f"{' '.join(arglist[opt_key_indices[ni-1]+2:i])}"))             
        
        bit=arglist[i]
        opt_key=bit.lstrip('-')
        if opt_key in synonyms:
            opt_key=synonyms[opt_key]

        ## Extra option, not present in default_opt
        if not opt_key in default_opt:
            if (tolerate_extra or 
                (len(tolerated_regexp)>0 and
                 match_any_word(opt_key, tolerated_regexp, ignore_case=False))):
                # not expecting this option but we tolerate it
                if warning_extra:
                    warnings.warn(f"command_line_options WARNING accepting unexpected command line option: -{opt_key}")
                expected_type=None                    
            else:
                raise CommandLineError(f"ERROR Unexpected command line option: -{opt_key}")
        else:
            expected_type=type(default_opt[opt_key])

        ## assigning a value of the appropriate type  
        next_ki=opt_key_indices[ni+1]   if len(opt_key_indices)>ni+1   else None #None if last option key

        if not expected_type is list:
            vi=i+1  #value index in arglist
            if ((not next_ki is None and  next_ki==vi) or
                (next_ki is None) and len(arglist)-1==i):
                # option is provided without argument
                if expected_type is bool or expected_type is None:
                    value=True
                else:
                    raise CommandLineError((f"ERROR {expected_type} expected type "
                                            f"for option -{opt_key} but no argument provided!"))
            else:
                if expected_type is None:  # if this option was not in default_opt, we cast it to string (unless it had no argument, in which case to bool)
                    expected_type=str
                if expected_type is bool:
                    if   arglist[i+1] in ('1', 'T', 'True'):
                        value=True
                    elif arglist[i+1] in ('0', 'F', 'False'):
                        value=False
                    elif opt_key=='h':
                        if not advanced_help_msg:
                            raise CommandLineError(f"ERROR option -h does not accept arguments. Received: {arglist[i+1]}") from None
                        elif not arglist[i+1] in advanced_help_msg:
                            raise CommandLineError(f"ERROR argument {arglist[i+1]} is not accepted by option -h. Possible values: {' '.join(advanced_help_msg.keys())}") from None
                        else:
                            value=arglist[i+1] ## accepting non-bool value for -h
                    else:
                        raise CommandLineError(f"ERROR boolean options can only take values F, False, 0, or T, True, 1, or none. Received: -{opt_key} : {arglist[i+1]}") from None
                else:
                  try:
                      value= expected_type(  arglist[i+1] ) 
                  except ValueError as e:
                      raise CommandLineError(f"ERROR wrong type for option -{opt_key} : {e}") from None
        else:  # expected_type is list: takes all values after this
            vis=[vi for vi in range(i+1, next_ki   if not next_ki is None else len(arglist))]     # value indices
            value=[arglist[vi] for vi in vis]  # list of strings
        opt[opt_key]=value

    if add_defaults:
      ## adding default values which were not specified in command line
      for opt_key in default_opt:
          if not opt_key in opt:
              opt[opt_key]=copy.copy(default_opt[opt_key])

    ## Printing help message
    if opt['h']:
        if advanced_help_msg and opt['h'] in advanced_help_msg:
            if not None in advanced_help_msg:
                write(help_msg)
            elif advanced_help_msg[None]:
                write(advanced_help_msg[None])                
            write(advanced_help_msg[opt['h']])
        else:
            write(help_msg)        
            
    if opt['print_opt']:
        write(opt)
            
    if 'h' in opt and opt['h']:
        sys.exit()            

    return(opt)




def read_config_file(fileh_or_path, types_from=None, sep='=', comment_char='#'):
    """Reads parameters from a configuration file

    The file is expected to have a structure like:

    ``option_name1 = value``

    ``option_name2 = another value``

    The file may contain any number of empty lines and comments (i.e. lines that start with #)    

    This function may be used in combination with command_line_options to have different levels
    of default values:
      1) built-in in your scripts
      2) defined in (editable) configuration file
      3) specified when running the script on the command line
    Check the scripts in the templates/ folder of easyterm github for examples.
    
    Parameters
    ----------
    
    fileh_or_path : file | str 
        file path specification or buffer of configuration file to be loaded

    types_from : dict | CommandLineOptions, optional
        If provided, this dictionary or dict-like object is used to infer the expected types of value
        for each key (=parameter name). Values are coerced to the type of values provided in this dictionary,
        and an exception is raised if conversion fails.
        Note: the type of the values of the types_from argument are used! Do not provide types directly as values.
        In a combined read_config_file / command_line_options set-up, def_opt is used here (see examples below)


    sep : str
        defines which separator is used between the option_name and the value in the configuration file.
        Defaults to ``=``

    comment_char : str
        lines starting with this characters are ignored.
        Defaults to ``#``

    Returns
    -------
    opt : CommandLineOptions
        dictionary like object with structure key:arg, carrying options loaded from the file

    Examples
    --------
    Showing the content of an example config file:

    >>> for line in open('example_config.txt'):
    ...   print(line)
    ## this is a config file
    i = inputfile
    o = outputfile
    n = 56

    >>> read_config_file('example_config.txt')
    i : str   = inputfile
    n : str   = 56
    o : str   = outputfile

    Using a default opt to coerce types:

    >>> def_opt={'i':'inputfile',  'n':5,  'o':''}
    ... read_config_file('example_config.txt', types_from=def_opt)
    i : str   = inputfile
    n : int   = 56
    o : str   = outputfile

    **Combining read_config_file and command_line_opt**

    Options have built-in values (initial ``def_opt``).
    Some may be overriden by a configuration file (``conf_opt``). 
    Then again, some may be overriden by command line options (``opt``):

    >>> def_opt = {'i':'inputfile',  'n':5,  'o':''}
    ... conf_opt = read_config_file('example_config.txt', types_from=def_opt)
    ... def_opt.update(conf_opt)  
    ... opt=command_line_opt(def_opt, help_msg='Command line usage: ...')

    """
    out=CommandLineOptions()
    with (fileh_or_path if isinstance(fileh_or_path, io.IOBase)
           else open(fileh_or_path)) as iter_lines:

        for line_index, line in enumerate(iter_lines):
            s=line.strip()
            if not s or s.startswith(comment_char): continue
            pos_sep=s.find(sep)
            if pos_sep==-1:
                raise CommandLineError(f'read_config_file ERROR reading file {fileh_or_path} at row n.{line_index}: {line}')
            key=  s[:pos_sep].strip()
            value=s[pos_sep+1:].strip()
             
            if ( len(value)>1 and 
                 any([value.startswith(q) and value.endswith(q) for q in "'\""]) ):
                value=value[1:-1]                 # dealing with quoted strings arguments

            if not types_from is None:
                if not key in types_from:
                    raise CommandLineError( (f"read_config_file ERROR types_from does not contain the key '{key}' found in config file {fileh_or_path}") )
                expected_type=type(types_from[key])
                if not expected_type in CommandLineOptions.accepted_option_types:
                    raise CommandLineError( (f"ERROR Only these value types are "
                                             f"accepted: {CommandLineOptions.accepted_option_types} "
                                             f"-- Instead it was provided {expected_type} for -{key}"))
                try:
                    if   expected_type is bool:
                        if   value in ('1', 'T', 'True'):
                            value=True
                        elif value in ('0', 'F', 'False'):
                            value=False
                        else:
                            raise CommandLineError(f"ERROR boolean options can only take values F, False, 0, or T, True, 1, or none. Received: -{key} : {value}") from None                        
                    elif expected_type is list:
                        value=shlex.split(value)   ## allowing complex quoted structures
                    elif expected_type in (float, int):
                        value=expected_type(value)
                    elif expected_type is str:
                        pass
                except error:
                    printerr(f'read_config_file ERROR reading file {fileh_or_path} at row n.{line_index}: {line}')
                    raise error from None
                
            out[key]=value
    return out
        
                

def match_any_word(main_string, word_list, is_pattern=True, ignore_case=True):
  """ Given a string and a list of strings/perl_patterns, it returns True is any of them matches the string, False otherwise  """
  for w in word_list:
      if is_pattern:
          if ignore_case:          pattern=re.compile(w, re.IGNORECASE)
          else:                    pattern=re.compile(w)
          if pattern.search(main_string):          return(True)
      else:
          if ignore_case:
              if w.lower() in main_string.lower():  return(True)
          elif w in main_string:                  return(True)
  return(False)

