from cloudregister import cloudregister as cr
import sys
def query_arguments():
    
    arguments = []
    
    if (len(sys.argv) > 1):
        
        for index, arg in enumerate(sys.argv):
        
            if (index):
            
                arguments.append(arg)
            
    return arguments
    
def f2b(index, length):
    
    return length - index - 1

def format_spaces(string):
    
    length = len(string)
    
    forward = [ False for x in string ]
    
    backward = [ False for x in string ]
    
    start = True
    
    for index, x in enumerate(forward):
        
        if (start or forward[index - 1]):
            
            if (string[index] == " "):
                
                forward[index] = True
                
        if (index == 0):
            
            start = False
            
    start = True
    
    for index, x in enumerate(backward):
        
        if (start or backward[index - 1]):
            
            _index = f2b(index, length)
            
            if (string[_index] == " "):
                
                backward[index] = True
                
        if (index == 0):
            
            start = False
                    
    result = "".join([ x for i, x in enumerate(string) if not (forward[i] or backward[f2b(i, length)])])
                 
    #print(string)
    
    #print(forward)
    
    #print(backward)
    
    #print(result)
    
    return result

def safe_eval(string):
    
    string = format_spaces(string)
    
    if (all([ (x.isnumeric() or x == '.') for x in string ])):
        
        return eval(string)
    
    elif (string == "True"):
        
        return True
    
    elif (string == "False"):
        
        return False
    
    elif (type(string) == str):
        
        return string
        
    else:
        
        print(f"Warning [__main__]: {string} is of unsupported datatype.\n")
        
        return 0

def create_register(arguments):
    
    if ((type(arguments) == list) and (len(arguments))):
        
        filename = arguments[0]
        
        register = cr.CRFormat()
        
        print("Enter in format [ key : val ] to add values. (e.g. 0 : True)")
        print("\tEnter [q] to terminate and create register.\n")
        
        while True:
            
            userInput = input("> ")
            
            if (("q" in userInput) and not (":" in userInput)):
                
                break
            
            elif not (":" in userInput):
                
                print(f"Warning [__main__]: {userInput} is invalid for input.")
                
            else:
                
                userInput = userInput.split(":")
                
                key, val = safe_eval(userInput[0]), safe_eval(userInput[1])
                
                register.alter(key, val)
                
        register.save_json(filename)
    
    else:
        
        print("Warning [__main__]: no arguments detected.\n")
        
create_register(query_arguments())