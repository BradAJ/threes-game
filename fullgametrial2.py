import numpy as np
from threes import ThreesBoard

brd0 = np.array([[3, 1, 1, 0],
       [1, 0, 0, 0],
       [2, 0, 3, 3],
       [0, 2, 3, 0]])

game0 = ThreesBoard(brd)

moves0 = [('u', 1, 1),
 ('d', 2, 2),
 ('u', 2, 3),
 ('d', 2, 0),
 ('u', 1, 2),
 ('l', 1, 0),
 ('r', 2, 0),
 ('r', 1, 3),
 ('l', 3, 0),
 ('d', 2, 0),
 ('d', 2, 3),
 ('u', 3, 1),
 ('r', 1, 2),
 ('d', 3, 0),
 ('u', 3, 0),
 ('d', 1, 3),
 ('u', 1, 2),
 ('r', 3, 2),
 ('l', 2, 2),
 ('d', 2, 0),
 ('u', 2, 3),
 ('l', 3, 2),
 ('r', 3, 3),
 ('l', 1, 3),
 ('r', 3, 0),
 ('d', 1, 1),
 ('u', 2, 3),
 ('d', 2, 0),
 ('r', 1, 3),
 ('l', 1, 1),
 ('r', 1, 0),
 ('l', 3, 3),
 ('u', 3, 0),
 ('r', 2, 3),
 ('d', 3, 0),
 ('u', 1, 3),
 ('l', 3, 1),
 ('d', 2, 1),
 ('r', 2, 2),
 ('l', 2, 1),
 ('d', 1, 1),
 ('u', 2, 1),
 ('r', 1, 1),
 ('l', 3, 0),
 ('r', 1, 2),
 ('d', 3, 0),
 ('d', 2, 3),
 ('l', 3, 1),
 ('u', 1, 0),
 ('r', 2, 3),
 ('l', 3, 1),
 ('r', 1, 1),
 ('l', 2, 2),
 ('d', 3, 2),
 ('u', 2, 3),
 ('r', 3, 2),
 ('l', 6, 3),
 ('u', 2, 3),
 ('l', 1, 3),
 ('r', 3, 0),
 ('l', 1, 1),
 ('r', 2, 1),
 ('l', 3, 2),
 ('r', 1, 3),
 ('r', 2, 3),
 ('u', 3, 3),
 ('l', 3, 1),
 ('d', 2, 3),
 ('r', 2, 1),
 ('d', 2, 1),
 ('l', 3, 1),
 ('u', 3, 3),
 ('d', 1, 3),
 ('u', 1, 3),
 ('r', 1, 0),
 ('d', 1, 2),
 ('l', 3, 2),
 ('r', 12, 0),
 ('u', 1, 0),
 ('d', 2, 3),
 ('u', 2, 1),
 ('l', 3, 2),
 ('r', 1, 3),
 ('r', 3, 3),
 ('u', 2, 3),
 ('d', 1, 1),
 ('u', 1, 0),
 ('r', 3, 2),
 ('d', 2, 3),
 ('l', 2, 1),
 ('l', 1, 1),
 ('u', 2, 0),
 ('l', 3, 3),
 ('r', 3, 3),
 ('d', 2, 3),
 ('u', 3, 3),
 ('l', 6, 0),
 ('u', 1, 2),
 ('d', 1, 1),
 ('r', 1, 2),
 ('u', 3, 1),
 ('r', 2, 0),
 ('l', 2, 3),
 ('l', 3, 2),
 ('d', 1, 3),
 ('l', 2, 3),
 ('u', 3, 3),
 ('r', 2, 0),
 ('l', 1, 3),
 ('r', 1, 3),
 ('d', 3, 2),
 ('l', 3, 3),
 ('u', 2, 3),
 ('r', 1, 0),
 ('l', 3, 2),
 ('u', 6, 1),
 ('r', 2, 3),
 ('d', 2, 1),
 ('u', 1, 2),
 ('d', 2, 3),
 ('l', 1, 0),
 ('r', 3, 2),
 ('l', 2, 3),
 ('l', 3, 3),
 ('d', 1, 3),
 ('r', 1, 2),
 ('u', 3, 1),
 ('d', 3, 0),
 ('r', 24, 0),
 ('u', 2, 2),
 ('d', 2, 1),
 ('u', 1, 0),
 ('l', 3, 2),
 ('l', 3, 3),
 ('d', 2, 2),
 ('r', 3, 1),
 ('l', 2, 1),
 ('u', 1, 3),
 ('l', 1, 3),
 ('d', 1, 0),
 ('d', 2, 3),
 ('u', 3, 3),
 ('d', 2, 0),
 ('d', 1, 3),
 ('u', 1, 0),
 ('r', 3, 3),
 ('u', 2, 0),
 ('d', 3, 1),
 ('u', 1, 1),
 ('l', 2, 3),
 ('u', 1, 3),
 ('l', 3, 2),
 ('d', 2, 3),
 ('r', 1, 3),
 ('d', 1, 3),
 ('u', 3, 3),
 ('d', 3, 0),
 ('r', 6, 3),
 ('d', 1, 3),
 ('l', 2, 1),
 ('r', 3, 1),
 ('u', 2, 3),
 ('l', 1, 0),
 ('d', 3, 0),
 ('r', 2, 1),
 ('d', 2, 2),
 ('l', 3, 0),
 ('u', 2, 3),
 ('r', 2, 0),
 ('d', 3, 2),
 ('u', 1, 0),
 ('r', 1, 3),
 ('u', 3, 0)]


arr20221115 = np.array([[0,1,2,768],[0,2,3,3],[0,0,3,0],[0,1,0,2]])
#game20221115 = ThreesAgent(arr20221115)

moves20221115 = [('l', 2, 2),
 ('r', 3, 0),
 ('l', 1, 2),
 ('r', 1, 3),
 ('l', 1, 0),
 ('r', 2, 0),
 ('d', 2, 1),
 ('u', 3, 0),
 ('d', 3, 3),
 ('l', 2, 2),
 ('r', 1, 3),
 ('u', 2, 3),
 ('d', 3, 0),
 ('u', 1, 1),
 ('d', 1, 3),
 ('l', 3, 2),
 ('u', 3, 3),
 ('l', 3, 0),
 ('u', 2, 3),
 ('d', 3, 3),
 ('u', 1, 2),
 ('l', 1, 3),
 ('d', 2, 3),
 ('l', 2, 3),
 ('r', 3, 3),
 ('l', 1, 3),
 ('r', 1, 1),
 ('l', 2, 0),
 ('r', 1, 0),
 ('d', 2, 0),
 ('l', 1, 0),
 ('u', 96, 0),
 ('r', 3, 0),
 ('d', 2, 3),
 ('u', 2, 2),
 ('r', 3, 0),
 ('u', 3, 1),
 ('l', 1, 1),
 ('r', 2, 2),
 ('u', 1, 0),
 ('d', 3, 0),
 ('r', 1, 1),
 ('u', 2, 2),
 ('d', 1, 3),
 ('r', 3, 3),
 ('u', 96, 3),
 ('d', 3, 0),
 ('l', 2, 3),
 ('r', 3, 0),
 ('l', 3, 2),
 ('r', 1, 0),
 ('d', 2, 3),
 ('r', 2, 1),
 ('u', 1, 0),
 ('d', 2, 2),
 ('u', 2, 0),
 ('d', 1, 0),
 ('r', 2, 1),
 ('l', 1, 2),
 ('u', 3, 0),
 ('d', 1, 0),
 ('r', 1, 3),
 ('u', 3, 3),
 ('l', 3, 0),
 ('d', 3, 1),
 ('r', 12, 3),
 ('l', 2, 3),
 ('r', 3, 1),
 ('d', 1, 0),
 ('r', 3, 0),
 ('l', 3, 1),
 ('u', 1, 3),
 ('l', 1, 0),
 ('d', 2, 3),
 ('l', 2, 3),
 ('u', 1, 1),
 ('r', 2, 0),
 ('d', 3, 0),
 ('l', 2, 3),
 ('u', 1, 2),
 ('d', 3, 0),
 ('d', 2, 0),
 ('r', 1, 3),
 ('l', 3, 1),
 ('r', 2, 0),
 ('u', 3, 0),
 ('l', 1, 3),
 ('r', 3, 0),
 ('d', 1, 2),
 ('r', 2, 0),
 ('u', 2, 1),
 ('u', 1, 0),
 ('l', 3, 3),
 ('u', 2, 3),
 ('r', 2, 0),
 ('d', 3, 1),
 ('u', 2, 2),
 ('r', 1, 3),
 ('d', 1, 3),
 ('u', 2, 0),
 ('d', 3, 0),
 ('d', 1, 0),
 ('u', 24, 1),
 ('r', 3, 0),
 ('r', 3, 0),
 ('l', 3, 0),
 ('d', 2, 1),
 ('r', 3, 0),
 ('r', 1, 0),
 ('r', 2, 0),
 ('l', 1, 0),
 ('l', 1, 0),
 ('l', 2, 0)]

arr20221116 = np.array([[1,0,0,768],[3,3,0,2],[1,0,0,0],[2,0,2,3]])
moves20221116 = [('r', 3, 0),
 ('d', 2, 3),
 ('l', 1, 2),
 ('r', 1, 1),
 ('u', 2, 2),
 ('l', 2, 2),
 ('r', 1, 0),
 ('d', 2, 3),
 ('u', 3, 1),
 ('u', 3, 0),
 ('l', 2, 1),
 ('d', 3, 1),
 ('u', 1, 1),
 ('r', 1, 1),
 ('l', 1, 3),
 ('r', 3, 3),
 ('u', 2, 1),
 ('d', 3, 0),
 ('u', 3, 1),
 ('l', 1, 1),
 ('r', 2, 2),
 ('l', 2, 1),
 ('d', 1, 3),
 ('u', 3, 1),
 ('d', 24, 3),
 ('l', 1, 3),
 ('l', 1, 1),
 ('u', 3, 2),
 ('d', 2, 3),
 ('u', 1, 1),
 ('l', 3, 1),
 ('r', 2, 1),
 ('d', 1, 1),
 ('u', 1, 0),
 ('d', 2, 0),
 ('u', 2, 3),
 ('r', 1, 3),
 ('d', 3, 0),
 ('l', 3, 3),
 ('u', 2, 3),
 ('l', 3, 3),
 ('r', 2, 2),
 ('l', 2, 2),
 ('d', 1, 1),
 ('r', 3, 2),
 ('l', 1, 0),
 ('r', 1, 0),
 ('l', 2, 2),
 ('d', 2, 3),
 ('r', 3, 0),
 ('l', 3, 3),
 ('u', 6, 2),
 ('d', 3, 2),
 ('d', 1, 0),
 ('r', 1, 1),
 ('d', 3, 3),
 ('u', 1, 3),
 ('l', 1, 0),
 ('d', 3, 3),
 ('l', 2, 0),
 ('u', 3, 3),
 ('r', 1, 1),
 ('u', 2, 0),
 ('r', 2, 0),
 ('l', 3, 2),
 ('r', 2, 0),
 ('d', 1, 1),
 ('r', 3, 0),
 ('u', 2, 3),
 ('l', 48, 0),
 ('d', 2, 3),
 ('u', 2, 1),
 ('r', 1, 2),
 ('r', 3, 2),
 ('d', 3, 1),
 ('l', 1, 1),
 ('d', 3, 2),
 ('r', 1, 0),
 ('u', 2, 0),
 ('r', 1, 3),
 ('l', 1, 1),
 ('d', 3, 1),
 ('r', 2, 3),
 ('r', 2, 0),
 ('r', 3, 0),
 ('u', 3, 3),
 ('r', 1, 3),
 ('l', 1, 0),
 ('d', 2, 3),
 ('d', 2, 3),
 ('u', 3, 0),
 ('u', 1, 0),
 ('l', 1, 2),
 ('d', 1, 3),
 ('l', 1, 3),
 ('l', 2, 3),
 ('d', 3, 3),
 ('l', 2, 3),
 ('u', 3, 3),
 ('l', 3, 3),
 ('r', 2, 3),
 ('u', 2, 0),
 ('l', 3, 2),
 ('u', 2, 1),
 ('d', 2, 2),
 ('l', 12, 1),
 ('d', 3, 3),
 ('r', 3, 0),
 ('d', 3, 3),
 ('d', 3, 0),
 ('u', 1, 0),
 ('l', 1, 3),
 ('d', 2, 2),
 ('l', 1, 0),
 ('u', 1, 3),
 ('l', 2, 1),
 ('u', 2, 0),
 ('r', 2, 2),
 ('d', 24, 0),
 ('u', 1, 2),
 ('r', 3, 0),
 ('l', 2, 3),
 ('u', 3, 3),
 ('r', 2, 0),
 ('d', 1, 3),
 ('u', 1, 3),
 ('l', 3, 3),
 ('l', 1, 3),
 ('u', 3, 1),
 ('r', 3, 3),
 ('d', 6, 1),
 ('l', 2, 3),
 ('d', 2, 1),
 ('l', 3, 3),
 ('r', 1, 1),
 ('d', 1, 0),
 ('l', 2, 3),
 ('u', 3, 3),
 ('d', 2, 2),
 ('u', 1, 0),
 ('d', 1, 0),
 ('u', 3, 1),
 ('l', 2, 2),
 ('u', 1, 3),
 ('u', 3, 3),
 ('r', 3, 2),
 ('l', 1, 3),
 ('d', 3, 0),
 ('d', 1, 3),
 ('u', 1, 3),
 ('l', 3, 2),
 ('u', 2, 2),
 ('r', 2, 3),
 ('d', 2, 3),
 ('d', 3, 3),
 ('d', 3, 3),
 ('r', 1, 0),
 ('d', 2, 3)]



arr20221117 = np.array([[2,3,2,3072],[0,3,12,768],[192,1,12,384],[3,1,3,96]])
moves20221117 = [('u', 3, 1),
 ('d', 3, 0),
 ('l', 2, 1),
 ('u', 3, 1),
 ('d', 1, 1),
 ('l', 1, 0),
 ('d', 1, 3),
 ('r', 3, 2),
 ('d', 2, 3),
 ('l', 3, 2),
 ('r', 2, 0),
 ('d', 2, 3),
 ('l', 1, 0),
 ('d', 1, 0),
 ('r', 3, 0),
 ('u', 3, 3),
 ('l', 2, 1),
 ('r', 1, 3),
 ('u', 2, 0),
 ('u', 48, 0),
 ('l', 2, 2)]