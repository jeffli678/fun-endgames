# encoding: utf-8
import requests
import re
import sys
from bs4 import BeautifulSoup

init_fen = '9/4k4/4ba3/3P5/9/9/9/8B/4K4/3A1pB2 w'
# init_fen = '3k5/9/8b/9/9/8R/9/9/9/4K4 w'
rows_count = 10
columns_count = 9

pieces_abbr = 'rnbakcpRNBAKCP'
pieces_name = ur'车马象士将炮卒车马相仕帅炮兵'
piece_map = {}
for i in range(len(pieces_abbr)):
	piece_map[pieces_abbr[i]] = pieces_name[i]

num_map = [u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九']
winning_side = {'w' : u'黑胜', 'b' : u'红胜'}

def board_to_fen(board, move_side):
	fen = []

	for line in board:
		line_str = ''.join(line)
		fen.append(re.sub(r'(\s+)', lambda m: str(len(m.group(0))), line_str))

	fen_str = '/'.join(fen) + ' ' + move_side

	return fen_str

def fen_to_board(fen):

	board = []

	if not fen: fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w"
	move_side = fen[-1]
	if move_side not in ['w', 'b']: move_side = 'w'

	board_str = fen.split(' ')[0]
	rows_str = board_str.split('/')
	if len(rows_str) != rows_count: return board
	
	for row_str in rows_str:
		row = []
		for char in row_str:
			if char.isdigit():
				num = int(char)
				row.extend([' '] * num)
			else:
				row.append(char)

		board.append(row)

	return (board, move_side)

def is_red_piece(piece):
	return piece.isupper()

def parse_pos(pos_str):
	column = ord(pos_str[0]) - ord('a')
	row = rows_count - 1 - int(pos_str[1])
	return [row, column]

def piece_action(piece_abbr, start_row, end_row):
	# not the row is the board row. not the natural wor
	action = ''
	is_red = is_red_piece(piece_abbr)

	if start_row == end_row:
		action = u'平'
	elif start_row < end_row:
		if is_red:
			action = u'退'
		else:
			action = u'进'
	else:	
		if is_red:
			action = u'进'
		else:
			action = u'退'

	return action

def get_row_str(piece_abbr, column):

	row_str = str(column + 1)
	if is_red_piece(piece_abbr):
		row_str = num_map[columns_count - 1 - column]

	return row_str

def get_piece_end(piece_abbr, action, start_row, start_column, end_row, end_column):

	piece_end = ''
	if action == u'平' or piece_abbr.lower() in ['n', 'b', 'a']:
		piece_end = get_row_str(piece_abbr, end_column)
	else:
		dist = abs(start_row - end_row)
		if is_red_piece(piece_abbr):
			piece_end = num_map[dist - 1]
		else:
			piece_end = str(dist)

	return piece_end

def parse_move(board, move):

	start = move[:2]
	end = move[2 : 4]

	(start_row, start_column) = parse_pos(start)
	(end_row, end_column) = parse_pos(end)

	piece_abbr = board[start_row][start_column]
	try:
		piece = piece_map[piece_abbr]
	except Exception as e:
		piece = '?'
	

	piece_start = get_row_str(piece_abbr, start_column)

	action = piece_action(piece_abbr, start_row, end_row)

	piece_end = get_piece_end(piece_abbr, action, start_row, start_column, end_row, end_column)

	move_str = piece + piece_start + action + piece_end

	return move_str

def update_board(board, move):

	start = move[:2]
	end = move[2:4]
	(start_row, start_column) = parse_pos(start)
	(end_row, end_column) = parse_pos(end)
	# update board
	board[end_row][end_column] = board[start_row][start_column]
	board[start_row][start_column] = ' '
	return board

def update_fen(board, move_side):

	if move_side == 'w': next_move_side = 'b'
	if move_side == 'b': next_move_side = 'w'
	new_fen = board_to_fen(board, next_move_side)
	return new_fen

def get_best_move(fen):
	api_path = 'http://api.chessdb.cn:81/chessdb.php?action=querybest&board=%s' % fen
	req = requests.get(api_path)
	if req.status_code == 200:
		return req.content
	else:
		return 'nobestmove'

def get_best_move_seq(fen):

	best_move_seq = []
	board = []
	move_side = ''

	while True:
		best_move = get_best_move(fen)
		# best_move = best_move.strip()
		print(best_move)
		if best_move.startswith('invalid board') or best_move.startswith('unknown'):
			best_move_seq.append('bug')
			return best_move_seq
		else:
			# end of the game
			(board, move_side) = fen_to_board(fen)
			if best_move.startswith('nobestmove'):
				print(winning_side[move_side])
				best_move_seq.append(winning_side[move_side])
				return best_move_seq
				break
			else:
				# move:d6d7
				best_move = best_move[5:]
				move_str = parse_move(board, best_move)
				print(move_str)
				best_move_seq.append(move_str)
				board = update_board(board, best_move)
				fen = update_fen(board, move_side)

def td_to_float(td):
	s = td.string
	s = s[:-1]
	num = float(s)
	return num

def td_to_int(td):
	try:
		ret = int(td.string)
	except:
		ret = 0
	return ret

def is_fun_pos(win_rate, draw_rate, lose_rate, fen, longest_len):

	if longest_len < 20:
		return False

	if win_rate < 25 and (draw_rate > 60 or lose_rate > 60 ):
		return True

	return False

# move_seq = get_best_move_seq(init_fen)
# for move in move_seq:
# 	print(move)

# endgame_page = requests.get('http://www.chessdb.cn/egtb_info.html')
# if endgame_page.status_code != 200:
# 	print('fail to get endgame list')
# 	sys.exit(0)

# <td class="la">KPKP</td>
# <td class="la">兵 vs 卒</td>
# <td>2.19%</td>
# <td>95.19%</td>
# <td>2.62%</td>
# <td class="la"><a href="http://www.chessdb.cn/?9/9/5k3/6p2/5P3/9/9/9/9/4K4%20w" target="_blank">9/9/5k3/6p2/5P3/9/9/9/9/4K4 w</a></td>
# <td id="la">3</td>
# <td class="la"><a href="http://www.chessdb.cn/?9/9/4k4/9/9/9/4P1p2/5K3/9/9%20b" target="_blank">9/9/4k4/9/9/9/4P1p2/5K3/9/9 b</a></td>
# <td id="la">3</td>
# <td>175905</td>

endgame_page = open('endgame_dtc.html').read()
endgame_html = BeautifulSoup(endgame_page, 'html.parser')
lines = endgame_html.find_all('tr')
# print(len(lines)) ==> 7986

fun_pos = []

for line in lines[1 : ]:
	td_list = line.find_all('td')
	win_rate = td_to_float(td_list[2])
	draw_rate = td_to_float(td_list[3])
	lose_rate = td_to_float(td_list[4])

	red_longest_fen = td_list[5].string
	red_len = td_to_int(td_list[6])
	black_longest_fen = td_list[7].string
	black_len = td_to_int(td_list[8])

	if is_fun_pos(win_rate, draw_rate, lose_rate, red_longest_fen, red_len):
		fun_pos.append(red_longest_fen)

	if is_fun_pos(lose_rate, draw_rate, win_rate, black_longest_fen, black_len):
		fun_pos.append(black_longest_fen)

# 2013
print(len(fun_pos))		
for pos in fun_pos:
	print(pos)


