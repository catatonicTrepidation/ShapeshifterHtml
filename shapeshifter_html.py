from bs4 import BeautifulSoup
import re

# pieces information (Counter)
pieces_to_ints = dict()


def get_shapeshifter_config(filename):
    create_dict()

    with open(filename, encoding="utf8") as f:
        read_data = f.read()
    soup = BeautifulSoup(read_data, 'html.parser')

    cycle, goalpiece = update_dict_and_get_cycle(pieces_to_ints, soup)

    # this happens after update_dict and not before in order to get proper cycle numbers
    board = fetch_board_state(soup)

    final_pieces = []
    board_size = len(board)

    add_active_piece(soup, final_pieces, board_size)
    final_pieces = add_other_shape_pieces(soup, final_pieces, board_size)

    #print(final_pieces)
    return board, final_pieces, cycle, goalpiece


def create_dict():
    pieces_to_ints['gob_0'] = 0
    pieces_to_ints['gau_0'] = 0
    pieces_to_ints['swo_0'] = 0
    pieces_to_ints['cro_0'] = 0
    return pieces_to_ints


def update_dict_and_get_cycle(pieces_to_ints, soup):
    cycle_snapshot = soup.select(
        'td.content > center:nth-of-type(2) > table > tbody > tr > td > table > tbody > tr')

    # string format of all the different cycle images
    picturetypes = str(cycle_snapshot)

    cycle_images = []

    img_indices = [m.start() for m in re.finditer('.gif', picturetypes)]

    # identify goal piece
    goalpiecesnippet = [m.start() for m in re.finditer('GOAL', picturetypes)]
    goalpiecelines = picturetypes[goalpiecesnippet[0]-100:goalpiecesnippet[0]+4]
    goalpieceindex = [m.start() for m in re.finditer('.gif', goalpiecelines)]
    goalpiece = goalpiecelines[goalpieceindex[0]-5:goalpieceindex[0]]

    # index - 5 because all the picture names are in format xxx_x.gif
    # skip all odd indexes because they are "arrow.gif"
    for i in range(0, len(img_indices)-1, 2):
        shapegif = picturetypes[img_indices[i] - 5:img_indices[i]]
        # print(picturetypes[img_indices[i] - 5:])
        # if ('GOAL' in picturetypes[img_indices[i]:]):
        #     print(shapegif)
        cycle_images.append(shapegif)
    # length-1 because the last pic is the same as the first

    shapecount = 0;
    for shapepic in cycle_images:
        pieces_to_ints[shapepic] = shapecount
        shapecount = shapecount + 1
    # print(pieces_to_ints)
    cycle = []
    for i in range(len(cycle_images)):
        cycle.append(pieces_to_ints[cycle_images[i]])
        if (cycle_images[i] == goalpiece):
            goalpiece = i

    # print(cycle)
    return cycle, goalpiece


def fetch_board_state(soup):
    board_html = soup.select('td.content > table > tbody  tr')
    board = []

    for row in board_html:
        img_indices = [m.start() for m in re.finditer('.gif', str(row))]
        board.append(tuple(pieces_to_ints[str(row)[idx - 5:idx]] for idx in img_indices))

    board = tuple(board)

    return board


def add_active_piece(soup, final_pieces, board_size):
    #  need to get ACTIVE SHAPE separately
    active_shape_rows = soup.select(
        'td.content > center:nth-of-type(3) > table > tbody > tr > td > table > tbody > tr')

    cur_piece = []
    cp_dim = [0, 0]
    for pr in active_shape_rows:
        cur_row = []
        td_list = BeautifulSoup(str(pr), 'html.parser').findAll('td', recursive=True)
        for td in td_list:
            if 'img' in str(td):
                cur_row.append(1)
            else:
                cur_row.append(0)
        cp_dim[0] = max(cp_dim[0], len(cur_row))
        cur_row.extend((0,) * (board_size - len(cur_row)))
        cur_piece.append(tuple(cur_row))
    cp_dim[1] = max(cp_dim[1], len(cur_piece))
    cur_piece.extend([(0,) * board_size for _ in range(board_size - len(cur_piece))])  # add empty row(s)
    final_pieces.append(tuple((cp_dim, cur_piece)))


def add_other_shape_pieces(soup, final_pieces, board_size):
    #border="0", cellpadding="0", cellspacing="0"
    tables = soup.find_all(attrs={"border": 0, "cellpadding": 0, "cellspacing": 0})

    # 1st piece is javascript table logic for the game board
    # 2nd piece is current piece
    shapes = tables[2:]

    for shape in shapes:
        cur_piece = []
        cp_dim = [0, 0]
        piece_rows = BeautifulSoup(str(shape), 'html.parser').findAll('tr', recursive=True)
        for pr in piece_rows:
            cur_row = []
            td_list = BeautifulSoup(str(pr), 'html.parser').findAll('td', recursive=True)
            for td in td_list:
                if 'img' in str(td) and 'http://images.neopets.com/medieval/shapeshifter/square.gif' in str(td):
                    cur_row.append(1)
                else:
                    cur_row.append(0)
            cp_dim[0] = max(cp_dim[0], len(cur_row))

            # piece dimensions
            cur_row.extend((0,) * (board_size - len(cur_row)))
            cur_piece.append(tuple(cur_row))
        cp_dim[1] = max(cp_dim[1], len(cur_piece))

        # add empty row(s)
        cur_piece.extend([(0,) * board_size for _ in range(board_size - len(cur_piece))])

        final_pieces.append(tuple((cp_dim, cur_piece)))
    final_pieces = tuple(tuple(tuple(row) for row in piece) for piece in final_pieces)
    return final_pieces

def test_shapeshifter_html(filename):
    board, pieces, cycle, goalpiece = get_shapeshifter_config(filename)
    #Print Board
    print("Board: ")
    for row in board:
        print(row)
    print()

    #Gets Pieces
    count = 1
    for sizenxn, board in pieces:
        print("piece ", count, " size: ", sizenxn)
        for row in board:
            print(row)
        print()
        count = count + 1

    print("Cycle: ", cycle)
    print()
    print("Goal Piece: ", goalpiece)
    print('----------')
# uncomment to test this file
#test_shapeshifter_html('htmllevels/level29.html')

#test_shapeshifter_html('htmllevels/level1.html')