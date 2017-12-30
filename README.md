# fun-endgames
A python script that searches for interesting chess endgames from chessdb.cn

It first fetches endgame list from chessb (http://www.chessdb.cn/egtb_info.html) and then filter the endgams by the following criteria:

1. the length of the moves is longer than 20
2. winning rate < 25%
3. draw rate or lose rate > 60

2013 results are returned.

It can also pull the full best move sequencce from chessdb and convert it to Chinese notation. 
Enjoy.
