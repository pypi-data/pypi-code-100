class EquisCero:

    def __init__(self,CharPlayer1,CharPlayer2):
            
        """ TicTakToe game to have fun with a friend.
    
        Attributes:
            CharPlayer1 (char) representing the char that player 1 choose for playing
            CharPlayer2 (char) rrepresenting the char that player 2 choose for playing
            Matriz (list chars) a list that makes visual a matrix for the users
        """   
        
        self.Equis = CharPlayer1
        self.Cero = CharPlayer2
        self.Matriz = [[' ','1','2','3'],['A',' ',' ',' '],['B',' ',' ',' '],['C',' ',' ',' ']]

        
    def display(self):
        
        """Function to display the actual status of the matrix
        Args:
            None
        
        Returns:
            print the matrix in a visual way with the current status of the game      
        """
        for y in range(len(self.Matriz)):
            a=''
            for z in range(len(self.Matriz[y])):
                a += str(self.Matriz[y][z]) + ' | '
            print(a)
            print('-'*15) 
 

    def player1(self,ubicacion):
        
        """Function to ask the location of the char that was chosen by player 1.
        Also validate that the location is available, that the game isn't finish yet or return the result if a player wins.
        
        Args:
            location chosen by player1
        
        Returns:
            print the matrix in a visual way with the current status of the game or display a message if the 
            location isn't available or the result if a player won.
            and 
        """
        fila=0
        col=0
        for i in range(len(self.Matriz)):
            for j in range(len(self.Matriz[i])):
                if self.Matriz[i][j] == ubicacion[0].upper():
                    fila = i
                if self.Matriz[i][j] == ubicacion[1]:
                    col=j
        if self.Matriz[fila][col] ==' ':
            self.Matriz[fila][col] = self.Equis
        else:
            print("Location not available")
        self.display()
        if self.ganador():
            return
        if self.fin():
            return

        
    def player2(self,ubicacion2):
        """Function to input the location of the char that was chosen by player 2.
        Also validate that the location is available, that the game isn't finish yet or return the result if a player wins.
        
        Args:
            location chosen by player2
        
        Returns:
            print the matrix in a visual way with the current status of the game or display a message if the 
            location isn't available or the result if a player won.
            and 
        """      
        fila=0
        col=0
        for i in range(len(self.Matriz)):
            for j in range(len(self.Matriz[i])):
                if self.Matriz[i][j] == ubicacion2[0].upper():
                    fila = i
                if self.Matriz[i][j] == ubicacion2[1]:
                    col=j
        if self.Matriz[fila][col] ==' ':
            self.Matriz[fila][col] = self.Cero
        else:
            print("Location not available")
        self.display()
        if self.ganador():
            return
        if self.fin():
            return
        
        
    def fin(self):
        """Function to validate that the game wasn't a draw
        
        Args:
            None
        
        Returns:
            True to finish the main function and the message "DRAW". If the game is not finish, it just return False 
        """
        terminar= False
        if (self.Matriz[1].count(' ') + self.Matriz[2].count(' ') + self.Matriz[3].count(' '))== 0:
            print("Draw")
            terminar=True
        return terminar
    
    def ganador(self):
        """Function to validate if a player wins
        
        Args:
            None
        
        Returns:
            Returns the player that wins and True to end the game. If the game it's not over yer, return False.  
        """
        terminar= False
        
        #GANAR HORIZONTAL
        if self.Matriz[1][1:4].count(self.Cero)==3 or self.Matriz[2][1:4].count(self.Cero)==3 or self.Matriz[3][1:4].count(self.Cero)==3:
            terminar=True
            print(f"{self.Cero} Wins!!")
        elif self.Matriz[1][1:4].count(self.Equis)==3 or self.Matriz[2][1:4].count(self.Equis)==3 or self.Matriz[3][1:4].count(self.Equis)==3:
            print(f"{self.Equis} Wins!!")
            terminar=True
            
        #GANAR VERTICAL
        elif self.Matriz[1][1]+self.Matriz[2][1]+self.Matriz[3][1] == self.Equis*3:
            print(f"{self.Equis} Wins!!")
            terminar=True
        elif self.Matriz[1][1]+self.Matriz[2][1]+self.Matriz[3][1] == self.Cero*3:
            print(f"{self.Cero} Wins!!")
            terminar=True
        elif self.Matriz[1][2]+self.Matriz[2][2]+self.Matriz[3][2] == self.Equis*3:
            print(f"{self.Equis} Wins!!")
            terminar=True
        elif self.Matriz[1][2]+self.Matriz[2][2]+self.Matriz[3][2] == self.Cero*3:
            print(f"{self.Cero} Wins!!")
            terminar=True            
        elif self.Matriz[1][3]+self.Matriz[2][3]+self.Matriz[3][3] == self.Equis*3:
            print(f"{self.Equis} Wins!!")
            terminar=True
        elif self.Matriz[1][3]+self.Matriz[2][3]+self.Matriz[3][3] == self.Cero*3:
            print(f"{self.Cero} Wins!!")
            terminar=True                
            
            
           #GANAR DIAGONAL  
        elif self.Matriz[1][1]+self.Matriz[2][2]+self.Matriz[3][3] == self.Equis*3:
            print(f"{self.Equis} Wins!!")
            terminar=True
        elif self.Matriz[1][1]+self.Matriz[2][2]+self.Matriz[3][3] == self.Cero*3:
            print(f"{self.Cero} Wins!!")
            terminar=True
        elif self.Matriz[1][3]+self.Matriz[2][2]+self.Matriz[3][1] == self.Equis*3:
            print(f"{self.Equis} Wins!!")
            terminar=True
        elif self.Matriz[1][3]+self.Matriz[2][2]+self.Matriz[3][1] == self.Cero*3:
            print(f"{self.Cero} Wins!!")
            terminar=True
        return terminar