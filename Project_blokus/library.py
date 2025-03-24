from tkinter import *
from settings import *

def setup():
    global w
    master = Tk()
    w = Canvas(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
    w.pack()

# get all the coordinates of the orientations of a piece
def all_orientations(p):
    coord_list = set()
    matrix = piece_spec[p]['cover']
    coord_list = coord_list.union(coordinates_matrix(matrix))
    
    rotate = piece_spec[p]['rotation']
    if(rotate == 'yes'):
        coord_list = coord_list.union(coordinates_rotate(matrix))
    reflec = piece_spec[p]['reflection']
    if(reflec == 'yes'):
        matrix = piece_spec[p]['reflec_cover']
        coord_list = coord_list.union(coordinates_matrix(matrix))
        coord_list = coord_list.union(coordinates_rotate(matrix))
    
    
    return list(coord_list)

# get the coordinates from a given matrix
def coordinates_matrix( matrix ):
    coord_set = set()
    l = []
    b = 0
    for x in range(len(matrix[0])): # left to right
        a = 0
        for m1 in matrix:
            if m1[x] == 1:
                l.append((a,b))
            a += 1
        b += 1
    tup1 = tuple(l)
    coord_set.add(tup1)
    return coord_set

# get the rotation coordinates given a matrix
def coordinates_rotate( matrix ):
    coord_set = set()
    l = []
    b = 0
    for x in range(len(matrix)-1,-1,-1): # bottom to up
        a = 0
        for g in matrix[x]:
            if g == 1:
                l.append((a,b))
            a += 1
        b += 1
    tup2 = tuple(l)
    coord_set.add(tup2)
    l = []
    b = 0
    for g in range(len(matrix[0])-1,-1,-1):
        a = 0
        for x in range(len(matrix)-1,-1,-1): # right to left
            if matrix[x][g] == 1:
                l.append((a,b))
            a += 1
        b += 1
    tup3 = tuple(l)
    coord_set.add(tup3)
    l = []
    b = 0
    for x in matrix: # top to bottom
        a = 0
        for g in range(len(x)-1,-1,-1):
            if x[g] == 1:
                l.append((a,b))
            a += 1
        b += 1
    tup4 = tuple(l)
    coord_set.add(tup4)
    return coord_set


# place a piece on the board given the orientation position and coordinates
def place_piece( p, orientation_no, Y, X, state ):
    player = state[0]
    board = state[1]
    move_number = state[4]
    
    if not ((player == 1 and p in state[2]) or (player == 2 and p in state[3])):    
        print("FAIL. PLAYER DOES NOT HAVE THIS PIECE")
        return board
    newboard = deepcopy(board)
    initial = False
    valid = False
    plac = all_orientations(p)
    piece_to_place = plac[int(orientation_no)-1]
    (corners,edges) = get_all_corners_edges(board, player) 
    
    for coord in piece_to_place:
        y = Y+coord[0]
        x = X+coord[1]
        if (newboard[y][x] != 0):
            print("FAIL. OVERPLACING")
            return board
        elif (((move_number == 1 or move_number == 2 ) and ((y,x) == (0,0) or (y,x) == (BOARD_SIZE -1, BOARD_SIZE -1))) or move_number > 2):  # check whether the first move fills in the tiles on each corner of the grid 
            initial = True
        
        # check whether a valid move
        if ((move_number > 2 and (y,x) in corners) or move_number <= 2):
            valid = True
        elif ((y,x) in edges):
            print("FAIL. CAN'T PLACE ON EDGE")
            return board
        newboard[y][x] = player
    
    if (initial and valid):
        return newboard
    else:
        print("FAIL. PIECE NOT PLACED CORRECTLY ON CORNER")
        return board
    


# draw a square cell given the cell size and coordinates
def draw_cell(topleft_x,topleft_y,cell_size,y,x,col):
    w.create_rectangle(topleft_x + (x*cell_size),
    topleft_y + (y*cell_size)+10,
    topleft_x + ((x+1)*cell_size),
    topleft_y + ((y+1)*cell_size)+10,
    fill=col)
    #w.update()

# display the tiles on the canvas
def display_tiles( tiles, topleft_x, topleft_y, col ):
    initial = topleft_x
    n = 1
    e = 1
    for p in piece_list:
        if (p in tiles):
            e = 1
            for piece in all_orientations(p):
                for coord in piece:
                    draw_cell(topleft_x,topleft_y,10,coord[0],coord[1],col)
                    w.create_text(topleft_x + 10,topleft_y+60, text=str(n)+"."+str(e),font="bold")
                    #w.update()
                topleft_x += (10 + (len(piece) * 10))
                if topleft_x > CANVAS_WIDTH-230:
                    topleft_x = initial
                    topleft_y += (20 + (len(piece) * 10))
                e += 1
        n = n + 1

# display the board and the pieces of each player
def display_state( state ):
    w.delete("all")
    board = state[1]
    for y in range(BOARD_SIZE):
        w.create_text(55 + (y*25),35, text=str(y), font="bold")
        w.create_text(25,67 + (y*25), text=str(y), font="bold")
        #w.update()
        for x in range(BOARD_SIZE):
            draw_cell(45,45,25,y,x,'#dddddd' if board[y][x] == 0
            else "red" if board[y][x] == 1 else "blue")
            
            
    display_tiles(state[2],430,5,'red')
    display_tiles(state[3],30,430,'blue')

def check_orientation_with_corners( board, board_open_corners, board_edges, orientations, position, piece ):
    moves = []
    
    tilecorners = tile_corners(orientations[position])

    for corner in board_open_corners:
        Y = corner[0]
        X = corner[1]
        for t in tilecorners:
            c = [n for n in orientations[position] if not (n[0] == t[0] and n[1] == t[1])] # get all coords of tile except the corner tuple
            valid = True
            for r in c:
                diffY = Y+(r[0] - t[0])
                diffX = X+(r[1] - t[1])
                # check whether this orientation is a valid move on the board
                if not ( diffY < BOARD_SIZE and diffY > -1 and diffX > -1 and diffX < BOARD_SIZE and board[diffY][diffX] == 0 and (diffY,diffX) not in board_edges):
                    valid = False
                    break
            # add to the list of possible moves
            if valid:
                move = (Y-t[0],X-t[1],position+1,piece)
                moves.append(move)
    return moves

# get all the corner for a specific orientation of a tile
def tile_corners( coords ):
    corners = []
    for i in coords:
        y = i[0]
        x = i[1]
        if (((y+1,x) not in coords or (y-1,x) not in coords) and ((y,x-1) not in coords or (y,x+1) not in coords)):
            corners.append(i)
    
    return corners


# get all edges and corners of the board for the specific player
def get_all_corners_edges( board, player ):
    corners = set()
    edges = set()
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if (board[y][x] == player):
                if (y > 0 and board[y-1][x] == 0):
                    edges.add((y-1,x)) # top edge
                    if (x < BOARD_SIZE-1 and board[y-1][x+1] == 0 and edges_of_corner(y-1,x+1,board,player)): # top right corner
                        corners.add((y-1,x+1))
                    if (x > 0 and board[y-1][x-1] == 0 and edges_of_corner(y-1,x-1,board,player)): # top left corner
                        corners.add((y-1,x-1))
                if (y < BOARD_SIZE-1 and board[y+1][x] == 0):
                    edges.add((y+1,x)) # bottom edge
                    if(x < BOARD_SIZE-1 and board[y+1][x+1] == 0 and edges_of_corner(y+1,x+1,board,player)): # bottom right corner
                        corners.add((y+1,x+1))
                    if (x > 0 and board[y+1][x-1] == 0 and edges_of_corner(y+1,x-1,board,player)): # bottom left corner
                        corners.add((y+1,x-1))
                if (x > 0 and board[y][x-1] == 0): # left edge
                    edges.add((y,x-1))
                if (x < BOARD_SIZE-1 and board[y][x+1] == 0): # right edge
                    edges.add((y,x+1))
                    
    return (list(corners), list(edges))

def edges_of_corner(cy, cx, board, player):
    if(((cy > 0 and board[cy-1][cx] != player) or cy == 0) and # top
    ((cx < BOARD_SIZE-1 and board[cy][cx+1] != player) or cx ==
    BOARD_SIZE-1) and # right
    ((cy < BOARD_SIZE-1 and board[cy+1][cx] != player) or cy ==
    BOARD_SIZE-1) and # bottom
    ((cx > 0 and board[cy][cx-1] != player) or cx == 0)): # left
        return True
    return False

def calc_score_pieces( pieces ):
    n = 0
    for i in pieces:
        p = piece_spec[i]['size']
        n += p
    return n

def get_sized_pieces(pieces, size_pieces):
    new_pieces = []
    for i in pieces:
        n = piece_spec[i]['size']
        if n == size_pieces:
            new_pieces.append(i)
    return new_pieces

def win( state ):
    p1 = calc_score_pieces(state[2])
    p2 = calc_score_pieces(state[3])
    if p1 == 0:
        p1 -= 15
    if p2 == 0:
        p2 -= 15
    if ( p1 < p2 ):
        print ('Player 1 has won the game.')
    elif ( p2 < p1 ):
        print ('Player 2 has won the game.')
    else:
        print ('The game is a tie!')
    print()
    print ('Scores:')
    print('Player 1 = ', TOTAL_TILES - p1)
    print('Player 2 = ', TOTAL_TILES - p2)