import time
import copy

""" The number of moves (rounds) made during the game by both players.
 To complete stage 1 it takes 18 moves from both players."""
moves = 0

""" The number of moves made during the game by every player. 
    It also includes the number of pieces he captured after forming a mill. """
jmin_moves = 0
jmax_moves = 0

mills = [[0, 1, 2], [8, 9, 10], [16, 17, 18], [3, 11, 19], [20, 12, 4], [21, 22, 23], [13, 14, 15], [5, 6, 7],
         [0, 3, 5], [8, 11, 13], [16, 19, 21], [1, 9, 17], [22, 14, 6], [18, 20, 23], [10, 12, 15], [2, 4, 7]]

board_dictionary = {
    "a1": 5, "1a": 5, "a4": 3, "4a": 3, "a7": 0, "7a": 0,
    "b2": 13, "2b": 13, "b4": 11, "4b": 11, "b6": 8, "6b": 8,
    "c3": 21, "3c": 21, "c4": 19, "4c": 19, "c5": 16, "5c": 16,
    "d1": 6, "1d": 6, "d2": 14, "2d": 14, "d3": 22, "3d": 22,
    "d5": 17, "5d": 17, "d6": 9, "6d": 9, "d7": 1, "7d": 1,
    "e3": 23, "3e": 23, "e4": 20, "4e": 20, "e5": 18, "5e": 18,
    "f2": 15, "2f": 15, "f4": 12, "4f": 12, "f6": 10, "6f": 10,
    "g1": 7, "1g": 7, "g4": 4, "4g": 4, "g7": 2, "7g": 2
}


def adjacentLocations(position):
    """ Returns a list of adjacent positions of a given number. """

    adjacent = [[1, 3], [0, 2, 9], [1, 4], [0, 5, 11], [2, 7, 12], [3, 6], [5, 7, 14], [4, 6],
                [9, 11], [1, 8, 10, 17], [9, 12], [3, 8, 13, 19], [4, 10, 15, 20], [11, 14],
                [6, 13, 15, 22], [12, 14], [17, 19], [9, 16, 18], [17, 20], [11, 16, 21],
                [12, 18, 23], [19, 22], [21, 23, 14], [20, 22]]
    return adjacent[position]


def blocked(player, board):
    """ Returns True if the player can no longer make any moves. """

    for i in range(len(board)):
        if board[i] == player:
            for pos in adjacentLocations(i):
                if board[pos] == Game.EMPTY:
                    return False
    return True


def isMill(adj_list, player, board):
    """ Checks if a given list (a single line) is a mill """

    opponent = Game.JMIN if player == Game.JMAX else Game.JMAX
    for i in adj_list:
        if board[i] == Game.EMPTY or board[i] == opponent:
            return False
    return True


def checkMill(position, player, board):
    """ Checks if a player placed three of their pieces on contiguous points in a straight line,
        vertically or horizontally (they have formed a mill). """

    for adj_list in mills:
        if position in adj_list:
            if isMill(adj_list, player, board):
                return True
    return False


def removePiece(board_clone, opponent, successors):
    for j in range(len(board_clone)):
        if board_clone[j] == opponent and not checkMill(j, opponent, board_clone):
            new_board = copy.deepcopy(board_clone)
            new_board[j] = Game.EMPTY
            successors.append(Game(new_board))

    return successors


def openMills(position, opponent):
    """ Checks if a line is open """
    for mill in mills:
        if position in mill:
            if opponent not in mill:
                return True
    return False


def possibleMills(board, opponent):
    """ Counts the open lines """
    count = 0

    for i in range(len(board)):
        if board[i] == Game.EMPTY:
            if openMills(i, opponent):
                count += 1
    return count


class Game:
    """ Defines the game """

    SYMBOLS_PLAYERS = ['X', '0']
    JMIN = None
    JMAX = None
    EMPTY = '.'

    def __init__(self, board=None):
        self.board = board or [Game.EMPTY] * 24

    def final(self):
        """ Returns the symbol of the winning player
            - if the opponent is left with 2 pieces on the board
            - or if the opponent is blocked
            Returns False if the gave is not over yet
            The game can't end in stage 1"""

        if moves > 18:
            if self.board.count(Game.JMIN) == 2:
                return Game.JMAX
            pass

            if self.board.count(Game.JMAX) == 2:
                return Game.JMIN
            pass

            if blocked(Game.JMIN, self.board):
                return Game.JMAX
            pass

            if blocked(Game.JMAX, self.board):
                return Game.JMIN
            pass

        else:
            return False

    def game_moves(self, player):
        """ Returns a list of all possible successor configurations. """

        opponent = Game.JMIN if player == Game.JMAX else Game.JMAX
        successors = []

        if moves < 18:
            """ Phase 1: Placing pieces.
            The game begins with an empty board. The players take turns placing their men one per play on empty points.
            """

            for i in range(len(self.board)):
                if self.board[i] == Game.EMPTY:
                    board_clone = copy.deepcopy(self.board)
                    board_clone[i] = player

                    if checkMill(i, player, board_clone):
                        """  They have formed a mill and may remove one of their opponent's pieces from the board. """

                        successors = removePiece(board_clone, opponent, successors)

                    else:
                        successors.append(Game(board_clone))

        else:
            """ After all men have been placed. """

            if self.board.count(player) != 3:
                """ Phase 2: Moving pieces.
                Players continue to alternate moves, this time moving a man to an adjacent point.
                """

                for i in range(len(self.board)):
                    if self.board[i] == player:

                        for adjacent_pos in adjacentLocations(i):
                            if self.board[adjacent_pos] == Game.EMPTY:
                                board_clone = copy.deepcopy(self.board)
                                board_clone[i] = Game.EMPTY
                                board_clone[adjacent_pos] = player

                                if checkMill(adjacent_pos, player, board_clone):
                                    """ They have formed a mill and may remove one of their opponent's pieces from the 
                                    board. """

                                    successors = removePiece(board_clone, opponent, successors)

                                else:
                                    successors.append(Game(board_clone))

            else:
                """ Phase 3: "Flying" 
                When a player is reduced to three pieces, there is no longer a limitation on that player of moving 
                to only adjacent points: The player's men may "fly" from any point to any vacant point.
                """

                for i in range(len(self.board)):
                    if self.board[i] == player:

                        for j in range(len(self.board)):
                            if self.board[j] == Game.EMPTY:
                                board_clone = copy.deepcopy(self.board)

                                board_clone[i] = Game.EMPTY
                                board_clone[j] = player

                                if checkMill(j, player, board_clone):
                                    """ They have formed a mill and may remove one of their opponent's pieces from the 
                                    board. """

                                    successors = removePiece(board_clone, opponent, successors)

                                else:
                                    successors.append(Game(board_clone))

        return successors

    def heuristic(self):
        """ Heuristic that looks at the number of pieces on the board """
        if EVALUATION == 1:
            return self.board.count(Game.JMAX) - self.board.count(Game.JMIN)

        """ Heuristic that prioritizes the middle square """
        if EVALUATION == 2:
            pieces_JMAX_squares13 = self.board[1:8].count(Game.JMAX) + self.board[16:24].count(Game.JMAX)
            pieces_JMAX_square2 = self.board[8:16].count(Game.JMAX)

            pieces_JMIN_squares13 = self.board[1:8].count(Game.JMIN) + self.board[16:24].count(Game.JMIN)
            pieces_JMIN_square2 = self.board[8:16].count(Game.JMIN)

            evaluation = pieces_JMAX_squares13 - pieces_JMIN_squares13 + 1.5 * (pieces_JMAX_square2 - pieces_JMIN_square2)

            return evaluation

        """ Heuristic that looks at the number of potential mills on the board """
        if EVALUATION == 3:
            return possibleMills(self.board, Game.JMIN) - possibleMills(self.board, Game.JMAX) + \
                   self.board.count(Game.JMAX) - self.board.count(Game.JMIN)

    def estimate_score(self, depth):
        t_final = self.final()
        if t_final == Game.JMAX:
            return 999 + depth
        elif t_final == Game.JMIN:
            return -999 - depth
        else:
            return self.heuristic()

    def __str__(self):
        string = "7  [{}]------------------------[{}]------------------------[{}]\n".format(self.board[0],
                                                                                            self.board[1],
                                                                                            self.board[2])
        string += "    |                          |                          |\n"
        string += "    |                          |                          |\n"
        string += "6   |       [{}]---------------[{}]---------------[{}]       |\n".format(self.board[8],
                                                                                            self.board[9],
                                                                                            self.board[10])
        string += "    |        |                 |                 |        |\n"
        string += "    |        |                 |                 |        |\n"
        string += "5   |        |        [{}]-----[{}]-----[{}]        |        |\n".format(self.board[16],
                                                                                            self.board[17],
                                                                                            self.board[18])
        string += "    |        |         |               |         |        |\n"
        string += "    |        |         |               |         |        |\n"
        string += "4  [{}]------[{}]-------[{}]             [{}]-------[{}]------[{}]\n".format(self.board[3],
                                                                                                self.board[11],
                                                                                                self.board[19],
                                                                                                self.board[20],
                                                                                                self.board[12],
                                                                                                self.board[4])
        string += "    |        |         |               |         |        |\n"
        string += "    |        |         |               |         |        |\n"
        string += "3   |        |        [{}]-----[{}]-----[{}]        |        |\n".format(self.board[21],
                                                                                            self.board[22],
                                                                                            self.board[23])
        string += "    |        |                 |                 |        |\n"
        string += "    |        |                 |                 |        |\n"
        string += "2   |       [{}]---------------[{}]---------------[{}]       |\n".format(self.board[13],
                                                                                            self.board[14],
                                                                                            self.board[15])
        string += "    |                          |                          |\n"
        string += "    |                          |                          |\n"
        string += "1  [{}]------------------------[{}]------------------------[{}]\n\n".format(self.board[5],
                                                                                               self.board[6],
                                                                                               self.board[7])
        string += "    a        b         c       d        e        f        g\n"
        return string


class GameState:
    MAX_DEPTH = None

    def __init__(self, board_game, current_player, depth, parent=None, score=None):
        self.board_game = board_game
        self.current_player = current_player
        self.depth = depth
        self.parent = parent
        self.score = score

        # list of possible moves from the current state
        self.possible_moves = []

        # the best move from the list of possible moves for the current player
        self.chosen_state = None

    def opponent(self):
        if self.current_player == Game.JMIN:
            return Game.JMAX
        else:
            return Game.JMIN

    def state_moves(self):
        l_moves = self.board_game.game_moves(self.current_player)
        opponent = self.opponent()
        l_state_moves = [GameState(move, opponent, self.depth - 1, parent=self) for move in l_moves]

        return l_state_moves

    def __str__(self):
        string = str(self.board_game) + "(Current player: " + self.current_player + ")"
        return string


""" MinMax Algorithm """


def min_max(state):
    if state.depth == 0 or state.board_game.final():
        state.score = state.board_game.estimate_score(state.depth)
        return state

    # calculate all possible moves from the current state
    state.possible_moves = state.state_moves()

    # apply the minimax algorithm to all possible moves (thus calculating their subtrees)
    moves_score = [min_max(move) for move in state.possible_moves]

    if state.current_player == Game.JMAX:
        # if the player is JMAX I choose the state with the maximum score
        state.chosen_state = max(moves_score, key=lambda x: x.score)
    else:
        # if the player is JMIN I choose the state with the minimum score
        state.chosen_state = min(moves_score, key=lambda x: x.score)

    state.score = state.chosen_state.score
    return state


""" Alpha-Beta Algorithm """


def alpha_beta(alpha, beta, state):
    if state.depth == 0 or state.board_game.final():
        state.score = state.board_game.estimate_score(state.depth)
        return state

    if alpha >= beta:
        return state

    state.possible_moves = state.state_moves()

    if state.current_player == Game.JMAX:
        current_score = float('-inf')

        for move in state.possible_moves:
            new_state = alpha_beta(alpha, beta, move)

            if current_score < new_state.score:
                state.chosen_state = new_state
                current_score = new_state.score

            if alpha < new_state.score:
                alpha = new_state.score
                if alpha >= beta:
                    break

    elif state.current_player == Game.JMIN:
        current_score = float('inf')

        for move in state.possible_moves:
            new_state = alpha_beta(alpha, beta, move)

            if current_score > new_state.score:
                state.chosen_state = new_state
                current_score = new_state.score

            if beta > new_state.score:
                beta = new_state.score
                if alpha >= beta:
                    break

    state.score = state.chosen_state.score

    return state


def print_if_final(current_state):
    final = current_state.board_game.final()
    if final:
        print("The winner: " + final)
        print("User's final score: ", current_state.board_game.board.count(Game.JMIN))
        print("Computer's final score: ", current_state.board_game.board.count(Game.JMAX))
        return True
    return False


def main():
    # Algorithm initialization
    valid_answer = False
    while not valid_answer:
        algorithm_type = input("Choose an algorithm:\n1. Minimax\n2. Alpha-beta\n")

        if algorithm_type in ['1', '2']:
            valid_answer = True
        else:
            print("You did not choose a valid option.")

    # Players initialization
    [s1, s2] = Game.SYMBOLS_PLAYERS.copy()
    valid_answer = False
    while not valid_answer:
        Game.JMIN = str(input("Do you want to play with {} or {}? ".format(s1, s2))).upper()

        if Game.JMIN in Game.SYMBOLS_PLAYERS:
            valid_answer = True
        else:
            print("You have to choose between {} and {}.".format(s1, s2))
    Game.JMAX = s1 if Game.JMIN == s2 else s2

    # Max-depth initialization
    valid_answer = False
    while not valid_answer:
        level = input("Level of difficulty: (Beginner/Medium/Advanced) ")

        if level.lower() in ["beginner", "medium", "advanced"]:
            GameState.MAX_DEPTH = 1 if level == "beginner" else 3 if level == "medium" else 5
            valid_answer = True
        else:
            print("Invalid level of difficulty.")

    # Evaluation
    global EVALUATION
    valid_answer = False
    while not valid_answer:
        evaluation = input("Choose an evaluation method:\n1. Heuristic that looks at the number of pieces on the board"
                           "\n2. The middle square has priority"
                           "\n3. Heuristic that looks at the number of potential mills on the board\n")
        if evaluation in ['1', '2', '3']:
            valid_answer = True
            EVALUATION = int(evaluation)
        else:
            print("You did not choose a valid option.")

    # Board initialization
    current_table = Game()
    print("\nInitial board")
    print(str(current_table))

    # Create initial state
    current_state = GameState(current_table, Game.SYMBOLS_PLAYERS[0], GameState.MAX_DEPTH)

    exit_option = False
    while not exit_option:
        global moves
        global jmin_moves
        global jmax_moves

        if current_state.current_player == Game.JMIN:
            """ Users's move """
            print("USER'S TURN...")

            start_t = int(round(time.time() * 1000))

            if moves < 18:
                """ Phase 1: Placing pieces. """

                valid_answer = False
                while not valid_answer:

                    try:
                        new_pos = input("Place one piece (exit if done): ")

                        if new_pos.lower() == "exit":
                            exit_option = True
                            break

                        if current_state.board_game.board[board_dictionary[new_pos]] == Game.EMPTY:
                            valid_answer = True
                        else:
                            print("There is already a piece there")

                    except Exception:
                        print("Couldn't get the input value")

            else:
                """ Phase 2 or 3 """

                user_has_moved = False
                while not user_has_moved:
                    try:
                        old_pos = input("\nMove '{}' piece (exit if done): ".format(Game.JMIN))

                        if old_pos.lower() == "exit":
                            exit_option = True
                            break

                        while current_state.board_game.board[board_dictionary[old_pos]] != Game.JMIN:
                            old_pos = input("\nMove '{}' piece: ".format(Game.JMIN))

                        while Game.EMPTY not in [current_state.board_game.board[i] for i in
                                                 adjacentLocations(board_dictionary[old_pos])]:
                            old_pos = int(input("\nYou can't move this piece, it is blocked. Choose another one: "))

                        user_has_placed = False
                        while not user_has_placed:
                            new_pos = input("New position: ")

                            if current_state.board_game.board.count(Game.JMIN) != 3:
                                """ Phase 2: Moving pieces.
                                    User can move a man to an adjacent point.
                                """

                                if current_state.board_game.board[board_dictionary[new_pos]] == Game.EMPTY \
                                        and board_dictionary[new_pos] in adjacentLocations(board_dictionary[old_pos]):

                                    current_state.board_game.board[board_dictionary[old_pos]] = Game.EMPTY

                                    user_has_placed = True
                                    user_has_moved = True

                                else:
                                    print("You cannot move there")

                            else:
                                """ Phase 3: Moving pieces anywhere.
                                    User can move a man to an any point.
                                """

                                if current_state.board_game.board[board_dictionary[new_pos]] == Game.EMPTY:
                                    current_state.board_game.board[board_dictionary[old_pos]] = Game.EMPTY

                                    user_has_placed = True
                                    user_has_moved = True

                                else:
                                    print("You cannot move there")

                    except Exception:
                        print("You cannot move there")

            if exit_option is True:
                if current_state.board_game.heuristic() == 0:
                    print("\nDraw!")
                elif current_state.board_game.heuristic() < 0:
                    print("\nYou won!")
                else:
                    print("\nYou lost!")
                print("User's score:", current_state.board_game.board.count(Game.JMIN))
                print("Computer's score:", current_state.board_game.board.count(Game.JMAX))
                break

            current_state.board_game.board[board_dictionary[new_pos]] = Game.JMIN

            print("\nThe board after user's move")
            print(str(current_state))

            moves += 1
            jmin_moves += 1

            if checkMill(board_dictionary[new_pos], Game.JMIN, current_state.board_game.board):
                user_has_removed = False

                # If user has formed a mill he can remove a jmax-piece
                jmin_moves += 1

                while not user_has_removed:
                    try:
                        pos = input("\nRemove one piece: ")

                        if current_state.board_game.board[board_dictionary[pos]] == Game.JMAX \
                                and not checkMill(board_dictionary[pos], Game.JMAX, current_state.board_game.board) \
                                or (checkMill(board_dictionary[pos], Game.JMAX, current_state.board_game.board)
                                    and current_state.board_game.board.count(Game.JMIN) == 3):

                            current_state.board_game.board[board_dictionary[pos]] = Game.EMPTY
                            user_has_removed = True

                        else:
                            print("Invalid position")

                    except Exception:
                        print("Error while accepting input")

                print("\nThe board after removing one piece")
                print(str(current_state))

            end_t = int(round(time.time() * 1000))
            print("User's thinking time: " + str(end_t - start_t) + " milliseconds.\n")

            if print_if_final(current_state):
                break

            current_state.current_player = current_state.opponent()

        else:
            print("COMPUTER'S TURN...")

            start_t = int(round(time.time() * 1000))
            if algorithm_type == '1':
                updated_state = min_max(current_state)
            else:
                updated_state = alpha_beta(-5000, 5000, current_state)
            updated_state_jmin_pieces = updated_state.board_game.board.count(Game.JMIN)

            current_state.board_game = updated_state.chosen_state.board_game
            print("\nThe board after computer's move")
            print(str(current_state))

            moves += 1
            jmax_moves += 1

            # If the current state has fewer jmin-pieces than the previous state,
            # it means that the computer has removed one of the user's pieces
            if current_state.board_game.board.count(Game.JMIN) < updated_state_jmin_pieces:
                jmax_moves += 1

            end_t = int(round(time.time() * 1000))

            print("Computer's thinking time: " + str(end_t - start_t) + " milliseconds.\n")

            if print_if_final(current_state):
                break

            current_state.current_player = current_state.opponent()


if __name__ == "__main__":
    start = int(round(time.time() * 1000))
    main()
    end = int(round(time.time() * 1000))
    print("\nRuntime: " + str(end - start) + " milliseconds.")
    print("User's moves:", jmin_moves)
    print("Computer's moves:", jmax_moves)
