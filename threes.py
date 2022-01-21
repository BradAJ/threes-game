from shutil import move
import numpy as np
from itertools import product

class ThreesEmulator:
    pass

class ThreesBoard:
    def __init__(self, init_arr=None):
        self.values = set([0, 1, 2] + [3 * 2**i for i in range(12)])
        self.move_coords = {'u': [-1,0], 'd':[1,0], 'l':[0,-1], 'r':[0,1]}
        self.match_d = {}
        if init_arr is not None:
            if type(init_arr) is not np.ndarray:
                raise TypeError(f'Unexpected type for init_arr, {type(init_arr)}. Expecting np.ndarray.')
            elif init_arr.shape != (4, 4):
                raise AttributeError(f'init_arr has shape {init_arr.shape}. Expecting (4, 4)')
            elif (set(np.unique(init_arr)) - self.values) != set():
                raise ValueError(f'Non-Threes number seen: {np.unique(init_arr)}')
            else:
                self.board = init_arr
        else:
            #seems consistent in starting with 9 tiles and 7 blanks (zeros)
            #the rest are {1, 2, 3} with equal prob (no starting boost implemented):
            board = np.concatenate([np.zeros(7), np.random.choice([1,2,3], size=9)])
            np.random.shuffle(board)
            self.board = board.reshape([4, 4])


    def get_score(self):
        """self.values scores: {0, 0, 3**1, 3**2, 3**3, ...}"""
        return (3**(np.log2(self.board[self.board >= 3] / 3) + 1)).sum()


    def can_play(self):
        if 0 in self.board:
            return True

        for i in range(4):
            for j in range(4):
                for dir in self.move_coords:
                    if self.__combinable(i, j, dir):
                        return True

        return False


    def __combinable(self, i, j, dir):
        """given coords (i, j) and direction dir {'u', 'd', 'l', 'r'}, would the 
        move result combined tiles"""
        val = self.board[i, j]
        if val == 0:
            return False
        #tiles on edges can't be pushed in one dir
        elif (i, dir) in {(0, 'u'), (3, 'd')} or (j, dir) in {(0, 'l'), (3, 'r')}:
            return False

        di, dj = self.move_coords[dir]
        adj_val = self.board[i + di, j + dj]
        combs = set([val, adj_val])
        if len(combs) != 1 and combs == {1, 2}:
            return True 
        else:
            return False
        
    def move(self, dir, new_val, new_ind):
        """move tiles in direction dir and place a new tile with value new_val at
        location new_ind. (where dir and new_ind together determine the new i,j
        coordinates e.g. ['u', 2] means [3, 2], and ['r', 1] -> [1, 0]).
        
        returns: boolean of 'move successful' """

        new_b = -1 * np.ones([4, 4])
        moved_bool = False
        
        coords = list(product(range(4), range(4)))
        if dir == 'l':
            coords.sort(key=lambda x: x[1])
        elif dir == 'd':
            coords.sort(key=lambda x: -x[0])
        elif dir == 'r':
            coords.sort(key=lambda x: -x[1])
        else: #dir == 'u'
            pass

        first4 = tuple(zip(*coords[:4]))
        new_b[first4] = self.board[first4]
        
        for i, j in coords[4:]:
            val = self.board[i, j]
            if val == 0:
                new_b[i, j] = 0
                moved_bool = True
                continue

            di, dj = self.move_coords[dir]
            adj_i, adj_j = i + di, j + dj
            adj_val = new_b[adj_i, adj_j]
            #TODO rewrite __combinable (as __moveable(?)) to make it more useable here...
            combs = set([val, adj_val])
            if len(combs) != 1:
                if combs == {1, 2}:
                    new_b[adj_i, adj_j] = 3
                    new_b[i, j] = 0
                    moved_bool = True 
                else:
                    new_b[i, j] = val
            else:
                if combs == {1} or combs == {2}:
                    new_b[i, j] = val
                else:
                    new_b[adj_i, adj_j] = 2 * val
                    new_b[i, j] = 0
                    moved_bool = True        

            
        #return new_b
        return moved_bool


        
        




if __name__ == '__main__':
    hiscore = np.array([[1, 192, 1536, 6144], [1, 48, 384, 48], [3, 12, 96, 12], [1, 3, 6, 3]])
    assert ThreesBoard(init_arr=hiscore).get_score() == 600525
    
    try:
        ThreesBoard(init_arr=hiscore-1)
    except ValueError:
        pass

    try:
        ThreesBoard(init_arr=hiscore[:, :-1])
    except AttributeError:
        pass

    try:
        ThreesBoard(init_arr=list(hiscore))
    except TypeError:
        pass

    assert not ThreesBoard(init_arr=hiscore).can_play()
    assert ThreesBoard().can_play()


    for dir in ['u', 'd', 'l', 'r']:
        assert not ThreesBoard(init_arr=hiscore).move(dir, 1, 0)
        #print(ThreesBoard(init_arr=hiscore).move(dir, 1, 0))
        assert ThreesBoard().move(dir, 1, 0)