class sudoko:
    """
      
    """
    def __init__(self,puzzle):
        self.puzzle = puzzle
    
	def find_next_empty(self,puzzle):
         """
         Find the empty location in puzzle. As 1 represents a an empty space  so find next space with -1.
        
        Args:
            puzzle : array of sudoko grid       
        
        Returns:
            row, col tuple(or (None,none) if there is none)
        """
       
        for  r in range(9):
            for c in range(9):
                if puzzle[r][c] == -1:
                    return r,c
        return None,None # if already filled
    
    
    def is_valid(self,puzzle,guess,row,col):
         """
         Figure out whether to put the guess at row, col in the puzzle is valid or not.
        
        Args:
            puzzle : array of sudoko grid
            guess : the value input given by the user
            row : traced row for the location of input
            col : traced column for the location of input            
        
        Returns:
            boolean: return True if valid, else False
        """
        
        #row
        row_vals = puzzle[row]
        if guess in row_vals:
            return False

        #column
        col_vals =[]
        col_vals = [puzzle[i][col] for i in range(9)]
        if guess in col_vals:
            return False

        # 3x3 matrix square search
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3

        for r in range(row_start,row_start + 3):
            for c in range(col_start,col_start + 3):
                if puzzle[r][c] == guess:
                    return False


        return True

	def solve_sudoku(self,puzzle):
        """
        Solve sudoku using backtracking
        
        Args:
            puzzle: array of 3x3 matrix sudoko
            
         Returns:
            boolean : True if solved successfully else False
        """
        row,col = find_next_empty(puzzle)

        # if all spaces filled
        if row is None:
            return True

        #if the space is empty make a guess number 1-9
        for guess in range(1,10):
            # check validity of guess
            if is_valid(puzzle,guess,row,col):
                puzzle[row][col] = guess
                # recurse using the puzzle
                if solve_sudoku(puzzle):
                    return True
            # not valid or guess doesnt solve the puzzle, backtrack and try new number
            puzzle[row][col] = -1 # reset the space to -1 as empty

        #if none of the number fits to sovle the puzzle, puzzle is unsolvable
        return False
