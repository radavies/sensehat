from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
board = [[0 for x in range(8)] for y in range(8)]
white = (255, 255, 255)
black = (0, 0, 0)
pattern_index = 0
last_timestamp = 0


def run():
    global last_timestamp
    delay = 0.5
    start_up_ani()
    init()
    change_pattern(True)
    update()
    sleep(delay)

    while True:
        step()
        update()
        events = sense.stick.get_events()
        if len(events) > 0:
            event = events[0]
            # Debounce events
            if event.timestamp - last_timestamp > delay:
                if event.direction is "right":
                    change_pattern(True)
                elif event.direction is "left":
                    change_pattern(False)
            last_timestamp = event.timestamp
        sleep(delay)


def init():
    global board
    for x in range(0, 8):
        for y in range(0, 8):
            board[x][y] = False


def joystick_right():
    change_pattern(True)


def joystick_left():
    change_pattern(False)


def change_pattern(forward):

    global pattern_index
    if forward:
        pattern_index += 1
        if pattern_index > 7:
            pattern_index = 1
    else:
        pattern_index -= 1
        if pattern_index < 1:
            pattern_index = 7
    print(pattern_index)
    init()
    if pattern_index is 1:
        create_glider()
    elif pattern_index is 2:
        create_small_exploder()
    elif pattern_index is 3:
        create_exploder()
    elif pattern_index is 4:
        create_spaceship()
    elif pattern_index is 5:
        create_blinkers()
    elif pattern_index is 6:
        create_toad()
    else:
        create_beacon()


def step():
    global board
    new_board = [[0 for x in range(8)] for y in range(8)]
    for x in range(0, 8):
        for y in range(0, 8):
            # For a space that is populated:
            if board[x][y]:
                neighbors = how_many_neighbors(x, y)
                # Each cell with one or no neighbors dies, as if by solitude.
                # Each cell with four or more neighbors dies, as if by overpopulation.
                if neighbors <= 1 or neighbors >= 4:
                    new_board[x][y] = False
                # Each cell with two or three neighbors survives.
                if neighbors is 2 or neighbors is 3:
                    new_board[x][y] = True
            else:
                # For a space that is empty or unpopulated
                # Each cell with three neighbors becomes populated.
                if how_many_neighbors(x, y) is 3:
                    new_board[x][y] = True

    board = new_board


def how_many_neighbors(x, y):
    global board
    neighbors = 0
    up_ok = False
    down_ok = False
    right_ok = False
    left_ok = False

    if y + 1 <= 7:
        up_ok = True
    if y - 1 >= 0:
        down_ok = True
    if x + 1 <= 7:
        right_ok = True
    if x - 1 >= 0:
        left_ok = True

    if up_ok:
        if board[x][y+1]:
            neighbors += 1
        if left_ok:
            if board[x-1][y+1]:
                neighbors += 1
        if right_ok:
            if board[x+1][y+1]:
                neighbors += 1

    if left_ok:
        if board[x - 1][y]:
            neighbors += 1

    if right_ok:
        if board[x + 1][y]:
            neighbors += 1

    if down_ok:
        if board[x][y-1]:
            neighbors += 1
        if left_ok:
            if board[x-1][y-1]:
                neighbors += 1
        if right_ok:
            if board[x+1][y-1]:
                neighbors += 1

    return neighbors


def start_up_ani():
    toggle = False
    blue = (0, 90, 255)
    green = (0, 255, 90)
    red = (255, 90, 90)

    delay = 0.015
    for x in range(0, 8):
        if toggle:
            for y in reversed(range(0, 8)):
                sense.set_pixel(x, y, blue)
                sleep(delay)
                toggle = False
        else:
            for y in range(0, 8):
                sense.set_pixel(x, y, blue)
                sleep(delay)
                toggle = True

    for y in range(0, 8):
        if toggle:
            for x in reversed(range(0, 8)):
                sense.set_pixel(x, y, green)
                sleep(delay)
                toggle = False
        else:
            for x in range(0, 8):
                sense.set_pixel(x, y, green)
                sleep(delay)
                toggle = True

    for x in reversed(range(0, 8)):
        if toggle:
            for y in reversed(range(0, 8)):
                sense.set_pixel(x, y, red)
                sleep(delay)
                toggle = False
        else:
            for y in range(0, 8):
                sense.set_pixel(x, y, red)
                sleep(delay)
                toggle = True


def update():
    for x in range(0, 8):
        for y in range(0, 8):
            sense.set_pixel(x, y, white if board[x][y] else black)


def create_glider():
    global board
    board[1][0] = True
    board[2][1] = True
    board[0][2] = True
    board[1][2] = True
    board[2][2] = True


def create_small_exploder():
    global board
    board[4][3] = True
    board[3][4] = True
    board[4][4] = True
    board[5][4] = True
    board[3][5] = True
    board[5][5] = True
    board[4][6] = True


def create_exploder():
    global board
    board[1][1] = True
    board[1][2] = True
    board[1][3] = True
    board[1][4] = True
    board[1][5] = True

    board[5][1] = True
    board[5][2] = True
    board[5][3] = True
    board[5][4] = True
    board[5][5] = True

    board[3][1] = True
    board[3][5] = True


def create_spaceship():
    global board
    board[0][2] = True
    board[0][4] = True

    board[1][1] = True
    board[2][1] = True
    board[3][1] = True
    board[4][1] = True

    board[4][2] = True
    board[4][3] = True

    board[3][4] = True


def create_blinkers():
    global board

    board[1][2] = True
    board[2][2] = True
    board[3][2] = True

    board[5][4] = True
    board[5][5] = True
    board[5][6] = True


def create_toad():

    board[3][3] = True
    board[4][3] = True
    board[5][3] = True

    board[2][4] = True
    board[3][4] = True
    board[4][4] = True


def create_beacon():
    board[2][2] = True
    board[3][2] = True
    board[2][3] = True

    board[5][5] = True
    board[4][5] = True
    board[5][4] = True


sense.clear()
run()
