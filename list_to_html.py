#encoding: utf-8

endgame_list = open('endgame_list.txt').read().splitlines()

endgame_html = open('endgame.part3.me/endgame.html', 'wb')
endgame_private_html = open('endgame.part3.me/endgame_private.html', 'wb')

for line in endgame_list:
    # print(line)
    endgame_html.write('<a href="http://www.chessdb.cn/query/?%s" target="_blank">%s</a><br />\n'\
    % (line, line))

    endgame_private_html.write('<a href="http://chess.frp.part3.me#%s" target="_blank">%s</a><br />\n'\
    % (line, line)
    )

endgame_html.close()
endgame_private_html.close()
