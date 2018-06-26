from bs4 import BeautifulSoup
import requests
import re


def get_shapeshifter_config():

    pieces_to_ints = dict()
    pieces_to_ints['gob_0'] = 0
    pieces_to_ints['gau_0'] = 0
    pieces_to_ints['swo_0'] = 0
    pieces_to_ints['cro_0'] = 0

    #HTML LEVEL GOES HERE:
    with open('htmllevels/defaultlevel.txt', encoding="utf8") as f:
        read_data = f.read()
    soup = BeautifulSoup(read_data, 'html.parser')

    cycle_images = soup.select('#content > table > tbody > tr > td.content > center:nth-of-type(2) > table > tbody > tr > td > table > tbody > tr')[0]
    img_indices = [m.start() for m in re.finditer('.gif', str(cycle_images))]
    cycle_images = [str(cycle_images)[img_indices[i]-5:img_indices[i]] for i in range(len(img_indices))]

    for i in range(0,5,2):
        pieces_to_ints[cycle_images[i]] = i//2
    print(pieces_to_ints)

    cycle = [pieces_to_ints[cycle_images[i]] for i in range(len(img_indices)) if i%2 == 0 and i < 5]


    board_html = soup.select('#content > table > tbody > tr > td.content > table > tbody tr')

    board = []

    for row in board_html:
        img_indices = [m.start() for m in re.finditer('.gif', str(row))]
        board.append(tuple(pieces_to_ints[str(row)[idx-5:idx]] for idx in img_indices))

    board = tuple(board)

    #need to get ACTIVE SHAPE separately

    BOARD_DIMENSIONS = 4
    final_pieces = []

    #  need to get ACTIVE SHAPE separately
    active_shape_rows = soup.select('#content > table > tbody > tr > td.content > center:nth-of-type(3) > table > tbody > tr > td > table > tbody > tr')
    cur_piece = []
    cp_dim = [0, 0]
    for pr in active_shape_rows:
        cur_row = []
        td_list = BeautifulSoup(str(pr),'html.parser').findAll('td', recursive=True)
        for td in td_list:
            if 'img' in str(td):
                cur_row.append(1)
            else:
                cur_row.append(0)
        cp_dim[0] = max(cp_dim[0], len(cur_row))
        cur_row.extend((0,) * (BOARD_DIMENSIONS - len(cur_row)))
        cur_piece.append(tuple(cur_row))
    cp_dim[1] = max(cp_dim[1], len(cur_piece))
    cur_piece.extend([(0,) * BOARD_DIMENSIONS for _ in range(BOARD_DIMENSIONS - len(cur_piece))])  # add empty row(s)
    final_pieces.append(tuple((cp_dim, cur_piece)))

    # print()
    # print('active_shape_rows =', active_shape_rows)
    # print()


    shapes = soup.select('#content > table > tbody > tr > td.content > center:nth-of-type(3) > center > table > tbody > tr > td')


    for shape in shapes:
        cur_piece = []
        cp_dim = [0,0]
        piece_rows = BeautifulSoup(str(shape),'html.parser').findAll('tr', recursive=True)
        for pr in piece_rows:
            cur_row = []
            td_list = BeautifulSoup(str(pr),'html.parser').findAll('td', recursive=True)
            for td in td_list:
                if 'img' in str(td):
                    cur_row.append(1)
                else:
                    cur_row.append(0)
            cp_dim[0] = max(cp_dim[0], len(cur_row))
            cur_row.extend((0,)*(BOARD_DIMENSIONS - len(cur_row)))
            cur_piece.append(tuple(cur_row))
        cp_dim[1] = max(cp_dim[1], len(cur_piece))

        # add empty row(s)
        cur_piece.extend([(0,)*BOARD_DIMENSIONS for _ in range(BOARD_DIMENSIONS - len(cur_piece))])

        final_pieces.append(tuple((cp_dim, cur_piece)))

    final_pieces = tuple(tuple(tuple(row) for row in piece) for piece in final_pieces)


    return board, final_pieces, cycle


def test_shapeshifter_html():
    board, pieces, cycle = get_shapeshifter_config();

    #Print Board
    print("Board: ")
    for row in board:
        print(row)
    print()

    #Gets Pieces
    count = 1;
    for sizenxn,board in pieces:
        print("piece ", count, ":")
        for row in board:
            print(row);
        print();
        count=count+1;
    print("Cycle: ", cycle)

#test this file
get_shapeshifter_config()