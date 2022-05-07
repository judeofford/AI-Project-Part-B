from audioop import minmax
from random import randrange

class Player:
    def __init__(self, player, n):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "red" if your player will
        play as Red, or the string "blue" if your player will play
        as Blue.
        """
        self.colour = player
        self.size = n
        self.board = [[None for i in range(n)] for m in range(n)]
        
      

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
       
        # if self.colour == "red": 
        #     return ("PLACE",2,1)
        # else:
        #     return ("PLACE",3,2)

       
            

        
        
        print("this board is ", type(self.board[2][1]))
        def minimax(board, depth, isMax,self):
            #if this is the maximizer turn
            #need something to detect win here
            #need an evaluation function
          
            if (isMax):
                best = -1000

                for i in range(self.size):
                    for j in range(self.size):
                        if board[i][j] == None:
                            board[i][j] = "r"

                            best = max(best, minimax(board,depth+1,not isMax,self))

                            board[i][j] = None
                return best
            else:
                best = 1000
                for i in range(self.size):
                    for j in range(self.size):
                        if board[i][j] == None:
                            board[i][j] = "b"
                            best = min(best, minimax(board, depth + 1, not isMax, self))
                            board[i][j] = None
                return best
                        
        def findBestMove(board,self):
            bestVal = -1000
            bestMove = (-1,-1)
            
            print(self.size)
            for i in range(self.size):
                
                for j in range(self.size):
                   
                    if (board[i][j] == None):
                      
                        board[i][j] = "red"
                        
                        moveVal = minimax(board, 0 ,False,self)
                        
                        board[i][j] = None
                        if (moveVal > bestVal):
                            bestMove = (i,j)
                            bestVal = moveVal

            return bestMove


        # bestMove = findBestMove(self.board,self)
        # print("best move is",bestMove)

        return ("PLACE",2,1)    
                    
    def turn(self, player, action):
        """
        Called at the end of each player's turn to inform this player of 
        their chosen action. Update your internal representation of the 
        game state based on this. The parameter action is the chosen 
        action itself. 
        
        Note: At the end of your player's turn, the action parameter is
        the same as what your player returned from the action method
        above. However, the referee has validated it at this point.
        """
        # put your code here
        
        def diamondCheck(dneighbours, board, row, column, capturearray):
            playercount = 0
            oppcount = 0
            if board[dneighbours[0][0]][dneighbours[0][1]] != None and board[dneighbours[1][0]][dneighbours[1][1]] != None:
                if (board[dneighbours[0][0]][dneighbours[0][1]] != board[row][column] and
                board[dneighbours[1][0]][dneighbours[1][1]] != board[row][column] and
                board[dneighbours[2][0]][dneighbours[2][1]] == board[row][column]):
                    print("DIAMOND FOUND\n")
                    for i in range(3):
                        if board[dneighbours[i][0]][dneighbours[i][1]] != board[row][column]:
                            capturearray.append([dneighbours[i][0], dneighbours[i][1]])
        
        r = action[1]
        q = action[2]

        self.board[r][q] = player

        #check for diamonds, most nodes have 12 possible diamonds
        captured = []

        #---vertice diamonds---
        if r+2 < self.size and q-1 > -1:
            #top vertice
            neighbours = [[r+1, q-1], [r+1, q], [r+2, q-1]]
            diamondCheck(neighbours, self.board, r, q, captured)
            
        if r+1 < self.size and q+1 < self.size:
            #upper right vertice
            neighbours = [[r+1, q], [r, q+1], [r+1, q+1]]
            diamondCheck(neighbours, self.board, r, q, captured)
            
        if q+2 < self.size and r-1 > -1:
            #lower right vertice
            neighbours = [[r, q+1], [r-1, q+1], [r-1, q+2]]
            diamondCheck(neighbours, self.board, r, q, captured)

        if q+1 < self.size and r-2 > -1:
            #bottom vertice
            neighbours = [[r-1, q], [r-1, q+1], [r-2, q+1]]
            diamondCheck(neighbours, self.board, r, q, captured)
            
        if r-1 > -1 and q-1 > -1:
            #lower left vertice
            neighbours = [[r, q-1], [r-1, q], [r-1, q-1]]
            diamondCheck(neighbours, self.board, r, q, captured)
            
        if r+1 < self.size and q-2 > -1:
            #upper left vertice
            neighbours = [[r, q-1], [r+1, q-1], [r+1, q-2]]
            diamondCheck(neighbours, self.board, r, q, captured)



        #---side diamonds---
        if r+1 < self.size and q+1 < self.size and q-1 > -1:
            #upper right side
            neighbours = [[r, q+1], [r+1, q-1], [r+1, q]]
            diamondCheck(neighbours, self.board, r, q, captured)

        if q+1 < self.size and r+1 < self.size and r-1 > -1:
            #right side
            neighbours = [[r-1, q+1], [r+1, q], [r, q+1]]
            diamondCheck(neighbours, self.board, r, q, captured)

        if q+1 < self.size and r-1 > -1:
            #lower right side
            neighbours = [[r, q+1], [r-1, q], [r-1, q+1]]
            diamondCheck(neighbours, self.board, r, q, captured)
            
        if r-1 > -1 and q-1 > -1 and q+1 < self.size:
            #lower left side
            neighbours = [[r-1, q+1], [r, q-1], [r-1, q]]
            diamondCheck(neighbours, self.board, r, q, captured)

        if r+1 < self.size and r-1 > -1 and q-1 > -1:
            #left side
            neighbours = [[r-1, q], [r+1, q-1], [r, q-1]]
            diamondCheck(neighbours, self.board, r, q, captured)
            
        if r+1 < self.size and q-1 > -1:
            #upper left side
            neighbours = [[r+1, q], [r, q-1], [r+1, q-1]]
            diamondCheck(neighbours, self.board, r, q, captured)


        for i in range(len(captured)):
            self.board[captured[i][0]][captured[i][1]] = None

     
        for i in range(self.size-1, -1, -1):
            
            print (self.board[i])


    


                 

 
    

        

