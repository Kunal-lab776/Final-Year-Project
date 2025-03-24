import copy

# Class for representing the board configuration of the game board
class BoardConfiguration:
    def __init__(self):
        # Dimensions of canvas or window
        self.Canvas_Width = 1413
        self.Canvas_Height = 800
        
        # Size of the game board
        self.board_size = 14
        
        # Size of each square cell on the board
        self.square_tile_size = 32
        
        # x and y coordinates for board (where to be made on window or canvas)
        self.upper_x = 500
        self.upper_y = 155
        
        # Initialize the board with all cells empty (-1 represents empty cells)
        self.board = [[-1] * self.board_size for _ in range(self.board_size)]
        

# Class representing the configuration of different piece
class PiecesConfiguration:
    def __init__(self):
        
        # Starting coordinates of the player 1 pieces on the canvas
        self.topX_Player1 = 20
        self.topY_Player1 = 100
        
        # Starting coordinates of the player 2 pieces on the canvas
        self.topX_Player2 = 1050
        self.topY_Player2 = 110
        
        # Dictionary containing configuration for each piece including their all orientations
        self.pieces_configurations = { 
            '1I': { 
                'isMirror': False,
                'isRotate': False,  
                'coordinates': [(0,0)], 
            },
            '2I': { 
                'isMirror': False,
                'isRotate': True,
                'coordinates': [(0,0), (0,1)], 
                'rotation_coordinates': [((0, 0), (1, 0))],
            },
            '3I': { 
                'isMirror': False,
                'isRotate': True,
                'coordinates': [(0, 0), (0, 1), (0, 2)], 
                'rotation_coordinates': [((0, 0), (1, 0), (2, 0))],
            },
            '3V': { 
                'isMirror': False,
                'isRotate': True,
                'coordinates': [(0, 0), (0, 1), (1, 1)], 
                'rotation_coordinates': [
                    ((0, 0), (1, 0), (0, 1)), 
                    ((1, 0), (0, 1), (1, 1)), 
                    ((0, 0), (1, 0), (1, 1))],
            },
            '4I': {
                'isMirror': False,
                'isRotate': True,
                'coordinates': [(0, 0), (0, 1), (0, 2), (0,3)], 
                'rotation_coordinates': [((0, 0), (1, 0), (2, 0), (3, 0))],
            },
            '4L': { 
                'flip_coordinates': [(0,0), (0,1), (0,2), (1,2)],
                'isMirror': True,
                'isRotate': True,
                'coordinates': [(0, 0), (1, 0), (0, 1), (0,2)], 
                'rotation_coordinates': [
                    ((1, 0), (1, 1), (0, 2), (1, 2)), 
                    ((0, 0), (1, 0), (2, 0), (2, 1)), 
                    ((0, 0), (0, 1), (1, 1), (2, 1))],
                'flip_rotation_coordinates': [
                    ((0, 0), (1, 0), (1, 1), (1, 2)), 
                    ((2, 0), (0, 1), (1, 1), (2, 1)), 
                    ((0, 0), (1, 0), (2, 0), (0, 1))],
            },
            '4T': {
                'isMirror': False,
                'isRotate': True,
                'coordinates': [(0, 0), (0, 1), (1, 1), (0,2)], 
                'rotation_coordinates': [
                    ((1, 0), (0, 1), (1, 1), (1, 2)), 
                    ((1, 0), (0, 1), (1, 1), (2, 1)), 
                    ((0, 0), (1, 0), (2, 0), (1, 1))],
            },
            '4O': { 
                'isMirror': False,
                'isRotate': False,
                'coordinates': [(0, 0), (1, 0), (0, 1), (1,1)], 
            },
            '4Z': { 
                'flip_coordinates': [(1, 0), (0, 1), (1, 1), (0, 2)],
                'isMirror': True,
                'isRotate': True,
                'coordinates': [(0,0), (0,1), (1,1), (1,2)], 
                'rotation_coordinates': [((1, 0), (2, 0), (0, 1), (1, 1))],
                'flip_rotation_coordinates': [((0, 0), (1, 0), (1, 1), (2, 1))],
            },
            '5I': { 
                'isMirror': False,
                'isRotate': True,
                'coordinates': [(0,0), (0,1), (0,2), (0,3), (0,4)], 
                'rotation_coordinates': [((0, 0), (1, 0), (2, 0), (3, 0), (4, 0))],
            },
            '5P': { 
                'flip_coordinates': [(0, 0), (0, 1), (1, 1), (0, 2), (1, 2)],
                'isMirror': True,
                'isRotate': True,
                'coordinates': [(0,0), (1,0), (0,1), (1,1), (0,2)], 
                'rotation_coordinates': [
                    ((0, 0), (1, 0), (0, 1), (1, 1), (2, 1)), 
                    ((1, 0), (0, 1), (1, 1), (0, 2), (1, 2)), 
                    ((0, 0), (1, 0), (2, 0), (1, 1), (2, 1))],
                'flip_rotation_coordinates': [
                    ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1)), 
                    ((0, 0), (1, 0), (0, 1), (1, 1), (1, 2)), 
                    ((1, 0), (2, 0), (0, 1), (1, 1), (2, 1))],
            },
            '5Z': { 
                'flip_coordinates': [(1, 0), (1, 1), (0, 2), (1, 2), (0, 3)],
                'isMirror': True,
                'isRotate': True,
                'coordinates': [(0,0), (0,1), (1,1), (1,2), (1,3)], 
                'rotation_coordinates': [
                    ((1, 0), (2, 0), (3, 0), (0, 1), (1, 1)), 
                    ((0, 0), (0, 1), (0, 2), (1, 2), (1, 3)), 
                    ((2, 0), (3, 0), (0, 1), (1, 1), (2, 1))],
                'flip_rotation_coordinates': [
                    ((0, 0), (1, 0), (2, 0), (2, 1), (3, 1)), 
                    ((1, 0), (0, 1), (1, 1), (0, 2), (0, 3)), 
                    ((0, 0), (1, 0), (1, 1), (2, 1), (3, 1))],
            },
            '5L': { 
                'flip_coordinates': [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3)],
                'isMirror': True,
                'isRotate': True,
                'coordinates': [(0,0), (1,0), (0,1), (0,2), (0,3)], 
                'rotation_coordinates': [
                    ((1, 0), (1, 1), (1, 2), (0, 3), (1, 3)), 
                    ((0, 0), (1, 0), (2, 0), (3, 0), (3, 1)), 
                    ((0, 0), (0, 1), (1, 1), (2, 1), (3, 1))],
                'flip_rotation_coordinates': [
                    ((3, 0), (0, 1), (1, 1), (2, 1), (3, 1)), 
                    ((0, 0), (1, 0), (2, 0), (3, 0), (0, 1)), 
                    ((0, 0), (1, 0), (1, 1), (1, 2), (1, 3))],
            },
            '5U': { 
                'isMirror': False,
                'isRotate': True,
                'coordinates': [(0,0), (1,0), (1,1), (0,2), (1,2)], 
                'rotation_coordinates': [
                    ((0, 0), (1, 0), (0, 1), (0, 2), (1, 2)), 
                    ((0, 0), (2, 0), (0, 1), (1, 1), (2, 1)), 
                    ((0, 0), (1, 0), (2, 0), (0, 1), (2, 1))],
            },  
            '5Y': { 
                'flip_coordinates': [(0, 0), (0, 1), (0, 2), (1, 2), (0, 3)],
                'isMirror': True,
                'isRotate': True,
                'coordinates': [(0,0), (0,1), (1,1), (0,2), (0,3)], 
                'rotation_coordinates': [
                    ((0, 0), (1, 0), (2, 0), (3, 0), (2, 1)), 
                    ((1, 0), (1, 1), (0, 2), (1, 2), (1, 3)), 
                    ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1))],
                'flip_rotation_coordinates': [
                    ((2, 0), (0, 1), (1, 1), (2, 1), (3, 1)), 
                    ((1, 0), (0, 1), (1, 1), (1, 2), (1, 3)), 
                    ((0, 0), (1, 0), (2, 0), (3, 0), (1, 1))],
            },
            '5T': { 
                'isMirror': False,
                'isRotate': True,
                'coordinates': [(0,0), (0,1), (1,1), (2,1), (0,2)], 
                'rotation_coordinates': [
                    ((2, 0), (0, 1), (1, 1), (2, 1), (2, 2)), 
                    ((1, 0), (1, 1), (0, 2), (1, 2), (2, 2)), 
                    ((0, 0), (1, 0), (2, 0), (1, 1), (1, 2))],
            },
            '5V': { 
                'isMirror': False,
                'isRotate': True,
                'coordinates': [(0,0), (1,0), (2,0), (2,1), (2,2)], 
                'rotation_coordinates': [
                    ((0, 0), (0, 1), (0, 2), (1, 2), (2, 2)), 
                    ((0, 0), (1, 0), (2, 0), (0, 1), (0, 2)), 
                    ((2, 0), (2, 1), (0, 2), (1, 2), (2, 2))],
            },
            '5W': { 
                'isMirror': False,
                'isRotate': True,
                'coordinates': [(0,0), (1,0), (1,1), (2,1), (2,2)], 
                'rotation_coordinates': [
                    ((2, 0), (1, 1), (2, 1), (0, 2), (1, 2)), 
                    ((1, 0), (2, 0), (0, 1), (1, 1), (0, 2)), 
                    ((0, 0), (0, 1), (1, 1), (1, 2), (2, 2))],
            },
            '5S': { 
                'flip_coordinates': [(2, 0), (0, 1), (1, 1), (2, 1), (0, 2)],
                'isMirror': True,
                'isRotate': True,    
                'coordinates': [(0,0), (0,1), (1,1), (2,1), (2,2)], 
                'rotation_coordinates': [((1, 0), (2, 0), (1, 1), (0, 2), (1, 2))],
                'flip_rotation_coordinates': [((0, 0), (1, 0), (1, 1), (1, 2), (2, 2))],
            },
            '5F': { 
                'flip_coordinates': [(1, 0), (0, 1), (1, 1), (2, 1), (0, 2)],
                'isMirror': True,
                'isRotate': True,
                'coordinates': [(0,0), (0,1), (1,1), (2,1), (1,2)],
                'rotation_coordinates': [
                    ((1, 0), (1, 1), (2, 1), (0, 2), (1, 2)), 
                    ((1, 0), (2, 0), (0, 1), (1, 1), (1, 2)), 
                    ((1, 0), (0, 1), (1, 1), (2, 1), (2, 2))],
                'flip_rotation_coordinates': [
                    ((1, 0), (0, 1), (1, 1), (1, 2), (2, 2)), 
                    ((0, 0), (1, 0), (1, 1), (2, 1), (1, 2)), 
                    ((2, 0), (0, 1), (1, 1), (2, 1), (1, 2))],
            },
            '5C': { 
                'isMirror': False,
                'isRotate': False,
                'coordinates': [(1,0), (0,1), (1,1), (2,1), (1,2)], 
            }
        }


# Class representing the placement of a piece on the board
class PutPieceConfiguration:
    def __init__(self, player):
        # Check if move played by the player is their first move
        self.isOpeningMoves = False
        
        # Check if move played by the player is valid 
        self.isCorrectMoves = False
        
        # Current player which is currently playing their move
        self.player = player
        
        # List of available corner position on the board
        self.available_corners = []
        
        #List of adjacent edge position on the board
        self.adjacent_edges = []
        
        self.all_orientation_of_piece = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        
        # check for opening move; means checking if the players placing their first move in respective positions 
        self.opening_move = [(0,13), (13,0)]   
        
    # Function to get a list of pieces for the current player
    def player_piece_collection(self):
        player_piece = {}
        
       
        player_items = {
            "green": Player1.items(),
            "yellow": Player2.items(),
            "N": PiecesConfiguration().pieces_configurations.items()
        }

        # Retrieve the items based on the player string
        playerPieces = player_items.get(self.player)
        
        # Iterating through piece of the player and adding them to the list
        for piece_name, piece_info in playerPieces:
            matrix = piece_info['coordinates']
            if piece_name in player_piece:
                if isinstance(player_piece[piece_name], list):
                    player_piece[piece_name[:2]].extend([matrix])
            else:
                player_piece[piece_name[:2]] = [matrix]
            
            if piece_info['isRotate']:
                rotation_matrix = piece_info['rotation_coordinates']
                player_piece[piece_name[:2]].extend(rotation_matrix)
                
            if piece_info['isMirror']:
                reflection_matrix = piece_info['flip_coordinates']
                reflection_rotation_matrix = piece_info['flip_rotation_coordinates']
                player_piece[piece_name[:2]].extend([reflection_matrix])
                player_piece[piece_name[:2]].extend(reflection_rotation_matrix)
        
        return player_piece
    
    
    # Function to place piece on board
    def Put_Piece(self, piece_name, row, col, board, step):
        # Deepcopy of the board to prevent changes of the original board
        updated_board = copy.deepcopy(board)
        
        self.avaialbleCornerEdge(board)
        
        pieces_dict = self.player_piece_collection()
        
        # Get the coordinates of the selected piece
        coordinates = pieces_dict[piece_name[0]][self.all_orientation_of_piece[piece_name[1]]] if piece_name in ["1A", "2A", "2B"] else pieces_dict[piece_name[:2]][self.all_orientation_of_piece[piece_name[2]]]
             
        i = 0
        while i < len(coordinates):
            x = row + coordinates[i][0]
            y = col + coordinates[i][1]
            
            # Check if the position on board is not already occupied
            if updated_board[x][y] in ["green" , "yellow"]:
                print("RESERVED PLACE. PLEASE RETRY!")
                return board
            else:
                # Check if step number is 1 or 2, if it is then it means that players are playing their first turn
                if step <= 2:
                    # Check if players our putting their respective first piece in correct place
                    if (x, y) in self.opening_move:
                        self.isOpeningMoves = True
                else:
                    self.isOpeningMoves = True
                
                # Check if piece is satisfying the game rules
                if step > 2:
                    # Check if player place piece on the available corners of the board
                    if (x, y) in self.available_corners:
                        self.isCorrectMoves = True
                else:
                    self.isCorrectMoves = True
                
                # Check if the player not placing the piece on the edge of same color piece
                if (x, y) in self.adjacent_edges:
                    print("PIECE TOUCH EDGE OF SAME COLOR! PLEASE RETRY!")
                    return board

            # Place tile of player piece on iterating coordinates
            updated_board[x][y] = self.player
            
            i+=1
        
        # Return the modified board if piece is correctly placed on board or condition are met, otherwise return the original board
        return updated_board if self.isOpeningMoves and self.isCorrectMoves else board
        
    
   
    # Function to check the adjacent edges of a piece
    def check_edge(self, i, j, currentBoard, flag):
        check = False
        if flag == 1:
            check  = j > 0 and currentBoard[i][j-1] == -1
        elif flag == 2:
            check = j < len(currentBoard) - 1 and currentBoard[i][j+1] == -1
        elif flag == 3:    
            check = i > 0 and currentBoard[i-1][j] == -1
        elif flag == 4:    
            check = i < len(currentBoard) - 1 and currentBoard[i+1][j] == -1
        
        return check

    # Function for getting available corners of a current player on the board
    def corner(self, currentBoard):
        i = 0
        j = 0
        while i < len(currentBoard):
            j = 0
            while j < len(currentBoard):
                # Checking if the square tile belong to current player
                if (currentBoard[i][j] == self.player):
                    
                    # Coordinates of corners of piece
                    possible_corners = [
                        (i-1, j-1),  # Upper-left corner
                        (i-1, j+1),  # Upper-right corner
                        (i+1, j-1),  # Bottom-left corner
                        (i+1, j+1)   # Bottom-right corner
                    ]
                    # Find out those corners which can be placed and add them to the list of available corners
                    for corner_i, corner_j in possible_corners:
                        if 0 <= corner_i < len(currentBoard) and 0 <= corner_j < len(currentBoard[i]):
                            # Check if the corner is vacant and has no adjacent piece of the current player
                            top_edge = (corner_i == 0 or (corner_i > 0 and currentBoard[corner_i-1][corner_j] != self.player))
                            right_edge = (corner_j == len(currentBoard) - 1 or (corner_j < len(currentBoard) - 1 and currentBoard[corner_i][corner_j+1] != self.player))
                            bottom_edge = (corner_i == len(currentBoard) - 1 or (corner_i < len(currentBoard) - 1 and currentBoard[corner_i+1][corner_j] != self.player))
                            left_edge = (corner_j == 0 or (corner_j > 0 and currentBoard[corner_i][corner_j-1] != self.player))
                            
                            if top_edge and right_edge and bottom_edge and left_edge:
                                # Add the corner to the list of available corners
                                self.available_corners.append((corner_i, corner_j))
                    
                j += 1
            i += 1      
            
        return list(dict.fromkeys(self.available_corners))
                
    # Function for getting adjacent edges of current player on the board
    def adj(self, currentBoard):
        leftEdge = 1
        rightEdge = 2
        topEdge = 3
        bottomEdge = 4
        
        i = 0
        j = 0
        while i < len(currentBoard):
            j = 0
            while j < len(currentBoard):
                # Checking if the square tile belong to current player
                if (currentBoard[i][j] == self.player):
                    # Check the piece adjacent edge at left side
                    if (self.check_edge(i, j, currentBoard, leftEdge)): 
                        self.adjacent_edges.append((i,j-1))
                    
                    # Check the piece adjacent edge at right side
                    if (self.check_edge(i, j, currentBoard, rightEdge)): 
                        self.adjacent_edges.append((i,j+1))
                    
                    # Check the piece adjacent edge at upper side
                    if (self.check_edge(i, j, currentBoard, topEdge)):
                        self.adjacent_edges.append((i-1,j))
                    
                    # Check the piece adjacent edge at bottom side
                    if (self.check_edge(i, j, currentBoard, bottomEdge)):
                        self.adjacent_edges.append((i+1,j))
                j += 1
            i += 1
            
        return list(dict.fromkeys(self.adjacent_edges))
    
    # Function for getting all available corners and adjacent edges of the board for the specific player
    def avaialbleCornerEdge(self, currentBoard):
        # return the avaialble corners and adjacent edges of current player on the board
        return self.corner(currentBoard), self.adj(currentBoard)
        
        
        
# Initializing the piece for player 1 and player 2
Player1 = PiecesConfiguration().pieces_configurations
Player2 = PiecesConfiguration().pieces_configurations