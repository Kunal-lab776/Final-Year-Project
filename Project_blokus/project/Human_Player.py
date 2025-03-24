# Importing necessary files
from Pieces_Board_Configuration import PutPieceConfiguration


# Class representing the human player implementation
class HumanPlayer:
    def __init__(self, node):
        # Node represent state of the game which initialized with class GameState
        self.node = node 
        
        # rows and column of board
        self.rows = 13
        self.columns = 13
    
    # Main method of human player to make move 
    def human_player(self):
        # Main loop runs until the board state changes 
        while True:
            try:
                # Getting user input for move  
                player_input = str(input("Please enter piece: "))
                
                try:
                    # Checking if the player wants to skip or pass their turn        
                    if player_input == "skip":
                        return self.node.board, ''
                    
                    # Check if piece is available in player piece list
                    if player_input[:2] in list(PutPieceConfiguration(self.node.player).player_piece_collection().keys()): 
                        # Ask user to input coordinate for piece where to place
                        coord = input("Only write X-coordinate,Y-coordinates? ")
                        
                        # Splitting the coordinates (x and y from comma)
                        coord_x_y = coord.split(",") 
                        
                        # Validating coordinates
                        while ((int(coord_x_y[0]) < 0 or int(coord_x_y[0]) > self.rows) or (int(coord_x_y[1]) < 0 or int(coord_x_y[1]) > self.columns)):
                            coord = input("Only write X-coordinate,Y-coordinates? ")
                            coord_x_y = coord.split(",") 
                        
                        try:
                            # Placing the piece on the board and updating the board state
                            updatedBoard = PutPieceConfiguration(self.node.player).Put_Piece(player_input, int(coord_x_y[0]), int(coord_x_y[1]), 
                                                                        self.node.board, self.node.step)
                        except IndexError: 
                            print("TRY AGAIN!")
                        
                        if self.node.board != updatedBoard:
                            return updatedBoard, player_input
                    
                    else:
                        print("PIECE IS ALREADY USED OR PIECE IS INVALID! TRY AGAIN")
                    
                # Error handling
                except:
                    print("INVLALID VALUES!")
            
            except:
                print("NOT A VALID MOVE! TRY AGAIN!")