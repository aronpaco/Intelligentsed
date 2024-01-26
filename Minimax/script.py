import copy

# Constants
EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2

# Game board class
class Board:
    def __init__(self):
        # Initialize the board with the correct initial state
        self.board = [
            [EMPTY, PLAYER_X, EMPTY, PLAYER_X, EMPTY, PLAYER_X],
            [PLAYER_X, EMPTY, PLAYER_X, EMPTY, PLAYER_X, EMPTY],
            [EMPTY] * 6,
            [EMPTY] * 6,
            [PLAYER_O, EMPTY, PLAYER_O, EMPTY, PLAYER_O, EMPTY],
            [EMPTY, PLAYER_O, EMPTY, PLAYER_O, EMPTY, PLAYER_O],
        ]

    def print_board(self):
        for row in self.board:
            print(row)
        print()

    def make_move(self, move, player):
        row, col, direction = move
        self.board[row][col] = EMPTY  # Remove current position
        if direction == "up":
            self.board[row - 1][col - 1] = player
        elif direction == "down":
            self.board[row + 1][col - 1] = player

    def get_possible_moves(self, player):
        moves = []
        for row in range(6):
            for col in range(6):
                if self.board[row][col] == player:
                    if row - 1 >= 0 and col - 1 >= 0 and self.board[row - 1][col - 1] == EMPTY:
                        moves.append((row, col, "up"))
                    if row + 1 < 6 and col - 1 >= 0 and self.board[row + 1][col - 1] == EMPTY:
                        moves.append((row, col, "down"))
        return moves


# Minimax algorithm
def minimax(board, depth, maximizing_player):
    if depth == 0 or game_over(board):
        return evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in board.get_possible_moves(PLAYER_O):
            board_copy = copy.deepcopy(board)
            board_copy.make_move(move, PLAYER_O)
            eval = minimax(board_copy, depth - 1, False)
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.get_possible_moves(PLAYER_X):
            board_copy = copy.deepcopy(board)
            board_copy.make_move(move, PLAYER_X)
            eval = minimax(board_copy, depth - 1, True)
            min_eval = min(min_eval, eval)
        return min_eval


def get_best_move(board):
    best_eval = float('-inf')
    best_move = None
    for move in board.get_possible_moves(PLAYER_O):
        board_copy = copy.deepcopy(board)
        board_copy.make_move(move, PLAYER_O)
        eval = minimax(board_copy, 2, False)  # Adjust depth based on desired AI difficulty
        if eval > best_eval:
            best_eval = eval
            best_move = move
    return best_move


def game_over(board):
    return not board.get_possible_moves(PLAYER_X) or not board.get_possible_moves(PLAYER_O)


def evaluate_board(board):
    # A simple evaluation function, you can customize it based on your preferences
    return len(board.get_possible_moves(PLAYER_O)) - len(board.get_possible_moves(PLAYER_X))


# Main game loop
def play_game():
    board = Board()

    while not game_over(board):
        # Player X's turn
        print("Player X's turn:")
        board.print_board()
        x_move = tuple(map(int, input("Enter your move (row, col, direction - up/down): ").split()))
        board.make_move(x_move, PLAYER_X)

        if game_over(board):
            break

        # Player O's turn (AI)
        print("\nPlayer O's turn (AI):")
        o_move = get_best_move(board)
        board.make_move(o_move, PLAYER_O)

    print("\nGame Over!")
    board.print_board()
    print("Player X's score:", len(board.get_possible_moves(PLAYER_X)))
    print("Player O's score:", len(board.get_possible_moves(PLAYER_O)))


if __name__ == "__main__":
    play_game()
