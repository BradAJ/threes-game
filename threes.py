import numpy as np
from itertools import product


class ThreesBoard:
    """Emulate the mobile game Threes https://asherv.com/threes/ using Numpy
    arrays. Can either specify the initial board as a 4x4 array or randomly
    generate one."""
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


    def move(self, dir, new_val, new_ind, new_board=None):
        """move tiles in direction dir and place a new tile with value new_val at
        location new_ind. (where dir and new_ind together determine the new i,j
        coordinates e.g. ['u', 2] means [3, 2], and ['r', 1] -> [1, 0]).

        new_board is a moved board array w/o the new tile (should be specified
        if .get_intermediate_board has been called separately)

        returns: boolean of 'move successful' """

        if new_board is None:
            new_b, moved_inds = self.get_intermediate_board(dir)
        else:
            new_b = new_board
            moved_inds = set([new_ind])

        if dir == 'l':
            new_coords = [new_ind, 3]
        elif dir == 'd':
            new_coords = [0, new_ind]
        elif dir == 'r':
            new_coords = [new_ind, 0]
        else: #dir == 'u'
            new_coords = [3, new_ind]

        if new_ind in moved_inds:
            new_b[new_coords[0], new_coords[1]] = new_val
            self.board = new_b
            return True
        else:
            return False

    def get_intermediate_board(self, dir, return_moving=False):
        """move tiles in direction dir w/o adding new tile.

        returns: tuple: (new_board array, set of indices available for new tile) """
        new_b = -1 * np.ones([4, 4], dtype=int)
        moving = self.board.copy()
        moved_inds = set()

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
            mv_ind = i if dir in {'l', 'r'} else j
            val = self.board[i, j]
            if val == 0:
                new_b[i, j] = 0
                #moved_inds.add(mv_ind)
                continue

            di, dj = self.move_coords[dir]
            adj_i, adj_j = i + di, j + dj
            adj_val = new_b[adj_i, adj_j]
            if adj_val == 0:
                new_b[adj_i, adj_j] = val
                new_b[i, j] = 0
                moving[adj_i, adj_j] = -1
                moving[i, j] = -1
                moved_inds.add(mv_ind)
                continue
            #TODO rewrite __combinable (as __moveable(?)) to make it more useable here...
            combs = set([val, adj_val])
            if len(combs) != 1:
                if combs == {1, 2}:
                    new_b[adj_i, adj_j] = 3
                    new_b[i, j] = 0
                    moving[adj_i, adj_j] = -1
                    moving[i, j] = -1
                    moved_inds.add(mv_ind)
                else:
                    new_b[i, j] = val
            else:
                if combs == {1} or combs == {2}:
                    new_b[i, j] = val
                else:
                    new_b[adj_i, adj_j] = 2 * val
                    new_b[i, j] = 0
                    moving[adj_i, adj_j] = -1
                    moving[i, j] = -1
                    moved_inds.add(mv_ind)
        if return_moving:
          return new_b, moved_inds, moving
        else:
          return new_b, moved_inds


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
        #assert ThreesBoard().move(dir, 1, 0)

    b1 = np.array([[1, 6, 1, 3], [0, 12, 6, 0], [0, 2, 2, 3], [0, 6, 0, 1]])
    game1 = ThreesBoard(init_arr=b1)
    assert game1.move('l', 2, 0) == False
    game1.move('l', 2, 0)
    assert (game1.board == b1).all()
    assert game1.move('r', 2, 0) == False
    assert game1.move('d', 2, 1) == False
    game1.move('l', 2, 1)
    assert (game1.board == np.array([[1, 6, 1, 3], [12, 6, 0, 2], [2, 2, 3, 0], [6, 0, 1, 0]])).all()

    game2 = ThreesBoard(init_arr=b1)
    for ind in range(3):
        assert game2.move('u', 2, ind) == False
    game2.move('u', 2, 3)
    assert (game2.board == np.array([[1, 6, 1, 3], [0, 12, 6, 3], [0, 2, 2, 1], [0, 6, 0, 2]])).all()

    game3 = ThreesBoard(init_arr=b1)
    game3.move('d', 2, 0)
    assert (game3.board == np.array([[2, 6, 0, 0], [1, 12, 1, 3], [0, 2, 6, 3], [0, 6, 2, 1]])).all()

    game4 = ThreesBoard(init_arr=b1)
    assert game4.move('r', 2, 2) == False
    game4.move('r', 2, 1)
    assert (game4.board == np.array([[1, 6, 1, 3], [2, 0, 12, 6], [0, 2, 2, 3], [0, 0, 6, 1]])).all()
    game4.move('l', 3, 2)
    assert (game4.board == np.array([[1, 6, 1, 3], [2, 12, 6, 0], [2, 2, 3, 3], [0, 6, 1, 0]])).all()
    game4.move('r', 2, 3)
    assert (game4.board == np.array([[1, 6, 1, 3], [0, 2, 12, 6], [0, 2, 2, 6], [2, 0, 6, 1]])).all()
    game4.move('d', 1, 1)
    assert (game4.board == np.array([[0, 1, 1, 0], [1, 6, 12, 3], [0, 2, 2, 12], [2, 2, 6, 1]])).all()
    game4.move('r', 3, 0)
    assert (game4.board == np.array([[3, 0, 1, 1], [1, 6, 12, 3], [0, 2, 2, 12], [2, 2, 6, 1]])).all()
    game4.move('l', 1, 2)
    assert (game4.board == np.array([[3, 1, 1, 0], [1, 6, 12, 3], [2, 2, 12, 1], [2, 2, 6, 1]])).all()
    game4.move('u', 2, 3)
    assert (game4.board == np.array([[3, 1, 1, 3], [3, 6, 24, 1], [2, 2, 6, 1], [0, 2, 0, 2]])).all()
    game4.move('l', 1, 3)
    assert (game4.board == np.array([[3, 1, 1, 3], [3, 6, 24, 1], [2, 2, 6, 1], [2, 0, 2, 1]])).all()
    game4.move('r', 3, 3)
    assert (game4.board == np.array([[3, 1, 1, 3], [3, 6, 24, 1], [2, 2, 6, 1], [3, 2, 0, 3]])).all()
    game4.move('d', 3, 0)
    assert (game4.board == np.array([[3, 1, 0, 3], [6, 6, 1, 1], [2, 2, 24, 1], [3, 2, 6, 3]])).all()
    game4.move('l', 1, 1)
    assert (game4.board == np.array([[3, 1, 3, 0], [12, 1, 1, 1], [2, 2, 24, 1], [3, 2, 6, 3]])).all()
    game4.move('r', 2, 0)
    assert (game4.board == np.array([[2, 3, 1, 3], [12, 1, 1, 1], [2, 2, 24, 1], [3, 2, 6, 3]])).all()
    game4.move('d', 3, 1)
    assert (game4.board == np.array([[2, 3, 1, 3], [12, 3, 1, 1], [2, 3, 24, 1], [3, 2, 6, 3]])).all()
    game4.move('u', 2, 1)
    assert (game4.board == np.array([[2, 6, 1, 3], [12, 3, 1, 1], [2, 2, 24, 1], [3, 2, 6, 3]])).all()
    for dir in ['u', 'd', 'l', 'r']:
        for ind in range(4):
            assert game4.move(dir, 1, ind) == False
    assert game4.can_play() == False
    assert game4.get_score() == 138

    ############# OCT 2022 UPDATE

    recorded = ThreesBoard(np.array([[  0 ,  1,   2, 768],
     [  0 ,  3 ,  0 ,  3],
     [  2  , 2 ,  0 ,  0],
     [  0 ,  0 ,  2 ,  3]]))

    #print(recorded.get_intermediate_board('r', return_moving=True))

    recorded.move('r', 1, 0)
    #print(recorded.board)

    #print(recorded.get_intermediate_board('u', return_moving=True))

    recorded.move('u', 1, 2)
    print(recorded.board)

    print(recorded.get_intermediate_board('u', return_moving=True))
