#encoding: utf-8

endgame_list = open('endgame_list.txt').read().splitlines()

endgame_html = open('endgame.part3.me/endgame.html', 'wb')
endgame_filter_html = open('endgame.part3.me/endgame_filter.html', 'wb')
endgame_private_html = open('endgame.part3.me/endgame_private.html', 'wb')
endgame_filter_private_html = open('endgame.part3.me/endgame_filter_private.html', 'wb')

def is_good_game(fen):

    # both sides has no knight
    if 'n' in line or "N" in line:
        return False

    # the winning side cannot have pawn
    if fen.endswith('b') and 'p' in fen:
        return False

    if fen.endswith('w') and 'P' in fen:
        return False

    return True

for i in range(len(endgame_list)):

    line = endgame_list[i]
    index = i + 1

    endgame_html.write('%s. <a href="http://www.chessdb.cn/query/?%s" target="_blank">%s</a><br />\n'\
    % (index, line, line))

    endgame_private_html.write('%s. <a href="http://chess.frp.part3.me#%s" target="_blank">%s</a><br />\n'\
    % (index, line, line)
    )

    if is_good_game(line):

        endgame_filter_html.write('%s. <a href="http://www.chessdb.cn/query/?%s" target="_blank">%s</a><br />\n'\
        % (index, line, line))

        endgame_filter_private_html.write('%s. <a href="http://chess.frp.part3.me#%s" target="_blank">%s</a><br />\n'\
        % (index, line, line)
        )

endgame_html.close()
endgame_filter_html.close()
endgame_private_html.close()
endgame_filter_private_html.close()
