from copy import deepcopy

TOTAL_TILES = 89
BOARD_SIZE = 14
MIN_MAX_LEVELS = 2
CANVAS_WIDTH = 1500
CANVAS_HEIGHT = 800
INFINITY = 1.e400

INTRO = "Each piece placed must be touching a corner (but not on an edge) of a piece of same colour. Place as many tiles as possible. Most number of tiles on the board wins."
INTRO2 = "When asked for a move, type the decimal number of piece. When prompted, enter y coordinate and x coordinates to place the (0,0) tile of the piece."

piece_list = [  'unit', 'pair',
                '3line', '3v',
                '4line', '4el', '4tee', '4sq', '4z',
                '5line', '5el', '5z', '5l', '5u', '5t', '5T',
                '5v', '5w', '5s', '5?', '5cross' ]

# cover, corner and edge squares are listed as (y,x) coords
# with (0,0) being the top leftmost cell of the piece.
piece_spec = {  'unit': { 'cover': [[1]],
                'reflection': 'no',
                'rotation': 'no',
                'size': 1
                },
                'pair': { 'cover': [[1,1]],
                'reflection': 'no',
                'rotation': 'yes',
                'size': 2
                },
                '3line': { 'cover': [[1,1,1]],
                'reflection': 'no',
                'rotation': 'yes',
                'size': 3
                },
                '3v': { 'cover': [[1,1],[0,1]],
                'reflection': 'no',
                'rotation': 'yes',
                'size': 3
                },
                '4line': { 'cover': [[1,1,1,1]],
                'reflection': 'no',
                'rotation': 'yes',
                'size': 4
                },
                '4el': { 'cover': [[1,1,1],[1,0,0]],
                'reflec_cover': [[1,1,1],[0,0,1]],
                'reflection': 'yes',
                'rotation': 'yes',
                'size': 4
                },
                '4tee': { 'cover': [[1,1,1],[0,1,0]],
                'reflection': 'no',
                'rotation': 'yes',
                'size': 4
                },
                '4sq': { 'cover': [[1,1],[1,1]],
                'reflection': 'no',
                'rotation': 'no',
                'size': 4
                },
                '4z': { 'cover': [[1,1,0],[0,1,1]],
                'reflec_cover': [[0,1,1],[1,1,0]],
                'reflection': 'yes',
                'rotation': 'yes',
                'size': 4
                },
                '5line': { 'cover': [[1,1,1,1,1]],
                'reflection': 'no',
                'rotation': 'yes',
                'size': 5
                },
                '5el': { 'cover': [[1,1,1],[1,1,0]],
                'reflec_cover': [[1,1,1],[0,1,1]],
                'reflection': 'yes',
                'rotation': 'yes',
                'size': 5
                },
                '5z': { 'cover': [[1,1,0,0],[0,1,1,1]],
                'reflec_cover': [[0,0,1,1],[1,1,1,0]],
                'reflection': 'yes',
                'rotation': 'yes',
                'size': 5
                },
                '5l': { 'cover': [[1,1,1,1],[1,0,0,0]],
                'reflec_cover': [[1,1,1,1],[0,0,0,1]],
                'reflection': 'yes',
                'rotation': 'yes',
                'size': 5
                },
                '5u': { 'cover': [[1,0,1],[1,1,1]],
                'reflection': 'no',
                'rotation': 'yes',
                'size': 5
                },
                '5t': { 'cover': [[1,1,1,1],[0,1,0,0]],
                'reflec_cover': [[1,1,1,1],[0,0,1,0]],
                'reflection': 'yes',
                'rotation': 'yes',
                'size': 5
                },
                '5T': { 'cover': [[1,1,1],[0,1,0],[0,1,0]],
                'reflection': 'no',
                'rotation': 'yes',
                'size': 5
                },
                '5v': { 'cover': [[1,0,0],[1,0,0],[1,1,1]],
                'reflection': 'no',
                'rotation': 'yes',
                'size': 5
                },
                '5w': { 'cover': [[1,0,0],[1,1,0],[0,1,1]],
                'reflection': 'no',
                'rotation': 'yes',
                'size': 5
                },
                '5s': { 'cover': [[1,1,0],[0,1,0],[0,1,1]],
                'reflec_cover': [[0,1,1],[0,1,0],[1,1,0]],
                'reflection': 'yes',
                'rotation': 'yes',
                'size': 5
                },
                '5?': { 'cover': [[1,1,0],[0,1,1],[0,1,0]],
                'reflec_cover': [[0,1,1],[1,1,0],[0,1,0]],
                'reflection': 'yes',
                'rotation': 'yes',
                'size': 5
                },
                '5cross': { 'cover': [[0,1,0],[1,1,1],[0,1,0]],
                'reflection': 'no',
                'rotation': 'no',
                'size': 5
                }
            }

initial_board = [[ 0 for x in range(BOARD_SIZE) ]
                        for y in range(BOARD_SIZE) ]
piece_list1 = deepcopy( piece_list )
piece_list2 = deepcopy( piece_list )
initial_state = ( 1, initial_board, piece_list1, piece_list2, 1 )