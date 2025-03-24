import curses
from copy import deepcopy
from random import shuffle


BOARD_WIDTH, BOARD_HEIGHT = 28, 28


class colors:
    blue = 1
    cyan = 2
    red = 3
    magenta = 4
    yellow = 5
    black = 6


class Cell():
    '''
    A Pixel 
    '''

    def __init__(self, color):
        self.color = color
        self.box = u"\u2588".encode('utf-8')

    def draw(self, x, y, dx, dy):
        color = curses.color_pair(self.color)
        screen.addstr(y + dy, x + 2*dx, self.box, color)
        screen.addstr(y + dy, x + 2*dx+1, self.box, color)


class Piece():
    '''
    The Fundamenal Game Object  
    '''

    def __init__(self, shape, initial_loc):
        self.initial_shape = shape
        self.initial_loc = initial_loc
        self.shape = shape
        self.selectable = True
        self.grid_x, self.grid_y = 0, 0

    def set_board_location(self, screen, left, top):
        self.screen = screen

        self.board_left = left
        self.board_top = top
        self.board_right = BOARD_WIDTH
        self.board_bottom = BOARD_HEIGHT

    def height(self):
        return len(self.shape)

    def width(self):
        return len(self.shape[0])

    # Horizontal board position to terminal coordinate transformation
    def grid_to_xpos(self):
        return 2*self.grid_x + self.board_left

    # Vertical board position to terminal coordinate transformation
    def grid_to_ypos(self):
        return self.grid_y + self.board_top

    def draw_piece(self, x, y, highlight):
        for col in range(self.height()):
            for row in range(self.width()):
                if self.shape[col][row] == 1:
                    if highlight:
                        c = Cell(self.highlight)
                    else:
                        c = Cell(self.color)
                    c.draw(x, y, row, col)

    def draw_in_stockpile(self, highlight=False):
        self.reset_shape()
        self.draw_piece(
            self.initial_loc[0],
            self.initial_loc[1],
            highlight
        )

    def draw_in_grid(self, highlight=False):
        self.draw_piece(
            self.grid_to_xpos(),
            self.grid_to_ypos(),
            highlight
        )

    def set_color(self, color):
        self.color = color
        self.highlight = color + 1

    def blackout(self):
        self.color = colors.black
        self.selectable = False
        self.draw_in_stockpile()

    def reset_shape(self):
        self.shape = [row[:] for row in self.initial_shape]

    def place_on_board(self):
        self.grid_x, self.grid_y = 0, 0
        self.draw_in_grid(highlight=True)

    def rotate(self):
        if self.grid_y + self.width() < self.board_bottom:
            if self.grid_x + self.height() <= self.board_right:
                self.shape = list(zip(*reversed(self.shape)))

    def flip(self):
        self.shape = [row[::-1] for row in self.shape]

    def player_move(self, move):
        if move == 'UP':
            if self.grid_y > 0:
                self.grid_y -= 2
        elif move == 'DOWN':
            if self.grid_y + 2 < self.board_bottom - self.height():
                self.grid_y += 2
        elif move == 'LEFT':
            if self.grid_x - 2 >= 0:
                self.grid_x -= 2
        elif move == 'RIGHT':
            if self.grid_x + 2 <= self.board_right - self.width():
                self.grid_x += 2
        elif move == 'ROTATE':
            self.rotate()
        elif move == 'FLIP':
            self.flip()

        self.draw_in_grid(highlight=True)


LONG_L = Piece(
    [[1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0],
     [1, 0, 0, 0, 0],
     [1, 0, 0, 0, 0],
     [1, 0, 0, 0, 0]],
    initial_loc=[0, 0]
)

LANKY_L = Piece(
    [[1, 1, 1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0, 0, 0]],
    initial_loc=[12, 0]
)

SMALL_T = Piece(
    [[0, 0, 1, 0, 0],
     [0, 0, 1, 0, 0],
     [1, 1, 1, 1, 1]],
    initial_loc=[4, 2]
)

BACKPACK_L = Piece(
    [[0, 0, 1, 0, 0],
     [0, 0, 1, 0, 0],
     [1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0],
     [1, 0, 0, 0, 0]],
    initial_loc=[12, 4]
)

THUMB = Piece(
    [[1, 1, 1],
     [1, 1, 1],
     [1, 1, 1],
     [0, 0, 1],
     [0, 0, 1]],
    initial_loc=[20, 2]
)

SQUARE = Piece(
    [[1, 1, 1],
     [1, 1, 1],
     [1, 1, 1]],
    initial_loc=[0, 6]
)

THREE_LINE = Piece(
    [[1],
     [1],
     [1],
     [1],
     [1]],
    initial_loc=[0, 10]
)

HALBERD = Piece(
    [[0, 0, 1],
     [0, 0, 1],
     [1, 1, 1],
     [0, 0, 1],
     [0, 0, 1],
     [0, 0, 1],
     [0, 0, 1]],
    initial_loc=[4, 8]
)

PLUS = Piece(
    [[0, 0, 1, 0, 0],
     [0, 0, 1, 0, 0],
     [1, 1, 1, 1, 1],
     [0, 0, 1, 0, 0],
     [0, 0, 1, 0, 0]],
    initial_loc=[12, 8]
)

TWO_LINE = Piece(
    [[1],
     [1],
     [1]],
    initial_loc=[24, 8]
)

FOUR_LINE = Piece(
    [[1],
     [1],
     [1],
     [1],
     [1],
     [1],
     [1]],
    initial_loc=[0, 16]
)

T = Piece(
    [[1, 0, 0, 0, 0],
     [1, 0, 0, 0, 0],
     [1, 1, 1, 1, 1],
     [1, 0, 0, 0, 0],
     [1, 0, 0, 0, 0]],
    initial_loc=[4, 14]
)

WAVE = Piece(
    [[1, 0, 0, 0, 0],
     [1, 0, 0, 0, 0],
     [1, 1, 1, 0, 0],
     [0, 0, 1, 0, 0],
     [0, 0, 1, 1, 1]],
    initial_loc=[12, 12]
)

L = Piece(
    [[1, 1, 1],
     [0, 0, 1],
     [0, 0, 1],
     [0, 0, 1],
     [0, 0, 1]],
    initial_loc=[20, 12]
)

O = Piece(
    [[1]],
    initial_loc=[8, 18]
)

ELBOW = Piece(
    [[1, 1, 1],
     [1, 0, 0],
     [1, 0, 0]],
    initial_loc=[12, 18]
)

SNAKE = Piece(
    [[0, 0, 1],
     [0, 0, 1],
     [1, 1, 1],
     [1, 0, 0],
     [1, 0, 0],
     [1, 0, 0],
     [1, 0, 0]],
    initial_loc=[16, 18]
)

Z = Piece(
    [[0, 0, 1],
     [0, 0, 1],
     [1, 1, 1],
     [1, 0, 0],
     [1, 0, 0]],
    initial_loc=[0, 22]
)

S = Piece(
    [[0, 0, 1, 1, 1],
     [0, 0, 1, 0, 0],
     [0, 0, 1, 0, 0],
     [0, 0, 1, 0, 0],
     [1, 1, 1, 0, 0]],
    initial_loc=[4, 22]
)

U = Piece(
    [[1, 0, 0, 0, 1],
     [1, 0, 0, 0, 1],
     [1, 1, 1, 1, 1]],
    initial_loc=[12, 24]
)

FIVE_LINE = Piece(
    [[1],
     [1],
     [1],
     [1],
     [1],
     [1],
     [1],
     [1],
     [1]],
    initial_loc=[24, 18]
)

ALL_PIECES = [
    LONG_L,
    LANKY_L,
    SMALL_T,
    THUMB,
    SQUARE,
    BACKPACK_L,
    THREE_LINE,
    HALBERD,
    PLUS,
    TWO_LINE,
    FOUR_LINE,
    T,
    WAVE,
    L,
    O,
    ELBOW,
    SNAKE,
    Z,
    S,
    U,
    FIVE_LINE
]


class Input():
    '''
    Transforms Key Presses into Useful Names
    '''

    def __init__(self, screen):
        self.screen = screen
        self.moves = {
            259: 'UP',
            258: 'DOWN',
            260: 'LEFT',
            261: 'RIGHT',
            32: 'ROTATE',  # space
            114: 'ROTATE',  # r
            117: 'UNSELECT',  # u
            102: 'FLIP',  # f
            10: 'SELECT',  # enter
            27: 'QUIT',  # esc
            113: 'QUIT',  # q
        }

    def next(self):
        event = self.screen.getch()
        return self.moves.get(event)

    def __iter__(self):
        return self


class Curses():
    '''
    The Curses Library Handles the Graphics
    '''

    def __enter__(self):
        screen = curses.initscr()
        screen.keypad(1)

        curses.noecho()
        curses.curs_set(0)

        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        return screen

    def __exit__(self, type, value, traceback):
        curses.endwin()


class Board(list):
    '''
    Creates a Game Space and Sets Rules for the Game
    '''

    def __init__(self, screen, screen_height, screen_width):
        self.screen = screen
        self.top = int((screen_height - BOARD_HEIGHT)/2)
        self.left = int((screen_width - 2*BOARD_WIDTH)/2)

        self.add_title()
        self.add_help_menu()

        # The Blue player must start the game at this location
        self.blue_start = [8, 8]
        # The Red player must start the game at this location
        self.red_start = [18, 18]

        self.grid = []
        self.fill_in_grid()

    def draw_text(self, text, y_offset, color=colors.yellow):
        longest_line = max(text, key=len)
        x_offset = self.left + int(BOARD_WIDTH) - int(len(longest_line)/2)

        color = curses.color_pair(color)
        for index, text_row in enumerate(text):
            self.screen.addstr(y_offset + index, x_offset, text_row, color)

    def add_title(self):
        title = [
            ' ____  _       _',
            '|  _ \| |     | | ',
            '| |_) | | ___ | | ___   _ ___ ',
            '|  _ <| |/ _ \| |/ / | | / __| ',
            '| |_) | | (_) |   <| |_| \__ \ ',
            '|____/|_|\___/|_|\_\\__,__|___/ ',
        ]
        y_offset = self.top - len(title) - 1
        self.draw_text(title, y_offset)

    def add_help_menu(self):
        help_menu = [
            "MOVE     = ARROW KEYS",
            "SELECT   = ENTER",
            "UNSELECT = U",
            "ROTATE   = SPACE",
            "FLIP     = F",
            "QUIT     = Q",
        ]
        y_offset = self.top + BOARD_HEIGHT
        self.draw_text(help_menu, y_offset)

    def fill_in_grid(self):
        CyanCell = Cell(colors.cyan)
        MagentaCell = Cell(colors.magenta)
        YellowCell = Cell(colors.yellow)
        BlackCell = Cell(colors.black)
        for i in range(BOARD_WIDTH+1):
            row = []
            for j in range(BOARD_HEIGHT+1):
                if i % 2 == 0 and j % 2 == 0:
                    if [i, j] == self.blue_start:
                        row.append(CyanCell)
                    elif [i, j] == self.red_start:
                        row.append(MagentaCell)
                    else:
                        row.append(YellowCell)
                else:
                    row.append(BlackCell)

            self.grid.append(row)

    def count_corner_touches(self, piece):
        touch_count = 0
        corners = [
            [2, 2],
            [2, -2],
            [-2, 2],
            [-2, -2]
        ]
        adjacent = [
            [0, 2],
            [0, -2],
            [2, 0],
            [-2, 0],
        ]

        for col in range(piece.height()):
            for row in range(piece.width()):
                if piece.shape[col][row] == 1:
                    grid_x = piece.grid_x + row
                    grid_y = piece.grid_y + col
                    try:
                        if self.grid[grid_x][grid_y].color in [colors.blue, colors.red]:
                            return 0
                        for x, y in adjacent:
                            if self.grid[grid_x + x][grid_y + y].color == piece.color:
                                return 0
                        for x, y in corners:
                            if self.grid[grid_x + x][grid_y + y].color == piece.color:
                                touch_count += 1
                    except IndexError:
                        return 0

        return touch_count

    def contains_start_loc(self, piece, start_x, start_y):
        for col in range(piece.height()):
            for row in range(piece.width()):
                if piece.shape[col][row] == 1:
                    grid_x, grid_y = piece.grid_x + row, piece.grid_y + col
                    if [grid_x, grid_y] == [start_x, start_y]:
                        return True
        return False

    def confirm_valid_move(self, piece):
        is_valid = False
        blue_start_x, blue_start_y = self.blue_start
        red_start_x, red_start_y = self.red_start

        if self.grid[blue_start_x][blue_start_y].color == colors.cyan:
            is_valid = self.contains_start_loc(piece, *self.blue_start)
        elif self.grid[red_start_x][red_start_y].color == colors.magenta:
            is_valid = self.contains_start_loc(piece, *self.red_start)
        else:
            is_valid = self.count_corner_touches(piece) == 1

        return is_valid

    def save_piece_on_grid(self, piece):
        for col in range(piece.height()):
            for row in range(piece.width()):
                if piece.shape[col][row] == 1:
                    grid_x = piece.grid_x + row
                    grid_y = piece.grid_y + col
                    self.grid[grid_x][grid_y] = Cell(piece.color)
        self.draw_board()

    def draw_board(self):
        for i in range(BOARD_WIDTH):
            for j in range(BOARD_HEIGHT):
                if self.grid[i][j]:
                    self.grid[i][j].draw(self.left, self.top, i, j)

    def draw_endgame_score(self, message, winning_color):
        y_offset = self.top - 1
        self.draw_text([message], y_offset, winning_color)


class GameAI():
    '''
    A Simple Minimax algorithm with Alpha Beta Pruning Controls the Red Player
    '''

    def __init__(self, board, player_pieces, opponent_pieces):
        self.board = board
        self.player_pieces = player_pieces
        self.opponent_pieces = opponent_pieces
        self.tree_depth = 2
        self.alpha = -10000
        self.beta = 10000

    def save_and_record_piece_on_grid(self, piece):
        piece.selectable = False
        move_locations = []

        for col in range(piece.height()):
            for row in range(piece.width()):
                if piece.shape[col][row] == 1:
                    grid_x, grid_y = piece.grid_x + row, piece.grid_y + col

                    # Record grid colors before the piece was placed
                    previous_color = self.board.grid[grid_x][grid_y].color
                    move_locations.append([grid_x, grid_y, previous_color])

                    # Place the piece
                    self.board.grid[grid_x][grid_y] = Cell(piece.color)

        return move_locations

    def undo_last_move(self, piece, move_locations):
        piece.selectable = True
        piece.reset_shape()
        for grid_x, grid_y, color in move_locations:
            self.board.grid[grid_x][grid_y] = Cell(color)

    def generate_random_move(self, all_pieces):
        piece_indexes = list(range(len(all_pieces)))
        shuffle(piece_indexes)

        for piece_index in piece_indexes:
            piece = all_pieces[piece_index]
            if piece.selectable is True:
                for _ in range(4):
                    piece.rotate()
                    for _ in range(2):
                        piece.flip()
                        for i in range(0, BOARD_WIDTH+1, 2):
                            for j in range(0, BOARD_HEIGHT+1, 2):
                                if self.board.grid[i][j].color == colors.yellow:
                                    piece.grid_x, piece.grid_y = i, j
                                    if self.board.confirm_valid_move(piece):
                                        return piece

    def minimax(self, tree_depth, alpha, beta, isMaximisingPlayer):
        # Larger pieces closer to the center are high scoring moves
        if tree_depth == 0:
            def distance_to_center(x, y):
                return 1 + (x - 0.5*BOARD_WIDTH)**2 + (y - 0.5*BOARD_HEIGHT)**2

            score = 0
            for row_index, row in enumerate(self.board.grid):
                for column_index, col in enumerate(row):
                    if col.color == colors.red:
                        score += (2 + 1 / distance_to_center(row_index, column_index))
                    elif col.color == colors.blue:
                        score -= (2 + 1 / distance_to_center(row_index, column_index))
            return score

        if isMaximisingPlayer:
            best_move = -10000
            pieces_to_try = len(self.opponent_pieces)
            for _ in range(pieces_to_try):
                piece = self.generate_random_move(self.opponent_pieces)
                if piece is None:
                    return best_move

                move_locations = self.save_and_record_piece_on_grid(piece)
                best_move = max(
                    best_move,
                    self.minimax(tree_depth - 1, alpha, beta, not isMaximisingPlayer)
                )
                self.undo_last_move(piece, move_locations)

                alpha = max(alpha, best_move)
                if beta <= alpha:
                    break

            return best_move

        else:
            best_move = 10000
            pieces_to_try = len(self.player_pieces)
            for _ in range(pieces_to_try):
                piece = self.generate_random_move(self.player_pieces)
                if piece is None:
                    return best_move

                move_locations = self.save_and_record_piece_on_grid(piece)
                best_move = min(
                    best_move,
                    self.minimax(tree_depth - 1, alpha, beta, not isMaximisingPlayer)
                )
                self.undo_last_move(piece, move_locations)

                beta = min(beta, best_move)
                if beta <= alpha:
                    break

            return best_move

    def find_best_piece(self):
        best_move = -10000
        pieces_to_try = len(self.opponent_pieces)
        for _ in range(pieces_to_try):
            piece = self.generate_random_move(self.opponent_pieces)
            if piece is None:
                return

            move_locations = self.save_and_record_piece_on_grid(piece)

            score = self.minimax(
                self.tree_depth,
                self.alpha,
                self.beta,
                isMaximisingPlayer=True
            )

            if score >= best_move:
                best_move = score
                best_piece = piece
                best_piece_location = (piece.grid_x, piece.grid_y)
                best_piece_shape = piece.shape

            self.undo_last_move(piece, move_locations)

        best_piece.grid_x, best_piece.grid_y = best_piece_location
        best_piece.shape = best_piece_shape
        return best_piece


class Game():
    '''
    Sets up the game, defines the flow, and links the user and AI actions 
    '''

    def __init__(self, screen):
        self.is_playing = True

        screen_height, screen_width = screen.getmaxyx()
        if screen_height < 45 or screen_width < 115:
            raise Exception('Increase size of Terminal')

        self.board = Board(screen, screen_height, screen_width)
        self.board.draw_board()
        self.input_generator = Input(screen)

        self.piece_index = 0
        self.selected_piece = None

        self.setup_player_pieces()
        self.setup_opponent_pieces()

    def setup_player_pieces(self):
        self.player_pieces = deepcopy(ALL_PIECES)
        for index, piece in enumerate(self.player_pieces):
            piece.set_board_location(screen, self.board.left, self.board.top)
            piece.initial_loc[0] += piece.board_left - BOARD_WIDTH
            piece.initial_loc[1] += piece.board_top
            piece.set_color(colors.blue)
            if index == 0:
                piece.draw_in_stockpile(highlight=True)
            else:
                piece.draw_in_stockpile()

    def setup_opponent_pieces(self):
        self.opponent_pieces = deepcopy(ALL_PIECES)
        for piece in self.opponent_pieces:
            piece.set_board_location(screen, self.board.left, self.board.top)
            piece.initial_loc[0] += piece.board_left + 2*BOARD_WIDTH
            piece.initial_loc[1] += piece.board_top
            piece.set_color(colors.red)
            piece.draw_in_stockpile()

    def select_game_piece(self, move):
        if move == 'RIGHT':
            self.piece_index += 1
            if self.piece_index > len(self.player_pieces) - 1:
                self.piece_index = 0
                self.player_pieces[0].draw_in_stockpile(highlight=True)
                self.player_pieces[-1].draw_in_stockpile()
            else:
                self.player_pieces[self.piece_index].draw_in_stockpile(highlight=True)
                self.player_pieces[self.piece_index-1].draw_in_stockpile()
        elif move == 'LEFT':
            self.piece_index -= 1
            if self.piece_index < 0:
                self.piece_index = len(self.player_pieces) - 1
                self.player_pieces[-1].draw_in_stockpile(highlight=True)
                self.player_pieces[0].draw_in_stockpile()
            else:
                self.player_pieces[self.piece_index].draw_in_stockpile(highlight=True)
                self.player_pieces[self.piece_index+1].draw_in_stockpile()

        if move == 'SELECT':
            self.selected_piece = self.player_pieces[self.piece_index]
            self.selected_piece.place_on_board()

    def cleanup_selected_piece(self):
        self.selected_piece.blackout()
        self.selected_piece = None
        self.player_pieces = [p for p in self.player_pieces if p.selectable]
        self.piece_index = 0
        if self.player_pieces:
            self.player_pieces[0].draw_in_stockpile(highlight=True)

    # Checks if the Blue Player is able to place a single piece
    def endgame_check(self):
        for piece in self.player_pieces:
            if piece.selectable is True:
                for rotation_count in range(4):
                    piece.rotate()
                    for flip_count in range(2):
                        piece.flip()
                        for i in range(0, BOARD_WIDTH+1, 2):
                            for j in range(0, BOARD_HEIGHT+1, 2):
                                if self.board.grid[i][j].color == colors.yellow:
                                    piece.grid_x, piece.grid_y = i, j
                                    if self.board.count_corner_touches(piece) == 1:
                                        return False
        return True

    def opponent_turn(self):
        game_ai = GameAI(self.board, self.player_pieces, self.opponent_pieces)
        best_piece = game_ai.find_best_piece()
        if best_piece:
            self.board.save_piece_on_grid(best_piece)
            best_piece.blackout()
            self.opponent_pieces = [p for p in self.opponent_pieces if p.selectable]
        else:
            self.is_playing = False

    def game_loop(self):
        while True:
            move = self.input_generator.next()

            if move == 'QUIT':
                break

            self.board.draw_board()

            if self.is_playing:
                if self.selected_piece is None:
                    self.select_game_piece(move)
                else:
                    if move == 'UNSELECT':
                        self.selected_piece = None
                    elif move == 'SELECT':
                        if self.board.confirm_valid_move(self.selected_piece):
                            self.board.save_piece_on_grid(self.selected_piece)
                            self.cleanup_selected_piece()

                            if self.endgame_check():
                                self.board.draw_endgame_score('Red Won', colors.red)
                                self.is_playing = False
                            else:
                                self.opponent_turn()
                                if self.is_playing is False:
                                    self.board.draw_endgame_score('Blue Won', colors.blue)
                    else:
                        self.selected_piece.player_move(move)

    def play(self):
        try:
            self.game_loop()
        except:
            exit(0)


if __name__ == "__main__":
    # If python2, use locale.LC_ALL for a solid pixel box
    import locale
    locale.setlocale(locale.LC_ALL, '')

    with Curses() as screen:
        game = Game(screen)
        game.play()
