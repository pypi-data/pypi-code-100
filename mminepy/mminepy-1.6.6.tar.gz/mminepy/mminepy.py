import inspect
import os
import sys
#시스템 아웃풋을 없게 한다
sys.tracebacklimit = 0
#이벤트 분류를 할 때 사용한다.
global Event_name
Event_name = ''
#에러가 있다면 몇줄에 있는지
global whenerror
whenerror = 0
#command가 들어가 있는지 여부 판단
global command_contain
command_contain = 0
#repeat을 할 떄 list의 종류를 차례로 받는것이다.
global list_name_list
list_name_list = []
#부득이 하게 자료형을 변환해야 할떄 쓰는 리스트
global type_list
type_list = []
#메인. 행동에 대해 분류하는 리스트다.
global check_list
check_list = []
#들여쓰기를 위해 만든 변수. 이 변수를 통해 연산자의 끝나는 위치를 찾는데도 활용된다.
global python_space
python_space = 0
#event의 개수에 따라 함수가 겹치지 않게 만들어 주는 변수
global event_value
event_value = 0
#변수에 이름이 key,변수값이 value인 dictionary
global var_dict
var_dict = {}
#import package를 추가하는 리스트
global addition_list
addition_list = []
#command문을 적을 떄 return false가 필요한지 물어보는 문제
global isreturnneed
isreturnneed = -1
#반복할 때 필요한 변수. 한번 돌고 나오도록 만들어주는 코드이다.
global repeat_var
repeat_var = 0
#if를 사용 할 떄 필요한 변수. 한번 돌고 나오도록 만들어주는 코드이다.
global when_var
when_var = 0
#변수가 이미 선언되었는지 필요한 리스트 없다면 코드를 자동 선언해준다
global var_list
var_list = []
#메인2.자바의 쓸 코드를 실질적 string에 저장해주는 곳.
global javacode
javacode = ''
#range는 range만의 알고리즘이 필요하기 때문에, for_range라는 이름으로 행동을 분류하였다.
def range(first,second):
    global check_list
    check_list.append("for_range")
    return [1] #아무값이나 넣어줌(힌번만 돌게)
class time:
    def sleep(second):
        global check_list
        check_list.append("activity")
#random값을 넣게 되면 python자체 값으로 돌아가므로 java값을 만들기 위해 random 클래스를 만듬(물론 randint만 필요)
class random:
    def randint(first,second):
        pass
#자동으로 변수를 선언 해주는 함수이다.
#m에 type에 맞는 code를 만들어
#javacode에 추가해준다.
def define_auto(code):
    var_name = code.split("=")[0]
    global addition_list
    global var_dict_type
    global var_list
    global var_dict
    global javacode
    m = ''
    code1 = code.split(".")[-1]
    if code1.__contains__("size"):
        code1 = code.split(".")[-2]
    elif code1.__contains__("get("):
        code1 = code
    code = code1
    type_Var = ""
    code = code.replace(" ","")
    if code.__contains__('getPlayer') or code.__contains__('sender') or code.__contains__('getEntity') or code.__contains__('getDamager'):
        type_Var = "Player"
        m = 'public Player '+var_name+";\n"
        if not addition_list.__contains__("org.bukkit.entity.Player"):
            addition_list.append("org.bukkit.entity.Player")
    elif code.__contains__('getWorld'):
        type_Var = "World"
        m = 'public World '+var_name+";\n"
        if not addition_list.__contains__("org.bukkit.World"):
            addition_list.append("org.bukkit.World")
    elif code.__contains__('getItemInHand'):
        type_Var = "ItemStack"
        m = 'public ItemStack '+var_name+" = new ItemStack();\n"
    elif code.__contains__('getName') or code.__contains__('toString'):
        type_Var = "String"
        m = 'public String '+var_name+";\n"
    elif code.__contains__('getInventory'):
        type_Var = "Inventory"
        m = 'public Inventory '+var_name+";\n"
        if not addition_list.__contains__("org.bukkit.inventory.Inventory"):
            addition_list.append("org.bukkit.inventory.Inventory")
    elif code.__contains__('getLocation'):
        type_Var = "Location"
        m = 'public Location '+var_name+";\n"
        if not addition_list.__contains__("org.bukkit.Location"):
            addition_list.append("org.bukkit.Location")
    elif (code.__contains__('getX') or code.__contains__('getY') or code.__contains__('getZ') or code.__contains__("randint") 
    or code.__contains__("getDamage")):
        m = 'public Integer '+var_name+";\n"
        type_Var = "Integar"
    elif code.__contains__('getBlock'):
        type_Var = "Block"
        m = 'public Block '+var_name+" = new Block();\n"
        if not addition_list.__contains__("org.bukkit.block.Block"):
            addition_list.append("org.bukkit.block.Block")
    elif code.__contains__('getMaterial'):
        m = 'public Material '+var_name+";\n"
        type_Var = "Material"
        if not addition_list.__contains__("org.bukkit.Material"):
            addition_list.append("org.bukkit.Material")
    elif code.__contains__(".get("):
        code = code.replace(".get("," ")
        code = code.replace(")"," ")
        code = code.replace("="," ")
        code1 = code.split(" ")[0]
        code2 = code.split(" ")[1]
        var_name = code1
        m = 'public '+str(var_dict.get(code2))+' '+code1+";\n"
        type_Var = str(var_dict.get(code2))
    type_Var2 = type_Var.lower()
    var_name = var_name.replace(" ","")
    kq = str(var_dict.get(var_name))
    kq = kq.lower()
    kq = kq.replace(" ","")
    if var_dict.__contains__(var_name) and kq != type_Var2:
        raise Exception("you already defined in other type")
    if not var_list.__contains__(var_name):
        var_name = var_name.replace(" ","")
        var_dict[var_name] = (type_Var)
        javacode = javacode.replace("implements Listener{\n","implements Listener{\n"+'    '+m)
        var_list.append(var_name)
    return javacode
class space:
    def forfinish(code):
        global python_space
        global javacode
        global java_space
        global isreturnneed
        global check_list
        while not code.__contains__("    "*python_space):
            java_space -=1
            javacode = space.getspace(javacode)
            javacode += "}\n"
            python_space -=1
        return code
    def getspace(string):
        global java_space
        string += "    "*java_space
        return string
def init():
    global entitydamagebyentityevent1
    global entitydamageevent1
    global playermoveevent1
    global blockbreakevent1
    global playerinteractevent1
    global playerjoinevent1
    global playeritemheldevent1
    global blockfertilizeevent1
    global blockexplodeevent1
    global blockcookevent1
    global blockdropitemevent1
    global blockredstoneevent1
    global entitydeathevent1
    global entitydropitemevent1
    global entitypickupitemevent1
    global playerdeathevent1
    global projectilehitevent1
    entitydamagebyentityevent1 = entitydamagebyentityevent()
    entitydamageevent1 = entitydamageevent()
    playerjoinevent1 = playerjoinevent()
    playermoveevent1 = playermoveevent()
    blockbreakevent1 = blockbreakevent()
    playerinteractevent1 = playerinteractevent()
    playeritemheldevent1 = playeritemheldevent()
    blockfertilizeevent1 = blockfertilizeevent()
    blockexplodeevent1 = blockexplodeevent()
    blockcookevent1 = blockcookevent()
    blockdropitemevent1 = blockdropitemevent()
    blockredstoneevent1 = blockredstoneevent()
    entitydeathevent1 = entitydeathevent()
    entitydropitemevent1 = entitydropitemevent()
    entitypickupitemevent1 = entitypickupitemevent()
    playerdeathevent1 = playerdeathevent()
    projectilehitevent1 = projectilehitevent()
    global bc1
    bc1 = Block()
    global ac1
    ac1 = Action()
    global material1
    material1 = Material()
    global inven1
    inven1 = Inventory()
    global itemstack1
    itemstack1 = ItemStack()
    global world1
    world1 = World()
    global al_wr_1
    al_wr_1 = ArrayList(world())
    global al_pl_1
    al_pl_1 = ArrayList(player())
    global player1
    player1 = Player()
    global location1
    location1 = Location()
    if os.path.isdir("data/src/main/resources"):
        import shutil
        shutil.rmtree("data/src/main")
    os.makedirs("data/src/main/resources")
    os.makedirs("data/src/main/java/Main")
    file = open("data/src/main/resources/plugin.yml","w")
    file.write("name: minepy\nmain: Main.Main\nversion: 1.0\napi-version: 1.16\n")
    file.close()
    global check_list
    check_list.append('init')
def dojava(code):
    global check_list
    check_list.append('java')
def print(message):
    check_list.append('sys_activity')
class Player:
    def __init__(self):
        global addition_list
        global check_list
        if check_list.__contains__("init"):
            if not addition_list.__contains__('org.bukkit.entity.Player'):
                addition_list.append('org.bukkit.entity.Player')
        self.type = "player"
        check_list.append("define")
    def setHealth(self,value):
        global check_list
        check_list.append("activity")
    def getName(self):
        return "hello"
    def sendMessage(self,*args):
        global check_list
        check_list.append("activity_message")
    def getLocation(self):
        return location1
    def teleport(self,Location):
        global check_list
        check_list.append("activity")
    def sendTitle(self,main_,sub,open_time,status,close):
        global check_list
        check_list.append("activity_message")
    def hasPlayedBefore(self):
        pass
    def removePotionEffect(self,effectype,*detail):
        global check_list
        check_list.append("activity_potion")
    def addPotionEffect(self,effectype,second,hard,*detail):
        global check_list    
        check_list.append("activity_potion")
    def getName(self):
        return ""
    def getItemInHand(self):
        global itemstack1
        return itemstack1
    def getInventory(self):
        global inven1
        return inven1
class ArrayList:
    def __init__(self,typeof):
        global addition_list
        global check_list
        if check_list.__contains__("init"):
            if not addition_list.__contains__('java.util.ArrayList'):
                addition_list.append('java.util.ArrayList')
        global var_dict_type
        check_list.append("define")
        self.type = typeof
    def add(self,something):
        import inspect
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__
        g = str(type(something))
        if g.__contains__("."):
            g = g.split(".")[-1]
            g = g.split("'")[0]
        else:
            g = g.split("'")[1]
            g = g.split("'")[0]
        g = g.lower()
        if g != self.type:
            if not(type(something) == "str" and self.type == "string"):
                if not(type(something) == "int" and self.type == "Integar"):
                    raise Exception("ArrayList type and input value's type isn't same |"+"ArrayList type : "+g+" | input value type : "+str(self.type)+" |")
        global check_list    
        check_list.append("activity")
    def get(self,index):
        g = str(type(index))
        if g.__contains__("."):
            raise Exception("must be int")
        global material1
        global player1
        if self.type == "player":
            return player1
        elif self.type == "material":
            return material1
    def size(self):
        pass
    def __contains__(self,something):
        import inspect
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__
        g = str(type(something))
        if g.__contains__("."):
            g = g.split(".")[-1]
            g = g.split("'")[0]
        else:
            g = g.split("'")[1]
            g = g.split("'")[0]
        g = g.lower()
        if self.type != g:
            if not self.type == "string" and type(something) == "str":
                raise Exception('compare thing type have to be same as type of list '+filename+'", line '+str(whenerror)+',')
class String:
    def __init__(self):
        global check_list
        check_list.append("define")
def Event():
    global check_list_var
    check_list.append("define_python")
    global event_name
    global entitydamageevent
    global entitydamagebyentityevent
    global playermoveevent1
    global blockbreakevent1
    global playerinteractevent1
    global playerjoinevent1
    global playeritemheldevent1
    global blockfertilizeevent1
    global blockexplodeevent1
    global blockcookevent1
    global blockdropitemevent1
    global blockredstoneevent1
    global entitydeathevent1
    global entitydropitemevent1
    global entitypickupitemevent1
    global playerdeathevent1
    global projectilehitevent1
    event_name = event_name.lower()
    if event_name == "playermoveevent":
        return playermoveevent1
    elif event_name == "blockbreakevent":
        return blockbreakevent1
    elif event_name == "playerinteractevent":
        return playerinteractevent1
    elif event_name == "playerjoinevent":
        return playerjoinevent1
    elif event_name == "playeritemheldevent":
        return playeritemheldevent1
    elif event_name == "blockfertilizeevent":
        return blockfertilizeevent1
    elif event_name == "blockexplodeevent":
        return blockexplodeevent1
    elif event_name == "blockcookevent":
        return blockcookevent1
    elif event_name == "blockdropItemevent":
        return blockdropitemevent1
    elif event_name == "blockredstoneevent":
        return blockredstoneevent1
    elif event_name == "entitydeathevent":
        return entitydeathevent1
    elif event_name == "entitydropItemevent":
        return entitydropitemevent1
    elif event_name == "entitypickupitemevent":
        return entitypickupitemevent1
    elif event_name == "playerdeathevent":
        return playerdeathevent1
    elif event_name == "projectilehitevent":
        return projectilehitevent1
    elif event_name == "entitydamageevent":
        return entitydamageevent1
    elif event_name == "entitydamagebyentityevent":
        return entitydamagebyentityevent1
class Location:
    def __init__(self):
        global addition_list
        global check_list
        if check_list.__contains__("init"):
            if not addition_list.__contains__('org.bukkit.Location'):
                addition_list.append('org.bukkit.Location')
        check_list.append("define")
    def getBlock(self):
        global bc1
        return bc1
    def setX(self,set):
        global check_list    
        check_list.append("activity") 
    def setY(self,set):
        global check_list    
        check_list.append("activity") 
    def setZ(self,set):
        global check_list    
        check_list.append("activity") 
    def getX(self):
        global type_list
        type_list.append("int")
        return 1
    def getY(self):
        global type_list
        type_list.append("int")
        return 1
    def getZ(self):
        global type_list
        type_list.append("int")
        return 1
    def getWorld(self):
        global world1
        return world1
class Random:
    def __init__(self):
        global addition_list
        addition_list.append('java.util.Random')
        global check_list
        check_list.append("define")
    def nextInt(self,value):
        return 1
class Minecraft:
    def getPlayers():
        global player1
        global Playerinclude
        Playerinclude = True
        return player1
    def getWorlds():
        global world1
        return world1
    def MaterialList():
        global material1
        return material1
class Inventory:
    def __init__(self):
        global check_list
        check_list.append("define")
        global addition_list
        if check_list.__contains__("init"):
            if not addition_list.__contains__('org.bukkit.inventory.Inventory'):
                addition_list.append('org.bukkit.inventory.Inventory')
    def addItem(self,itemStack):
        global check_list
        check_list.append("activity")
class ItemStack:
    def __init__(self):
        global addition_list
        global check_list
        if check_list.__contains__("init"):
            if not addition_list.__contains__('org.bukkit.inventory.ItemStack'):
                addition_list.append('org.bukkit.inventory.ItemStack')
        check_list.append("define")
    def setMaterial(self,something):
        global check_list
        check_list.append("activity")
    def setAmount(self,amount):
        global check_list
        check_list.append("activity")
    def getMaterial(self):
        global itemstack1
        return itemstack1
class Command:
    def sender():
        global player1
        return player1
    def label():
        return ""
class World:
    def __init__(self):
        self.type = "world"
        global addition_list
        global check_list
        if check_list.__contains__("init"):
            if not addition_list.__contains__('org.bukkit.World'):
                addition_list.append('org.bukkit.World')
        check_list.append("define")
    def setGameRule(self,gamerule,status):
        if not addition_list.__contains__('org.bukkit.GameRule'):
            addition_list.append('org.bukkit.GameRule')
        global check_list    
        check_list.append("activity")
    def dropItem(self,location,itemstack):
        global check_list    
        check_list.append("activity")
class Block:
    def __init__(self):
        self.type = "Block"
        global addition_list
        global check_list
        if check_list.__contains__("init"):
            if not addition_list.__contains__('org.bukkit.block.Block'):
                addition_list.append('org.bukkit.block.Block')    
        check_list.append("define")
    def getMaterial(self):
        global material1    
        return material1
    def getLocation(self):
        global location1
        return location1
    def getWorld(self):
        global world1
        return world1
def time(when):
    global repeat_var
    repeat_var +=1
    if repeat_var ==1:
        global check_list
        check_list.append("while_time")
        return True
    else:
        repeat_var = 0
        return False
def event(when):
    global event_name
    event_name = when
    global repeat_var
    repeat_var +=1
    if repeat_var ==1:
        global check_list
        check_list.append("while_event")
        return True
    else:
        repeat_var = 0
        return False
def when(*test):
    global when_var
    when_var +=1
    if when_var ==1:
        global check_list
        check_list.append("if")
        return True
    else:
        when_var = 0
        return False
def repeat(*var_name):
    if len(var_name) ==1:
        list_name = var_name[0]
        global player1
        global world1
        global material1
        check_list.append("for")
        g = []
        global list_name_list
        list_name_list.append(list_name.type)
        if list_name.type == "player":
            if not addition_list.__contains__("org.bukkit.entity.Player"):
                addition_list.append("org.bukkit.entity.Player")
            g.append(player1)
            return g
        elif list_name.type == "world":
            if not addition_list.__contains__("org.bukkit.World"):
                addition_list.append("org.bukkit.World")
            g.append(world1)
            return g
        elif list_name.type == "material":
            if not addition_list.__contains__("org.bukkit.Material"):
                addition_list.append("org.bukkit.Material")
            g.append(material1)
            return g
        elif list_name == "Minecraft.MaterialList()":
            g.append(material1)
            return g
def command(some):
    global repeat_var
    repeat_var +=1
    if repeat_var ==1:
        global check_list
        check_list.append("command")
        return True
    else:
        repeat_var = 0
        return False       
def tell():
    global check_list
    sys.stdout.write(",".join(check_list))
    sys.stdout.write("\n")
    check_list.append("tell")
def distinguish_execution(code):
    code = str(code)
    global whenerror
    whenerror +=1
    if not code.__contains__("import"):
        no_blank_i = code.replace(" ","")
        if not no_blank_i[0] == "#":
            if not code == "tell()":
                if not code == "Enable":
                    if not code == "Disable":
                        m = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
                        for h in code:
                            if m.__contains__(h):
                                return True
                        
    return False
class Action:
    def __init__(self):
        self.type = "Action"
        global addition_list
        global check_list
        if check_list.__contains__("init"):
            if not addition_list.__contains__('org.bukkit.event.block.Action'):
                addition_list.append('org.bukkit.event.block.Action')
            
        check_list.append("define")
def player():
    return "player"
def world():
    return "world"
def string():
    return "string"
def Enable():
    return "Enable"
def Disable():
    return "Disable"
def material():
    return "material"
class entitydamageevent:
    def getEntity(self):
        global player1
        return player1
    def getDamage(self):
        global type_list
        type_list.append("int")
        return 1
class entitydamagebyentityevent:
    def getEntity(self):
        global player1
        return player1
    def getDamage(self):
        global type_list
        type_list.append("int")
        return 1
    def getDamager(self):
        global player1
        return player1
class playermoveevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
    def getPlayer(self):
        global player1
        return player1
    def getFrom(self):
        global location1
        return location1
    def getTo(self):
        global location1
        return location1
    def setCancelled(self,status):
        global check_list
        check_list.append("activity")
class blockbreakevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
    def getPlayer(self):
        global player1
        return player1
    def setCancelled(self,status):
        global check_list
        check_list.append("activity")
    def getBlock(self):
        global bc1
        return bc1
    def setDropItems(self,bool):
        global check_list
        check_list.append("activity")
class playerinteractevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
    def getAction(self):
        pass
    def getClickedBlock(self):
        global bc1
        return bc1
    def setCancelled(self,status):
        global check_list
        check_list.append("activity")
    def getItem(self):
        global itemstack1
        return itemstack1
    def getMaterial(self):
        global material1
        return material1
class playerjoinevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
    def getPlayer(self):
        global player1
        return player1
    def setJoinMessage(self,message):
        global check_list
        check_list.append("activity")
class playeritemheldevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
class blockfertilizeevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
    def setCancelled(self,status):
        global check_list
        check_list.append("activity")
class blockexplodeevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
class blockcookevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
class blockdropitemevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
class blockredstoneevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
class entitydeathevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
class entitydropitemevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
class entitypickupitemevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
class playerdeathevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
    def getEventName(self):
        return "hello"
    def getEntity(self):
        global player1
        return player1
    def setDeathMessage(self,something):
        global check_list
        check_list.append("activity")
class projectilehitevent:
    def getEventName(self):
        return "hello"
    def __init__(self):
        pass
def PlayerMoveEvent():
    return "PlayerMoveEvent"
def BlockBreakEvent():
    return "BlockBreakEvent"
def PlayerInteractEvent():
    return "PlayerInteractEvent"
def PlayerJoinEvent():
    return "PlayerJoinEvent"
def PlayerItemHeldEvent():
    return "PlayerItemHeldEvent"
def BlockFertilizeEvent():
    return "BlockFertilizeEvent"
def BlockExplodeEvent():
    return "BlockExplodeEvent"
def BlockCookEvent():
    return "PlayerInteractEvent"
def BlockDropItemEvent():
    return "BlockDropItemEvent"
def BlockRedstoneEvent():
    return "BlockRedstoneEvent"
def EntityDeathEvent():
    return "EntityDeathEvent"
def EntityDropItemEvent():
    return "EntityDropItemEvent"
def EntityPickupItemEvent():
    return "EntityPickupItemEvent"
def EntityTeleportEvent():
    return "EntityTeleportEvent"
def PlayerDeathEvent():
    return "PlayerDeathEvent"
def ProjectileHitEvent():
    return "ProjectileHitEvent"
def EntityDamageEvent():
    return "EntityDamageEvent"
def EntityDamageByEntityEvent():
    return "EntityDamageByEntityEvent"
# m = ""
# file = open("hello.txt","r")
# for i in file.readlines():
#     i = i.lower()
#     m += i
# file = open("hello.txt","w")
# file.write(m)
def make(server,**setting):
    online = True
    port = False
    if server == True:
        for h,s in setting.items():
            if h == "port":
                port = s
            elif h == "online":
                online = s 
    global Playerinclude
    global enable_space
    global addition_list
    global python_space
    global java_space
    java_space = 0
    global check_list
    global check_list_var
    global javacode
    global isreturnneed
    check_list.append("make")
    while check_list[0] != 'init':
        del check_list[0]
    sys.stdout.write("['")
    sys.stdout.write("','".join(check_list))
    sys.stdout.write("']")
    sys.stdout.write("\n")
    javacode = ''
    frame = inspect.stack()[1]
    module = inspect.getmodule(frame[0])
    filename = module.__file__
    file = open(filename,"r")
    lines = file.readlines()
    global whenerror
    for code in lines:
        code = str(code)
        code = code.replace("when=", "")
        getvalue = distinguish_execution(code)
        if getvalue == True:
            m = check_list[0]
            code = space.forfinish(code)
            if m != 'make' and isreturnneed ==1:
                isreturnneed = 0
                code = space.forfinish(code)
                isreturnneed =1
            code = code.replace("    ","")
            code = code.replace("\n","")
            if code.__contains__("if"):
                raise Exception("I'm Sorry you can't use 'if' instead you can use 'while when():'"+'"'+filename+'", line '+str(whenerror)+',')
            elif code.__contains__("elif") or code.__contains__("else"):
                raise Exception("I'm Sorry who can't use elif or else"+'"'+filename+'", line '+str(whenerror)+',')
            elif m == 'init':
                del check_list[0] 
                javacode = space.getspace(javacode)
                javacode += 'public class Main extends JavaPlugin implements Listener{\n'
                java_space +=1
                addition_list.append('org.bukkit.plugin.java.JavaPlugin')
                addition_list.append('org.bukkit.event.Listener')
            elif code.__contains__(".")  and code.__contains__("=") and not(code.__contains__("while")) and not(code.__contains__("for")):
                if not (code.__contains__("randint")):
                    if not (code.__contains__("get(")):
                        if not code[len(code)-2:len(code)] == "()":
                            # raise ValueError("you have to set () in '"+code+"'\n")
                            raise Exception('you should put () in "'+filename+'", line '+str(whenerror)+',')
                else:
                    if not var_list.__contains__("random"):
                        m = "public Random random = new Random();\n"
                        javacode = javacode.replace("implements Listener{\n","implements Listener{\n"+'    '+m)
                        var_list.append("random")
                        addition_list.append("java.util.Random")
                    var = code.split("=")[0]
                    code1 = code.split("=")[1]
                    code1 = code1.split("(")[1]
                    code2 = code1.split(",")[0]
                    code3 = code1.split(",")[1]
                    code3 = code3.split(")")[0]
                    code = var+"="+"random.randint("+code3+")"
                code = code.replace("getEntity()","getEntity")
                if code.__contains__("getEntity") and code.__contains__("()"):
                    raise Exception("you only can use getEntity in one line")
                javacode = define_auto(code)
                code = code.replace(" ","")
                code = code.replace("randint","nextInt")
                code = code.replace("="," = ")
                if code.__contains__("getItemInHand"):
                    if not javacode.__contains__('@SuppressWarnings("deprecation")\n'+'    '+'public boolean'):
                        javacode = javacode.replace('public boolean','@SuppressWarnings("deprecation")\n'+'    '+'public boolean')
                code = code.replace("Command.sender()", "(Player) sender")
                code = code.replace("Command.","")
                code = code.replace("()","")
                code = code.replace("getPlayer","getPlayer()")
                code = code.replace("getWorld","getWorld()")
                code = code.replace("getLocation","getLocation()")
                code = code.replace("getInventory","getInventory()")
                code = code.replace("getBlock","getBlock()")
                code = code.replace("getName","getName()")
                code = code.replace("size","size()")
                code = code.replace("Material","Type")
                code = code.replace("getType","getType()")
                code = code.replace("toString","toString()")
                if code.__contains__("getEntity") or code.__contains__("getDamager"):
                    code = code.replace("= ","= (Player) ")
                    code = code.replace("Entity","Entity()")
                    code = code.replace("Damager","Damager()")
                elif (code.__contains__("getX") or code.__contains__("getY") or code.__contains__("getZ") or code.__contains__("getDamage")):
                    code = code.replace("= ","= (int) ")
                    code = code.replace("getX","getX()")
                    code = code.replace("getY","getY()")
                    code = code.replace("getZ","getZ()")
                    code = code.replace("getDamage","getDamage()")
                javacode = space.getspace(javacode)
                javacode += code +';\n'
            elif not code.__contains__("("):
                code = code.replace(" ","")
                var_name = code.split("=")[0]
                if not var_list.__contains__(var_name):
                    data = code.split("=")[1]
                    if data.__contains__('"'):
                        javacode = space.getspace(javacode)
                        javacode += 'String '+var_name+' = "";\n'
                    else:
                        javacode = space.getspace(javacode)
                        javacode += 'Integer '+var_name+";\n"
                    var_list.append(var_name)
                javacode = space.getspace(javacode)
                code = code.replace("="," = ")
                javacode += code+";\n"
            elif m == 'while_time':
                del check_list[0] 
                javacode = space.getspace(javacode)
                javacode += '@Override\n'
                javacode = space.getspace(javacode)
                code = code.replace(" ","")
                code1 = code.replace('whiletime', '')
                code1 = code1.replace('(', '')
                code1 = code1.replace(')','')
                code1 = code1.replace(':','')
                code1 = code1.replace('\n','')
                if code1 == "Enable":
                    javacode += 'public void onEnable(){\n'
                if code1 == "Disable":
                    javacode += 'public void onDisable(){\n'
                python_space =1
                java_space = 2
            elif m == 'while_event':
                java_space =1
                python_space = 0
                global Event_name
                Event_name = ''
                del check_list[0] 
                code = code.replace("    ","")
                if not javacode.__contains__("Bukkit.getPluginManager().registerEvents(this,this)"):
                    addition_list.append("org.bukkit.Bukkit")
                    r = 2*"    "
                    javacode = javacode.replace('public void onEnable(){\n', 'public void onEnable(){\n'+r+'Bukkit.getPluginManager().registerEvents(this,this);\n')
                global event_value
                event_value +=1
                name = 'test'+str(event_value)
                javacode += "    "*(java_space-1)
                javacode += "    "
                javacode += "@EventHandler\n"
                code = code.replace(" ","")
                code1 = code.replace('(', '')
                code1 = code1.replace(')','')
                code1 = code1.replace(':','')
                code1 = code1.replace('\n','')
                code1 = code1.replace('whileevent', '')
                if not addition_list.__contains__('org.bukkit.event.EventHandler'):
                    addition_list.append('org.bukkit.event.EventHandler')
                if code1 == "PlayerDeathEvent" and not addition_list.__contains__('org.bukkit.event.player.'+code1):
                    addition_list.append('org.bukkit.event.entity.'+code1)
                elif code1.__contains__("Player") and not addition_list.__contains__('org.bukkit.event.player.'+code1):
                    addition_list.append('org.bukkit.event.player.'+code1)
                elif code1.__contains__("Block") and not addition_list.__contains__('org.bukkit.event.block.'+code1):
                    addition_list.append('org.bukkit.event.block.'+code1)
                elif code1.__contains__("Entity") and not addition_list.__contains__('org.bukkit.event.entity.'+code1):
                    addition_list.append('org.bukkit.event.entity.'+code1)
                elif code1 == "ProjectileHitEvent":
                    addition_list.append('org.bukkit.event.entity.'+code1)
                javacode = space.getspace(javacode)
                javacode += 'public void '+name+'('+code1+' e'+') {\n'
                python_space +=1
                java_space +=1
                Event_name = code1
            elif m == 'define_python':
                del check_list[0] 
                pass
            elif m == 'define':
                
                del check_list[0] 
                code = code.replace(" ","")
                i_list = code.split("=")
                variable_name = i_list[0]
                middle_part = i_list[1].replace("(","")
                middle_part = middle_part.replace(")","")
                if middle_part.__contains__("ArrayList"):
                    species = middle_part.replace("ArrayList","")
                    k = str(species[0])
                    species = k.upper() + species[1:len(species)]
                    m = 'public ArrayList<'+species+'> '+variable_name+' = new ArrayList<>();\n'
                    var_dict[variable_name] = species
                elif middle_part == "Random":
                    m = 'Random '+variable_name+' = new Random();\n'
                elif middle_part == "ItemStack":
                    m = 'ItemStack '+variable_name+' = new ItemStack(Material.AIR,1);\n'
                else:
                    if middle_part == "Player":
                        Playerinclude = True
                    m = 'public '+middle_part+' '+variable_name+';\n'
                javacode = javacode.replace("public class Main extends JavaPlugin implements Listener{\n",
                "public class Main extends JavaPlugin implements Listener{\n"+'    '+m)
                var_list.append(variable_name)
            elif m == 'activity':
                del check_list[0] 
                code = code.replace(" ","")
                code = code.replace("="," = ")
                javacode = space.getspace(javacode)
                code = code.replace("Material","Type")
                code = code.replace("()","")
                code = code.replace("True","true")
                code = code.replace("False","false")
                if code.__contains__("setCancel") and Event_name == "PlayerJoinEvent":
                    raise Exception('PlayerJoinEvent cannot put setCancel "'+filename+'", line '+str(whenerror)+',')
                javacode += code +';\n'
            elif m == 'activity_message':
                del check_list[0] 
                i1 = code.split(".")[0]
                i2 = i1.replace(" ","")
                javacode = space.getspace(javacode)
                if not code.__contains__('"'):
                    if code.__contains__('()'):
                        raise Exception('you should put only variable in "'+filename+'", line '+str(whenerror)+',')
                    first_part = code.split("(")[1]
                    first_part = first_part.split(")")[0]
                    first_part = first_part.replace('"','')
                    try:
                        g = int(first_part)
                    except Exception:
                        if not (var_dict.get(first_part) == "String") and not(var_dict.get(first_part) == "Integar"):
                            raise Exception('you should put only String or int in "'+filename+'", line '+str(whenerror)+',')
                code = code.replace(i1,i2)
                code = code.replace(")",'+"")')
                javacode += code+';\n'
                
            #potion들 다루어논것
            elif m == 'activity_potion':
                del check_list[0] 
                code = code.replace(" ","")
                code += ';\n'
                code = code.replace(" ","")
                if code.__contains__("add"):
                    code = code.replace(");","));")
                    code = code.replace("(Potion","(new PotionEffect(Potion")
                code = code.replace("()","")
                r = int(code.split(",")[1])
                r = r * 20
                code = code.split(",")[0]+','+str(r)+','+code.split(",")[2]
                javacode = space.getspace(javacode)
                javacode += code
                if not addition_list.__contains__("org.bukkit.potion.PotionEffect"):
                    addition_list.append("org.bukkit.potion.PotionEffect")
                    addition_list.append("org.bukkit.potion.PotionEffectType")
            elif m == 'sys_activity':
                del check_list[0] 
                if code.__contains__("print"):
                    javacode = space.getspace(javacode)
                    code = code.replace("print(","")
                    code = code.replace('")','"+"")')
                    javacode += 'System.out.println('+code+';\n'
            elif m == "java":
                del check_list[0]
                code = code.replace(')',"")
                code = code.replace('dojava(',"")
                code = code.replace('"','')
                code = code.lstrip()
                javacode = space.getspace(javacode)
                javacode += code+';\n'
            elif m == "setnum":
                del check_list[0] 
                javacode = space.getspace(javacode)
                code = code.replace(" ","")
                code = code.replace("="," = ")
                code = code.replace("(","")
                code = code.replace(")","")
                if code.__contains__("add"):
                    code = code.replace("add","")
                    code = code.replace("setvar","")
                    code = code.replace(",","+")
                elif code.__contains__("subtract") or code.__contains__("minus"):
                    code = code.replace("subtract","")
                    code = code.replace("minus","")
                    code = code.replace("setvar","")
                    code = code.replace(",","-")
                elif code.__contains__("multiply"):
                    code = code.replace("multiply","")
                    code = code.replace("setvar","")
                    code = code.replace(",","*")
                elif code.__contains__("divide"):
                    code = code.replace("divide","")
                    code = code.replace("setvar","(int) ")
                    code = code.replace(",","/")
                else:
                    code = code.replace("setvar","")
                javacode += code+';\n'
            elif m == "for":
                del check_list[0] 
                code = code.replace(" ","")
                javacode = space.getspace(javacode)
                code = code.replace("Minecraft.MaterialList()","Material.values()")
                code = code.replace("Minecraft","Bukkit")
                code = code.replace("for","")
                code = code.replace("t(","t")
                code = code.replace("):","")
                code = code.replace("in"," in")
                code = code.replace("repeat","")
                code = code.replace("getPlayers()","getOnlinePlayers()")
                i1 = code.split(" in")[0]
                i2 = code.split(" in")[1]
                i2 = i2.replace("\n","")
                global list_name_list
                type_var = list_name_list[0]
                k = str(type_var[0])
                type_var = k.upper() + type_var[1:len(type_var)]
                javacode += "for ("+type_var+" "+i1+":"+i2+"){\n"
                del list_name_list[0]
                python_space +=1
                java_space +=1
            elif m == 'for_range':
                del check_list[0] 
                code = code.replace(" ","")
                code = code.replace('):','')
                code = code.replace("for","")
                var_name = code.split("inrange(")[0]
                code = code.split("inrange(")[1]
                start_1 = code.split(",")[0]
                end = code.split(",")[1]
                javacode = space.getspace(javacode)
                if not var_list.__contains__(var_name):
                    javacode += 'Integer '+var_name +';\n'
                    javacode = space.getspace(javacode)
                javacode += 'for('+var_name+' = '+str(int(start_1)-1)+'; '+var_name+' < '+end+'; '+ var_name+"++ ) {\n"
                python_space +=1
                java_space +=1
            elif m == 'if':
                del check_list[0] 
                code = code.replace(" ","")
                code = code.replace("when(","(")
                code = code.replace("while","if")
                code = code.replace("__contains__","contains")
                if code.__contains__("=="):
                    code = code.replace("==",".equals(")
                    
                    code = code.replace("):",")):")
                if code.__contains__("not"):
                    code = code.replace("not","!")
                code = code.replace(":"," {")
                code =  code.replace("()","")
                if not code.__contains__("!"):
                    code = code.replace(")))","))")
                code1 = code.split(" ")[0]
                if code.__contains__("and"):
                    code2 = code.split("and")
                    if code2.__contains__("!"):
                        code = code.replace("and","))and")
                    else:
                        code = code.replace("and",")and")
                elif code.__contains__("or"):
                    code2 = code.split("or")
                    if code2.__contains__("!"):
                        code = code.replace("or","))or")
                    else:
                        code = code.replace("or",")or")
                code = code.replace("and"," && ")
                code = code.replace("or"," || ")
                javacode = space.getspace(javacode)
                javacode += code+'\n'
                java_space +=1
                python_space +=1
            elif m == 'command':
                del check_list[0]
                code = space.forfinish(code)
                global command_contain
                code = code.replace(" ","")
                code = code.replace('whilecommand(',"")
                code = code.replace('):',"")
                code = code.replace('"',"")
                code = code.replace("'","")
                name = 'onCommand'
                command_contain +=1
                java_space =1
                python_space = 0
                if not javacode.__contains__('public boolean '+name+'(CommandSender sender, Command cmd, String Label, String[] args) {\n'):
                    javacode += '    '
                    javacode += 'public boolean '+name+'(CommandSender sender, Command cmd, String Label, String[] args) {\n'
                java_space +=1
                python_space +=1
                javacode += '    '*2+'if (Label.equalsIgnoreCase("'+code+'")) {\n'
                java_space +=1
                isreturnneed =1
                if not addition_list.__contains__("org.bukkit.command.Command"): 
                    addition_list.append("org.bukkit.command.Command")
                    addition_list.append("org.bukkit.command.CommandSender")
                r = 2*"    "
                file1 = open("data/src/main/resources/plugin.yml","r")
                filek = open("data/src/main/resources/plugin.yml","a")
                if not file1.readlines().__contains__("commands:\n"):
                    file1.close()
                    filek.write('commands:\n')
                filek.write('  '+code+':\n')
                filek.close()
            elif m == "make":
                del check_list[0]
                if isreturnneed ==1:
                    while java_space > 0:
                        if java_space == 2:
                            javacode = space.getspace(javacode)
                            javacode += "return false;\n"
                        java_space -=1
                        javacode = space.getspace(javacode)
                        javacode += "}\n"
                else:
                    while java_space > 0:
                        java_space -=1
                        javacode = space.getspace(javacode)
                        javacode += "}\n"
    addition = ""
    for code1 in addition_list:
        addition += 'import '+code1 +';\n'
    files = open("data/src/main/java/Main/Main.java","w")
    last_String = 'package Main;\n\n'+addition+javacode
    files.write(last_String)
    files.close()
    minepy = "minepy"
    if server == True:
        minepy += " -s"
    if port == True:
        minepy += " -p"
    if online == False:
        minepy += " -n"
    minepy += " "+filename
    os.system(minepy)
class PotionEffectType:
    def SPEED(): return "effect"
    def SLOW(): return "effect"
    def FAST_DIGGING(): return "effect"
    def SLOW_DIGGING(): return "effect"
    def INCREASE_DAMAGE(): return "effect"
    def HEAL(): return "effect"
    def HARM(): return "effect"
    def JUMP(): return "effect"
    def CONFUSION(): return "effect"
    def REGENERATION(): return "effect"
    def DAMAGE_RESISTANCE(): return "effect"
    def FIRE_RESISTANCE(): return "effect"
    def WATER_BREATHING(): return "effect"
    def INVISIBILITY(): return "effect"
    def BLINDNESS(): return "effect"
    def NIGHT_VISION(): return "effect"
    def HUNGER(): return "effect"
    def WEAKNESS(): return "effect"
    def POISON(): return "effect"
    def WITHER(): return "effect"
    def HEALTH_BOOST(): return "effect"
    def ABSORPTION(): return "effect"
    def SATURATION(): return "effect"
    def GLOWING(): return "effect"
    def LEVITATION(): return "effect"
    def LUCK(): return "effect"
    def UNLUCK(): return "effect"
    def SLOW_FALLING(): return "effect"
    def CONDUIT_POWER(): return "effect"
    def DOLPHINS_GRACE(): return "effect"
    def BAD_OMEN(): return "effect"
    def HERO_OF_THE_VILLAGE(): return "effect"
class GameRule:
    def ANNOUNCE_ADVANCEMENTS(): return "gamerule"
    def COMMAND_BLOCK_OUTPUT(): return "gamerule"
    def DISABLE_ELYTRA_MOVEMENT_CHECK(): return "gamerule"
    def DO_DAYLIGHT_CYCLE(): return "gamerule"
    def DO_ENTITY_DROPS(): return "gamerule"
    def DO_FIRE_TICK(): return "gamerule"
    def DO_LIMITED_CRAFTING(): return "gamerule"
    def DO_MOB_LOOT(): return "gamerule"
    def DO_MOB_SPAWNING(): return "gamerule"
    def DO_TILE_DROPS(): return "gamerule"
    def DO_WEATHER_CYCLE(): return "gamerule"
    def KEEP_INVENTORY(): return "gamerule"
    def LOG_ADMIN_COMMANDS(): return "gamerule"
    def MOB_GRIEFING(): return "gamerule"
    def NATURAL_REGENERATION(): return "gamerule"
    def REDUCED_DEBUG_INFO(): return "gamerule"
    def SEND_COMMAND_FEEDBACK(): return "gamerule"
    def SHOW_DEATH_MESSAGES(): return "gamerule"
    def SPECTATORS_GENERATE_CHUNKS(): return "gamerule"
    def DISABLE_RAIDS(): return "gamerule"
    def DO_INSOMNIA(): return "gamerule"
    def DO_IMMEDIATE_RESPAWN(): return "gamerule"
    def DROWNING_DAMAGE(): return "gamerule"
    def FALL_DAMAGE(): return "gamerule"
    def FIRE_DAMAGE(): return "gamerule"
    def DO_PATROL_SPAWNING(): return "gamerule"
    def DO_TRADER_SPAWNING(): return "gamerule"
    def FORGIVE_DEAD_PLAYERS(): return "gamerule"
    def UNIVERSAL_ANGER(): return "gamerule"
    def RANDOM_TICK_SPEED(): return "gamerule"
    def SPAWN_RADIUS(): return "gamerule"
    def MAX_ENTITY_CRAMMING(): return "gamerule"
    def MAX_COMMAND_CHAIN_LENGTH(): return "gamerule"
class Material:
    def __init__(self):
        self.type = "Material"
        global check_list
        global addition_list
        if check_list.__contains__("init"):
            if not addition_list.__contains__('org.bukkit.Material'):
                addition_list.append('org.bukkit.Material')
        self.type = "material"    
        check_list.append("define")
    def toString(self):
        return "hello"
    def AIR(): return material1
    def STONE(): return material1
    def GRANITE(): return material1
    def POLISHED_GRANITE(): return material1
    def DIORITE(): return material1
    def POLISHED_DIORITE(): return material1
    def ANDESITE(): return material1
    def POLISHED_ANDESITE(): return material1
    def GRASS_BLOCK(): return material1
    def DIRT(): return material1
    def COARSE_DIRT(): return material1
    def PODZOL(): return material1
    def CRIMSON_NYLIUM(): return material1
    def WARPED_NYLIUM(): return material1
    def COBBLESTONE(): return material1
    def OAK_PLANKS(): return material1
    def SPRUCE_PLANKS(): return material1
    def BIRCH_PLANKS(): return material1
    def JUNGLE_PLANKS(): return material1
    def ACACIA_PLANKS(): return material1
    def DARK_OAK_PLANKS(): return material1
    def CRIMSON_PLANKS(): return material1
    def WARPED_PLANKS(): return material1
    def OAK_SAPLING(): return material1
    def SPRUCE_SAPLING(): return material1
    def BIRCH_SAPLING(): return material1
    def JUNGLE_SAPLING(): return material1
    def ACACIA_SAPLING(): return material1
    def DARK_OAK_SAPLING(): return material1
    def BEDROCK(): return material1
    def SAND(): return material1
    def RED_SAND(): return material1
    def GRAVEL(): return material1
    def GOLD_ORE(): return material1
    def IRON_ORE(): return material1
    def COAL_ORE(): return material1
    def NETHER_GOLD_ORE(): return material1
    def OAK_LOG(): return material1
    def SPRUCE_LOG(): return material1
    def BIRCH_LOG(): return material1
    def JUNGLE_LOG(): return material1
    def ACACIA_LOG(): return material1
    def DARK_OAK_LOG(): return material1
    def CRIMSON_STEM(): return material1
    def WARPED_STEM(): return material1
    def STRIPPED_OAK_LOG(): return material1
    def STRIPPED_SPRUCE_LOG(): return material1
    def STRIPPED_BIRCH_LOG(): return material1
    def STRIPPED_JUNGLE_LOG(): return material1
    def STRIPPED_ACACIA_LOG(): return material1
    def STRIPPED_DARK_OAK_LOG(): return material1
    def STRIPPED_CRIMSON_STEM(): return material1
    def STRIPPED_WARPED_STEM(): return material1
    def STRIPPED_OAK_WOOD(): return material1
    def STRIPPED_SPRUCE_WOOD(): return material1
    def STRIPPED_BIRCH_WOOD(): return material1
    def STRIPPED_JUNGLE_WOOD(): return material1
    def STRIPPED_ACACIA_WOOD(): return material1
    def STRIPPED_DARK_OAK_WOOD(): return material1
    def STRIPPED_CRIMSON_HYPHAE(): return material1
    def STRIPPED_WARPED_HYPHAE(): return material1
    def OAK_WOOD(): return material1
    def SPRUCE_WOOD(): return material1
    def BIRCH_WOOD(): return material1
    def JUNGLE_WOOD(): return material1
    def ACACIA_WOOD(): return material1
    def DARK_OAK_WOOD(): return material1
    def CRIMSON_HYPHAE(): return material1
    def WARPED_HYPHAE(): return material1
    def OAK_LEAVES(): return material1
    def SPRUCE_LEAVES(): return material1
    def BIRCH_LEAVES(): return material1
    def JUNGLE_LEAVES(): return material1
    def ACACIA_LEAVES(): return material1
    def DARK_OAK_LEAVES(): return material1
    def SPONGE(): return material1
    def WET_SPONGE(): return material1
    def GLASS(): return material1
    def LAPIS_ORE(): return material1
    def LAPIS_BLOCK(): return material1
    def DISPENSER(): return material1
    def SANDSTONE(): return material1
    def CHISELED_SANDSTONE(): return material1
    def CUT_SANDSTONE(): return material1
    def NOTE_BLOCK(): return material1
    def POWERED_RAIL(): return material1
    def DETECTOR_RAIL(): return material1
    def STICKY_PISTON(): return material1
    def COBWEB(): return material1
    def GRASS(): return material1
    def FERN(): return material1
    def DEAD_BUSH(): return material1
    def SEAGRASS(): return material1
    def SEA_PICKLE(): return material1
    def PISTON(): return material1
    def WHITE_WOOL(): return material1
    def ORANGE_WOOL(): return material1
    def MAGENTA_WOOL(): return material1
    def LIGHT_BLUE_WOOL(): return material1
    def YELLOW_WOOL(): return material1
    def LIME_WOOL(): return material1
    def PINK_WOOL(): return material1
    def GRAY_WOOL(): return material1
    def LIGHT_GRAY_WOOL(): return material1
    def CYAN_WOOL(): return material1
    def PURPLE_WOOL(): return material1
    def BLUE_WOOL(): return material1
    def BROWN_WOOL(): return material1
    def GREEN_WOOL(): return material1
    def RED_WOOL(): return material1
    def BLACK_WOOL(): return material1
    def DANDELION(): return material1
    def POPPY(): return material1
    def BLUE_ORCHID(): return material1
    def ALLIUM(): return material1
    def AZURE_BLUET(): return material1
    def RED_TULIP(): return material1
    def ORANGE_TULIP(): return material1
    def WHITE_TULIP(): return material1
    def PINK_TULIP(): return material1
    def OXEYE_DAISY(): return material1
    def CORNFLOWER(): return material1
    def LILY_OF_THE_VALLEY(): return material1
    def WITHER_ROSE(): return material1
    def BROWN_MUSHROOM(): return material1
    def RED_MUSHROOM(): return material1
    def CRIMSON_FUNGUS(): return material1
    def WARPED_FUNGUS(): return material1
    def CRIMSON_ROOTS(): return material1
    def WARPED_ROOTS(): return material1
    def NETHER_SPROUTS(): return material1
    def WEEPING_VINES(): return material1
    def TWISTING_VINES(): return material1
    def SUGAR_CANE(): return material1
    def KELP(): return material1
    def BAMBOO(): return material1
    def GOLD_BLOCK(): return material1
    def IRON_BLOCK(): return material1
    def OAK_SLAB(): return material1
    def SPRUCE_SLAB(): return material1
    def BIRCH_SLAB(): return material1
    def JUNGLE_SLAB(): return material1
    def ACACIA_SLAB(): return material1
    def DARK_OAK_SLAB(): return material1
    def CRIMSON_SLAB(): return material1
    def WARPED_SLAB(): return material1
    def STONE_SLAB(): return material1
    def SMOOTH_STONE_SLAB(): return material1
    def SANDSTONE_SLAB(): return material1
    def CUT_SANDSTONE_SLAB(): return material1
    def PETRIFIED_OAK_SLAB(): return material1
    def COBBLESTONE_SLAB(): return material1
    def BRICK_SLAB(): return material1
    def STONE_BRICK_SLAB(): return material1
    def NETHER_BRICK_SLAB(): return material1
    def QUARTZ_SLAB(): return material1
    def RED_SANDSTONE_SLAB(): return material1
    def CUT_RED_SANDSTONE_SLAB(): return material1
    def PURPUR_SLAB(): return material1
    def PRISMARINE_SLAB(): return material1
    def PRISMARINE_BRICK_SLAB(): return material1
    def DARK_PRISMARINE_SLAB(): return material1
    def SMOOTH_QUARTZ(): return material1
    def SMOOTH_RED_SANDSTONE(): return material1
    def SMOOTH_SANDSTONE(): return material1
    def SMOOTH_STONE(): return material1
    def BRICKS(): return material1
    def TNT(): return material1
    def BOOKSHELF(): return material1
    def MOSSY_COBBLESTONE(): return material1
    def OBSIDIAN(): return material1
    def TORCH(): return material1
    def END_ROD(): return material1
    def CHORUS_PLANT(): return material1
    def CHORUS_FLOWER(): return material1
    def PURPUR_BLOCK(): return material1
    def PURPUR_PILLAR(): return material1
    def PURPUR_STAIRS(): return material1
    def SPAWNER(): return material1
    def OAK_STAIRS(): return material1
    def CHEST(): return material1
    def DIAMOND_ORE(): return material1
    def DIAMOND_BLOCK(): return material1
    def CRAFTING_TABLE(): return material1
    def FARMLAND(): return material1
    def FURNACE(): return material1
    def LADDER(): return material1
    def RAIL(): return material1
    def COBBLESTONE_STAIRS(): return material1
    def LEVER(): return material1
    def STONE_PRESSURE_PLATE(): return material1
    def OAK_PRESSURE_PLATE(): return material1
    def SPRUCE_PRESSURE_PLATE(): return material1
    def BIRCH_PRESSURE_PLATE(): return material1
    def JUNGLE_PRESSURE_PLATE(): return material1
    def ACACIA_PRESSURE_PLATE(): return material1
    def DARK_OAK_PRESSURE_PLATE(): return material1
    def CRIMSON_PRESSURE_PLATE(): return material1
    def WARPED_PRESSURE_PLATE(): return material1
    def POLISHED_BLACKSTONE_PRESSURE_PLATE(): return material1
    def REDSTONE_ORE(): return material1
    def REDSTONE_TORCH(): return material1
    def SNOW(): return material1
    def ICE(): return material1
    def SNOW_BLOCK(): return material1
    def CACTUS(): return material1
    def CLAY(): return material1
    def JUKEBOX(): return material1
    def OAK_FENCE(): return material1
    def SPRUCE_FENCE(): return material1
    def BIRCH_FENCE(): return material1
    def JUNGLE_FENCE(): return material1
    def ACACIA_FENCE(): return material1
    def DARK_OAK_FENCE(): return material1
    def CRIMSON_FENCE(): return material1
    def WARPED_FENCE(): return material1
    def PUMPKIN(): return material1
    def CARVED_PUMPKIN(): return material1
    def NETHERRACK(): return material1
    def SOUL_SAND(): return material1
    def SOUL_SOIL(): return material1
    def BASALT(): return material1
    def POLISHED_BASALT(): return material1
    def SOUL_TORCH(): return material1
    def GLOWSTONE(): return material1
    def JACK_O_LANTERN(): return material1
    def OAK_TRAPDOOR(): return material1
    def SPRUCE_TRAPDOOR(): return material1
    def BIRCH_TRAPDOOR(): return material1
    def JUNGLE_TRAPDOOR(): return material1
    def ACACIA_TRAPDOOR(): return material1
    def DARK_OAK_TRAPDOOR(): return material1
    def CRIMSON_TRAPDOOR(): return material1
    def WARPED_TRAPDOOR(): return material1
    def INFESTED_STONE(): return material1
    def INFESTED_COBBLESTONE(): return material1
    def INFESTED_STONE_BRICKS(): return material1
    def INFESTED_MOSSY_STONE_BRICKS(): return material1
    def INFESTED_CRACKED_STONE_BRICKS(): return material1
    def INFESTED_CHISELED_STONE_BRICKS(): return material1
    def STONE_BRICKS(): return material1
    def MOSSY_STONE_BRICKS(): return material1
    def CRACKED_STONE_BRICKS(): return material1
    def CHISELED_STONE_BRICKS(): return material1
    def BROWN_MUSHROOM_BLOCK(): return material1
    def RED_MUSHROOM_BLOCK(): return material1
    def MUSHROOM_STEM(): return material1
    def IRON_BARS(): return material1
    def CHAIN(): return material1
    def GLASS_PANE(): return material1
    def MELON(): return material1
    def VINE(): return material1
    def OAK_FENCE_GATE(): return material1
    def SPRUCE_FENCE_GATE(): return material1
    def BIRCH_FENCE_GATE(): return material1
    def JUNGLE_FENCE_GATE(): return material1
    def ACACIA_FENCE_GATE(): return material1
    def DARK_OAK_FENCE_GATE(): return material1
    def CRIMSON_FENCE_GATE(): return material1
    def WARPED_FENCE_GATE(): return material1
    def BRICK_STAIRS(): return material1
    def STONE_BRICK_STAIRS(): return material1
    def MYCELIUM(): return material1
    def LILY_PAD(): return material1
    def NETHER_BRICKS(): return material1
    def CRACKED_NETHER_BRICKS(): return material1
    def CHISELED_NETHER_BRICKS(): return material1
    def NETHER_BRICK_FENCE(): return material1
    def NETHER_BRICK_STAIRS(): return material1
    def ENCHANTING_TABLE(): return material1
    def END_PORTAL_FRAME(): return material1
    def END_STONE(): return material1
    def END_STONE_BRICKS(): return material1
    def DRAGON_EGG(): return material1
    def REDSTONE_LAMP(): return material1
    def SANDSTONE_STAIRS(): return material1
    def EMERALD_ORE(): return material1
    def ENDER_CHEST(): return material1
    def TRIPWIRE_HOOK(): return material1
    def EMERALD_BLOCK(): return material1
    def SPRUCE_STAIRS(): return material1
    def BIRCH_STAIRS(): return material1
    def JUNGLE_STAIRS(): return material1
    def CRIMSON_STAIRS(): return material1
    def WARPED_STAIRS(): return material1
    def COMMAND_BLOCK(): return material1
    def BEACON(): return material1
    def COBBLESTONE_WALL(): return material1
    def MOSSY_COBBLESTONE_WALL(): return material1
    def BRICK_WALL(): return material1
    def PRISMARINE_WALL(): return material1
    def RED_SANDSTONE_WALL(): return material1
    def MOSSY_STONE_BRICK_WALL(): return material1
    def GRANITE_WALL(): return material1
    def STONE_BRICK_WALL(): return material1
    def NETHER_BRICK_WALL(): return material1
    def ANDESITE_WALL(): return material1
    def RED_NETHER_BRICK_WALL(): return material1
    def SANDSTONE_WALL(): return material1
    def END_STONE_BRICK_WALL(): return material1
    def DIORITE_WALL(): return material1
    def BLACKSTONE_WALL(): return material1
    def POLISHED_BLACKSTONE_WALL(): return material1
    def POLISHED_BLACKSTONE_BRICK_WALL(): return material1
    def STONE_BUTTON(): return material1
    def OAK_BUTTON(): return material1
    def SPRUCE_BUTTON(): return material1
    def BIRCH_BUTTON(): return material1
    def JUNGLE_BUTTON(): return material1
    def ACACIA_BUTTON(): return material1
    def DARK_OAK_BUTTON(): return material1
    def CRIMSON_BUTTON(): return material1
    def WARPED_BUTTON(): return material1
    def POLISHED_BLACKSTONE_BUTTON(): return material1
    def ANVIL(): return material1
    def CHIPPED_ANVIL(): return material1
    def DAMAGED_ANVIL(): return material1
    def TRAPPED_CHEST(): return material1
    def LIGHT_WEIGHTED_PRESSURE_PLATE(): return material1
    def HEAVY_WEIGHTED_PRESSURE_PLATE(): return material1
    def DAYLIGHT_DETECTOR(): return material1
    def REDSTONE_BLOCK(): return material1
    def NETHER_QUARTZ_ORE(): return material1
    def HOPPER(): return material1
    def CHISELED_QUARTZ_BLOCK(): return material1
    def QUARTZ_BLOCK(): return material1
    def QUARTZ_BRICKS(): return material1
    def QUARTZ_PILLAR(): return material1
    def QUARTZ_STAIRS(): return material1
    def ACTIVATOR_RAIL(): return material1
    def DROPPER(): return material1
    def WHITE_TERRACOTTA(): return material1
    def ORANGE_TERRACOTTA(): return material1
    def MAGENTA_TERRACOTTA(): return material1
    def LIGHT_BLUE_TERRACOTTA(): return material1
    def YELLOW_TERRACOTTA(): return material1
    def LIME_TERRACOTTA(): return material1
    def PINK_TERRACOTTA(): return material1
    def GRAY_TERRACOTTA(): return material1
    def LIGHT_GRAY_TERRACOTTA(): return material1
    def CYAN_TERRACOTTA(): return material1
    def PURPLE_TERRACOTTA(): return material1
    def BLUE_TERRACOTTA(): return material1
    def BROWN_TERRACOTTA(): return material1
    def GREEN_TERRACOTTA(): return material1
    def RED_TERRACOTTA(): return material1
    def BLACK_TERRACOTTA(): return material1
    def BARRIER(): return material1
    def IRON_TRAPDOOR(): return material1
    def HAY_BLOCK(): return material1
    def WHITE_CARPET(): return material1
    def ORANGE_CARPET(): return material1
    def MAGENTA_CARPET(): return material1
    def LIGHT_BLUE_CARPET(): return material1
    def YELLOW_CARPET(): return material1
    def LIME_CARPET(): return material1
    def PINK_CARPET(): return material1
    def GRAY_CARPET(): return material1
    def LIGHT_GRAY_CARPET(): return material1
    def CYAN_CARPET(): return material1
    def PURPLE_CARPET(): return material1
    def BLUE_CARPET(): return material1
    def BROWN_CARPET(): return material1
    def GREEN_CARPET(): return material1
    def RED_CARPET(): return material1
    def BLACK_CARPET(): return material1
    def TERRACOTTA(): return material1
    def COAL_BLOCK(): return material1
    def PACKED_ICE(): return material1
    def ACACIA_STAIRS(): return material1
    def DARK_OAK_STAIRS(): return material1
    def SLIME_BLOCK(): return material1
    def GRASS_PATH(): return material1
    def SUNFLOWER(): return material1
    def LILAC(): return material1
    def ROSE_BUSH(): return material1
    def PEONY(): return material1
    def TALL_GRASS(): return material1
    def LARGE_FERN(): return material1
    def WHITE_STAINED_GLASS(): return material1
    def ORANGE_STAINED_GLASS(): return material1
    def MAGENTA_STAINED_GLASS(): return material1
    def LIGHT_BLUE_STAINED_GLASS(): return material1
    def YELLOW_STAINED_GLASS(): return material1
    def LIME_STAINED_GLASS(): return material1
    def PINK_STAINED_GLASS(): return material1
    def GRAY_STAINED_GLASS(): return material1
    def LIGHT_GRAY_STAINED_GLASS(): return material1
    def CYAN_STAINED_GLASS(): return material1
    def PURPLE_STAINED_GLASS(): return material1
    def BLUE_STAINED_GLASS(): return material1
    def BROWN_STAINED_GLASS(): return material1
    def GREEN_STAINED_GLASS(): return material1
    def RED_STAINED_GLASS(): return material1
    def BLACK_STAINED_GLASS(): return material1
    def WHITE_STAINED_GLASS_PANE(): return material1
    def ORANGE_STAINED_GLASS_PANE(): return material1
    def MAGENTA_STAINED_GLASS_PANE(): return material1
    def LIGHT_BLUE_STAINED_GLASS_PANE(): return material1
    def YELLOW_STAINED_GLASS_PANE(): return material1
    def LIME_STAINED_GLASS_PANE(): return material1
    def PINK_STAINED_GLASS_PANE(): return material1
    def GRAY_STAINED_GLASS_PANE(): return material1
    def LIGHT_GRAY_STAINED_GLASS_PANE(): return material1
    def CYAN_STAINED_GLASS_PANE(): return material1
    def PURPLE_STAINED_GLASS_PANE(): return material1
    def BLUE_STAINED_GLASS_PANE(): return material1
    def BROWN_STAINED_GLASS_PANE(): return material1
    def GREEN_STAINED_GLASS_PANE(): return material1
    def RED_STAINED_GLASS_PANE(): return material1
    def BLACK_STAINED_GLASS_PANE(): return material1
    def PRISMARINE(): return material1
    def PRISMARINE_BRICKS(): return material1
    def DARK_PRISMARINE(): return material1
    def PRISMARINE_STAIRS(): return material1
    def PRISMARINE_BRICK_STAIRS(): return material1
    def DARK_PRISMARINE_STAIRS(): return material1
    def SEA_LANTERN(): return material1
    def RED_SANDSTONE(): return material1
    def CHISELED_RED_SANDSTONE(): return material1
    def CUT_RED_SANDSTONE(): return material1
    def RED_SANDSTONE_STAIRS(): return material1
    def REPEATING_COMMAND_BLOCK(): return material1
    def CHAIN_COMMAND_BLOCK(): return material1
    def MAGMA_BLOCK(): return material1
    def NETHER_WART_BLOCK(): return material1
    def WARPED_WART_BLOCK(): return material1
    def RED_NETHER_BRICKS(): return material1
    def BONE_BLOCK(): return material1
    def STRUCTURE_VOID(): return material1
    def OBSERVER(): return material1
    def SHULKER_BOX(): return material1
    def WHITE_SHULKER_BOX(): return material1
    def ORANGE_SHULKER_BOX(): return material1
    def MAGENTA_SHULKER_BOX(): return material1
    def LIGHT_BLUE_SHULKER_BOX(): return material1
    def YELLOW_SHULKER_BOX(): return material1
    def LIME_SHULKER_BOX(): return material1
    def PINK_SHULKER_BOX(): return material1
    def GRAY_SHULKER_BOX(): return material1
    def LIGHT_GRAY_SHULKER_BOX(): return material1
    def CYAN_SHULKER_BOX(): return material1
    def PURPLE_SHULKER_BOX(): return material1
    def BLUE_SHULKER_BOX(): return material1
    def BROWN_SHULKER_BOX(): return material1
    def GREEN_SHULKER_BOX(): return material1
    def RED_SHULKER_BOX(): return material1
    def BLACK_SHULKER_BOX(): return material1
    def WHITE_GLAZED_TERRACOTTA(): return material1
    def ORANGE_GLAZED_TERRACOTTA(): return material1
    def MAGENTA_GLAZED_TERRACOTTA(): return material1
    def LIGHT_BLUE_GLAZED_TERRACOTTA(): return material1
    def YELLOW_GLAZED_TERRACOTTA(): return material1
    def LIME_GLAZED_TERRACOTTA(): return material1
    def PINK_GLAZED_TERRACOTTA(): return material1
    def GRAY_GLAZED_TERRACOTTA(): return material1
    def LIGHT_GRAY_GLAZED_TERRACOTTA(): return material1
    def CYAN_GLAZED_TERRACOTTA(): return material1
    def PURPLE_GLAZED_TERRACOTTA(): return material1
    def BLUE_GLAZED_TERRACOTTA(): return material1
    def BROWN_GLAZED_TERRACOTTA(): return material1
    def GREEN_GLAZED_TERRACOTTA(): return material1
    def RED_GLAZED_TERRACOTTA(): return material1
    def BLACK_GLAZED_TERRACOTTA(): return material1
    def WHITE_CONCRETE(): return material1
    def ORANGE_CONCRETE(): return material1
    def MAGENTA_CONCRETE(): return material1
    def LIGHT_BLUE_CONCRETE(): return material1
    def YELLOW_CONCRETE(): return material1
    def LIME_CONCRETE(): return material1
    def PINK_CONCRETE(): return material1
    def GRAY_CONCRETE(): return material1
    def LIGHT_GRAY_CONCRETE(): return material1
    def CYAN_CONCRETE(): return material1
    def PURPLE_CONCRETE(): return material1
    def BLUE_CONCRETE(): return material1
    def BROWN_CONCRETE(): return material1
    def GREEN_CONCRETE(): return material1
    def RED_CONCRETE(): return material1
    def BLACK_CONCRETE(): return material1
    def WHITE_CONCRETE_POWDER(): return material1
    def ORANGE_CONCRETE_POWDER(): return material1
    def MAGENTA_CONCRETE_POWDER(): return material1
    def LIGHT_BLUE_CONCRETE_POWDER(): return material1
    def YELLOW_CONCRETE_POWDER(): return material1
    def LIME_CONCRETE_POWDER(): return material1
    def PINK_CONCRETE_POWDER(): return material1
    def GRAY_CONCRETE_POWDER(): return material1
    def LIGHT_GRAY_CONCRETE_POWDER(): return material1
    def CYAN_CONCRETE_POWDER(): return material1
    def PURPLE_CONCRETE_POWDER(): return material1
    def BLUE_CONCRETE_POWDER(): return material1
    def BROWN_CONCRETE_POWDER(): return material1
    def GREEN_CONCRETE_POWDER(): return material1
    def RED_CONCRETE_POWDER(): return material1
    def BLACK_CONCRETE_POWDER(): return material1
    def TURTLE_EGG(): return material1
    def DEAD_TUBE_CORAL_BLOCK(): return material1
    def DEAD_BRAIN_CORAL_BLOCK(): return material1
    def DEAD_BUBBLE_CORAL_BLOCK(): return material1
    def DEAD_FIRE_CORAL_BLOCK(): return material1
    def DEAD_HORN_CORAL_BLOCK(): return material1
    def TUBE_CORAL_BLOCK(): return material1
    def BRAIN_CORAL_BLOCK(): return material1
    def BUBBLE_CORAL_BLOCK(): return material1
    def FIRE_CORAL_BLOCK(): return material1
    def HORN_CORAL_BLOCK(): return material1
    def TUBE_CORAL(): return material1
    def BRAIN_CORAL(): return material1
    def BUBBLE_CORAL(): return material1
    def FIRE_CORAL(): return material1
    def HORN_CORAL(): return material1
    def DEAD_BRAIN_CORAL(): return material1
    def DEAD_BUBBLE_CORAL(): return material1
    def DEAD_FIRE_CORAL(): return material1
    def DEAD_HORN_CORAL(): return material1
    def DEAD_TUBE_CORAL(): return material1
    def TUBE_CORAL_FAN(): return material1
    def BRAIN_CORAL_FAN(): return material1
    def BUBBLE_CORAL_FAN(): return material1
    def FIRE_CORAL_FAN(): return material1
    def HORN_CORAL_FAN(): return material1
    def DEAD_TUBE_CORAL_FAN(): return material1
    def DEAD_BRAIN_CORAL_FAN(): return material1
    def DEAD_BUBBLE_CORAL_FAN(): return material1
    def DEAD_FIRE_CORAL_FAN(): return material1
    def DEAD_HORN_CORAL_FAN(): return material1
    def BLUE_ICE(): return material1
    def CONDUIT(): return material1
    def POLISHED_GRANITE_STAIRS(): return material1
    def SMOOTH_RED_SANDSTONE_STAIRS(): return material1
    def MOSSY_STONE_BRICK_STAIRS(): return material1
    def POLISHED_DIORITE_STAIRS(): return material1
    def MOSSY_COBBLESTONE_STAIRS(): return material1
    def END_STONE_BRICK_STAIRS(): return material1
    def STONE_STAIRS(): return material1
    def SMOOTH_SANDSTONE_STAIRS(): return material1
    def SMOOTH_QUARTZ_STAIRS(): return material1
    def GRANITE_STAIRS(): return material1
    def ANDESITE_STAIRS(): return material1
    def RED_NETHER_BRICK_STAIRS(): return material1
    def POLISHED_ANDESITE_STAIRS(): return material1
    def DIORITE_STAIRS(): return material1
    def POLISHED_GRANITE_SLAB(): return material1
    def SMOOTH_RED_SANDSTONE_SLAB(): return material1
    def MOSSY_STONE_BRICK_SLAB(): return material1
    def POLISHED_DIORITE_SLAB(): return material1
    def MOSSY_COBBLESTONE_SLAB(): return material1
    def END_STONE_BRICK_SLAB(): return material1
    def SMOOTH_SANDSTONE_SLAB(): return material1
    def SMOOTH_QUARTZ_SLAB(): return material1
    def GRANITE_SLAB(): return material1
    def ANDESITE_SLAB(): return material1
    def RED_NETHER_BRICK_SLAB(): return material1
    def POLISHED_ANDESITE_SLAB(): return material1
    def DIORITE_SLAB(): return material1
    def SCAFFOLDING(): return material1
    def IRON_DOOR(): return material1
    def OAK_DOOR(): return material1
    def SPRUCE_DOOR(): return material1
    def BIRCH_DOOR(): return material1
    def JUNGLE_DOOR(): return material1
    def ACACIA_DOOR(): return material1
    def DARK_OAK_DOOR(): return material1
    def CRIMSON_DOOR(): return material1
    def WARPED_DOOR(): return material1
    def REPEATER(): return material1
    def COMPARATOR(): return material1
    def STRUCTURE_BLOCK(): return material1
    def JIGSAW(): return material1
    def TURTLE_HELMET(): return material1
    def SCUTE(): return material1
    def FLINT_AND_STEEL(): return material1
    def APPLE(): return material1
    def BOW(): return material1
    def ARROW(): return material1
    def COAL(): return material1
    def CHARCOAL(): return material1
    def DIAMOND(): return material1
    def IRON_INGOT(): return material1
    def GOLD_INGOT(): return material1
    def NETHERITE_INGOT(): return material1
    def NETHERITE_SCRAP(): return material1
    def WOODEN_SWORD(): return material1
    def WOODEN_SHOVEL(): return material1
    def WOODEN_PICKAXE(): return material1
    def WOODEN_AXE(): return material1
    def WOODEN_HOE(): return material1
    def STONE_SWORD(): return material1
    def STONE_SHOVEL(): return material1
    def STONE_PICKAXE(): return material1
    def STONE_AXE(): return material1
    def STONE_HOE(): return material1
    def GOLDEN_SWORD(): return material1
    def GOLDEN_SHOVEL(): return material1
    def GOLDEN_PICKAXE(): return material1
    def GOLDEN_AXE(): return material1
    def GOLDEN_HOE(): return material1
    def IRON_SWORD(): return material1
    def IRON_SHOVEL(): return material1
    def IRON_PICKAXE(): return material1
    def IRON_AXE(): return material1
    def IRON_HOE(): return material1
    def DIAMOND_SWORD(): return material1
    def DIAMOND_SHOVEL(): return material1
    def DIAMOND_PICKAXE(): return material1
    def DIAMOND_AXE(): return material1
    def DIAMOND_HOE(): return material1
    def NETHERITE_SWORD(): return material1
    def NETHERITE_SHOVEL(): return material1
    def NETHERITE_PICKAXE(): return material1
    def NETHERITE_AXE(): return material1
    def NETHERITE_HOE(): return material1
    def STICK(): return material1
    def BOWL(): return material1
    def MUSHROOM_STEW(): return material1
    def STRING(): return material1
    def FEATHER(): return material1
    def GUNPOWDER(): return material1
    def WHEAT_SEEDS(): return material1
    def WHEAT(): return material1
    def BREAD(): return material1
    def LEATHER_HELMET(): return material1
    def LEATHER_CHESTPLATE(): return material1
    def LEATHER_LEGGINGS(): return material1
    def LEATHER_BOOTS(): return material1
    def CHAINMAIL_HELMET(): return material1
    def CHAINMAIL_CHESTPLATE(): return material1
    def CHAINMAIL_LEGGINGS(): return material1
    def CHAINMAIL_BOOTS(): return material1
    def IRON_HELMET(): return material1
    def IRON_CHESTPLATE(): return material1
    def IRON_LEGGINGS(): return material1
    def IRON_BOOTS(): return material1
    def DIAMOND_HELMET(): return material1
    def DIAMOND_CHESTPLATE(): return material1
    def DIAMOND_LEGGINGS(): return material1
    def DIAMOND_BOOTS(): return material1
    def GOLDEN_HELMET(): return material1
    def GOLDEN_CHESTPLATE(): return material1
    def GOLDEN_LEGGINGS(): return material1
    def GOLDEN_BOOTS(): return material1
    def NETHERITE_HELMET(): return material1
    def NETHERITE_CHESTPLATE(): return material1
    def NETHERITE_LEGGINGS(): return material1
    def NETHERITE_BOOTS(): return material1
    def FLINT(): return material1
    def PORKCHOP(): return material1
    def COOKED_PORKCHOP(): return material1
    def PAINTING(): return material1
    def GOLDEN_APPLE(): return material1
    def ENCHANTED_GOLDEN_APPLE(): return material1
    def OAK_SIGN(): return material1
    def SPRUCE_SIGN(): return material1
    def BIRCH_SIGN(): return material1
    def JUNGLE_SIGN(): return material1
    def ACACIA_SIGN(): return material1
    def DARK_OAK_SIGN(): return material1
    def CRIMSON_SIGN(): return material1
    def WARPED_SIGN(): return material1
    def BUCKET(): return material1
    def WATER_BUCKET(): return material1
    def LAVA_BUCKET(): return material1
    def MINECART(): return material1
    def SADDLE(): return material1
    def REDSTONE(): return material1
    def SNOWBALL(): return material1
    def OAK_BOAT(): return material1
    def LEATHER(): return material1
    def MILK_BUCKET(): return material1
    def PUFFERFISH_BUCKET(): return material1
    def SALMON_BUCKET(): return material1
    def COD_BUCKET(): return material1
    def TROPICAL_FISH_BUCKET(): return material1
    def BRICK(): return material1
    def CLAY_BALL(): return material1
    def DRIED_KELP_BLOCK(): return material1
    def PAPER(): return material1
    def BOOK(): return material1
    def SLIME_BALL(): return material1
    def CHEST_MINECART(): return material1
    def FURNACE_MINECART(): return material1
    def EGG(): return material1
    def COMPASS(): return material1
    def FISHING_ROD(): return material1
    def CLOCK(): return material1
    def GLOWSTONE_DUST(): return material1
    def COD(): return material1
    def SALMON(): return material1
    def TROPICAL_FISH(): return material1
    def PUFFERFISH(): return material1
    def COOKED_COD(): return material1
    def COOKED_SALMON(): return material1
    def INK_SAC(): return material1
    def COCOA_BEANS(): return material1
    def LAPIS_LAZULI(): return material1
    def WHITE_DYE(): return material1
    def ORANGE_DYE(): return material1
    def MAGENTA_DYE(): return material1
    def LIGHT_BLUE_DYE(): return material1
    def YELLOW_DYE(): return material1
    def LIME_DYE(): return material1
    def PINK_DYE(): return material1
    def GRAY_DYE(): return material1
    def LIGHT_GRAY_DYE(): return material1
    def CYAN_DYE(): return material1
    def PURPLE_DYE(): return material1
    def BLUE_DYE(): return material1
    def BROWN_DYE(): return material1
    def GREEN_DYE(): return material1
    def RED_DYE(): return material1
    def BLACK_DYE(): return material1
    def BONE_MEAL(): return material1
    def BONE(): return material1
    def SUGAR(): return material1
    def CAKE(): return material1
    def WHITE_BED(): return material1
    def ORANGE_BED(): return material1
    def MAGENTA_BED(): return material1
    def LIGHT_BLUE_BED(): return material1
    def YELLOW_BED(): return material1
    def LIME_BED(): return material1
    def PINK_BED(): return material1
    def GRAY_BED(): return material1
    def LIGHT_GRAY_BED(): return material1
    def CYAN_BED(): return material1
    def PURPLE_BED(): return material1
    def BLUE_BED(): return material1
    def BROWN_BED(): return material1
    def GREEN_BED(): return material1
    def RED_BED(): return material1
    def BLACK_BED(): return material1
    def COOKIE(): return material1
    def FILLED_MAP(): return material1
    def SHEARS(): return material1
    def MELON_SLICE(): return material1
    def DRIED_KELP(): return material1
    def PUMPKIN_SEEDS(): return material1
    def MELON_SEEDS(): return material1
    def BEEF(): return material1
    def COOKED_BEEF(): return material1
    def CHICKEN(): return material1
    def COOKED_CHICKEN(): return material1
    def ROTTEN_FLESH(): return material1
    def ENDER_PEARL(): return material1
    def BLAZE_ROD(): return material1
    def GHAST_TEAR(): return material1
    def GOLD_NUGGET(): return material1
    def NETHER_WART(): return material1
    def POTION(): return material1
    def GLASS_BOTTLE(): return material1
    def SPIDER_EYE(): return material1
    def FERMENTED_SPIDER_EYE(): return material1
    def BLAZE_POWDER(): return material1
    def MAGMA_CREAM(): return material1
    def BREWING_STAND(): return material1
    def CAULDRON(): return material1
    def ENDER_EYE(): return material1
    def GLISTERING_MELON_SLICE(): return material1
    def BAT_SPAWN_EGG(): return material1
    def BEE_SPAWN_EGG(): return material1
    def BLAZE_SPAWN_EGG(): return material1
    def CAT_SPAWN_EGG(): return material1
    def CAVE_SPIDER_SPAWN_EGG(): return material1
    def CHICKEN_SPAWN_EGG(): return material1
    def COD_SPAWN_EGG(): return material1
    def COW_SPAWN_EGG(): return material1
    def CREEPER_SPAWN_EGG(): return material1
    def DOLPHIN_SPAWN_EGG(): return material1
    def DONKEY_SPAWN_EGG(): return material1
    def DROWNED_SPAWN_EGG(): return material1
    def ELDER_GUARDIAN_SPAWN_EGG(): return material1
    def ENDERMAN_SPAWN_EGG(): return material1
    def ENDERMITE_SPAWN_EGG(): return material1
    def EVOKER_SPAWN_EGG(): return material1
    def FOX_SPAWN_EGG(): return material1
    def GHAST_SPAWN_EGG(): return material1
    def GUARDIAN_SPAWN_EGG(): return material1
    def HOGLIN_SPAWN_EGG(): return material1
    def HORSE_SPAWN_EGG(): return material1
    def HUSK_SPAWN_EGG(): return material1
    def LLAMA_SPAWN_EGG(): return material1
    def MAGMA_CUBE_SPAWN_EGG(): return material1
    def MOOSHROOM_SPAWN_EGG(): return material1
    def MULE_SPAWN_EGG(): return material1
    def OCELOT_SPAWN_EGG(): return material1
    def PANDA_SPAWN_EGG(): return material1
    def PARROT_SPAWN_EGG(): return material1
    def PHANTOM_SPAWN_EGG(): return material1
    def PIG_SPAWN_EGG(): return material1
    def PIGLIN_SPAWN_EGG(): return material1
    def PIGLIN_BRUTE_SPAWN_EGG(): return material1
    def PILLAGER_SPAWN_EGG(): return material1
    def POLAR_BEAR_SPAWN_EGG(): return material1
    def PUFFERFISH_SPAWN_EGG(): return material1
    def RABBIT_SPAWN_EGG(): return material1
    def RAVAGER_SPAWN_EGG(): return material1
    def SALMON_SPAWN_EGG(): return material1
    def SHEEP_SPAWN_EGG(): return material1
    def SHULKER_SPAWN_EGG(): return material1
    def SILVERFISH_SPAWN_EGG(): return material1
    def SKELETON_SPAWN_EGG(): return material1
    def SKELETON_HORSE_SPAWN_EGG(): return material1
    def SLIME_SPAWN_EGG(): return material1
    def SPIDER_SPAWN_EGG(): return material1
    def SQUID_SPAWN_EGG(): return material1
    def STRAY_SPAWN_EGG(): return material1
    def STRIDER_SPAWN_EGG(): return material1
    def TRADER_LLAMA_SPAWN_EGG(): return material1
    def TROPICAL_FISH_SPAWN_EGG(): return material1
    def TURTLE_SPAWN_EGG(): return material1
    def VEX_SPAWN_EGG(): return material1
    def VILLAGER_SPAWN_EGG(): return material1
    def VINDICATOR_SPAWN_EGG(): return material1
    def WANDERING_TRADER_SPAWN_EGG(): return material1
    def WITCH_SPAWN_EGG(): return material1
    def WITHER_SKELETON_SPAWN_EGG(): return material1
    def WOLF_SPAWN_EGG(): return material1
    def ZOGLIN_SPAWN_EGG(): return material1
    def ZOMBIE_SPAWN_EGG(): return material1
    def ZOMBIE_HORSE_SPAWN_EGG(): return material1
    def ZOMBIE_VILLAGER_SPAWN_EGG(): return material1
    def ZOMBIFIED_PIGLIN_SPAWN_EGG(): return material1
    def EXPERIENCE_BOTTLE(): return material1
    def FIRE_CHARGE(): return material1
    def WRITABLE_BOOK(): return material1
    def WRITTEN_BOOK(): return material1
    def EMERALD(): return material1
    def ITEM_FRAME(): return material1
    def FLOWER_POT(): return material1
    def CARROT(): return material1
    def POTATO(): return material1
    def BAKED_POTATO(): return material1
    def POISONOUS_POTATO(): return material1
    def MAP(): return material1
    def GOLDEN_CARROT(): return material1
    def SKELETON_SKULL(): return material1
    def WITHER_SKELETON_SKULL(): return material1
    def PLAYER_HEAD(): return material1
    def ZOMBIE_HEAD(): return material1
    def CREEPER_HEAD(): return material1
    def DRAGON_HEAD(): return material1
    def CARROT_ON_A_STICK(): return material1
    def WARPED_FUNGUS_ON_A_STICK(): return material1
    def NETHER_STAR(): return material1
    def PUMPKIN_PIE(): return material1
    def FIREWORK_ROCKET(): return material1
    def FIREWORK_STAR(): return material1
    def ENCHANTED_BOOK(): return material1
    def NETHER_BRICK(): return material1
    def QUARTZ(): return material1
    def TNT_MINECART(): return material1
    def HOPPER_MINECART(): return material1
    def PRISMARINE_SHARD(): return material1
    def PRISMARINE_CRYSTALS(): return material1
    def RABBIT(): return material1
    def COOKED_RABBIT(): return material1
    def RABBIT_STEW(): return material1
    def RABBIT_FOOT(): return material1
    def RABBIT_HIDE(): return material1
    def ARMOR_STAND(): return material1
    def IRON_HORSE_ARMOR(): return material1
    def GOLDEN_HORSE_ARMOR(): return material1
    def DIAMOND_HORSE_ARMOR(): return material1
    def LEATHER_HORSE_ARMOR(): return material1
    def LEAD(): return material1
    def NAME_TAG(): return material1
    def COMMAND_BLOCK_MINECART(): return material1
    def MUTTON(): return material1
    def COOKED_MUTTON(): return material1
    def WHITE_BANNER(): return material1
    def ORANGE_BANNER(): return material1
    def MAGENTA_BANNER(): return material1
    def LIGHT_BLUE_BANNER(): return material1
    def YELLOW_BANNER(): return material1
    def LIME_BANNER(): return material1
    def PINK_BANNER(): return material1
    def GRAY_BANNER(): return material1
    def LIGHT_GRAY_BANNER(): return material1
    def CYAN_BANNER(): return material1
    def PURPLE_BANNER(): return material1
    def BLUE_BANNER(): return material1
    def BROWN_BANNER(): return material1
    def GREEN_BANNER(): return material1
    def RED_BANNER(): return material1
    def BLACK_BANNER(): return material1
    def END_CRYSTAL(): return material1
    def CHORUS_FRUIT(): return material1
    def POPPED_CHORUS_FRUIT(): return material1
    def BEETROOT(): return material1
    def BEETROOT_SEEDS(): return material1
    def BEETROOT_SOUP(): return material1
    def DRAGON_BREATH(): return material1
    def SPLASH_POTION(): return material1
    def SPECTRAL_ARROW(): return material1
    def TIPPED_ARROW(): return material1
    def LINGERING_POTION(): return material1
    def SHIELD(): return material1
    def ELYTRA(): return material1
    def SPRUCE_BOAT(): return material1
    def BIRCH_BOAT(): return material1
    def JUNGLE_BOAT(): return material1
    def ACACIA_BOAT(): return material1
    def DARK_OAK_BOAT(): return material1
    def TOTEM_OF_UNDYING(): return material1
    def SHULKER_SHELL(): return material1
    def IRON_NUGGET(): return material1
    def KNOWLEDGE_BOOK(): return material1
    def DEBUG_STICK(): return material1
    def MUSIC_DISC_13(): return material1
    def MUSIC_DISC_CAT(): return material1
    def MUSIC_DISC_BLOCKS(): return material1
    def MUSIC_DISC_CHIRP(): return material1
    def MUSIC_DISC_FAR(): return material1
    def MUSIC_DISC_MALL(): return material1
    def MUSIC_DISC_MELLOHI(): return material1
    def MUSIC_DISC_STAL(): return material1
    def MUSIC_DISC_STRAD(): return material1
    def MUSIC_DISC_WARD(): return material1
    def MUSIC_DISC_11(): return material1
    def MUSIC_DISC_WAIT(): return material1
    def MUSIC_DISC_PIGSTEP(): return material1
    def TRIDENT(): return material1
    def PHANTOM_MEMBRANE(): return material1
    def NAUTILUS_SHELL(): return material1
    def HEART_OF_THE_SEA(): return material1
    def CROSSBOW(): return material1
    def SUSPICIOUS_STEW(): return material1
    def LOOM(): return material1
    def FLOWER_BANNER_PATTERN(): return material1
    def CREEPER_BANNER_PATTERN(): return material1
    def SKULL_BANNER_PATTERN(): return material1
    def MOJANG_BANNER_PATTERN(): return material1
    def GLOBE_BANNER_PATTERN(): return material1
    def PIGLIN_BANNER_PATTERN(): return material1
    def COMPOSTER(): return material1
    def BARREL(): return material1
    def SMOKER(): return material1
    def BLAST_FURNACE(): return material1
    def CARTOGRAPHY_TABLE(): return material1
    def FLETCHING_TABLE(): return material1
    def GRINDSTONE(): return material1
    def LECTERN(): return material1
    def SMITHING_TABLE(): return material1
    def STONECUTTER(): return material1
    def BELL(): return material1
    def LANTERN(): return material1
    def SOUL_LANTERN(): return material1
    def SWEET_BERRIES(): return material1
    def CAMPFIRE(): return material1
    def SOUL_CAMPFIRE(): return material1
    def SHROOMLIGHT(): return material1
    def HONEYCOMB(): return material1
    def BEE_NEST(): return material1
    def BEEHIVE(): return material1
    def HONEY_BOTTLE(): return material1
    def HONEY_BLOCK(): return material1
    def HONEYCOMB_BLOCK(): return material1
    def LODESTONE(): return material1
    def NETHERITE_BLOCK(): return material1
    def ANCIENT_DEBRIS(): return material1
    def TARGET(): return material1
    def CRYING_OBSIDIAN(): return material1
    def BLACKSTONE(): return material1
    def BLACKSTONE_SLAB(): return material1
    def BLACKSTONE_STAIRS(): return material1
    def GILDED_BLACKSTONE(): return material1
    def POLISHED_BLACKSTONE(): return material1
    def POLISHED_BLACKSTONE_SLAB(): return material1
    def POLISHED_BLACKSTONE_STAIRS(): return material1
    def CHISELED_POLISHED_BLACKSTONE(): return material1
    def POLISHED_BLACKSTONE_BRICKS(): return material1
    def POLISHED_BLACKSTONE_BRICK_SLAB(): return material1
    def POLISHED_BLACKSTONE_BRICK_STAIRS(): return material1
    def CRACKED_POLISHED_BLACKSTONE_BRICKS(): return material1
    def RESPAWN_ANCHOR(): return material1
    def WATER(): return material1
    def LAVA(): return material1
    def TALL_SEAGRASS(): return material1
    def PISTON_HEAD(): return material1
    def MOVING_PISTON(): return material1
    def WALL_TORCH(): return material1
    def FIRE(): return material1
    def SOUL_FIRE(): return material1
    def REDSTONE_WIRE(): return material1
    def OAK_WALL_SIGN(): return material1
    def SPRUCE_WALL_SIGN(): return material1
    def BIRCH_WALL_SIGN(): return material1
    def ACACIA_WALL_SIGN(): return material1
    def JUNGLE_WALL_SIGN(): return material1
    def DARK_OAK_WALL_SIGN(): return material1
    def REDSTONE_WALL_TORCH(): return material1
    def SOUL_WALL_TORCH(): return material1
    def NETHER_PORTAL(): return material1
    def ATTACHED_PUMPKIN_STEM(): return material1
    def ATTACHED_MELON_STEM(): return material1
    def PUMPKIN_STEM(): return material1
    def MELON_STEM(): return material1
    def END_PORTAL(): return material1
    def COCOA(): return material1
    def TRIPWIRE(): return material1
    def POTTED_OAK_SAPLING(): return material1
    def POTTED_SPRUCE_SAPLING(): return material1
    def POTTED_BIRCH_SAPLING(): return material1
    def POTTED_JUNGLE_SAPLING(): return material1
    def POTTED_ACACIA_SAPLING(): return material1
    def POTTED_DARK_OAK_SAPLING(): return material1
    def POTTED_FERN(): return material1
    def POTTED_DANDELION(): return material1
    def POTTED_POPPY(): return material1
    def POTTED_BLUE_ORCHID(): return material1
    def POTTED_ALLIUM(): return material1
    def POTTED_AZURE_BLUET(): return material1
    def POTTED_RED_TULIP(): return material1
    def POTTED_ORANGE_TULIP(): return material1
    def POTTED_WHITE_TULIP(): return material1
    def POTTED_PINK_TULIP(): return material1
    def POTTED_OXEYE_DAISY(): return material1
    def POTTED_CORNFLOWER(): return material1
    def POTTED_LILY_OF_THE_VALLEY(): return material1
    def POTTED_WITHER_ROSE(): return material1
    def POTTED_RED_MUSHROOM(): return material1
    def POTTED_BROWN_MUSHROOM(): return material1
    def POTTED_DEAD_BUSH(): return material1
    def POTTED_CACTUS(): return material1
    def CARROTS(): return material1
    def POTATOES(): return material1
    def SKELETON_WALL_SKULL(): return material1
    def WITHER_SKELETON_WALL_SKULL(): return material1
    def ZOMBIE_WALL_HEAD(): return material1
    def PLAYER_WALL_HEAD(): return material1
    def CREEPER_WALL_HEAD(): return material1
    def DRAGON_WALL_HEAD(): return material1
    def WHITE_WALL_BANNER(): return material1
    def ORANGE_WALL_BANNER(): return material1
    def MAGENTA_WALL_BANNER(): return material1
    def LIGHT_BLUE_WALL_BANNER(): return material1
    def YELLOW_WALL_BANNER(): return material1
    def LIME_WALL_BANNER(): return material1
    def PINK_WALL_BANNER(): return material1
    def GRAY_WALL_BANNER(): return material1
    def LIGHT_GRAY_WALL_BANNER(): return material1
    def CYAN_WALL_BANNER(): return material1
    def PURPLE_WALL_BANNER(): return material1
    def BLUE_WALL_BANNER(): return material1
    def BROWN_WALL_BANNER(): return material1
    def GREEN_WALL_BANNER(): return material1
    def RED_WALL_BANNER(): return material1
    def BLACK_WALL_BANNER(): return material1
    def BEETROOTS(): return material1
    def END_GATEWAY(): return material1
    def FROSTED_ICE(): return material1
    def KELP_PLANT(): return material1
    def DEAD_TUBE_CORAL_WALL_FAN(): return material1
    def DEAD_BRAIN_CORAL_WALL_FAN(): return material1
    def DEAD_BUBBLE_CORAL_WALL_FAN(): return material1
    def DEAD_FIRE_CORAL_WALL_FAN(): return material1
    def DEAD_HORN_CORAL_WALL_FAN(): return material1
    def TUBE_CORAL_WALL_FAN(): return material1
    def BRAIN_CORAL_WALL_FAN(): return material1
    def BUBBLE_CORAL_WALL_FAN(): return material1
    def FIRE_CORAL_WALL_FAN(): return material1
    def HORN_CORAL_WALL_FAN(): return material1
    def BAMBOO_SAPLING(): return material1
    def POTTED_BAMBOO(): return material1
    def VOID_AIR(): return material1
    def CAVE_AIR(): return material1
    def BUBBLE_COLUMN(): return material1
    def SWEET_BERRY_BUSH(): return material1
    def WEEPING_VINES_PLANT(): return material1
    def TWISTING_VINES_PLANT(): return material1
    def CRIMSON_WALL_SIGN(): return material1
    def WARPED_WALL_SIGN(): return material1
    def POTTED_CRIMSON_FUNGUS(): return material1
    def POTTED_WARPED_FUNGUS(): return material1
    def POTTED_CRIMSON_ROOTS(): return material1
    def POTTED_WARPED_ROOTS(): return material1