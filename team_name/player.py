from audioop import minmax
from random import randrange
import math



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

        def getNeighbours(self, board, row, column, colour):
            arr = []
            
            if row+1 < self.size:
                if board[row+1][column] == colour:
                    arr.append((row+1, column))
            if row-1 > -1:
                if board[row-1][column] == colour:
                    arr.append((row-1, column))
            if column+1 < self.size:
                if board[row][column+1] == colour:
                    arr.append((row, column+1))
            if column-1 > -1:
                if board[row][column-1] == colour:
                    arr.append((row, column-1))
            if row-1 > -1 and column+1 < self.size:
                if board[row-1][column+1] == colour:
                    arr.append((row-1, column+1))
            if row+1 < self.size and column-1 > -1:
                if board[row+1][column-1] == colour:
                    arr.append((row+1, column-1))
            
            return arr


        def checkLine(self, board, row, column, colour, checked):
            if colour == "red" and row == self.size - 1: #checks if on the final row for red
                return True
            elif colour == "blue" and column == self.size - 1: #checks if on the final column for blue
                return True
            
            checked.append((row, column))
            
            neighbours = getNeighbours(self, board, row, column, colour)
            
            #if not at endpoint, move to first unchecked neighbour
            for i in range(len(neighbours)):
                if ((neighbours[i][0], neighbours[i][1]) not in checked): 
                    if checkLine(self, board, neighbours[i][0], neighbours[i][1], colour, checked):
                        return True
            return False


        def isMovesLeft(board, self):
            for i in range (self.size):
                for j in range (self.size):
                    if self.board[i][j] == None:
                        return True
            return False

       
        def evaluate(board, self):
            checked = []
            for i in range(self.size): #checks for any red winning line starting from the bottom row
                if board[0][i] == "red":
                    line = checkLine(self, board, 0, i, "red", checked)
                    if line == True and self.colour == "red":
                        return 10
                    if line == True and self.colour == "blue":
                        return -10
                        
            for j in range(self.size): #checks for any blue winning line starting from the leftmost column
                if board[j][0] == "blue":
                    line = checkLine(self, board, j, 0, "blue", checked)
                    if line == True and self.colour == "blue":
                        return 10
                    if line == True and self.colour == "red":
                        return -10
    
            return 0 #if no lines found, return 0.
        def heuristic_coneccted(game,board, player):
            oponent="blue" if player=="red" else "blue"
    
            ccp=countBetterConnected(game,board,player)
            cco=countBetterConnected(game,board,oponent)
    
            return (cco-ccp)/(max(ccp,cco)+1)
        def countBetterConnected(game,board, player):
            counted = set()
            connected = 0
    
            for i in range(game.size):
                for j in range(game.size):
                    if board[i][j] == player:
                        neighbors = getNeighbours(game,board,i,j,player)
                        for n in neighbors:
                            r, c= n
                            if board[i][j] == player and n not in counted:
                                counted.add((r,c))
                                connected += 1
            return connected    
        MAX, MIN = 1000, -1000
        def minimax(board, depth, isMax, self, alpha,beta):
            
            
            playerToMax = self.colour
            if self.colour == "red":
                playerToMin = "blue"
            elif self.colour == "blue":
                playerToMin = "red"

         
            score = heuristic_coneccted(self,board, self.colour)
            
            # if score == 10:
            #     return score

            # if score == -10:
            #     return score

            if isMovesLeft(board, self) == False:
                return score
            if not depth:
                return score    
            
          
            if (isMax):
                best = -math.inf
                

                for i in range(self.size):
                    for j in range(self.size):
                        if board[i][j] == None:
                            board[i][j] = playerToMax
                            #change here
                            best = max(best, minimax(board,depth-1,False,self,alpha,beta))
                            alpha = max(best,alpha)
                           
                            board[i][j] = None
                            if beta <= alpha:
                                
                                break
                            
                return best

            else:
                best =  math.inf
                for i in range(self.size):
                    for j in range(self.size):
                        if board[i][j] == None:
                            board[i][j] = playerToMin
                            best = min(best, minimax(board, depth -1,  True, self,alpha,beta))
                            board[i][j] = None
                            beta = min(beta,best)
                            if beta <= alpha:
                                
                                break
                            

                return best
       
        
                
                        
        def findBestMove(board,self,alpha,beta):
            playerToMax = self.colour
                  
            bestVal = -math.inf
            bestMove = (-1,-1)
             
            for i in range(self.size):
                
                for j in range(self.size):
                   
                    if (board[i][j] == None):
                      
                        board[i][j] = playerToMax
                        

                        moveVal = minimax(board, 3, True, self,MIN,MAX)
                        
                      
                        
                        board[i][j] = None
                        if (moveVal > bestVal):
                            bestMove = (i,j)
                            bestVal = moveVal
                        print("checking move: ", (i,j))
                        print("value: ", moveVal, "\n")
                       
                        

            return bestMove



        bestMove = findBestMove(self.board,self,-math.inf,math.inf)
        print("best move is", bestMove)
        return ("PLACE",bestMove[0],bestMove[1])    
                    
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


    


                 

 
    

        

