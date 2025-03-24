# Importing necessary libraries and modules
import tkinter as tk
from tkinter import *
from Pieces_Board_Configuration import PutPieceConfiguration, BoardConfiguration, PiecesConfiguration
import Pieces_Board_Configuration as Pieces_Board_Configuration
from AI_Player import AIPlayer
from Human_Player import HumanPlayer
from Game_State import GameState


# Main class of game
class BlokusGame:
    def __init__(self):
        # Initializing the game and setting player option
        print()
        print("Please read the Instruction(READ_THIS_FIRST.md) file before playing!!")
        print()
        print("Whom do you want to play the game with?")
        print()
        print("1. Human vs Computer")
        print("2. Human vs Human")
        print("3. Computer vs Computer")
        print()
        
        # Collecting user input; who are playing the game
        self.player1 = ""
        self.player2 = ""
        
        # Taking user input from player for their choice
        self.choice = int(input("Which option? "))
        
        # Validating user input
        while self.choice not in [1,2,3]:
            self.choice = int(input("Which option? "))

        self.choice = int(self.choice)
        
        # Depending on user choice, setting the player types
        if self.choice == 1:
            self.player1 = "Human Player"
            self.player2 = "Computer Player"
            
            print()
            print("Which strategy want to play with AI?")
            print()
            print("1: Random Strategy")
            print("2: Advance Strategy: Minimax with Alpha-Beta pruning using Iterative Deepening Depth-First Search")
            print()
            
            self.choice1 = int(input("Which option? "))
            
            while self.choice1 not in [1,2]:
                self.choice1 = int(input("Which option? "))
            
            self.choice1 = int(self.choice1)
            
        elif self.choice == 2:
            self.player1 = "Human Player"
            self.player2 = "Human Player"
        elif self.choice == 3:
            self.player1 = "Computer Player"
            self.player2 = "Computer Player"
            print()
            print("Which strategy want to play with AI?")
            print()
            print("1: Random Strategy")
            print("2: Advance Strategy: Minimax with Alpha-Beta pruning using Iterative Deepening Depth-First Search")
            print()
            
            self.choice1 = int(input("Which option? "))
            
            while self.choice1 not in [1,2]:
                self.choice1 = int(input("Which option? "))
            
            self.choice1 = int(self.choice1)
            
        
        # Initializing the main window for the game using Tktiner
        self.window = tk.Tk()
        # Setting window title
        self.window.title("Blokus Game")
 
        frame=Frame(self.window)
        frame.pack(expand=True, fill=BOTH)
        self.canvas=Canvas(frame,width=BoardConfiguration().Canvas_Width,height=BoardConfiguration().Canvas_Height,scrollregion=(0,0,1350,1350))
        vbar=Scrollbar(frame,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(width=BoardConfiguration().Canvas_Width,height=BoardConfiguration().Canvas_Height, background="black")
        self.canvas.config(yscrollcommand=vbar.set)
        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)
        
        # Display the label of the game
        Label(self.window, text = "Blokus Duo Game", bg="black", fg="white", font=("Comic Sans MS", 25)).place(x = 610,y = 40)  

        # Initializing the pieces of both players
        self.Player1 = Pieces_Board_Configuration.Player1
        self.Player2 = Pieces_Board_Configuration.Player2
        
        # Initializing the game step or which round of game player is playing
        self.step = 1
        
        # Initializing the first turn player of game
        self.current_Player = "green"
       
        # Initializing the initial game state
        self.mainNode = GameState(self.current_Player, BoardConfiguration().board, self.step, list(PutPieceConfiguration("green").player_piece_collection().keys()), 
                        list(PutPieceConfiguration("yellow").player_piece_collection().keys()))
         
        # Initialize the piece label which goes from 'A'-'H' including main piece and every orientation of piece
        self.piece_label = 'A'
        
        # Initializing variable for pieces on canvas where to be made
        self.topX = 0
        self.topY = 0
        
        # counter initialized for checking if either player ran out of move or they pass the turn to other player
        self.consecutive_count = 0
        
        # Initialized two variable to denote the score of player and update the score as game continues
        self.Playersum1 = 0
        self.Playersum2 = 0
        
        # Label to show the game scores on Tktiner window or canvas
        Label(self.window, text ="Player 1 Score: " + str(self.Playersum1), bg="black", fg="white", 
                font=("Comic Sans MS", 25)).place(x = 20, y = 40)  
        Label(self.window, text ="Player 2 Score: " + str(self.Playersum2), bg="black", fg="white", 
            font=("Comic Sans MS", 25)).place(x = 1050,y = 40)  
        
        # Main function to run whole game 
        self.startGame()
        
        self.window.mainloop()


   
    def startGame(self):
        # Main game loop
        while True:
            # Deleting existing old board and pieces 
            self.canvas.delete("all")
            # Creating the updated board every time a move is played 
            self.create_board(self.mainNode.board)
            
            # Creating and display the pieces for players  
            self.show_pieces('green', self.Player1.items())
            self.show_pieces('yellow', self.Player2.items())
            
            # Checking if the turn is of player 1 or player 2
            if self.current_Player == "yellow":
                print()
                print(self.player1)
                print()
                
                # Assigning the player according to user input
                if self.player1 == "Human Player" and self.player2 == "Computer Player":
                    human1 = HumanPlayer(self.mainNode)
                    board, move = human1.human_player()
                elif self.player1 == "Human Player" and self.player2 == "Human Player":
                    human2 = HumanPlayer(self.mainNode)
                    board, move = human2.human_player()
                elif self.player1 == "Computer Player" and self.player2 == "Computer Player":
                    ai1 = AIPlayer(self.choice1)
                    board, move = ai1.AI_turn(self.mainNode, self.player1, self.player2)
                    
                # Check if the player 1 doesn't play the move return the old board and player 2 ran out of moves then game reached to end condition
                if board == self.mainNode.board:
                    self.consecutive_count += 1
                    if self.consecutive_count >= 2:
                        break
                # Removing the piece from list after player 1 successfully played piece 
                else:
                    self.consecutive_count = 0
                    if (self.player1 == "Human Player" and self.player2 == "Computer Player") or (self.player1 == "Human Player" and self.player2 == "Human Player") or (self.player1 == "Computer Player" and self.player2 == "Computer Player"):
                        self.Player2.pop(move[:2])
                    
                    # Add the score of player 1 to their current score 
                    self.Playersum2 += int(move[0])
                
                # After player 1 played the turn it is changed to player 2
                self.current_Player = "green"
            else:
                print()
                print(self.player2)
                print()
                
                if self.player2 == "Computer Player" and self.player1 == "Human Player":
                    ai3 = AIPlayer(self.choice1)
                    board, move = ai3.AI_turn(self.mainNode, self.player1, self.player2)
                elif self.player2 == "Human Player" and self.player1 == "Human Player":
                    human3 = HumanPlayer(self.mainNode)
                    board, move = human3.human_player()
                elif self.player2 == "Computer Player" and self.player1 == "Computer Player":
                    ai4 = AIPlayer(self.choice1)
                    board, move = ai4.AI_turn(self.mainNode, self.player1, self.player2)
                    
                if board == self.mainNode.board:
                    self.consecutive_count += 1
                    if self.consecutive_count >= 2:
                        break
                
                # Removing the piece from list after player 2 successfully played piece
                else:
                    self.consecutive_count = 0
                    if (self.player2 == "Computer Player" and self.player1 == "Human Player") or (self.player2 == "Human Player" and self.player1 == "Human Player") or (self.player2 == "Computer Player" and self.player1 == "Computer Player"):
                        self.Player1.pop(move[:2])
                    
                    # Add the score of player 2 to their current score 
                    self.Playersum1 += int(move[0])
                
                # After player 2 played the turn it is changed to player 1
                self.current_Player = "yellow"
                
            # Incremening the step at every turn
            self.step += 1
            
            # Change the game state or node every time player played their turn
            self.mainNode = GameState(self.current_Player, board, self.step, list(PutPieceConfiguration("green").player_piece_collection().keys()), list(PutPieceConfiguration("yellow").player_piece_collection().keys()))
        
            # As game continue then the score on canvas also updates 
            Label(self.window, text ="Player 1 Score: " + str(self.Playersum1), bg="black", fg="white", 
                font=("Comic Sans MS", 25)).place(x = 20, y = 40)  
            Label(self.window, text ="Player 2 Score: " + str(self.Playersum2), bg="black", fg="white", 
                font=("Comic Sans MS", 25)).place(x = 1050,y = 40)  
        
        # After finishing the game, winner will be declared
        self.calculateWinner(self.Playersum1, self.Playersum2)
    
    
    # Find who win the game
    def calculateWinner(self, player1Score, player2Score):
        # Check if player score is 89, means player placed all pieces on board and gain additional +15 points as bonus.
        if player1Score == 89:
            player1Score += 15
        elif player2Score == 89:
            player2Score += 15
        
        # Checking if player score are equal means tie between them
        if player1Score == player2Score:
            print("GAME TIE!")
        elif player1Score > player2Score:
            if player1Score == 89:
                print("Player 1 has placed all the moves on the board, so awarded with additional +15 points as bonus.")
            print("Player 1 won the game!")
        elif player2Score > player1Score:
            if player2Score == 89:
                print("Player 1 has placed all the moves on the board, so awarded with additional +15 points as bonus.")
            print("Player 2 won the game!")    
        
            
    # Create game board on canvas
    def create_board(self, board):
        boardSize = BoardConfiguration().board_size
        i = 0
        j = 0
        
        while i < boardSize:
            j = 0
            while j < boardSize:
                x0 = BoardConfiguration().upper_x + (j * BoardConfiguration().square_tile_size)
                y0 = BoardConfiguration().upper_y + (i * BoardConfiguration().square_tile_size) + 11
                x1 = BoardConfiguration().upper_x + ((j+1)*BoardConfiguration().square_tile_size)
                y1 = BoardConfiguration().upper_y + ((i+1)*BoardConfiguration().square_tile_size)+11
                
                # Check if square tile on board is filled or empty
                if board[i][j] == -1:
                    # if square tile on board is empty then show the white color
                    fill_color = 'white'
                else:
                    # if the square tile on board is filled then show player respective color
                    if board[i][j] == 'green':
                        fill_color = 'green'
                    else:
                        fill_color = 'yellow'
                        
                # Create the square tiles of board as rectangle on the canvas
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color)
                
                j+=1
            i+=1
        
    # Function to place player pieces on canvas
    def canvas_player_pieces(self, player, opening, coordinates, upperX, upperY):
        max_x_values = {'yellow': BoardConfiguration().Canvas_Width - 40, 'green': BoardConfiguration().Canvas_Width - 1050}
        
        upperX = upperX + (10 + (len(coordinates) * 10))
        if upperX > max_x_values.get(player, BoardConfiguration().Canvas_Width):
            upperX = opening
            upperY = upperY + (40 + (len(coordinates) * 10))

        return upperX, upperY
    
    # Function to show player pieces on the canvas
    def show_pieces(self, player, pl):
        player_configurations = {
            "green": (PiecesConfiguration().topX_Player1, PiecesConfiguration().topY_Player1),
            "yellow": (PiecesConfiguration().topX_Player2, PiecesConfiguration().topY_Player2)
        }

        self.topX, self.topY = player_configurations[player]

        opening = self.topX
        
        for piece_name, piece_info in pl:
            main_coordinates = piece_info['coordinates']
            self.draw_piece(player, piece_name, main_coordinates, opening)

            if piece_info['isRotate']:
                rotation_coordinates = piece_info['rotation_coordinates']
                self.draw_rotated_pieces(player, piece_name, rotation_coordinates, opening)

            if piece_info['isMirror']:
                flip_coordinates = piece_info['flip_coordinates']
                flip_rotation_coordinates = piece_info['flip_rotation_coordinates']
                self.draw_flip_pieces(player, piece_name, flip_coordinates, flip_rotation_coordinates, opening)
                
            self.piece_label = 'A'

    # Function to draw player piece on the canvas
    def draw_piece(self, player, piece_name, coordinates, opening):
        for row in coordinates:
            self.draw_square_tiles(player, row)
            self.show_piece_label(piece_name)
        self.topX, self.topY = self.canvas_player_pieces(player, opening, coordinates, self.topX, self.topY)
        self.piece_label = chr(ord(self.piece_label[0]) + 1)

    # Function to draw rotated orientation of pieces on the canvas
    def draw_rotated_pieces(self, player, piece_name, rotation_coordinates, opening):
        for rotated_coordinates in range(0, len(rotation_coordinates)):
            self.draw_piece(player, piece_name, rotation_coordinates[rotated_coordinates], opening)
    
    # Function to draw flip orientation of pieces on the canvas
    def draw_flip_pieces(self, player, piece_name, flip_coordinates, flip_rotation_coordinates, opening):
        self.draw_piece(player, piece_name, flip_coordinates, opening) 
        for flip_rotated_coordinates in range(0, len(flip_rotation_coordinates)):
            self.draw_piece(player, piece_name, flip_rotation_coordinates[flip_rotated_coordinates], opening)
    
    # Function to draw pieces as rectangles representing player pieces on the canvas
    def draw_square_tiles(self, player, row):    
        self.canvas.create_rectangle(self.topX + (row[1] * 11), self.topY + (row[0]*11) + 11,
                                    self.topX + ((row[1]+1) * 11), self.topY + ((row[0]+1) * 11) + 11, fill=player)
   
    # Function to draw labels for player pieces on the canvas
    def show_piece_label(self,piece_name):        
        self.canvas.create_text(self.topX + 10, self.topY + 68, text=piece_name[:2] + self.piece_label, font="bold", fill="white")


# Main class for starting the game
if __name__ == "__main__":
    BlokusGame()