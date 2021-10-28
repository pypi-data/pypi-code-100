try:
    # Things to do
    # spell check function    
    # help Function for key combination in ^Alt Enter               
    # all alt a
    # find function upgrade
    # highlighting backspace pointer potiosion   
    # keep auto save on                                         
    #from ast import Index
    import sys
    import os
    import msvcrt
    from time import sleep as wait
    from traceback import format_exc  
    import ctypes
    from ctypes import wintypes
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    device = r'\\.\CONIN$'
    with open(device, 'r') as con:
        hCon = msvcrt.get_osfhandle(con.fileno())
        kernel32.SetConsoleMode(hCon, 0x0080)    
    user32 = ctypes.windll.user32
    handle=user32.GetForegroundWindow()
    rect = wintypes.RECT()
    class WINDOWINFO(ctypes.Structure):
        """ctype Structure for WINDOWINFO"""
        _fields_ = [
            ("cbSize", wintypes.DWORD),
            ("rcWindow", wintypes.RECT),
            ("rcClient", wintypes.RECT),
            ("dwStyle", wintypes.DWORD),
            ("dwExStyle", wintypes.DWORD),
            ("dwWindowStatus", wintypes.DWORD),
            ("cxWindowBorders", wintypes.UINT),
            ("cyWindowBorders", wintypes.UINT),
            ("atomWindowType", wintypes.ATOM),
            ("wCreatorVersion", wintypes.DWORD),
        ]
    ###get window info    
    info=WINDOWINFO()
    Length = os.get_terminal_size().lines-1
    Width = os.get_terminal_size().columns
    ctypes.windll.user32.GetWindowInfo(handle, ctypes.pointer(info)) 
    CmdLeft,CmdTop,CmdRight,CmdBottom=info.rcClient.left,info.rcClient.top,info.rcClient.right,info.rcClient.bottom
    CmdLength=CmdRight-CmdLeft
    CmdHeight=CmdBottom-CmdTop
    FontHeight=CmdHeight/Length
    FontWidth=CmdLength/Width

    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    pt=POINT()
    user32 = ctypes.WinDLL('user32')
    kernel32 = ctypes.WinDLL('kernel32')

    OpenClipboard = user32.OpenClipboard
    OpenClipboard.argtypes = wintypes.HWND,
    OpenClipboard.restype = wintypes.BOOL
    CloseClipboard = user32.CloseClipboard
    CloseClipboard.restype = wintypes.BOOL
    EmptyClipboard = user32.EmptyClipboard
    EmptyClipboard.restype = wintypes.BOOL
    GetClipboardData = user32.GetClipboardData
    GetClipboardData.argtypes = wintypes.UINT,
    GetClipboardData.restype = wintypes.HANDLE
    SetClipboardData = user32.SetClipboardData
    SetClipboardData.argtypes = (wintypes.UINT, wintypes.HANDLE)
    SetClipboardData.restype = wintypes.HANDLE

    GlobalLock = kernel32.GlobalLock
    GlobalLock.argtypes = wintypes.HGLOBAL,
    GlobalLock.restype = wintypes.LPVOID
    GlobalUnlock = kernel32.GlobalUnlock
    GlobalUnlock.argtypes = wintypes.HGLOBAL,
    GlobalUnlock.restype = wintypes.BOOL
    GlobalAlloc = kernel32.GlobalAlloc
    GlobalAlloc.argtypes = (wintypes.UINT, ctypes.c_size_t)
    GlobalAlloc.restype = wintypes.HGLOBAL
    GlobalSize = kernel32.GlobalSize
    GlobalSize.argtypes = wintypes.HGLOBAL,
    GlobalSize.restype = ctypes.c_size_t

    GMEM_MOVEABLE = 0x0002
    GMEM_ZEROINIT = 0x0040
    #functions
    sleep=lambda:wait(.01)
    def HighestLen(NestedList:list): # for scroll bar find the highest len sublist
        Greatest=0
        for List in NestedList:
            Len=len(List)
            if Len>Greatest:
                Greatest=Len
        return Greatest        
    def get():
        OpenClipboard(None)
        
        handle = GetClipboardData(CF_UNICODETEXT)
        pcontents = GlobalLock(handle)
        size = GlobalSize(handle)
        if pcontents and size:
            raw_data = ctypes.create_string_buffer(size)
            ctypes.memmove(raw_data, pcontents, size)
            text = raw_data.raw.decode('utf-16le').rstrip(u'\0')
        else:
            text = None

        GlobalUnlock(handle)
        CloseClipboard()
        return text

    def put(s):
        if not isinstance(s):
            s = s.decode('mbcs')
        data = s.encode('utf-16le')
        OpenClipboard(None)
        EmptyClipboard()
        handle = GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, len(data) + 2)
        pcontents = GlobalLock(handle)
        ctypes.memmove(pcontents, data, len(data))
        GlobalUnlock(handle)
        SetClipboardData(CF_UNICODETEXT, handle)
        CloseClipboard()   
    while 1:
        def flat(Function):
            global para,index,pointer,Highlight
            d=para.copy()
            try:
                d[index[0][0]][index[0][1]]="\u001b[44m"+d[index[0][0]][index[0][1]]
            except IndexError :
            
                print("foo")
            try:
                d[index[1][0]][index[1][1]]="\u001b[0m"+d[index[1][0]][index[1][1]]
            except IndexError:
                d[index[1][0]].extend(list(" "*(len(d[index[0][0]])-index[0][1]+1)))
                d[index[1][0]][index[1][1]]="\u001b[0m"+d[index[1][0]][index[1][1]]
            content=""
            for line in d:
                content+="".join(line)+"\n"
            if Function=="del":                                              
                chunks=content.split("\u001b[44m")
                chunk=chunks[-1].split("\u001b[0m")[1:]
                content=""
            if len(chunks)>1:
                content+=chunks[0]
            content+="".join(chunk)
            d=[]
            for line in content.split("\n"):

                d.append(list(line))
            para=d.copy()
            if Function=="copy":
                chunks=content.split("\u001b[44m")
                chunk=chunks[-1].split("\u001b[0m")[0]
                command = 'echo | set /p nul=' + chunk.strip() + '| clip'
                os.system(command)
            if Function =="cut":
                chunks=content.split("\u001b[44m")
                chunk=chunks[-1].split("\u001b[0m")
                command = 'echo | set /p nul=' + chunk[0].strip() + '| clip' 
                os.system(command)
                chunk=chunk[1:]                                            
                content=""
            if len(chunks)>1:
                content+=chunks[0]
            content+="".join(chunk)
            d=[]          
            for line in content.split("\n"):
                
                d.append(list(line))
            para=d.copy()                                                                                                                                                                           
        def Input():
            while 1:
                if ctypes.windll.user32.GetKeyState(0x01)>1:
                    return (1,0) 
                if msvcrt.kbhit():            
                    return (0,ord(msvcrt.getch()))
                sleep()
        def queryMousePosition():
            global pt
            ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
            return (pt.x,pt.y)                
    
        def saving(s=1,repl=1):
            global string, para, argument, Saved, tmp, postulnar, a,Named
            string = ""
            a = []
            if not Named:
                args.append('Un')
                Named=1
                rename()
                args[1]=argument
                
            for line in para:
                a.append(list(line))
                string += "".join(line)+"\n"
            try:    
                File = open(argument, "w")
                File.write(string)
                File.close()

                Saved = s
                if repl:
                    tmp = (a, pointer.copy(), postulnar.copy(),
                        tmp[0].copy(), tmp[1].copy(), tmp[2].copy())                  
            except PermissionError:
                1                   
        def rename():
            global argument,args,Exit,key,info
            A = argument
            argument = input("New File Name:")
            if os.path.isfile(argument):
                answer = input(
                    "File Name Already Exist Do You Want To Replace The File [y/n]:").lower()
                if answer in ["y", "yes"]:
                    if key in [18]:
                        os.remove(A)
                        a=open(argument,"w")
                        a.write(Text)
                        args[1] = argument
                        Exit = 1
                else:
                    argument = A
            else:
                if key in [18]:
                        os.remove(A)
                        a=open(argument,"w")
                        a.write(Text)
                        args[1] = argument
                        Exit = 1        
            Exit = 1  
            info=argument 
        Name = 0
        args = sys.argv
        Named=1
        WordCount=0
        if len(args) > 0:

            os.system("color")
            argument = ' '.join(args[1:])
            if len(args)>1:
                if os.path.isfile(argument):
                    Name = 1
                    File = open(argument, "r")
                    Text = File.read()
                    File.close()
            if len(args)<2:
                Text=""
                argument="Untitled"
                Named=0
                Name="Untitled"
            if not Name:
                if len(args) > 2:
                    if "n+" in args[1:]:
                        Name = 1
                        argument = args[1]
                        if os.path.isfile(argument):
                            File = open(argument, "r")
                            Text = File.read()
                            File.close()
                        else:
                            File = open(argument, "x")
                            File.close()
                            Text = ""        


                if not Name:
                    from glob import glob
                    print("No File Has That Name ")
                    choices=[]
                    for remove in range(len(argument)):
                        choices = glob(argument+"*")
                        if len(choices) > 2:
                            break
                        argument = argument[:-1]
                    if len(choices) > 0:
                        print("Here Are Similar Named Files:")
                        for item in choices:
                            print("-"+item)   
                        exit()
                    else:
                        print("No File With Similar Name")
                        exit()
            lines = Text.split('\n')
            para = []
            a = []
            t=[]
            for line in lines:
                t.append(line.replace("\x00"," "))
            lines=t
            while lines[-1].replace(" ","")=="": #removes enter characters add the end of the document
                del lines[-1]
            for line in lines:        
                para.append(list(line))
                a.append(list(line))   

            if len(para)<Length: 
                para.extend([[] for _ in range(Length-len(para))])   
            ###start 1    
            scrollBar=[(0,-1),(0,-1)] # false for columns and false for lines
            Exit = 0
            number =0
            postulnar = [0, 0]
            pointer = [0, 0]
            tmp = (a, pointer.copy(), postulnar.copy(), para, pointer, postulnar)
            info = argument[:Width-2]
            Saved = 1
            saves = ("*"," ")
            shortcut = 0
            Highlight = [0, [[]]]
            saver=0 
            batterySaver=0
            # \u001b[48;5;239m grey  \u001b[44m blue   \u001b[0m reset
            while Exit == 0:
                output=1 
                string = info+saves[Saved]
                string+=" "*(Width-len(string))
                key = 0
                Remove = ""
                num = 0
                i = 1
                index=[]
                w=Width
                if number:
                    l=len(str(postulnar[1]+1+Length))               
                    Width-=l+1
                    n=postulnar[1]+1
                for line in range(postulnar[1], postulnar[1]+Length):
                    if number:
                        nn=str(n)
                        string+="\u001b[38;5;245m"+"0"*(l-len(nn))+nn+"\u001b[0m"+" "
                        n+=1
                    for char in range(postulnar[0], postulnar[0]+Width):
                        try:
                            # pointer end highlighting
                            if Highlight[0] and [char, line] == Highlight[1][0]:
                        
                                if not num :
                                    index.append([line,char])
                                    string += "\u001b[44m"
                                else:
                                    if len(index)>0:
                                        index.append([line,char])
                                        string += "\u001b[0m"
                                num += 1
                            if pointer != [char, line]:
                                string += para[line][char]
                            else:
                                para[line] += " "
                                Remove = line
                                string += "\u001b[48;5;239m" + \
                                    para[line][char]+"\u001b[0m"

                                if Highlight[0]:
                                    index.append([line,char])
                                    if not num:
                                        string += "\u001b[44m"
                                    num += 1
                        except IndexError:
                            left= Width-(char)+postulnar[0]
                            if pointer[1]==line and pointer[0]>char:
                                string+=" "*(pointer[0]-char)+"\u001b[48;5;239m \u001b[0m"+" "*(left-(pointer[0]-char)-1)
                            else:
                                string +=" "*left
                            break
  
                if WordCount:

                    Count=0
                    for line in para:
                        Count+=len("".join(line).split())
                    string+="Word Count:"+str(Count)+"\n"                
                if Remove != "":
                    del para[Remove][-1]
                string+="\u001b[0m"
                if scrollBar[0][0]:
                    string+=" "*int(postulnar[0]//scrollBar[0][1])+"\u001b[48;5;248m"+" "*int(Width*scrollBar[0][1])+"\u001b[0m"+" "*(Width-(int(postulnar[0]//scrollBar[0][1])+int(Width*scrollBar[0][1])))
                print(string, end="",flush=1)
                ###start 2
                key = Input()
                if key[0]: # mouse 
                    MouseCords=queryMousePosition()
                    if (CmdRight>=MouseCords[0] and MouseCords[0]>=CmdLeft) and (CmdBottom>=MouseCords[1] and MouseCords[1]>=CmdTop):
                        lines=int(((MouseCords[1]-CmdTop)//FontHeight)) # possible 1.1 #ceil
                        columns=int(((MouseCords[0]-CmdLeft)//FontWidth))
                        NewPos=[postulnar[0]+columns,postulnar[1]+lines] # list so that if pointer != NewPos will work DO NOT TUPLIZE
                        if [postulnar[0]+pointer[0],postulnar[1]+pointer[1]] !=NewPos: # So that if mose be border will stay in same place
                            pointer=NewPos # change pointer to be where mouse was clicked           
                else:
                    key=key[1]  
                    #input(key)    
                    if number:
                        Width=w
                    if key not in [13, 8, 224, 19, 5, 31, 18, 26, 9, 127, 146, 10, 25,11,0,14,20,24,4,23,16,15,-1,12,2]:
                        Saved = 0
                        if len(para[pointer[1]])>=pointer[0]:
                            para[pointer[1]].insert(pointer[0], chr(key))
                        else:
                            para[pointer[1]].extend([" "]*(pointer[0]-len(para[pointer[1]])))
                            para[pointer[1]].append(chr(key))              
                        pointer[0] += 1
                    else:
                        ###start of Key Function
                        ###start of multi Input Function
                        if not  key: # help,highlight,shift tab,copy,cut,paste,begining/end of file,word count,find, battery saver
                            end=Input()[1]
                            #input(end)
                            if end==46: #^ Alt c spell check
                                for i in range(2): 
                                    try:
                                        WordCheck=open("words.txt","r")
                                        WORDS=WordCheck.read()
                                        Words=WORDS.split("\n")
                                        WordCheck.close()
                                        break
                                    except FileNotFoundError:
                                        os.system("curl -OL https://raw.githubusercontent.com/dwyl/english-words/master/words.txt")
                                            
                                import re
                                from difflib import get_close_matches as closest
                                hash={'':0}
                                words=""
                                for word in Words: 
                                    hash[word.lower()] = 0 
                                l=[]
                                for line in para:
                                    l.append("".join(line))
                                test="\n ".join(l)  

                                phrases=re.sub(r"[^a-zA-Z ]",'',test)
                                phrases=phrases.split(" ")
                                orginal=test.replace("\n","").split(" ")
                                FakeWords={}
                                n=0

                                for word in phrases:
                                    word=re.sub("[^0-9a-zA-Z]","",word)
                                    # mode=0
                                    # if word.isupper():
                                    #     mode=1
                                    # try:    
                                    #     if not word[0].islower():
                                    #         mode=2   
                                    # except IndexError:
                                    #     mode=0           
                                    if hash.get(word.lower(),1):
                                        FakeWords[orginal[n]]=word
                                    n+=1       
                                for Fake in FakeWords:
                                    orginalword=Fake.lower()
                                    RealWord=Fake
                                    Fake=FakeWords[Fake].lower()
                                    fake=Fake
                                    SubWords=[]
                                    add=RealWord.split(FakeWords[RealWord])
                                    a=add[0]
                                    if len(add)>1:
                                        b=add[-1]
                                    else:       
                                        b=""                         
                                    while len(SubWords)<100:
                                        SubWords=re.findall(r"\b"+fake+"\w+",WORDS)
                                        fake=fake[:-1]

                                    Choices=closest(Fake.lower(),SubWords,len(SubWords))
                                    old={}
                                    for choice in Choices:
                                        if not old.get(choice,0):
                                            old[choice]=1
                                    Choices=list(old.keys())  
                                    
                                    if RealWord.isupper():
                                        for i in range(len(Choices)):
                                            Choices[i]=Choices[i].upper() 
                                            Choices[i]=a+Choices[i]+b   
                                    elif not RealWord[0].islower():
                                        for i in range(len(Choices)):
                                            Choices[i]=Choices[i][0].upper()+Choices[i][1:]  
                                            Choices[i]=a+Choices[i]+b  
                                    elif RealWord[0].islower():
                                        print(i,len(Choices))
                                        Choices[i]=a+Choices[i]+b        
                                    if len(Choices)>3:
                                        choices=Choices[:3]
                                    else:
                                        choices=Choices                                                                                                                                                
                                    done=0 # vars for loop
                                    ViewAll=0
                                    while not done:
                                        print("")
                                        print("Possible Incorrectly Spelled Word:"+RealWord+"\n0.Do Not Change Word")
                                        Number=1
                                        a=""
                                        for change in choices:
                                            if change !=a:
                                                print(str(Number)+". Change "+RealWord+" to:",change)
                                                Number+=1
                                            
                                                a=change
                                            else:
                                                break   
                                        if not ViewAll:    
                                            print(str(Number)+". To See Full list") 
                                        else:
                                            print(str(Number)+". To See Best Words")    
                                        Number+=1
                                        print(str(Number)+". To Input Own Word(s) ") 
                                        Number+=1
                                        print(str(Number)+". To Add Word(s) To Dictonary ") 
                                        Number+=1                                
                                        print(str(Number)+". To Exit Spell Checking Menu")
                                        while 1:
                                            try:
                                                descion=int(input("Choice:"))
                                                if descion>-1 and descion<=Number:
                                                    break
                                                else:
                                                    print("Please Type In Integer From 0 To",Number)
                                            except ValueError:
                                                print("Please Type In Integer") 
                                        while 1:        
                                            if descion==0: # don't change word
                                                done=1
                                                break
                                            if descion<=Number-4:
                                                test=test.replace(RealWord,choices[descion-1])      
                                                done=1
                                                break
                                            if descion==Number-3:#See best or all of the word list
                                                if not ViewAll:
                                                    choices=sorted(Choices)  
                                                    ViewAll=1
                                                else:
                                                    choices=Choices[:3]
                                                break       
                                            if descion==Number-2:
                                                test=test.replace(RealWord,input("Replaced Incorrectly Spelled Word With:"))
                                                done=1
                                                break
                                            if descion==Number-1:
                                                WordCheck=open("words.txt","a")
                                                WordCheck.write("\n"+Fake)  
                                                WordCheck.close()    
                                                done=1                                          
                                                break
                                            break
                                        if descion==Number:
                                            break
                                    if descion==Number:
                                        break        
                                l=test.split("\n ") 
                                char=[]
                                for line in l:
                                    char.append(list(line))  
                                para=char.copy()                        



                                        
                                        
                            if end==33: # find
                                find=input("Find:")
                                l=[]
                                for line in para:
                                    l.append("".join(line))
                                test="\n".join(l)                          
                                replac=input("Replace With:").replace("\\n","\n")
                                answer = input("Do You Want To Replace All Occurrences [y/n]:").lower()
                                if answer in ["y", "yes"]:  
                                    test=test.replace(find,replac)
                                else:                        
                                    print(list(find))
                                    amount=test.count(find)
                                    Find=(find+chr(15))
                                    test=test.replace(find,Find)

                                    for num in range(amount):
                                        n=str(num+1)
                                        if num==0:
                                            n+="st"
                                        if num==1:
                                            n+="nd"
                                        if num==2:
                                            n+="rd"
                                        if num>=3:
                                            n+="th"            
                                        answer = input("Do You Want To Replace "+n+" Occurrences [y/n]:").lower()
                                        if answer in ["y", "yes"]:
                                            test=test.replace(Find,replac,1)
                                        else:
                                            test=test.replace(Find,find,1) 
                                b=[]
                                for line in test.split("\n"):
                                    b.append(list(line))
                                para=b.copy()                 
                                key=0 
                            if end==49: 
                                A=argument
                                argument = input("New File Name:")
                                if os.path.isfile(argument):
                                    answer = input(
                                        "File Name Already Exist Do You Want To Replace The File [y/n]:").lower()
                                    if answer in ["y", "yes"]:
                                            args[1] = argument

                                            saving()
                                            Exit = 1
                                    else:
                                        argument = A
                                else:
                                    args[1] = argument
                                    saving()
                                Exit = 1                           
                            if end==17: # Word Count
                                input("help")
                                WordCount=not WordCount
                                if WordCount:
                                    Length-=1
                                else:
                                    Length+=1    
                            if end==153: #Go to Begining of File
                                pointer[1]=0                                                                 
                            if end==161: # Go to end of File 
                                pointer[1]=len(para)-1                                                 
                            if end==30: # Highlight  all
                                input("all has not been implemented yet")                                               
                            if end==46: #copy
                                if Highlight[0]:
                                    flat("copy")
                            if end==45: # cut                        
                                flat("cut")                                                    
                            if end==47: # ^ Alt p paste           
                                data=get()
                                text=data.replace("\r","").split("\n")              
                                text[-1]+="".join(para[pointer[1]][pointer[0]:])
                                del para[pointer[1]][pointer[0]:]
                                para[pointer[1]].extend(list(text[0]))
                                for line in text[1:]:
                                    pointer[1]+=1
                                    para.insert(pointer[1],list(line))   
                                    Saved=0                          
                            if end==148:# ^Tab = Shift Tab
                                if pointer[0]<3:
                                    pointer[0]=3
                                try:
                                    para[pointer[1]]=para[pointer[1]][:pointer[0]-3]+para[pointer[1]][pointer[0]:]
                                except IndexError:
                                    1
                                pointer[0]-=3
                            if end in [53,35]: #help
                                input("""
        Key:           Function:

        ^+Alt+?        List Key Combation & Their Functions
        ^+Backspace    Delete Everythings
        ^+k            Auto Save
        ^+Enter        To Highlight and changes Function of Key Combation
        ^+Alt+c        To Spell Check Document

                                """)
                        ###start of monokey function
                        if key==2:#^b battery saver
                            if batterySaver:
                                batterySaver=0
                                sleep=lambda:wait(.01)
                            else:
                                batterySaver=1
                                sleep=lambda:wait(.05)   
                                         
                        if key==12: #load
                            handle=user32.GetForegroundWindow()
                            nfo=WINDOWINFO()
                            l=Length
                            Length = os.get_terminal_size().lines-1
                            Width = os.get_terminal_size().columns
                            ctypes.windll.user32.GetWindowInfo(handle, ctypes.pointer(nfo)) 
                            CmdLeft,CmdTop,CmdRight,CmdBottom=nfo.rcClient.left,nfo.rcClient.top,nfo.rcClient.right,nfo.rcClient.bottom
                            CmdLength=CmdRight-CmdLeft
                            CmdHeight=CmdBottom-CmdTop
                            FontHeight=CmdHeight//Length
                            FontWidth=CmdLength//Width
                            info = argument[:Width-2]
                            print("\n"*(Length-l))
                        if key==15: # open file
                            FileName=input("File Name:")  
                            del args[1:]
                            args.extend(FileName.split())

                            a="start cmd /c python "+" ".join(args)      
                            os.system(a)                    
                        if key==16: # ^p print file

                            saving()
                            File=open(info,"r")
                            contents=File.read()
                            orginal=contents
                            File.close()
                            done=0
                            change=input("Do You Want To Change The Printing Settings [y/n]:").lower()
                            while not done:                        
                                if change=="y":
                                    print("ln:a;b(print lines a throught b auto:1;-1),mc:(auto 0; max amount of chars on line),fmt:(auto:n; options n(normal) 0(none),spc:spacing number,ext:1(to exit from printing);Format input is cascading")
                                    args=input("Format:").lower()
                                    commands= args.split(",")
                                    EXIT=0
                                    for command in commands:
                                        while 1:
                                            func= command.split(":")
                                            name=func[0]
                                            if name=="ln":
                                                values=func[1].split(";")
                                                a,b=int(values[0]),int(values[1])
                                                if b<0:
                                                    b+=1 
                                                a-=1
                                                b-=1    
                                                contents="\n".join(contents.split("\n")[a:b])
                                                break
                                            if name=="mc":
                                                Max=int(func[1])
                                                if Max:
                                                    Lines=contents.split("\n")
                                                    String=""                                    
                                                    length=0                                  
                                                    for line in Lines:
                                                        word=""  
                                                        for char in line:
                                                            if  length>=Max:
                                                                String+="\n"
                                                                length=0
                                                            if char==" " :
                                                                String+=word+" "
                                                                word=""
                                                            else:
                                                                word+=char  
                                                            length+=1 
                                                        # if length+len(word)>Max:
                                                        #     String+="\n"+word+"\n"
                                                        else:
                                                            String+=word+"\n"

                                                    contents=String       
                                                break
                                            if name=="spc":
                                                contents=contents.replace("\n","\n"*int(func[1]))
                                                break
                                            if name=="fmt":
                                                name=func[1]
                                                if name=='n':
                                                    a=contents.split(".\n")
                                                    String=""
                                                    for chunk in a:
                                                        if "\n" in chunk:
                                                            String+="\n"+chunk+". "
                                                        else:
                                                            String+=chunk+". "
                                                    contents=String
                                                break
                                            if name=="ext":
                                                EXIT=1
                                                break
                                            break
                                else:
                                    a=contents.split(".\n")
                                    String=""
                                    for chunk in a:
                                        if "\n" in chunk:
                                            String+="\n"+chunk+". "
                                        else:
                                            String+=chunk+". "
                                    contents=String      
                                if EXIT:  
                                    break                                                
                                File=open("preview.txt","w+") 
                                File.write(contents)
                                File.close()      
                                a="start cmd /c python pykernel.py preview.txt" 
                                os.system(a) 
                                done=input("Are You Happy With The Format of The File [y/n]:").lower()
                                if done=="n":
                                    done=0
                                else:
                                    done=1    
                                change="y"  
                            if not EXIT:      
                                os.startfile("preview.txt", "print")  
                                wait(1)                    
                        if key==23: # ^w wipe 
                            answer = input(
                                "Are You Sure You Want To Delete This File File [y/n]:").lower()
                            if answer in ["y", "yes"]:                           
                                os.remove(info)
                                Exit=1
                                raise SystemExit("Delted File")
                        if key==4: # ^d Duplicate 
                            saving()
                            argument = input("Duplicate File Name:")
                            if os.path.isfile(argument):
                                answer = input(
                                    "File Name Already Exist Do You Want To Replace The File [y/n]:").lower()
                                if answer in ["y", "yes"]:
                                        args[1] = argument
                                        saving()
                                        Exit = 1
                                else:
                                    argument = argument
                            else:
                                args[1] = argument
                                saving()
                            Exit = 1   
                        if key==21:#^u output data       
                            key=24
                            output=1                        
                        if key==24: #^x Run
                            if saver:
                                saving()
                            l=[]
                            for line in para:
                                l.append("".join(line))
                            test="\n".join(l)  
                            def run(your_code, mode='activate'):
                                try:
                                    your_code=compile(your_code,info,"exec")
                                except Exception as e:
                                    print(format_exc())
                                    return
                                try:
                                    exec(your_code)    
                                except Exception as e:
                                    print(format_exc())
                                    #   a=format_exc()
                                    # b=a.splitlines()
                                    # c=b[5].split("<")[1].replace(">","")
                                    # if c=="listcomp":
                                    #     input("hello world")
                                    #     d=str(e.args).split("'")[1]
                                    #     print(d)
                                    #     args[d]=eval(d)
                                    #     run(test,args)
                                    
                                    # else:
                                    #     print(a)    
                                        
                            try: 
                                run(test)                        
                            except SystemError:
                                break
                            except KeyboardInterrupt:
                                break
                            input("\nGo Back To Code")
                            key=0
                        if key==14: #number
                            number= not number
                        if key==20: # go to ^t
                            while 1:
                                try:
                                    pointer[1]=int(input("To Line:"))-1
                                    postulnar[1]=pointer[1]
                                    character=0
                                    for char in para[pointer[1]]:
                                        if char==" ":
                                            character+=1
                                        else:
                                            break
                                    if character==len(para[pointer[1]]):
                                        character=0
                                    pointer[0]=character
                                    break
                                except (TypeError):
                                    1
                                except IndexError:
                                    if pointer[1]>=len(para):
                                        pointer[1]=len(para)-1
                                    else:
                                        pointer[1]=0   
                                    break     
                        if key==127:#delete all
                            para=[[]]
                            Saved=0
                        if key==11: # auto save
                            saver=not saver                       
                        if key == 10:  # ^Enter
                            shortcut = not shortcut
                            Highlight[0] = 0
                        #Saved = Saved
                        if key in [224]:  # arrow keys
                            Saved = Saved
                            end = Input()[1]
                            #input(end)
                            keys = {75: [-1, 0], 72: [0, -1], 80: [0, 1], 77: [1, 0]}
                            Key = keys.get(end, [0, 0])
                            if shortcut:
                                if not  Highlight[0]:
                                    Highlight = [1, [pointer.copy()]]

                            pointer = [pointer[i] + Key[i] for i in range(2)]
                            if end==115: #to last word
                                Line=para[pointer[1]]
                                end=pointer[0]
                                space=0
                                start=end
                                breaking=1
                                for char in reversed(Line[:end]): 
                                    if char==" ":
                                        if space==2:
                                            break
                                        elif space==0:
                                            space=1                                   
                                    elif space==1:
                                        space=2
        
                                    end-=1  
                                if start==end:
                                    if pointer[1]>0:
                                        pointer[1]-=1
                                        end=len(para[pointer[1]])-1
                                        for char in reversed(para[pointer[1]]):
                                            if char!=" ":
                                                break
                                            end-=1
                                pointer[0]=end  
                            if end==116: #to next word
                                Line=para[pointer[1]]
                                end=pointer[0]
                                space=0
                                start=end
                                breaking=1
                                for char in Line[end:]: 
                                    if char!=" ":
                                        if space==2:
                                            break
                                        elif space==0:
                                            space=1                                   
                                    elif space==1:
                                        space=2
        
                                    end+=1       
                                pointer[0]=end-1                                        
                            if end == 79:  # Fn -> End of Line
                                character=len(para[pointer[1]])
                                for char in reversed(para[pointer[1]]): # find last non space character
                                    if char==" ":
                                        character-=1
                                    else:
                                        break
                                if not character or character==pointer[0]:
                                    character=len(para[pointer[1]])
                                pointer[0] = character
                            if end == 71:  # home:
                                character=0
                                for char in para[pointer[1]]:
                                    if char==" ":
                                        character+=1
                                    else:
                                        break
                                if character==len(para[pointer[1]]) or character==pointer[0]:
                                    character=0    
                                pointer[0] = character
                            if end == 81:  # page down
                                pointer[1] +=Length
                            if end == 73:  # page up
                                pointer[1] -=Length
                            if end==83:
                                try:
                                    del para[pointer[0]][pointer[1]]  
                                    Saved = 0     
                                except IndexError:
                                    1     
                        if key == 8:  # backspace                              
                            if Highlight[0] == 0:
                                if pointer != [0, 0]:
                                    Saved = 0
                                    pointer[0] -= 1
                                    try:
                                        if pointer[0] == -1:
                                            pointer[0] = len(para[pointer[1]-1])
                                            para[pointer[1]-1].extend(para[pointer[1]])
                                            del para[pointer[1]]
                                            pointer[1] -= 1
                                        else:
                                            del para[pointer[1]][pointer[0]]
                                    except IndexError:
                                        1
                            else:                                                                           
                                p=flat("del")                                            
                        if key == 13:  # enter:
                            Saved = 0
                            if para[pointer[1]][pointer[0]:]!=[" "]*len(para[pointer[1]][pointer[0]:]): # not end of line 
                                para[pointer[1]+1:pointer[1] +1] = [para[pointer[1]][pointer[0]:]]   
                            else: # end of line
                                para[pointer[1]+1:pointer[1]+1]=[[]]                                
                            para[pointer[1]] = para[pointer[1]][:pointer[0]]                   
                            para[pointer[1]+1][0:0]=[" "]*(len(para[pointer[1]])-len("".join(para[pointer[1]])))
                            character=0                                
                            for char in para[pointer[1]]:
                                if char==" ":
                                    character+=1
                                else:
                                    break                       
                            pointer[1]+=1
                            pointer[0]=character
                        if key == 19:  # ^s
                            saving()
                        if key == 5:  # ^e
                            if not Saved:
                                answer = input(
                                    "Work Is Unsaved Do You Want To Save Your Work [y/n]:").lower()
                                if answer in ["y", "yes"]:
                                    saving()
                            raise SystemExit("\nUser Exited Program")
                        if key in [31, 18]:  # rename/save as
                            rename()
                        if key == 26:  # undo
                            tmp = [tmp[i].copy() for i in range(len(tmp))]
                            para = tmp[0]
                            pointer = tmp[1]
                            postulnar = tmp[2]  
                            Saved = 1
                        if key == 25:  # redo
                            para = tmp[3]
                            Saved = 0
                        if key == 9:  # tab
                            para[pointer[1]] = para[pointer[1]][:pointer[0]] + \
                                list(" "*3)+para[pointer[1]][pointer[0]:]
                            pointer[0] += 3
                i=1        
                if Highlight[0] == 1:
                    i = 2
                #start of reformatting   
                for i in range(i):
                    if len(para)<Length: #document has less lines than view
                        para.extend([[] for _ in range(Length-len(para))])   
                    if postulnar[1]>=len(para)-Length:# view past document
                        postulnar[1]=len(para)-Length
                    if postulnar[1]>pointer[1]-4: # view out of document -4 for better view of document not need 
                        #print(-2)
                        if postulnar[1]>3: # so you cannot get negtive values
                            postulnar[1]=pointer[1]-4
                        else:
                            postulnar[1]=0      
                    if saver:
                        saving(1,0)
                    if pointer[1] >= len(para)-1: #pointer past document
                        #print(-1)
                        pointer[1] = len(para)-1 #pointer above document
                    if pointer[0] < 0:
                        #print(0)
                        pointer = [len(para[pointer[1]-1])-1, pointer[1]-1]
                    if pointer[1] < 0:
                        #print("1")
                        pointer,postulnar = [0, 0],[0,0]
                    if pointer[1] >= len(para)-1: # pointer past document
                        #print("3")
                        pointer[1] = len(para)-1    
                    if pointer[0] > Width+postulnar[0]-4: # pointer out of view
                        #print(4)
                        postulnar[0] +=pointer[0]-(Width+postulnar[0]-4)
                    if pointer[1] > Length+postulnar[1]-4:
                        #print(5)
                        postulnar[1] += pointer[1]-(Length+postulnar[1])+4
                    if postulnar[0] > pointer[0]-3:# pointer right of view
                        #print(6)
                        if postulnar[0]>3:
                            postulnar[0] -=postulnar[0]-pointer[0]+3
                        else:
                            postulnar[0]=0    
                
                    if postulnar[0] < 0:
                        #print(7)
                        postulnar[0] = 0
                        if(len(para[pointer[1]-1])) < 1:
                            pointer = [0, pointer[1]-1]
                    if postulnar[1]+Length>len(para): # view encapesale line after the documet
                        postulnar[1]=len(para)-Length
                    if i == 0:
                        p = pointer.copy()
                        pointer = Highlight[1][0].copy()   
                Highlight[1][0] = pointer.copy()
                pointer = p.copy()
                ###scroll bar code
                # wBar=Width/HighestLen(para)
                # lBar=Length/len(para)
                # if scrollBar[0][0]:
                #     if wBar>=1:
                #         Length+=1
                #         scrollBar[0]=(0,-1)
                #     else:
                #         scrollBar[0]=(1,wBar)    
                # else:
                #     if wBar<1:
                #         Length-=1
                #         scrollBar[0]=(1,wBar)


                
except KeyboardInterrupt:
    if not Saved:
        answer = input("Work Is Unsaved Do You Want To Save Your Work [y/n]:").lower()
        if answer in ["y", "yes"]:
            saving()
    raise SystemExit("\nUser Exited Program")    





