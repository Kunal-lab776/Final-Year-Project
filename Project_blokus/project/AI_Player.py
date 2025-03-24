# Importing necessary files and libraries
from Pieces_Board_Configuration import PutPieceConfiguration
import random
import Minimax_Implementation as Minimax_Implementation
import Workable_Moves_Player as Workable_Moves_Player


# Class representing AI or computer player implementation 
class AIPlayer:
    def __init__(self, choice):
        self.choice = choice  # Which strategy human want to play with AI 
        self.TimeLimit = 5000 # Time limit for the minimax algorithm and IDDFS to process, can be manually changed according to user
        
    # Implemented the random strategy for AI player
    def random_strategy(self, ai_available_pieces, node):  
        # Randomly select a move from AI possible move list
        move = random.choice(ai_available_pieces)
        
        # place piece on board 
        updatedBoard = PutPieceConfiguration(node.player).Put_Piece(move.get("pieces"), move.get("coordinates")[0], move.get("coordinates")[1], 
                    node.board, node.step)
        
        # returns the updated board with piece on board, and piece which is placed on the board
        return (updatedBoard, move.get("pieces"))
    
    # Implementation of minimax strategy for AI player
    def advance_strategy(self, ai_available_pieces, node, player1, player2):  
        # Initializing the best evaluation and best move to lowest possible values 
        best_evaluation = float('-inf')
        best_move = None
        
        # Iterating over each possible legal moves of player
        i = 0
        while i < len(ai_available_pieces): 
            # Calculating the search time limit for each move         
            TimeLimitForEachMove = ((self.TimeLimit - 1000)/len(ai_available_pieces))
            
            # Applying the minimax algorithm using IDDFS to find the evaluation of the current move  
            evaluation = Minimax_Implementation.MinimaxAlgorithm().iterative_deepning_depth_first_search(node, TimeLimitForEachMove, ai_available_pieces[i], player1, player2)    
            
            # If the evaluation is better than the previous best then update best evaluation value and move
            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_move = ai_available_pieces[i]
           
            i += 1
            
        # return the best_move
        return best_move
    
    # This function executes when AI turn comes 
    def AI_turn(self, node, player1, player2):
        # Calculate all legal or possible moves or pieces for the AI
        ai_available_pieces = Workable_Moves_Player.WorkableMovesPlayer(node.player, node.board, node.player1_pieces, 
                    node.player2_pieces, node.step, player1, player2).movesForPlayer()
        
        # if there are no avaialble move or pieces for AI then return current board
        if not ai_available_pieces:
                return node.board, ''
        
        # if choice written by user is 1 then executes the random strategy
        if self.choice == 1:
            # process the random strategy and return the best move and new board
            return self.random_strategy(ai_available_pieces, node)
        
        # if choice written by user is 2 then executes the minimax strategy
        elif self.choice == 2: 
            # process minimax strategy and find out best move from possible move list
            best_move = self.advance_strategy(ai_available_pieces, node, player1, player2)
            
            # After finding the best move, placing the move on board
            updatedBoard = PutPieceConfiguration(node.player).Put_Piece(best_move.get("pieces"), best_move.get("coordinates")[0], 
                        best_move.get("coordinates")[1], node.board, node.step)

            # return the updated board after piece is placed and piece which is choosen
            return updatedBoard, best_move.get("pieces")