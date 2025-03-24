from Pieces_Board_Configuration import PutPieceConfiguration

# Class workable moves to get the valid and legal move for player's
class WorkableMovesPlayer:
    def __init__(self, player, boardInfo, Player1_Pieces, Player2_Pieces, step, player1, player2):
        # Initializing the AI with player information, board state, both player pieces, current step
        self.player = player
        self.boardInfo = boardInfo
        self.Player1_Pieces = Player1_Pieces
        self.Player2_Pieces = Player2_Pieces
        self.step = step
        
        # Dictionary to place piece on board in descending order
        self.allPiece = {'five': [], 'four': [],  'three': [], 'two': [],  'one': []}
        
        # Determining the current player pieces based on player piece color
        self.current_player_pieces = self.Player1_Pieces if self.player == "green" else self.Player2_Pieces
        
        # List to store all legal moves of current player 
        self.player_legal_moves = []
        
        self.allPiecesLength = {
            '1': 'one',
            '2': 'two',
            '3': 'three',
            '4': 'four',
            '5': 'five'
        }
        
        self.all_orientation = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H'}
        
        # Check if players are playing their initial move or not
        self.available_corners, self.adjacent_edges = [], []
        
        if player1 == "Computer Player" and player2 == "Computer Player":
            if self.step <= 2:
                self.available_corners, self.adjacent_edges = ([(0,13)], []) if self.boardInfo[0][13] == -1 else ([(13,0)], [])
            else:
                self.available_corners, self.adjacent_edges = PutPieceConfiguration(self.player).avaialbleCornerEdge(self.boardInfo)
        else:
            self.available_corners, self.adjacent_edges = ([(0,13)], []) if self.step <= 2 and self.boardInfo[0][13] == -1 else PutPieceConfiguration(self.player).avaialbleCornerEdge(self.boardInfo)
            
            
    # Method to find all legal moves for the computer or player
    def movesForPlayer(self):
        # Iterate through each current player pieces
        for p in self.current_player_pieces:
            prefix = p[:1]
            if prefix in self.allPiecesLength:
                category = self.allPiecesLength[prefix]
                self.allPiece[category].append(p)

        i = 0
        # Loop until moves are found or at least one length of piece is explored
        while True:
            if not self.player_legal_moves: 
                if i < len(self.allPiece):
                    key = list(self.allPiece.keys())
                    pieces = self.allPiece[key[i]]
                    
                    # Iterate through each piece 
                    for piece in pieces:
                        # Get all orientations of the piece
                        orientation = PutPieceConfiguration("N").player_piece_collection()[piece]
                        
                        # Iterate through each orientation of piece
                        for position in range(len(orientation)):
                            # Find legal moves for the piece in the current orientation
                            self.player_legal_moves.extend(self.possibleOrientationForPlayer(orientation, position, piece))
                else:
                    break
            else:
                break
            
            i += 1
        
        return self.player_legal_moves
        
    # Method to find possible piece for the current player 
    def possibleOrientationForPlayer(self, orientation, position, piece):
        # List for storing the possible moves
        legalMoves = []
        
        # Iterate through each available corners of the board  
        for corner_x, corner_y in self.available_corners:
            # Iterate over the orientation coordinates of respective piece
            for corner in orientation[position]:
                # Calculate the new position by aligning the corner of the piece with the corner of the board
                new_x = corner_x - corner[0]
                new_y = corner_y - corner[1]
               
                # Check if the new position is valid for piece and piece can fits on the corner and board
                if self.is_valid_position(orientation[position], new_x, new_y):
                    # add the valid position and pieces into the list
                    legalMoves.append({"coordinates":(new_x, new_y), "pieces": piece + str(self.all_orientation.get(position+1))})
       
        return legalMoves
    
    # Function to check if a position is within the board boundaries and empty
    def check_for_board(self, i, j, board):
        return (0 <= i < len(board) and 0 <= j < len(board) and board[i][j] == -1)

    # Function to check if a position is valid on the board
    def is_valid_position(self, piece, x, y):
        i = 0
        check = False
        
        while i < len(piece):
            new_x = x + piece[i][0]
            new_y = y + piece[i][1]
            
            # Check if the new position is out of bounds or already occupied
            if self.check_for_board(new_x, new_y, self.boardInfo):
                if (new_x, new_y) not in self.adjacent_edges:
                    check = True
                else:
                    return False
            else:
                return False
            i+=1
        
        return check