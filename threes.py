import numpy as np

class ThreesEmulator:
    pass

class ThreesBoard:
    def __init__(self, init_arr=None):
        self.values = set([0, 1, 2] + [3 * 2**i for i in range(12)])
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


if __name__ == '__main__':
    hiscore = np.array([[1, 192, 1536, 6144], [1, 48, 384, 48], [3, 12, 96, 12], [1, 3, 6, 3]])
    assert ThreesBoard(init_arr=hiscore).get_score() == 600525
