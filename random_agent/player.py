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
        self.turnCount = 1

    def action(self):
        """
        Called at the beginning of your turn. Based on the current state
        of the game, select an action to play.
        """
        while True:
            r = randrange(self.size)
            q = randrange(self.size)
            if self.board[r][q] == None:
                return("PLACE", r, q)
                        
                
                    
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
        

