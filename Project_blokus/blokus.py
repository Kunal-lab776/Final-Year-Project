from copy import deepcopy
import time
from settings import *
from library import *


maxcalls = 0
mincalls = 0

# get all the possible moves that the computer can do, given the state of the board
def possible_moves( state ):
    player = state[0]
    board = state[1]
    move_number = state[4]
    if player == 1:
        player_pieces = state[2]
    else:
        player_pieces = state[3]
    moves = []
    sizes = [5,4,3,2,1]
    
    # if it's first move of the computer then must place on either corner of the board
    if(move_number == 1 or move_number == 2):
        if board[0][0] == 0:
            board_open_corners = [(0,0)]
        else:
            board_open_corners = [(BOARD_SIZE-1, BOARD_SIZE-1)]
        board_edges = []
    else:
        (board_open_corners, board_edges) = get_all_corners_edges(board, player)
    
    i = 0
    while moves == [] and not i == len(sizes):
        sized_pieces = get_sized_pieces(player_pieces, sizes[i])
        for x in sized_pieces:
            p = all_orientations(x) # find all orientations of the piece  
            for u in range(len(p)):
                moves_each_orientation = check_orientation_with_corners(board, board_open_corners,board_edges, p, u, x)
                moves = moves + moves_each_orientation
        i += 1
    
    return moves

def max_min_value( state, player, max_or_min, no_of_levels, move ):
    global maxcalls, mincalls
    if (max_or_min == 'min'):
        mincalls += 1
    else:
        maxcalls += 1
    if (state[0] == 1):
        current_player = 1
        next_player = 2
        player_pieces = state[2]
        other_player_pieces = state[3]
    else:
        current_player = 2
        next_player = 1
        player_pieces = state[3]
        other_player_pieces = state[2]
        
    new_pieces = deepcopy(player_pieces)
    newboard = place_piece( move[3], move[2], move[0], move[1],state )
    new_pieces.remove(move[3])
    
    if no_of_levels-1 == 0:
        return heuristic(newboard, player)
    if (current_player == 1):
        new_state = (next_player, newboard, new_pieces, other_player_pieces, state[4] + 1)
    else:
        new_state = (next_player, newboard, other_player_pieces,new_pieces, state[4] + 1)
    
    if (max_or_min == 'min'):
        v = INFINITY
    else:
        v = -INFINITY

    next_player_moves = possible_moves(new_state)

    # if there are more levels than can be searched for current player, skip search of next player
    if next_player_moves == [] and no_of_levels > 2:
        if(current_player == 1):
            new_state = (current_player, newboard, new_pieces,
            other_player_pieces, state[4] + 2)
        else:
            new_state = (current_player, newboard,
            other_player_pieces, new_pieces, state[4] + 2)
        return skip_turn(new_state, player, no_of_levels-1, max_or_min)
    
    # analyse each move
    for m in next_player_moves:
        if(max_or_min == 'min'):
            r = max_min_value(new_state, player, 'max', no_of_levels-1, m)
            v = min(v, r)
        else:
            r = max_min_value(new_state, player, 'min', no_of_levels-1, m)
            v = max(v, r)
            
    if next_player_moves == []:
        return heuristic(newboard, player)

    return v

def skip_turn (state, player, no_of_rounds, max_or_min):
    global maxcalls, mincalls
    if (max_or_min == 'min'):
        mincalls += 1
    else:
        maxcalls += 1
    moves = possible_moves(state)
    if moves == []:
        return heuristic(state[1], player)
    if (max_or_min == 'min'):
        v = -INFINITY
    else:
        v = INFINITY
    for m in moves:
        if(max_or_min == 'min'):
            r = max_min_value(state, player, 'min', no_of_rounds-1, m)
            v = max(v, r)
        else:
            r = max_min_value(state, player, 'max', no_of_rounds-1, m)
            v = min(v, r)
    return v

def computer_turn( state ):
    moves = possible_moves(state)
    
    if(moves == []):
        return (state[1],'')
    pos = -1
    heu = -INFINITY
    inc = 0
    for m in moves:
        h = max_min_value( state, 1, 'min', MIN_MAX_LEVELS, m) # place the piece and find heuristic value
        if ( h > heu ):
            pos = inc
            heu = h
        inc += 1
        
    move = moves[pos]
    newboard = place_piece( move[3], move[2], move[0], move[1], state )
   
    return (newboard, move[3])

# find best move using this function
def heuristic( board, player ):
    if player == 1:
        other_player = 2
    else:
        other_player = 1
    open_corners = get_all_corners_edges(board, player)[0]
    open_corners_other = get_all_corners_edges(board, other_player)[0]
    return (len(open_corners)*2) - len(open_corners_other)


# implements a human turn of the game
def human_turn( state ):
    board = state[1]
    newboard = board
    while (newboard == board): # until their move is valid keep asking
        print()
        p = input('Your move? ')
        if(p.lower() == 'pass'):
            return (board,'')
        l = p.split('.')
        piece = list(piece_spec)[int(l[0])-1]
        
        y = int(input('Y coordinate '))
        x = int(input('X coordinate '))
        try:
            newboard = place_piece(piece,l[1],y,x,state)
        except IndexError:
            print('PLEASE TRY AGAIN')
    return (newboard, piece)

# PLAY GAME
def game( state ):
    print(INTRO)
    print()
    print(INTRO2)
    print()
    print("GAME START")
    move_number = state[4]
    player = 1
    finish1 = False
    finish2 = False
    while True:
        display_state(state)
        board = state[1]
        print( '\nPlayer to move: ', state[0], "\n" )
        if(move_number%2 == 0): # Player 2
            (newboard, piece) = human_turn(state)
            if(newboard == board and finish1):
                break
            elif(newboard == board):
                finish2 = True
            else:
                state[3].remove(piece)
            player = 1
        else: # Player 1
            (newboard, piece) = computer_turn(state)
            if(newboard == board and finish2):
                break
            elif(newboard == board):
                finish1 = True
            else:
                state[2].remove(piece)
            player = 2            
        move_number += 1
        new_state = (player, newboard, state[2], state[3], move_number)
        state = new_state
        
    win(state)


def main():
    setup()
    game(initial_state)
main()