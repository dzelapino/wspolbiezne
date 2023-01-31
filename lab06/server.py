from multiprocessing import Process
import sysv_ipc

key = 13

board = [['-', '-', '-'],
         ['-', '-', '-'],
         ['-', '-', '-']]


class GameStatus:
    pass


class Won(GameStatus):
    def __init__(self, player):
        self.player = player

    def __str__(self):
        return "Wygrana " + self.player


class Tie(GameStatus):
    def __str__(self):
        return "Remis"


class OnGoing(GameStatus):
    pass


def is_input_valid(input1: int, input2: int, play_matrix) -> bool:
    if input1 > 2 or input1 < 0 or input2 > 2 or input2 < 0:
        return False
    if play_matrix[input1][input2] != '-':
        return False
    else:
        return True


def is_game_won(game_board) -> GameStatus | None:
    # DIAGONAL
    if game_board[0][0] == game_board[1][1] == game_board[2][2] != '-':
        return Won(game_board[0][0])
    if game_board[0][2] == game_board[1][1] == game_board[2][0] != '-':
        return Won(game_board[0][0])
    # VERTICAL
    if game_board[0][0] == game_board[1][0] == game_board[2][0] != '-':
        return Won(game_board[0][0])
    if game_board[0][1] == game_board[1][1] == game_board[2][1] != '-':
        return Won(game_board[0][1])
    if game_board[0][2] == game_board[1][2] == game_board[2][2] != '-':
        return Won(game_board[0][2])
    # HORIZONTAL
    if game_board[0][0] == game_board[0][1] == game_board[0][2] != '-':
        return Won(game_board[0][0])
    if game_board[1][0] == game_board[1][1] == game_board[1][2] != '-':
        return Won(game_board[1][0])
    if game_board[2][0] == game_board[2][1] == game_board[2][2] != '-':
        return Won(game_board[2][0])
    return


def is_game_tie(game_board) -> GameStatus | None:
    freeCount = game_board.count('-')
    if freeCount:
        return Tie()


def check_game_status(game_board) -> GameStatus:
    wonStatus = is_game_won(game_board)
    if wonStatus is not None:
        return wonStatus
    tieStatus = is_game_tie(game_board)
    if tieStatus is not None:
        return tieStatus
    return OnGoing()


def move_player(sem, mem, char):
    sem.acquire()
    current_board_state = mem.read()
    current_board_state = current_board_state.decode()
    play_matrix = eval(current_board_state)
    for line in play_matrix:
        print(line)
    print("Plansza:")
    inputStr = input("[0 0, 0 1, 0 2], [1 0, 1 1, 1 2], [2 0, 2 1, 2 2]: ").strip()
    input_array = inputStr.split(' ')
    while not is_input_valid(int(input_array[0]), int(input_array[1]), play_matrix):
        inputStr = input("[0 0, 0 1, 0 2], [1 0, 1 1, 1 2], [2 0, 2 1, 2 2]: ").strip()
        input_array = inputStr.split(' ')
    play_matrix[int(input_array[0])][int(input_array[1])] = char
    mem.write(str(play_matrix))
    return play_matrix


def start_game(play_matrix):
    game_is_active = True
    try:
        mem = sysv_ipc.SharedMemory(key, sysv_ipc.IPC_CREX)
        sem = sysv_ipc.Semaphore(key, sysv_ipc.IPC_CREX, 0o600, 1)
        mem.write(str(play_matrix))
        pierwszy = True
    except sysv_ipc.ExistentialError:
        sem = sysv_ipc.Semaphore(key)
        mem = sysv_ipc.SharedMemory(key)
        pierwszy = False
    while game_is_active:
        if pierwszy:
            play_matrix = move_player(sem, mem, "X")
        else:
            play_matrix = move_player(sem, mem, "O")
        gameStatus = check_game_status(play_matrix)
        if type(gameStatus) != OnGoing:
            print(gameStatus.__str__())
            break
        sem.release()

    mem.remove()
    sem.remove()


start_game(board)
