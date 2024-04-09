import numpy as np


class Board:
    def __init__(self, horizontal_size = 3, vertical_size = 3):
        self.horizontal_size = horizontal_size
        self.vertical_size = vertical_size
        self.board = np.zeros((horizontal_size * vertical_size), dtype=int)
    
    def make_move(self, move:int,  player):
        """
        Makes a move on the board for a player at the given position
        :param move: the position to make the move at
        :param player: the player making the move (1 or -1)
        """
        if self.board[move] == 0:
            self.board[move] = player
        else:
            raise ValueError("Invalid move: a player has already made a move at this position")
    
    def is_valid_move(self, move:int):
        return self.board[move] == 0
        
    def check_winner(self):
        """
        Checks if a player has won the game
        :return: the player that has won the game, 0 if no player has won
        """
        # Check for horizontal win
        for i in range(self.horizontal_size):
            if all(self.board[i*self.vertical_size:(i+1)*self.vertical_size] == 1):
                return 1
            elif all(self.board[i*self.vertical_size:(i+1)*self.vertical_size] == -1):
                return -1
        
        # Check for vertical win
        for i in range(self.vertical_size):
            if all(self.board[i::self.vertical_size] == 1):
                return 1
            elif all(self.board[i::self.vertical_size] == -1):
                return -1
        # Check for diagonal win
        if all(self.board[0::self.vertical_size+1] == 1) or all(self.board[self.vertical_size-1:-1:self.vertical_size-1] == 1):
            return 1
        elif all(self.board[0::self.vertical_size+1] == -1) or all(self.board[self.vertical_size-1:-1:self.vertical_size-1] == -1):
            return -1
        
        return 0
    
    def check_draw(self):
        """
        Checks if the game is a draw
        :return: True if the game is a draw, False otherwise
        """
        return (0 not in set([i for i in self.board])) and (self.check_winner() == 0)
    
    def get_possible_moves(self):
        """
        Gets all possible moves on the board
        :return: a list of possible moves
        """
        return np.where(self.board == 0)
        
    def get_board(self):
        return self.board[i*self.horizontal_size:(i+1)*self.horizontal_size]

    def print_board(self):
        for i in range(self.vertical_size):
            print(self.board[i*self.horizontal_size:(i+1)*self.horizontal_size])

if __name__ == "__main__":            
    board = Board()
    print(board)
    board.print_board()