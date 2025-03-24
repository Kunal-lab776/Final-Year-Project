# Importing necessary files and libraries
import Workable_Moves_Player as Workable_Moves_Player
import copy
from Pieces_Board_Configuration import PutPieceConfiguration, BoardConfiguration
import time
from Game_State import GameState



# Class for handling transposition operations
class TranspositionTable: 
    def __init__(self):
        # Initialize the transposition table as an empty dictionary
        self.table = {}
        
    # Function to look up a board hash exist or not in the transposition table    
    def look_for_key(self, board):
        # Generate hash value for the given board configuration and return the score if it exists in transposition table
        board_hash = hash(str(board))
        # return the values associated with hashed key, if present in table
        return self.table.get(board_hash)

    # Function to store board configuration in the transposition table
    def store(self, board, score): 
        # Calculating the hash of board configuration
        board_hash = hash(str(board))
        # Store the computed hash key and associated values in transposition table
        self.table[board_hash] = score



# Class of implemented IDDFS and minimax with alpha-beta pruning algorithm
class MinimaxAlgorithm:
    def __init__(self):
        # Initializing the temporary board because of not deletion of current main board 
        self.temporary_board = [[-1] * BoardConfiguration().board_size for _ in range(BoardConfiguration().board_size)]
        
        # Initializing the temporary pieces for the player because of not deletion of the main pieces of the current player
        self.temporary_pieces = []
        
        # Flag for searching of tree to be stop if time limit is reached
        self.stopSearching = False
        
        # Initializing the transposition table 
        self.table = TranspositionTable()   
        
   
    # Function for IDDFS which runs until the time limit is reached, and incrementing the depth as move searched
    def iterative_deepning_depth_first_search(self, node, timeLimit, ai_moves, player1, player2):
        # Note start time of program in milliseconds
        startTime = int(time.time()*1000)
        
        # End time until function needs to find the best move 
        endTime = startTime + timeLimit
        
        # Initializing depth limit to 1 
        depth = 1
        
        # Initializing the score to 0
        score = 0
        
        self.stopSearching = False

        # Main loop of function run until time limit exceed
        while True:
            # Calculating the current time in milliseconds at every instance after minimax algorithm conducted search and result the evaluation score in variable search result 
            currentTime = int(time.time()*1000)
            
            self.stopSearching = False
            
            # check if current time exceed the end time then break the function and return the last best score which is recorded in variable score
            if currentTime >= endTime:
                break
            else:
                # Perform minimax with alpha-beta pruning
                searchResult = self.minimax_with_alpha_beta_pruning(node, 'green', True, depth, ai_moves, 
                            float('-inf'), float('inf'), currentTime, endTime - currentTime, player1, player2)
                
                # Update the score if the searchResult have better score
                if searchResult > score:
                    score = searchResult  
                
                # Check if time limit exceed in minimax function
                if not self.stopSearching:
                    score = searchResult
            
            # depth increases iteratively
            depth += 1    
        
        # return the best score
        return score
        
    # Function exeucted when maximizing player have chance to play the game
    def max_player(self, movesForNextPlayer, new_node, player, depth, alpha, beta, startTime, timeLimit, player1, player2):
        # Initializing the Evaluation score with lowest score possible which is negative infinity
        Evaluation = float('-inf')

        i = 0
        # Iterate through all possible moves for the next player
        while i < len(movesForNextPlayer):
            # Calling the minimax with alpha-beta pruning for the next player (opponent, minimizing the score)
            result = self.minimax_with_alpha_beta_pruning(new_node, player, False, depth-1, movesForNextPlayer[i], alpha, beta, startTime, timeLimit, player1, player2)
            # Update Evaluation score with the maximum of current Evaluation and result
            Evaluation = max(Evaluation, result)
            # Update alpha with the maximum of alpha and Evaluation
            alpha = max(alpha, Evaluation)
            # Prune branches if beta is less than or equal to alpha
            if(beta <= alpha):
                break
            i+=1
            
        # Return the maximum Evaluation score found
        return Evaluation
    
    # Function executed when minimizing player have chance to play the game 
    def min_player(self, movesForNextPlayer, new_node, player, depth, alpha, beta, startTime, timeLimit, player1, player2):
        # Initializing the Evaluation score with highest score possible which is positive infinity
        Evaluation = float('inf')
        
        i = 0
        # Iterate through all possible moves for the next player
        while i < len(movesForNextPlayer):
            # Calling the minimax with alpha-beta pruning for the next player (AI player, maximizing the score)
            result = self.minimax_with_alpha_beta_pruning(new_node, player, True, depth-1, movesForNextPlayer[i], alpha, beta, startTime, timeLimit, player1, player2)
            # Update Evaluation score with the minimum of current Evaluation and result
            Evaluation = min(Evaluation, result)
            # Update beta with the minimum of beta and Evaluation
            beta = min(beta, Evaluation)
            # Prune branches if beta is less than or equal to alpha
            if(beta <= alpha):
                break
            i+=1
            
        # Return the maximum Evaluation score found
        return Evaluation
                
    
    # Function executing minimax with alpha-beta pruning
    def minimax_with_alpha_beta_pruning(self, node, player, maximizing_player, depth, available_pieces, alpha, beta, startTime, timeLimit, player1, player2):
        # The amount of time passed due to evaluating the moves or time for finding the optimal move
        elapsedTime = int(time.time() * 1000) - startTime
        
        # Check if the time limit has been reached
        if elapsedTime >= timeLimit:
            self.stopSearching = True
        
        # Lookup the transposition table for the current board state
        table_result = self.table.look_for_key(self.temporary_board)
        if table_result and table_result['depth'] >= depth:
            if table_result['flag'] == 'exact':
                return table_result['score']
            elif table_result['flag'] == 'lowerbound':
                alpha = max(alpha, table_result['score'])
            elif table_result['flag'] == 'upperbound':
                beta = min(beta, table_result['score'])
            if alpha >= beta:
                return table_result['score']
            
        # Initializing the next player based on current player playing the game
        another_player = "yellow" if player == "green" else "green"
        
        # Initializing the temporary pieces and board, so that cannot lose the actual board and pieces of the player
        if node.player == "green":
            player2piece = node.player2_pieces
            self.temporary_pieces = copy.deepcopy(node.player1_pieces)
            player1piece = self.temporary_pieces
        else:
            player1piece = node.player1_pieces
            self.temporary_pieces = copy.deepcopy(node.player2_pieces)
            player2piece = self.temporary_pieces
        
        # Putting the temporary piece on temporary board of current player
        self.temporary_board = PutPieceConfiguration(node.player).Put_Piece(
                            available_pieces.get("pieces"), available_pieces.get("coordinates")[0], 
                            available_pieces.get("coordinates")[1], node.board, node.step)
        
        # After placing the piece on the board, remove the placed piece from temperorary piece list
        self.temporary_pieces.remove(available_pieces.get("pieces")[:2])
        
        # if time limit reached or depth of minimax tree reached to 0, evaluate the terminal or leaf node of the minimax tree
        if self.stopSearching or depth == 0:
            score = self.evaluation_function(self.temporary_board, player, another_player)
            flag = 'exact'
            self.table.store(self.temporary_board, {'player': node.player, 'score': score, 'depth': depth, 'flag': flag, 
                            'piece': available_pieces.get("pieces"), 'coordinates': (available_pieces.get("coordinates")[0], available_pieces.get("coordinates")[1])})
            return score
        else:
            # Initializing the child node or state for next player 
            child_node = GameState(node.player, node.board, node.step, node.player1_pieces, node.player2_pieces).next_state(
                                                                                    self.temporary_board, player1piece, player2piece)
            
            # Generate legal or possible moves for the next player 
            movesForNextPlayer = Workable_Moves_Player.WorkableMovesPlayer(
                                child_node.player, child_node.board, child_node.player1_pieces, 
                                child_node.player2_pieces, child_node.step, player1, player2).movesForPlayer()
            
            
            # If there are no moves or avaliable pieces for the next player, then evaluate the move 
            if not movesForNextPlayer:
                score = self.evaluation_function(self.temporary_board, player, another_player)
                flag = 'exact'
                self.table.store(self.temporary_board, {'player': node.player, 'score': score, 'depth': depth, 'flag': flag, 
                        'piece': available_pieces.get("pieces"), 'coordinates': (available_pieces.get("coordinates")[0], available_pieces.get("coordinates")[1])})
                
                return score
            
            
            # Performing minimax recursively for the next player according to which player is playing next, meaning the maximizing player (AI Player) turn or minimizing player (Human Player) turn
            if maximizing_player:
                score = self.max_player(movesForNextPlayer, child_node, player, depth, alpha, beta, startTime, timeLimit, player1, player2)
                flag = 'exact' if score <= alpha else 'upperbound'
                alpha = max(alpha, score)  
            else:
                score = self.min_player(movesForNextPlayer, child_node, player, depth, alpha, beta, startTime, timeLimit, player1, player2)
                flag = 'exact' if score >= beta else 'lowerbound'
                beta = min(beta, score)
                
                
            # Store the board state and associated values in the transposition table
            self.table.store(self.temporary_board, {'player': node.player, 'score': score, 'depth': depth, 'flag': flag, 
                                'piece': available_pieces.get("pieces"), 'coordinates': (available_pieces.get("coordinates")[0], available_pieces.get("coordinates")[1])})
        
            # return the score
            return score

    def evaluation_function(self, board, player1, player2):
        # Current player area of influence calculated based on number of corners the piece have
        # if large piece is selected then the area of influence is higher meaning that large piece can cover most of the area on the board and have maximum corners
        # if small piece is selected then the area of influence is lower meaning that small piece can cover minimum area on the board and have minimum corners
        player_area_of_influence = PutPieceConfiguration(player1).corner(board)
        opponent_area_of_influence = PutPieceConfiguration(player2).corner(board)
    
        # Want to maximize the current player area of influence and decrease the opponent corner or area of influence
        return len(player_area_of_influence) - len(opponent_area_of_influence)