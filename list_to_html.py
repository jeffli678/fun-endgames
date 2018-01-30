#encoding: utf-8

endgame_list = open('endgame_list.txt').read().splitlines()

endgame_html = open('endgame.part3.me/endgame.html', 'wb')
endgame_private_html = open('endgame.part3.me/endgame_private.html', 'wb')

for i in range(len(endgame_list)):

    line = endgame_list[i]
    index = i + 1

    endgame_html.write('%s. <a href="http://www.chessdb.cn/query/?%s" target="_blank">%s</a><br />\n'\
    % (index, line, line))

    endgame_private_html.write('%s. <a href="http://chess.frp.part3.me#%s" target="_blank">%s</a><br />\n'\
    % (index, line, line)
    )

endgame_html.close()
endgame_private_html.close()
