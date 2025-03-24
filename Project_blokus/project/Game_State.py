# class game state to record the state of game when player played their pieces
class GameState:
    def __init__(self, player, board,  step, player1_pieces, player2_pieces):
        # game state initialized and includes with current player playing the game, board, player 1 available piece list, player 2 available piece list, step number 
        self.player = player
        self.board = board
        self.player1_pieces = player1_pieces
        self.player2_pieces = player2_pieces
        self.step = step
    
    # function to return the next state for next player; only used in minimax algorithm via recursive calls 
    def next_state(self, updated_board, new_player1_pieces, new_player2_pieces):
        # determining the next player according to current player
        next_player = "yellow" if self.player == "green" else "green"
        
        # returning the new game state with updated board, player 1 pieces, player 2 pieces, step number
        return GameState(next_player, updated_board, self.step + 1, new_player1_pieces, new_player2_pieces)
