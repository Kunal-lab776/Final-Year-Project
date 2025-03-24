import tkinter as tk
import copy
from tkinter import *
import time

INFINITY = 1.e400
MIN_MAX_LEVELS = 2
maxcalls = 0
mincalls = 0
TOTAL_TILES = 89

class BlokusGame:
    def __init__(self):
        
        #Label(self.window, text = "Blokus Game", bg="black", fg="white", font=("Comic Sans MS", 25)).place(x = 610,y = 20)  
       
        self.board_size = 14
        self.cell_size = 30
        self.top_x = 485
        self.top_y = 155

        self.board = [[0] * self.board_size for _ in range(self.board_size)]
       
        self.pieces_specification = { 
            '1': { 'matrix': [[1]],
            'reflection': '0',
            'rotation': '0',
            'matrix_coordinates': [(0,0)], 
            },
            '2': { 'matrix': [[1,1]],
            'reflection': '0',
            'rotation': '1',
            'matrix_coordinates': [(0,0), (0,1)], 
            'rotation_matrix': [((0, 0), (1, 0))],
            },
            '3line': { 'matrix': [[1,1,1]],
            'reflection': '0',
            'rotation': '1',
            'matrix_coordinates': [(0, 0), (0, 1), (0, 2)], 
            'rotation_matrix': [((0, 0), (1, 0), (2, 0))],
            },
            '3v': { 'matrix': [[1,1],[0,1]],
            'reflection': '0',
            'rotation': '1',
            'matrix_coordinates': [(0, 0), (0, 1), (1, 1)], 
            'rotation_matrix': [((0, 0), (1, 0), (0, 1)), ((1, 0), (0, 1), (1, 1)), ((0, 0), (1, 0), (1, 1))],
            },
            '4line': { 'matrix': [[1,1,1,1]],
            'reflection': '0',
            'rotation': '1',
            'matrix_coordinates': [(0, 0), (0, 1), (0, 2), (0,3)], 
            'rotation_matrix': [((0, 0), (1, 0), (2, 0), (3, 0))],
            },
            '4el': { 'matrix': [[1,1,1],[1,0,0]],
            'reflec_cover': [[1,1,1],[0,0,1]],
            'reflection_matrix': [(0,0), (0,1), (0,2), (1,2)],
            'reflection': '1',
            'rotation': '1',
            'matrix_coordinates': [(0, 0), (1, 0), (0, 1), (0,2)], 
            'rotation_matrix': [((1, 0), (1, 1), (0, 2), (1, 2)), ((0, 0), (1, 0), (2, 0), (2, 1)), ((0, 0), (0, 1), (1, 1), (2, 1))],
            'reflection_rotation_matrix': [((0, 0), (1, 0), (1, 1), (1, 2)), ((2, 0), (0, 1), (1, 1), (2, 1)), ((0, 0), (1, 0), (2, 0), (0, 1))],
            },
            '4tee': { 'matrix': [[1,1,1],[0,1,0]],
            'reflection': '0',
            'rotation': '1',
            'matrix_coordinates': [(0, 0), (0, 1), (1, 1), (0,2)], 
            'rotation_matrix': [((1, 0), (0, 1), (1, 1), (1, 2)), ((1, 0), (0, 1), (1, 1), (2, 1)), ((0, 0), (1, 0), (2, 0), (1, 1))],
            },
            '4sq': { 'matrix': [[1,1],[1,1]],
            'reflection': '0',
            'rotation': '0',
            'matrix_coordinates': [(0, 0), (1, 0), (0, 1), (1,1)], 
            },
            '4z': { 'matrix': [[1,1,0],[0,1,1]],
            'reflec_cover': [[0,1,1],[1,1,0]],
            'reflection_matrix': [(1, 0), (0, 1), (1, 1), (0, 2)],
            'reflection': '1',
            'rotation': '1',
            'matrix_coordinates': [(0,0), (0,1), (1,1), (1,2)], 
            'rotation_matrix': [((1, 0), (2, 0), (0, 1), (1, 1))],
            'reflection_rotation_matrix': [((0, 0), (1, 0), (1, 1), (2, 1))],
            },
            '5n': { 'matrix': [[1,1,1,1,1]],
            'reflection': '0',
            'rotation': '1',
            'matrix_coordinates': [(0,0), (0,1), (0,2), (0,3), (0,4)], 
            'rotation_matrix': [((0, 0), (1, 0), (2, 0), (3, 0), (4, 0))],
            },
            '5el': { 'matrix': [[1,1,1],[1,1,0]],
            'reflec_cover': [[1,1,1],[0,1,1]],
            'reflection_matrix': [(0, 0), (0, 1), (1, 1), (0, 2), (1, 2)],
            'reflection': '1',
            'rotation': '1',
            'matrix_coordinates': [(0,0), (1,0), (0,1), (1,1), (0,2)], 
            'rotation_matrix': [((0, 0), (1, 0), (0, 1), (1, 1), (2, 1)), ((1, 0), (0, 1), (1, 1), (0, 2), (1, 2)), ((0, 0), (1, 0), (2, 0), (1, 1), (2, 1))],
            'reflection_rotation_matrix': [((0, 0), (1, 0), (2, 0), (0, 1), (1, 1)), ((0, 0), (1, 0), (0, 1), (1, 1), (1, 2)), ((1, 0), (2, 0), (0, 1), (1, 1), (2, 1))],
            },
            '5z': { 'matrix': [[1,1,0,0],[0,1,1,1]],
            'reflec_cover': [[0,0,1,1],[1,1,1,0]],
            'reflection_matrix': [(1, 0), (1, 1), (0, 2), (1, 2), (0, 3)],
            'reflection': '1',
            'rotation': '1',
            'matrix_coordinates': [(0,0), (0,1), (1,1), (1,2), (1,3)], 
            'rotation_matrix': [((1, 0), (2, 0), (3, 0), (0, 1), (1, 1)), ((0, 0), (0, 1), (0, 2), (1, 2), (1, 3)), ((2, 0), (3, 0), (0, 1), (1, 1), (2, 1))],
            'reflection_rotation_matrix': [((0, 0), (1, 0), (2, 0), (2, 1), (3, 1)), ((1, 0), (0, 1), (1, 1), (0, 2), (0, 3)), ((0, 0), (1, 0), (1, 1), (2, 1), (3, 1))],
            },
            '5l': { 'matrix': [[1,1,1,1],[1,0,0,0]],
            'reflec_cover': [[1,1,1,1],[0,0,0,1]],
            'reflection_matrix': [(0, 0), (0, 1), (0, 2), (0, 3), (1, 3)],
            'reflection': '1',
            'rotation': '1',
            'matrix_coordinates': [(0,0), (1,0), (0,1), (0,2), (0,3)], 
            'rotation_matrix': [((1, 0), (1, 1), (1, 2), (0, 3), (1, 3)), ((0, 0), (1, 0), (2, 0), (3, 0), (3, 1)), ((0, 0), (0, 1), (1, 1), (2, 1), (3, 1))],
            'reflection_rotation_matrix': [((3, 0), (0, 1), (1, 1), (2, 1), (3, 1)), ((0, 0), (1, 0), (2, 0), (3, 0), (0, 1)), ((0, 0), (1, 0), (1, 1), (1, 2), (1, 3))],
            },
            '5u': { 'matrix': [[1,0,1],[1,1,1]],
            'reflection': '0',
            'rotation': '1',
            'matrix_coordinates': [(0,0), (1,0), (1,1), (0,2), (1,2)], 
            'rotation_matrix': [((0, 0), (1, 0), (0, 1), (0, 2), (1, 2)), ((0, 0), (2, 0), (0, 1), (1, 1), (2, 1)), ((0, 0), (1, 0), (2, 0), (0, 1), (2, 1))],
            },  
            '5t': { 'matrix': [[1,1,1,1],[0,1,0,0]],
            'reflec_cover': [[1,1,1,1],[0,0,1,0]],
            'reflection_matrix': [(0, 0), (0, 1), (0, 2), (1, 2), (0, 3)],
            'reflection': '1',
            'rotation': '1',
            'matrix_coordinates': [(0,0), (0,1), (1,1), (0,2), (0,3)], 
            'rotation_matrix': [((0, 0), (1, 0), (2, 0), (3, 0), (2, 1)), ((1, 0), (1, 1), (0, 2), (1, 2), (1, 3)), ((1, 0), (0, 1), (1, 1), (2, 1), (3, 1))],
            'reflection_rotation_matrix': [((2, 0), (0, 1), (1, 1), (2, 1), (3, 1)), ((1, 0), (0, 1), (1, 1), (1, 2), (1, 3)), ((0, 0), (1, 0), (2, 0), (3, 0), (1, 1))],
            },
            '5T': { 'matrix': [[1,1,1],[0,1,0],[0,1,0]],
            'reflection': '0',
            'rotation': '1',
            'matrix_coordinates': [(0,0), (0,1), (1,1), (2,1), (0,2)], 
            'rotation_matrix': [((2, 0), (0, 1), (1, 1), (2, 1), (2, 2)), ((1, 0), (1, 1), (0, 2), (1, 2), (2, 2)), ((0, 0), (1, 0), (2, 0), (1, 1), (1, 2))],
            },
            '5v': { 'matrix': [[1,0,0],[1,0,0],[1,1,1]],
            'reflection': '0',
            'rotation': '1',
            'matrix_coordinates': [(0,0), (1,0), (2,0), (2,1), (2,2)], 
            'rotation_matrix': [((0, 0), (0, 1), (0, 2), (1, 2), (2, 2)), ((0, 0), (1, 0), (2, 0), (0, 1), (0, 2)), ((2, 0), (2, 1), (0, 2), (1, 2), (2, 2))],
            },
            '5w': { 'matrix': [[1,0,0],[1,1,0],[0,1,1]],
            'reflection': '0',
            'rotation': '1',
            'matrix_coordinates': [(0,0), (1,0), (1,1), (2,1), (2,2)], 
            'rotation_matrix': [((2, 0), (1, 1), (2, 1), (0, 2), (1, 2)), ((1, 0), (2, 0), (0, 1), (1, 1), (0, 2)), ((0, 0), (0, 1), (1, 1), (1, 2), (2, 2))],
            },
            '5s': { 'matrix': [[1,1,0],[0,1,0],[0,1,1]],
            'reflec_cover': [[0,1,1],[0,1,0],[1,1,0]],
            'reflection_matrix': [(2, 0), (0, 1), (1, 1), (2, 1), (0, 2)],
            'reflection': '1',
            'rotation': '1',    
            'matrix_coordinates': [(0,0), (0,1), (1,1), (2,1), (2,2)], 
            'rotation_matrix': [((1, 0), (2, 0), (1, 1), (0, 2), (1, 2))],
            'reflection_rotation_matrix': [((0, 0), (1, 0), (1, 1), (1, 2), (2, 2))],
            },
            '5?': { 'matrix': [[1,1,0],[0,1,1],[0,1,0]],
            'reflec_cover': [[0,1,1],[1,1,0],[0,1,0]],
            'reflection_matrix': [(1, 0), (0, 1), (1, 1), (2, 1), (0, 2)],
            'reflection': '1',
            'rotation': '1',
            'matrix_coordinates': [(0,0), (0,1), (1,1), (2,1), (1,2)],
            'rotation_matrix': [((1, 0), (1, 1), (2, 1), (0, 2), (1, 2)), ((1, 0), (2, 0), (0, 1), (1, 1), (1, 2)), ((1, 0), (0, 1), (1, 1), (2, 1), (2, 2))],
            'reflection_rotation_matrix': [((1, 0), (0, 1), (1, 1), (1, 2), (2, 2)), ((0, 0), (1, 0), (1, 1), (2, 1), (1, 2)), ((2, 0), (0, 1), (1, 1), (2, 1), (1, 2))],
            },
            '5cross': { 'matrix': [[0,1,0],[1,1,1],[0,1,0]],
            'reflection': '0',
            'rotation': '0',
            'matrix_coordinates': [(1,0), (0,1), (1,1), (2,1), (1,2)], 
            }
        }
        self.humanPlayer = copy.deepcopy(self.pieces_specification)
        self.artificialPlayerG = copy.deepcopy(self.pieces_specification) 
        
        self.move_number = 1
        
        # self.players = int(input("How many players you want to add?"))
        # while (self.players != 1 and self.players != 2) or (self.players == 0 or self.players == ""):
        #     self.players = int(input("How many players you want to add?"))
            
        self.window = tk.Tk()
        self.window.title("Blokus Game")

        self.BOARD_WIDTH = 1500
        self.BOARD_HEIGHT = 800
        
        frame=Frame(self.window)
        frame.pack(expand=True, fill=BOTH)
        self.canvas=Canvas(frame,width=self.BOARD_WIDTH,height=self.BOARD_HEIGHT,scrollregion=(0,0,1800,1800))
        vbar=Scrollbar(frame,orient=VERTICAL)
        vbar.pack(side=RIGHT,fill=Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(width=self.BOARD_WIDTH,height=self.BOARD_HEIGHT, background="black")
        self.canvas.config(yscrollcommand=vbar.set)
        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)
        
        self.state = ["green", self.board, list(self.piece_list("yellow").keys()), list(self.piece_list("green").keys()),self.move_number]
        
        self.start()
            
        self.window.mainloop()
    
    
    
    def human_turn(self, state):
        while True:
            try:
                player_input = str(input("Your move? ")) 
                try:
                    if player_input == "1A" or player_input == "2A" or player_input == "2B":
                        if player_input[0] in list(self.piece_list(player).keys()):     
                            coord_xInput = int(input("X-coordinate? "))
                            coord_yInput = int(input("Y-coordinate? "))
                            while ((coord_xInput < 0 or coord_xInput > 13) or (coord_yInput < 0 or coord_yInput > 13)):
                                coord_xInput = int(input("X-coordinate? "))
                                coord_yInput = int(input("Y-coordinate? "))
                            try:
                                board = self.choose_and_place_piece(player_input, coord_xInput, coord_yInput, state)
                                if board != state[1]:
                                    break
                            except IndexError: 
                                print("TRY AGAIN!")
                    elif player_input == "pass":
                        player = "green"
                        board = state[1]
                        finish2 = True
                        break
                    else:
                        if player_input[:2] in list(self.piece_list(player).keys()):     
                            coord_xInput = int(input("X-coordinate? "))
                            coord_yInput = int(input("Y-coordinate? "))
                            while ((coord_xInput < 0 or coord_xInput > 13) or (coord_yInput < 0 or coord_yInput > 13)):
                                coord_xInput = int(input("X-coordinate? "))
                                coord_yInput = int(input("Y-coordinate? "))
                            try:
                                board = self.choose_and_place_piece(player_input, coord_xInput, coord_yInput, state)
                                if board != state[1]:
                                    break
                            except IndexError: 
                                print("TRY AGAIN!")
                except:
                    print("Invalid Values")
            except:
                print("not a valid move! Try again")
        
        return board, player_input 
            
        
    def start(self):
        finish1 = False
        finish2 = False
        Playersum2 = 0
        Playersum3 = 0
        pieces_to_remove = {"5c": "5cross", "1A": "1", "2A": "2", "2B": "2", "5e": "5el", "4s": "4sq", "4t": "4tee", "4e": "4el", "4l": "4line", "3l": "3line"}
        
        while True:
            self.create_board(self.state[1])
            print('\nPlayer to move: ', self.state[0], "\n" )
            if self.move_number % 2 == 0:
                board, move = board, ''
                if board == self.state[1] and finish1:
                    break
                elif board == self.state[1]:
                    finish2 = True
                else:
                    piece_input = move[:2]
                    if piece_input in pieces_to_remove:
                        self.humanPlayer.pop(pieces_to_remove[piece_input])
                    else:
                        self.humanPlayer.pop(piece_input)
                        
                    Playersum2 += int(move[0])
                    
                player = "green"
                
            elif self.move_number % 2 == 1:
                board,move = self.artificialPlayerTurn(self.state[0], self.state[1], self.state[2], self.state[3], self.state[4])
                if board == self.state[1] and finish2:
                    break
                elif board == self.state[1]:
                    finish1 = True
                else:
                    if move in pieces_to_remove:
                        self.artificialPlayerG.pop(pieces_to_remove[move])
                    else:
                        self.artificialPlayerG.pop(move)
                    Playersum3 += int(move[0])
                   
                player = "yellow"
            
            self.move_number += 1
            self.state = [player, board, list(self.piece_list("yellow").keys()), list(self.piece_list("green").keys()), self.move_number]
            
            #Label(self.window, text ="Player 1 Score: " + str(Playersum1), bg="black", fg="white", font=("Comic Sans MS", 25)).place(x = 20, y = 550)  
            #Label(self.window, text ="Player 2 Score: " + str(Playersum2), bg="black", fg="white", font=("Comic Sans MS", 25)).place(x = 1050,y = 550) 
            #Label(self.window, text ="Player 3 Score: " + str(Playersum3), bg="black", fg="white", font=("Comic Sans MS", 25)).place(x = 590,y = 800)  
            #Label(self.window, text ="Player 4 Score: " + str(Playersum3), bg="black", fg="white", font=("Comic Sans MS", 25)).place(x = 590,y = 90) 
        
        print("win")
        
        
    def piece_list(self, player):
        piece_list1 = {}
        
        player_pieces = {"yellow": self.humanPlayer, "green": self.artificialPlayerG, "N": self.pieces_specification}

        if player in player_pieces:
            v = player_pieces[player].items()
        else:
            raise ValueError("Invalid player color")

        for piece_name, piece_info in v:
            matrix = piece_info['matrix_coordinates']
            if piece_name in piece_list1:
                if isinstance(piece_list1[piece_name], list):
                    piece_list1[piece_name[:2]].extend([matrix])
            else:
                piece_list1[piece_name[:2]] = [matrix]
            
            if piece_info['rotation'] == '1':
                rotation_matrix = piece_info['rotation_matrix']
                piece_list1[piece_name[:2]].extend(rotation_matrix)
                
            if piece_info['reflection'] == '1':
                reflection_matrix = piece_info['reflection_matrix']
                reflection_rotation_matrix = piece_info['reflection_rotation_matrix']
                piece_list1[piece_name[:2]].extend([reflection_matrix])
                piece_list1[piece_name[:2]].extend(reflection_rotation_matrix)
        
        return piece_list1

    def create_board(self, state):
        self.canvas.delete("all")
        for i, row in enumerate(state):
            for j, cell in enumerate(row):
                fill_color = 'white' if cell == 0 else "green" if cell == "green" else "red" if cell == "red" else "yellow" if cell == "yellow" else "blue"
                self.canvas.create_rectangle(self.top_x + (j * self.cell_size), self.top_y + (i * self.cell_size) + 10, self.top_x + ((j + 1) * self.cell_size), self.top_y + ((i + 1) * self.cell_size) + 10, fill=fill_color)
       
        self.display_pieces('yellow', 1050, 100, self.humanPlayer.items())
        self.display_pieces('green', 20, 100, self.artificialPlayerG.items())

    def canvas_player_pieces(self, player, initial, matrix, topleft_x, topleft_y):
        max_x_values = {'yellow': self.BOARD_WIDTH - 120, 'green': self.BOARD_WIDTH - 1150, 'red': self.BOARD_WIDTH - 500, 'blue': self.BOARD_WIDTH - 150}
        
        topleft_x += (10 + (len(matrix) * 10))
        if topleft_x > max_x_values.get(player, self.BOARD_WIDTH):
            topleft_x = initial
            topleft_y += (30 + (len(matrix) * 10))

        return topleft_x, topleft_y

    
    def display_pieces(self, player, topleft_x, topleft_y, pl):
        initial = topleft_x
        st = 'A'
        for piece_name, piece_info in pl:
            matrix = piece_info['matrix_coordinates']
            for row in matrix:
                self.canvas.create_rectangle(topleft_x + (row[1] * 10), topleft_y + (row[0]*10)+10, topleft_x + ((row[1]+1)*10), topleft_y + ((row[0]+1)*10)+10, fill=player)
                self.canvas.create_text(topleft_x + 10,topleft_y+60, text=piece_name[:2] + st, font="bold", fill="white")  
            i = ord(st[0])
            i += 1
            st = chr(i)            
            topleft_x, topleft_y = self.canvas_player_pieces(player, initial, matrix, topleft_x, topleft_y)
            
            if piece_info['rotation'] == '1':
                rotation_matrix = piece_info['rotation_matrix']
                for col in range(0, len(rotation_matrix)):
                    for row in rotation_matrix[col]:
                        self.canvas.create_rectangle(topleft_x + (row[1] * 10), topleft_y + (row[0]*10)+10, topleft_x + ((row[1]+1)*10), topleft_y + ((row[0]+1)*10)+10, fill=player)
                        self.canvas.create_text(topleft_x + 10,topleft_y+60, text=piece_name[:2] + st,font="bold", fill="white")
                    i = ord(st[0])
                    i += 1
                    st = chr(i)
                    topleft_x, topleft_y = self.canvas_player_pieces(player, initial, matrix, topleft_x, topleft_y)

            if piece_info['reflection'] == '1':
                
                reflection_matrix = piece_info['reflection_matrix']
                for row in reflection_matrix:
                    self.canvas.create_rectangle(topleft_x + (row[1] * 10), topleft_y + (row[0]*10)+10, topleft_x + ((row[1]+1)*10), topleft_y + ((row[0]+1)*10)+10, fill=player)
                    self.canvas.create_text(topleft_x + 10,topleft_y+60, text=piece_name[:2] + st,font="bold", fill="white")
                i = ord(st[0])
                i += 1
                st = chr(i)
                topleft_x, topleft_y = self.canvas_player_pieces(player, initial, matrix, topleft_x, topleft_y)
                
                reflection_rotation_matrix = piece_info['reflection_rotation_matrix']
                for col in range(0, len(reflection_rotation_matrix)):
                    for row in reflection_rotation_matrix[col]:
                        self.canvas.create_rectangle(topleft_x + (row[1] * 10), topleft_y + (row[0]*10)+10, topleft_x + ((row[1]+1)*10), topleft_y + ((row[0]+1)*10)+10, fill=player)
                        self.canvas.create_text(topleft_x + 10,topleft_y+60, text=piece_name[:2] + st ,font="bold", fill="white")
                    i = ord(st[0])
                    i += 1
                    st = chr(i)
                    topleft_x, topleft_y = self.canvas_player_pieces(player, initial, matrix, topleft_x, topleft_y)
            st = 'A'
            
        
    def choose_and_place_piece(self, piece_name, row, col, state):
        # Dictionary mapping piece letters to their corresponding index
        dic1 = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7}
        
        # Extracting necessary information from the game state
        player = state[0]
        board = state[1]
        move_number = state[4]
        
        # Creating a deepcopy of the board to avoid mutating the original state
        newboard = copy.deepcopy(board)
        
        # Flags for move validation
        initial = False
        valid = False
        
        # Getting corner and edge positions on the board
        corners, edges = self.get_all_corners_edges(board, player)
        
        # Extracting coordinates for the current piece
        if piece_name in ["1A", "2A", "2B"]:
            pieces = self.piece_list(player)[piece_name[0]]
            c = pieces[dic1.get(piece_name[1])]
        else:
            pieces = self.piece_list(player)[piece_name[:2]]
            c = pieces[dic1.get(piece_name[2])]
        
        # Iterating over the coordinates of the current piece
        for coord in c:
            y = row + coord[0]
            x = col + coord[1]
            
            # Checking if the placement is valid
            if newboard[y][x] != 0:
                print("FAIL. OVERPLACING")
                return board
            
            elif ((move_number <= 2 and (y, x) == (0, 13) or (y, x) == (13, 0))) or move_number > 2:
                initial = True  # The move is one of the first four or it's after the initial phase
                
            if (move_number > 2 and (y, x) in corners) or move_number <= 2:
                valid = True  # The move is valid if it's within corners after the initial phase or within the first four moves
            elif (y, x) in edges:
                print("FAIL. CAN'T PLACE ON EDGE")
                return board
            newboard[y][x] = player  # Placing the piece on the board
            
        # Checking if the placement meets both initial and valid conditions
        if initial and valid:
            return newboard
        else:
            print("FAIL. PIECE NOT PLACED CORRECTLY ON CORNER")
            return board

        
    def get_all_corners_edges(self, board, player):
        corners = set()
        edges = set()

        # Function to check if a given position is an edge of a corner
        def is_edge_of_corner(y, x, board, player):
            # Check if the position meets the conditions of an edge of a corner
            if (((y > 0 and board[y - 1][x] != player) or y == 0) and  # top
                    ((x < self.board_size - 1 and board[y][x + 1] != player) or x == self.board_size - 1) and  # right
                    ((y < self.board_size - 1 and board[y + 1][x] != player) or y == self.board_size - 1) and  # bottom
                    ((x > 0 and board[y][x - 1] != player) or x == 0)):  # left
                return True
            return False

        # Iterate through each cell of the board
        for y in range(self.board_size):
            for x in range(self.board_size):
                # Check if the cell belongs to the player
                if board[y][x] == player:
                    # Check adjacent cells to determine edges and corners
                    if y > 0 and board[y - 1][x] == 0:
                        edges.add((y - 1, x))  # top edge
                        # Check top right and top left corners
                        if (x < self.board_size - 1 and board[y - 1][x + 1] == 0 and is_edge_of_corner(y - 1, x + 1, board, player)):
                            corners.add((y - 1, x + 1))
                        if (x > 0 and board[y - 1][x - 1] == 0 and is_edge_of_corner(y - 1, x - 1, board, player)):
                            corners.add((y - 1, x - 1))
                    if y < self.board_size - 1 and board[y + 1][x] == 0:
                        edges.add((y + 1, x))  # bottom edge
                        # Check bottom right and bottom left corners
                        if (x < self.board_size - 1 and board[y + 1][x + 1] == 0 and is_edge_of_corner(y + 1, x + 1, board, player)):
                            corners.add((y + 1, x + 1))
                        if (x > 0 and board[y + 1][x - 1] == 0 and is_edge_of_corner(y + 1, x - 1, board, player)):
                            corners.add((y + 1, x - 1))
                    if x > 0 and board[y][x - 1] == 0:  # left edge
                        edges.add((y, x - 1))
                    if x < self.board_size - 1 and board[y][x + 1] == 0:  # right edge
                        edges.add((y, x + 1))
       
        return list(corners), list(edges)

    
    def check_orientation_with_corners(self, board, board_open_corners, board_edges, orientations, position, piece ):
        dic1 = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H'}
        moves = []
        
        # get all the corner for a specific orientation of a tile
        def tile_corners(coords ):
            corners = []
            for i in coords:
                y = i[0]
                x = i[1]
                if (((y+1,x) not in coords or (y-1,x) not in coords) and ((y,x-1) not in coords or (y,x+1) not in coords)):
                    corners.append(i)
            return corners
        
        tilecorners = tile_corners(orientations[position])
        
        for corner in board_open_corners:
            Y,X = corner[0], corner[1]
            for t in tilecorners:
                # get all coords of tile except the corner tuple
                c = []
                for n in orientations[position]:
                    if not (n[0] == t[0] and n[1] == t[1]):
                        c.append(n)
                        
                valid = True
                for r in c:
                    diffY = Y+(r[0] - t[0])
                    diffX = X+(r[1] - t[1])
                    # check whether this orientation is a valid move on the board
                    if not ( diffY < self.board_size and diffY > -1 and diffX > -1 and diffX < self.board_size and board[diffY][diffX] == 0 and (diffY,diffX) not in board_edges):
                        valid = False
                        break
                # add to the list of possible moves
                if valid:
                    move = (Y-t[0],X-t[1],dic1.get(position+1),piece)
                    moves.append(move)
        return moves
    
    def possible_moves(self, player, board, humanpiece, artificialpieceG, moveno):
        def get_sized_pieces(pieces, size_pieces):
            return [piece for piece in pieces if (piece == 1 or piece == 2) and int(piece) == size_pieces or int(piece[:1]) == size_pieces]

        # Function to generate all orientations of a piece
        def all_orientations(p):
            piece_mapping = {"5el": "5e", "5cross": "5c", "4line": "4l", "3line": "3l", "4el": "4e", "4tee": "4t", "4sq": "4s"}
            p = piece_mapping.get(p, p)
            return self.piece_list("N")[p]
        
        # Determine player's pieces based on color
        player_pieces = {"yellow": humanpiece, "green": artificialpieceG}.get(player, [])

        # Initialize moves list and sizes
        moves = []
        sizes = [5,4,3,2,1]
        board_edges = []
        
        # Determine open corners and edges based on move number
        if moveno in [1, 2]:
            if board[0][13] == 0:
                board_open_corners = [(0, 13)] 
            elif board[13][0] == 0:
                board_open_corners = [(13, 0)]
            
        else:
            board_open_corners, board_edges = self.get_all_corners_edges(board, player)
            
        i = 0
        while moves == [] and not i == len(sizes):
            sized_pieces = get_sized_pieces(player_pieces, sizes[i])
            for piece in sized_pieces:
                orientations = all_orientations(piece)
                for orientation in range(len(orientations)):
                    moves_each_orientation = self.check_orientation_with_corners(board, board_open_corners, board_edges, orientations, orientation, piece)
                    moves.extend(moves_each_orientation)
            i+=1
        return moves    
    
    def minimax_with_alpha_beta_pruning(self, stateplayer, board, humanpiece, artificialpieceG, moveno, player, max_or_min, no_of_levels, move, alpha, beta):
        global maxcalls, mincalls
        if max_or_min == 'min':
            mincalls += 1
        else:
            maxcalls += 1
        
        players = {"yellow": ["yellow", "green", humanpiece, artificialpieceG],
            "green": ["green", "yellow", artificialpieceG, humanpiece]
        }

        current_player, next_player, player_pieces1, other_player_pieces1 = players[stateplayer]

        new_pieces = copy.deepcopy(player_pieces1)
        newboard = self.choose_and_place_piece(move[3] + move[2], move[0], move[1], [stateplayer, board, humanpiece, artificialpieceG, moveno])
        new_pieces.remove(move[3])
        
        if no_of_levels-1 == 0:
            return self.heuristic(newboard, player)
        
        # Define a dictionary to map player colors to their corresponding piece lists
        piece_lists = {
            "yellow": [new_pieces, other_player_pieces1],
            "green": [other_player_pieces1, new_pieces]
        }
            
        if (max_or_min == 'min'):
            v = INFINITY 
        else:
            v = -INFINITY
        
        next_player_moves = self.possible_moves(next_player, newboard, piece_lists[current_player][0], piece_lists[current_player][1], moveno + 1)

        # if there are more levels than can be searched for current player, skip search of next player
        if next_player_moves == [] and no_of_levels > 2:
            player_pieces = {
                "yellow": [new_pieces, other_player_pieces1],
                "green": [other_player_pieces1, new_pieces]
            }
            return self.skip_turn(next_player, newboard, player_pieces[current_player][0], player_pieces[current_player][1], moveno + 2, player, no_of_levels - 1, max_or_min)
           
        # analyse each move
        for m in next_player_moves:
            if(max_or_min == 'min'):
                v = min(v, self.minimax_with_alpha_beta_pruning(next_player, newboard, piece_lists[current_player][0], piece_lists[current_player][1], moveno + 1, player, 'max', no_of_levels-1, m, alpha, beta))
                beta = min(beta, v)
                if beta <= alpha:
                    break
            else:
                v = max(v, self.minimax_with_alpha_beta_pruning(next_player, newboard, piece_lists[current_player][0], piece_lists[current_player][1], moveno + 1, player, 'min', no_of_levels-1, m, alpha, beta))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
                
        if next_player_moves == []:
            return self.heuristic(newboard, player)
        
        return v
    
    
    def artificialPlayerTurn(self, player, board, humanpiece, artificialpieceG, moveno):
        # Get possible moves for the computer player
        moves = self.possible_moves(player, board, humanpiece, artificialpieceG, moveno)
        
        # If there are no possible moves, return the current board
        if not moves:
            return board, ''
        
        # Initialize variables to track the best move and its heuristic value
        best_move_index = -1
        best_heuristic = -INFINITY
        move_index = 0
        
        # Iterate over each possible move
        for move in moves:
            # Calculate the heuristic value for the current move
            heuristic = self.minimax_with_alpha_beta_pruning(player, board, humanpiece, artificialpieceG, moveno, player, 'min', MIN_MAX_LEVELS, move, INFINITY, -INFINITY)
            
            # Update the best move if the current move has a higher heuristic value
            if heuristic > best_heuristic:
                best_move_index = move_index
                best_heuristic = heuristic
            
            move_index += 1
        
        # Retrieve the best move
        best_move = moves[best_move_index]
        
        # Place the piece on the board based on the best move
        new_board = self.choose_and_place_piece(best_move[3] + best_move[2], best_move[0], best_move[1], [player, board, humanpiece, artificialpieceG, moveno])
        
        return new_board, best_move[3]
    
    def heuristic(self, board, player):
        if player == "green":
            other_player = "yellow"
        else:
            other_player = "green"
            
        opponent_corners_count = self.get_all_corners_edges(board, player)[0]
        open_corners = self.get_all_corners_edges(board, other_player)[0]
        
        return (len(opponent_corners_count * 2)) - len(open_corners)

    def skip_turn(self, stateplayer, board, humanpiece, artificialpieceG, moveno, player, no_of_rounds, max_or_min, alpha, beta):
        global maxcalls, mincalls
        if (max_or_min == 'min'):
            mincalls += 1
        else:
            maxcalls += 1
        moves = self.possible_moves(stateplayer, board, humanpiece, artificialpieceG, moveno)
        
        if moves == []:
            return self.heuristic(board, player)
        
        if (max_or_min == 'min'):
            v = -INFINITY
        else:
            v = INFINITY
            
        for m in moves:
            if(max_or_min == 'min'):
                v = min(v, self.minimax_with_alpha_beta_pruning(stateplayer, board, humanpiece, artificialpieceG, moveno, player, 'min', no_of_rounds-1, m, alpha, beta))
                beta = min(beta, v)
                if beta <= alpha:
                    break
            else:
                v = max(v, self.minimax_with_alpha_beta_pruning(stateplayer, board, humanpiece, artificialpieceG, moveno, player, 'max', no_of_rounds-1, m, alpha, beta))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
        return v
    
    
    # def calc_score_pieces(self, pieces):
    #     return sum(int(piece) if piece == 1 or piece == 2 else int(piece[0]) for piece in pieces)
    
    # def win(self, state):
    #     scores = [self.calc_score_pieces(state[i]) for i in range(2, 6)]
    #     adjusted_scores = [score if score != 0 else -15 for score in scores]
    #     winners = [i + 1 for i, score in enumerate(scores) if score == min(scores)]

    #     if len(winners) == 1:
    #         print(f'Player {winners[0]} has won the game.')
    #     else:
    #         print('The game is a tie!')

    #     print()
    #     print('Scores:')
    #     for i, score in enumerate(scores):
    #         print(f'Player {i + 1} = {TOTAL_TILES - adjusted_scores[i]}')


if __name__ == "__main__":
    BlokusGame()