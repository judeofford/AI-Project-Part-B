from audioop import minmax
from random import randrange
from queue import PriorityQueue
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
        self.turnCount = 1
      

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """

        #if blue, always steal on first turn
        if self.colour == "blue" and self.turnCount == 2:
            return("STEAL", )


        #gets the neighbours of any given node in the board
        def getNeighbours(self, board, row, column, colour):
            arr = []
            
            if row+1 < self.size:
                arr.append((row+1, column))
            if row-1 > -1:
                arr.append((row-1, column))
            if column+1 < self.size:
                arr.append((row, column+1))
            if column-1 > -1:
                arr.append((row, column-1))
            if row-1 > -1 and column+1 < self.size:
                arr.append((row-1, column+1))
            if row+1 < self.size and column-1 > -1:
                arr.append((row+1, column-1))
        
            return arr

        #gets the neighbours matching a specified colour for any given node in the board
        def getColourNeighbours(self, board, row, column, colour):
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


        #checks for a complete line (win state)
        def checkLine(self, board, row, column, colour, checked):
            if colour == "red" and row == self.size - 1: #checks if on the final row for red
                return True
            elif colour == "blue" and column == self.size - 1: #checks if on the final column for blue
                return True
            
            checked.append((row, column))
            
            neighbours = getColourNeighbours(self, board, row, column, colour)
            
            #if not at endpoint, move to first unchecked neighbour
            for i in range(len(neighbours)):
                if ((neighbours[i][0], neighbours[i][1]) not in checked): 
                    if checkLine(self, board, neighbours[i][0], neighbours[i][1], colour, checked):
                        return True
            return False


        #checks if the supplied neighbours form a diamond
        def diamondCheck(dneighbours, board, row, column, capturearray):
            playercount = 0
            oppcount = 0
            if board[dneighbours[0][0]][dneighbours[0][1]] != None and board[dneighbours[1][0]][dneighbours[1][1]] != None:
                if (board[dneighbours[0][0]][dneighbours[0][1]] != board[row][column] and
                board[dneighbours[1][0]][dneighbours[1][1]] != board[row][column] and
                board[dneighbours[2][0]][dneighbours[2][1]] == board[row][column]):
                    for i in range(3):
                        if board[dneighbours[i][0]][dneighbours[i][1]] != board[row][column]:
                            capturearray.append([dneighbours[i][0], dneighbours[i][1]])

        #checks all possible diamond variations and returns which nodes to remove
        def checkAllDiamonds(self, board, r, q):
            captured = []

            #---vertice diamonds---
            if r+2 < self.size and q-1 > -1:
                #top vertice
                neighbours = [[r+1, q-1], [r+1, q], [r+2, q-1]]
                diamondCheck(neighbours, board, r, q, captured)                
            if r+1 < self.size and q+1 < self.size:
                #upper right vertice
                neighbours = [[r+1, q], [r, q+1], [r+1, q+1]]
                diamondCheck(neighbours, board, r, q, captured)                
            if q+2 < self.size and r-1 > -1:
                #lower right vertice
                neighbours = [[r, q+1], [r-1, q+1], [r-1, q+2]]
                diamondCheck(neighbours, board, r, q, captured)
            if q+1 < self.size and r-2 > -1:
                #bottom vertice
                neighbours = [[r-1, q], [r-1, q+1], [r-2, q+1]]
                diamondCheck(neighbours, board, r, q, captured)
            if r-1 > -1 and q-1 > -1:
                #lower left vertice
                neighbours = [[r, q-1], [r-1, q], [r-1, q-1]]
                diamondCheck(neighbours, board, r, q, captured)   
            if r+1 < self.size and q-2 > -1:
                #upper left vertice
                neighbours = [[r, q-1], [r+1, q-1], [r+1, q-2]]
                diamondCheck(neighbours, board, r, q, captured)

            #---side diamonds---
            if r+1 < self.size and q+1 < self.size and q-1 > -1:
                #upper right side
                neighbours = [[r, q+1], [r+1, q-1], [r+1, q]]
                diamondCheck(neighbours, board, r, q, captured)
            if q+1 < self.size and r+1 < self.size and r-1 > -1:
                #right side
                neighbours = [[r-1, q+1], [r+1, q], [r, q+1]]
                diamondCheck(neighbours, board, r, q, captured)
            if q+1 < self.size and r-1 > -1:
                #lower right side
                neighbours = [[r, q+1], [r-1, q], [r-1, q+1]]
                diamondCheck(neighbours, board, r, q, captured)                
            if r-1 > -1 and q-1 > -1 and q+1 < self.size:
                #lower left side
                neighbours = [[r-1, q+1], [r, q-1], [r-1, q]]
                diamondCheck(neighbours, board, r, q, captured)
            if r+1 < self.size and r-1 > -1 and q-1 > -1:
                #left side
                neighbours = [[r-1, q], [r+1, q-1], [r, q-1]]
                diamondCheck(neighbours, board, r, q, captured)
            if r+1 < self.size and q-1 > -1:
                #upper left side
                neighbours = [[r+1, q], [r, q-1], [r+1, q-1]]
                diamondCheck(neighbours, board, r, q, captured)

            return captured


        #returns an array containing the distance between a given node and every other node in the board
        def dijkstra(self, board, start_node, visited, colour):
            D = {}
            for i in range(self.size):
                for j in range(self.size):
                    D[(i,j)] = float('inf')
            D[start_node] = 0

            pq = PriorityQueue()
            pq.put((0, start_node))

            while not pq.empty():
                (dist, current_node) = pq.get()
                visited.append(current_node)
                neighbours = getNeighbours(self, board, current_node[0], current_node[1], colour)
                for i in range(len(neighbours)):
                    if board[neighbours[i][0]][neighbours[i][1]] == colour:
                        distance = 0
                        if neighbours[i] not in visited:
                            old_cost = D[neighbours[i]]
                            new_cost = D[current_node] + distance
                            if new_cost < old_cost:
                                pq.put((new_cost, neighbours[i]))
                                D[neighbours[i]] = new_cost
                    if board[neighbours[i][0]][neighbours[i][1]] == None:
                        distance = 1
                        if neighbours[i] not in visited:
                            old_cost = D[neighbours[i]]
                            new_cost = D[current_node] + distance
                            if new_cost < old_cost:
                                pq.put((new_cost, neighbours[i]))
                                D[neighbours[i]] = new_cost
            return D


        #checks if there are still moves available
        def isMovesLeft(board, self):
            for i in range (self.size):
                for j in range (self.size):
                    if self.board[i][j] == None:
                        return True
            return False

        #returns a score value representing how good a given board state is for the player
        def evaluate(self, board):
            redShortest = 1000
            blueShortest = 1000
            
            for i in range(self.size):
                start = (0, i) #red start points, bottom row
                visited = []

                #generate distances from start point to all nodes
                distances = dijkstra(self, board, start, visited, "red")
                
                for j in range(self.size):
                    end = (self.size - 1, j) #red end points, top row
                    #find the shortest distance to any end node
                    if distances[end] < redShortest:
                        redShortest = distances[end]
                        
            for i in range(self.size):
                start = (i, 0) #blue start points, leftmost column
                visited = []

                #generate distances from start point to all nodes
                distances = dijkstra(self, board, start, visited, "blue")
                
                for j in range(self.size):
                    end = (j, self.size - 1) #blue end points, rightmost column
                    #find the shortest distance to any end node
                    if distances[end] < blueShortest:
                        blueShortest = distances[end]


            if self.colour == "red":
                score = blueShortest - redShortest
                return score

            if self.colour == "blue":
                score = redShortest - blueShortest
                return score     

        #minimax with alpha-beta pruning, analyzes the future board states a move might result in to find the best move
        MAX, MIN = 1000, -1000
        def minimax(board, depth, isMax, self, alpha, beta):
            
            playerToMax = self.colour
            if self.colour == "red":
                playerToMin = "blue"
            elif self.colour == "blue":
                playerToMin = "red"

            score = evaluate(self, board)
            
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
                            best = min(best, minimax(board, depth -1,True,self,alpha,beta))
                            board[i][j] = None
                            beta = min(beta,best)
                            if beta <= alpha:
                                break
                            

                return best
             
        #checks all potential moves and finds the one with the highest score                
        def findBestMove(board,self,alpha,beta):
            playerToMax = self.colour
            if self.colour == "red":
                playerToMin = "blue"
            elif self.colour == "blue":
                playerToMin = "red"
                  
            bestVal = -math.inf
            bestMove = (-1,-1)
            diamondAvailable = False
            diamondStore = (-1,-1)
             
            for i in range(self.size):
                
                for j in range(self.size):
                   
                    if (board[i][j] == None):
                      
                        board[i][j] = playerToMax
                        
                        moveVal = minimax(board, 0, False, self,MIN,MAX)

                        #if diamond capture available, store for later
                        captured = []
                        captured = checkAllDiamonds(self, board, i, j)
                        if captured != []:
                            diamondAvailable = True
                            diamondStore = (i, j)

                        #prioritize preventing opponent diamond captures
                        captured = []
                        board[i][j] = playerToMin
                        captured = checkAllDiamonds(self, board, i, j)
                        if captured != []:
                            moveVal = 9998
                        board[i][j] = playerToMax
                        
                        #always takes a winning move if available
                        checked = []
                        line = False
                        if playerToMax == "red":
                            for x in range(self.size):
                                if board[0][x] == "red":
                                    line = checkLine(self, board, 0, x, "red", checked)
                        if playerToMax == "blue":
                            for x in range(self.size):
                                if board[x][0] == "blue":
                                    line = checkLine(self, board, x, 0, "blue", checked)
                        if line == True:
                            moveVal = 9999
  
                        board[i][j] = None
                        
                        if (moveVal > bestVal):
                            bestMove = (i,j)
                            bestVal = moveVal

            #when losing, go for captures if possible
            if (bestVal <= 0 and diamondAvailable == True):
                bestMove = diamondStore

            return bestMove

        bestMove = findBestMove(self.board,self,-math.inf,math.inf)
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
                    for i in range(3):
                        if board[dneighbours[i][0]][dneighbours[i][1]] != board[row][column]:
                            capturearray.append([dneighbours[i][0], dneighbours[i][1]])

        #check for diamonds, most nodes have 12 possible diamonds
        def checkAllDiamonds(self, board, r, q):
            captured = []

            #---vertice diamonds---
            if r+2 < self.size and q-1 > -1:
                #top vertice
                neighbours = [[r+1, q-1], [r+1, q], [r+2, q-1]]
                diamondCheck(neighbours, board, r, q, captured)
                
            if r+1 < self.size and q+1 < self.size:
                #upper right vertice
                neighbours = [[r+1, q], [r, q+1], [r+1, q+1]]
                diamondCheck(neighbours, board, r, q, captured)
                
            if q+2 < self.size and r-1 > -1:
                #lower right vertice
                neighbours = [[r, q+1], [r-1, q+1], [r-1, q+2]]
                diamondCheck(neighbours, board, r, q, captured)

            if q+1 < self.size and r-2 > -1:
                #bottom vertice
                neighbours = [[r-1, q], [r-1, q+1], [r-2, q+1]]
                diamondCheck(neighbours, board, r, q, captured)
                
            if r-1 > -1 and q-1 > -1:
                #lower left vertice
                neighbours = [[r, q-1], [r-1, q], [r-1, q-1]]
                diamondCheck(neighbours, board, r, q, captured)
                
            if r+1 < self.size and q-2 > -1:
                #upper left vertice
                neighbours = [[r, q-1], [r+1, q-1], [r+1, q-2]]
                diamondCheck(neighbours, board, r, q, captured)



            #---side diamonds---
            if r+1 < self.size and q+1 < self.size and q-1 > -1:
                #upper right side
                neighbours = [[r, q+1], [r+1, q-1], [r+1, q]]
                diamondCheck(neighbours, board, r, q, captured)

            if q+1 < self.size and r+1 < self.size and r-1 > -1:
                #right side
                neighbours = [[r-1, q+1], [r+1, q], [r, q+1]]
                diamondCheck(neighbours, board, r, q, captured)

            if q+1 < self.size and r-1 > -1:
                #lower right side
                neighbours = [[r, q+1], [r-1, q], [r-1, q+1]]
                diamondCheck(neighbours, board, r, q, captured)
                
            if r-1 > -1 and q-1 > -1 and q+1 < self.size:
                #lower left side
                neighbours = [[r-1, q+1], [r, q-1], [r-1, q]]
                diamondCheck(neighbours, board, r, q, captured)

            if r+1 < self.size and r-1 > -1 and q-1 > -1:
                #left side
                neighbours = [[r-1, q], [r+1, q-1], [r, q-1]]
                diamondCheck(neighbours, board, r, q, captured)
                
            if r+1 < self.size and q-1 > -1:
                #upper left side
                neighbours = [[r+1, q], [r, q-1], [r+1, q-1]]
                diamondCheck(neighbours, board, r, q, captured)

            return captured


        #updates internal board with action
        if action[0] == "PLACE":
            r = action[1]
            q = action[2]

            self.board[r][q] = player
            
            captured = checkAllDiamonds(self, self.board, r, q)
            for i in range(len(captured)):
                self.board[captured[i][0]][captured[i][1]] = None

        else:
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == "red":
                        self.board[i][j] = None
                        self.board[j][i] = "blue"

        self.turnCount = self.turnCount + 1


    


                 

 
    

        

