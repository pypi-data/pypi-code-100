import os
from threading import Thread
try: 
  import chess
except ModuleNotFoundError: 
  os.system("pip install chess")
  import chess
import chess.svg

def thrSet(number_of_threads,func_list,arguments=None,daemon=False):
  newThreads=[]
  results=[None]*number_of_threads
  if len(func_list)==1:
    func_list*=number_of_threads
  if arguments==None:
    for i in range(number_of_threads-1):
      newThreads.append(Thread(target = func_list[i],args=(results,i)))
      if daemon:
        newThreads[i].setDaemon(True)
  else:
    for i in range(number_of_threads-1):
      newThreads.append(Thread(target = func_list[i], args=(results,i)+arguments[i]))
      if daemon:
        newThreads[i].setDaemon(True)
  return (newThreads, results)
def thrStart(newThreads):
  for i in newThreads:
    i.start()
def thrJoin(newThreads,results):
  for i in newThreads:
    i.join()
  print(results)
  return results
def Chess():# returns class Game()
  class Game():
    Board,turn,kingsmoved,rooksmoved,enpassant,push_or_take,movecount,fenregister=[[-49,-29,-32,0,-2000,-32,-29,-50],[-10,10,-10,0,-10,-10,-10,0],[0,0,0,0,0,-90,0,0],[0,0,0,-10,0,0,0,-10],[0,0,0,0,0,0,10,0],[0,0,0,0,0,0,0,0],[10,10,0,10,10,10,0,10],[49,29,32,90,2000,32,29,50]],True,[False,False],[False,False,False,False],"",0,6,[]
    piece={
      "0":"□",
      "-2000":"k", #black king
      "-90":"q", #black queen
      "-50":"r", #black king rook
      "-49":"r", #black queen rook
      "-32":"b", #black bishop
      "-29":"n", #black knight
      "-10":"p", #black 
      "10":"P", #white 
      "29":"N", #white knight
      "32":"B", #white bishop
      "49":"R", #white rook
      "50":"R", #white rook
      "90":"Q", #white queen
      "2000":"K", #white king
      "k":-2000, #black king
      "q":-90, #black queen
      "r":-49, #black queen's rook
      "b":-32, #black bishop
      "n":-29, #black knight
      "p":-10, #black 
      "P":10, #white 
      "N":29, #white knight
      "B":32, #white bishop
      "R":49, #white queen's rook
      "Q":90, #white queen
      "K":2000, #white king
    }
    def things(self):
      print(self.Board, self.turn, self.kingsmoved, self.rooksmoved, self.enpassant, self.push_or_take, self.movecount, self.fenregister)
    def set_constants(self,constants):
      (self.Board, self.turn, self.kingsmoved, self.rooksmoved, self.enpassant, self.push_or_take, self.movecount, self.fenregister)=constants
    def UCI_to_NCN(self,uci,a={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}): 
      if len(uci)==4:
        return ((8-int(uci[1]),a[uci[0]]),(8-int(uci[3]),a[uci[2]]),"")
      else:
        return ((8-int(uci[1]),a[uci[0]]),(8-int(uci[3]),a[uci[2]]), (self.piece[uci[4].upper()] if self.turn else self.piece[uci[4]]))
    def NCN_to_UCI(self,ncn,promotion="",a={0:"a", 1:"b", 2:"c", 3:"d", 4:"e", 5:"f", 6:"g", 7:"h"}):
      uci=str(f"{a[8-ncn[0][1]]}{8-ncn[0][0]}{a[8-ncn[1][1]]}{8-ncn[1][0]}{promotion.lower()}")
      return uci
    def push(self,uci=None):
      self.fenregister.append(self.get_fen())
      if uci==None:
        c=self.legalMoves()
        uci=str(input("Enter UCI move: "))
        while not uci in c:
          uci=str(input("Enter UCI move: "))
      move=self.UCI_to_NCN(uci)
      piece=self.Board[move[0][0]][move[0][1]]
      b=self.Board[move[1][0]][move[1][1]]
      if piece==10 and move[0][0]==6 and move[1][0]==4:
        self.enpassant=uci[0]+"3"
      elif piece==-10 and move[0][0]==1 and move[1][0]==3:
        self.enpassant=uci[0]+"6"
      else:
        self.enpassant=""
      if piece in (10,-10) or  b!=0:
        self.push_or_take=0
      else:
        self.push_or_take+=1
      if piece==2000:
        self.kingsmoved[0]=True
      elif piece==-2000:
        self.kingsmoved[1]=True
      elif move[0]==[7,7]:
        self.rooksmoved[0]=True
      elif move[0]==[7,0]:
        self.rooksmoved[1]=True
      elif move[0]==[0,7]:
        self.rooksmoved[0]=True
      elif move[0]==[0,0]:
        self.rooksmoved[0]=True
      if move[2]!="":
        piece=move[2]
      self.Board[move[0][0]][move[0][1]]=0
      self.Board[move[1][0]][move[1][1]]=piece
      if self.turn:
        self.turn=False
      else:
        self.turn=True
        self.movecount+=1

    def show(self,mode=None):
      if mode==None:
        os.system("clear" if os.name=="posix" else "cls")
        print(f"\n{self.piece[str(self.Board[0][0])]} {self.piece[str(self.Board[0][1])]} {self.piece[str(self.Board[0][2])]} {self.piece[str(self.Board[0][3])]} {self.piece[str(self.Board[0][4])]} {self.piece[str(self.Board[0][5])]} {self.piece[str(self.Board[0][6])]} {self.piece[str(self.Board[0][7])]}\n{self.piece[str(self.Board[1][0])]} {self.piece[str(self.Board[1][1])]} {self.piece[str(self.Board[1][2])]} {self.piece[str(self.Board[1][3])]} {self.piece[str(self.Board[1][4])]} {self.piece[str(self.Board[1][5])]} {self.piece[str(self.Board[1][6])]} {self.piece[str(self.Board[1][7])]}\n{self.piece[str(self.Board[2][0])]} {self.piece[str(self.Board[2][1])]} {self.piece[str(self.Board[2][2])]} {self.piece[str(self.Board[2][3])]} {self.piece[str(self.Board[2][4])]} {self.piece[str(self.Board[2][5])]} {self.piece[str(self.Board[2][6])]} {self.piece[str(self.Board[2][7])]}\n{self.piece[str(self.Board[3][0])]} {self.piece[str(self.Board[3][1])]} {self.piece[str(self.Board[3][2])]} {self.piece[str(self.Board[3][3])]} {self.piece[str(self.Board[3][4])]} {self.piece[str(self.Board[3][5])]} {self.piece[str(self.Board[3][6])]} {self.piece[str(self.Board[3][7])]}\n{self.piece[str(self.Board[4][0])]} {self.piece[str(self.Board[4][1])]} {self.piece[str(self.Board[4][2])]} {self.piece[str(self.Board[4][3])]} {self.piece[str(self.Board[4][4])]} {self.piece[str(self.Board[4][5])]} {self.piece[str(self.Board[4][6])]} {self.piece[str(self.Board[4][7])]}\n{self.piece[str(self.Board[5][0])]} {self.piece[str(self.Board[5][1])]} {self.piece[str(self.Board[5][2])]} {self.piece[str(self.Board[5][3])]} {self.piece[str(self.Board[5][4])]} {self.piece[str(self.Board[5][5])]} {self.piece[str(self.Board[5][6])]} {self.piece[str(self.Board[5][7])]}\n{self.piece[str(self.Board[6][0])]} {self.piece[str(self.Board[6][1])]} {self.piece[str(self.Board[6][2])]} {self.piece[str(self.Board[6][3])]} {self.piece[str(self.Board[6][4])]} {self.piece[str(self.Board[6][5])]} {self.piece[str(self.Board[6][6])]} {self.piece[str(self.Board[6][7])]}\n{self.piece[str(self.Board[7][0])]} {self.piece[str(self.Board[7][1])]} {self.piece[str(self.Board[7][2])]} {self.piece[str(self.Board[7][3])]} {self.piece[str(self.Board[7][4])]} {self.piece[str(self.Board[7][5])]} {self.piece[str(self.Board[7][6])]} {self.piece[str(self.Board[7][7])]}\n")
      if mode==0:
        print(str(chess.svg.board(chess.Board(self.get_fen()), size=350)),file=open("board.svg", "w"))
    def get_fen(self):
      fen=""
      n=8
      for i in self.Board:
        k=0
        b=False
        for j in i:
          if b and j==0:
            k+=1
          elif b:
            fen+=str(k)+self.piece[str(j)] 
            k=0
            b=False
          elif j==0:
            k=1
            b=True
          else:
            fen+=self.piece[str(j)] 
        if b:
          fen+=str(k)
        n-=1
        if n>0:
          fen+="/"
      if self.turn:
        fen+=" w "
      else:
        fen+=" b "
      if self.kingsmoved[0] or (self.rooksmoved[0] and self.rooksmoved[1]):
        wk=""
      elif self.rooksmoved[0]:
        wk="K"
      elif self.rooksmoved[1]:
        wk="Q"
      else:
        wk="KQ"
      if self.kingsmoved[1] or (self.rooksmoved[2] and self.rooksmoved[3]):
        bk=""
      elif self.rooksmoved[2]:
        bk="k"
      elif self.rooksmoved[3]:
        bk="q"
      else:
        bk="kq"
      kk=wk+bk+" "
      if kk==" ":
        if self.enpassant=="":
          fen+=f"- - {self.push_or_take} {self.movecount}"
        else:
          fen+=f"- {self.enpassant} {self.push_or_take}   {self.movecount}"
      else:
        if self.enpassant=="":
          fen+=f"{kk}- {self.push_or_take} {self.movecount}"
        else:
          fen+=f"{kk}{self.enpassant} {self.push_or_take}   {self.movecount}"
      return str(fen)
    def legalMoves(self):
      return [str(i) for i in chess.Board(self.get_fen()).generate_legal_moves()]
    def gamestatus(self):
      fen=self.get_fen()
      a=chess.Board(fen)
      if a.is_checkmate():
        return (True,not self.turn)
      elif self.push_or_take>=50 or a.is_stalemate() or a.is_insufficient_material():
        return (True,None)
      else:
        del a
        b=self.halfen(fen)
        n=0
        for i in self.fenregister:
          if b == self.halfen(i):
            n+=1
          if n>=2:
            return (True,None)
        return (False,None)
    def halfen(self, fen):
      half=""
      for i in fen:
        if i==" ":
          return half
        else:
          half+=i
    def after_move_score(self):
      a=self.gamestatus()
      if a[0]:
        if a[1]==None:
          if self.turn:
            return 20
          else:
            return -20
        elif a[1]:
          return 4000
        else:
          return -4000
      else:
        return sum([sum(i) for i in self.Board])
    def before_move_score(self):
      a=self.gamestatus()
      if a[0]:
        if a[1]==None:
          if self.turn:
            return -20
          else:
            return 20
        elif a[1]:
          return -4000
        else:
          return 4000
      else:
        return sum([sum(i) for i in self.Board])
    def undo(self):
      a=self.fenregister
      del self
      b=a[len(a)-1]
      a.pop()
      constants=fromfen(b,a)
      new_Board=Chess()
      new_Board.set_constants(constants)
      return new_Board
  return Game()
def fromfen(fe,fenreg=None):
  d={"k":-2000,"q":-90,"r":-49,"b":-32,"n":-29,"p":-10,"P":10,"N":29,"B":32,"R":49,"Q":90,"K":2000}
  fenregister=[]
  if fenreg!=None:
    for i in fenreg:
      fenregister.append(str(i))
  a=True
  b=0
  Board=[]
  kingsmoved=[True,True]
  rooksmoved=[True,True,True,True]
  c=[]
  for i in fe:
    if b==0:
      if a:
        if i=="/":
          Board.append(c)
          c=[]
        elif i in ("1","2","3","4","5","6","7","8"):
          c+=[0,]*int(i)
        elif i==" ":
          Board.append(c)
          a=False
        else:
          c.append(d[i])
      else:
        if i=="w":
          turn=True
        elif i=="b":
          turn=False
        elif i==" ":
          b=1
    elif b==1:
      if i=="K":
        kingsmoved[0]=False
        rooksmoved[0]=False
      elif i=="Q":
        kingsmoved[0]=False
        rooksmoved[1]=False
      elif i=="k":
        kingsmoved[1]=False
        rooksmoved[2]=False
      elif i=="k":
        kingsmoved[1]=False
        rooksmoved[3]=False
      elif i==" ":
        b=2
    elif b==2:
      if i=="-":
        enpassant=""
      elif i==" ":
        b=3
      elif a:
        enpassant+=i
      elif not a:
        enpassant=i
        a=True
    elif b==3:
      if i!=" ":
        push_or_take=int(i)
      else:
        b=4
    else:
      if i!=" ":
        movecount=int(i)
  return (Board,turn,kingsmoved,rooksmoved,enpassant,push_or_take,movecount,fenregister)
