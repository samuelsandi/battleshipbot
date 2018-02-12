import argparse
import json
import os
import time
import sys
import ast
from random import choice

command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
output_path = '.'
map_size = 0

#--------GREEDY---------#

def greedy(targets,opponent_map):
    for (x,y) in targets:
        if (x+y) % 2 == 0: #parity
            return x,y
        else: #find cell that is near Damaged cell
            for cell in opponent_map:
                x_a = cell['X']
                y_a = cell['Y']
                if (((x_a == x - 1) or (x_a == x + 1)) and (y_a == y)) or (((y_a == y + 1) or (y_a == y - 1)) and (x_a == x)):
                    if cell['Damaged']:
                        return x,y
    #kalau ngga ada ya udah, pake random
    return choice(targets)

#--------GREEDY---------#


def main(player_key):
    global map_size
    # Retrieve current game state
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)
    map_size = state['MapDimension']
    if state['Phase'] == 1:
        place_ships()
    else:
        shiplength = [] #list of panjang kapal yang belum ketembak
        for ship in state['OpponentMap']['Ships']:
            if not ship['Destroyed']:
                if ship['ShipType'] == 'Destroyer':
                    shiplength.append(2)
                elif ship['ShipType'] == 'Cruiser':
                    shiplength.append(3)
                elif ship['ShipType'] == 'Submarine':
                    shiplength.append(3)
                elif ship['ShipType'] == 'Battleship':
                    shiplength.append(4)
                elif ship['ShipType'] == 'Carrier':
                    shiplength.append(5)

        fire_shot(state['OpponentMap']['Cells'])


def output_shot(x, y):
    move = 1  # 1=fire shot command code
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass

def fire_shot(opponent_map):
    # To send through a command please pass through the following <code>,<x>,<y>
    # Possible codes: 1 - Fireshot, 0 - Do Nothing (please pass through coordinates if
    #  code 1 is your choice)
    targets = []
    for cell in opponent_map:
        if not cell['Damaged'] and not cell['Missed']:
            valid_cell = cell['X'], cell['Y']
            targets.append(valid_cell)

    while not os.path.exists(sys.path[0] + 'tes.txt'):
        time.sleep(1)

    if os.path.isfile(sys.path[0] + 'tes.txt'):
        # read file
        with open(os.path.join(sys.path[0], 'tes.txt'), 'r') as f_out:
            f_out.read(literal_eval(target))
        pass

    x = target[0]
    y = target[1]

    for cell in opponent_map:
        if x == cell['X'] and y == cell['Y']:
            if cell['Damaged']:
                status = 'Menembak'
            elif cell['Missed']:
                status = 'Mencari'
                # hapus koordinat

    target = greedy(targets,opponent_map)

    with open(os.path.join(sys.path[0], 'tes.txt'), 'a+') as f_out:
        f_out.write(str(target))
        f_out.write('\n')
    pass

    output_shot(*target)
    return


def place_ships():
    # Please place your ships in the following format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west

    ships =[
        'Battleship 1 0 north',
        'Carrier 3 1 East',
        'Cruiser 4 2 north',
        'Destroyer 7 3 north',
        'Submarine 1 8 East'
    ]

    with open(os.path.join(output_path, place_ship_file), 'w') as f_out:
        for ship in ships:
            f_out.write(ship)
            f_out.write('\n')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PlayerKey', nargs='?', help='Player key registered in the game')
    parser.add_argument('WorkingDirectory', nargs='?', default=os.getcwd(), help='Directory for the current game files')
    args = parser.parse_args()
    assert (os.path.isdir(args.WorkingDirectory))
    output_path = args.WorkingDirectory
    main(args.PlayerKey)
