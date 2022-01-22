from threes import ThreesBoard
import numpy as np

class ThreesEmulator:
    def __init__(self, init_arr=None):
        self.b = ThreesBoard(init_arr=init_arr)

    
    def gen_next_tile(self, p_bigtile = 0.04):
        """Next tile probabilities are taken to be equal for 1,2,3. For 6 and 
        higher these *jointly* appear with probability p_bigtile, with the 
        caveat that no 'next tile' will be higher than 3 steps below the 
        current high tile on the board. 
        (e.g. with 768 max on board, the prob of getting one of 6-96 inclusive 
        is p_bigtile/5. or if p_bigtile = 0.04 -> probs = {1:.32, 2:.32, 3:.32, 
        6:.008, 12:.008, 24:.008, 48:.008, 96:.008} when 768 is max on board.
        """
        base = [1, 2, 3]
        maxtile = self.b.board.max()
        if maxtile < 48:
            return np.random.choice(base)
        else:
            bigs =  [3 * 2**i for i in range(1, 12)]
            next_bigs = bigs[:bigs.index(maxtile) - 2]
            big_p = p_bigtile / len(next_bigs)
            base_p = (1 - p_bigtile) / 3.
            ps = [base_p] * 3 + [big_p] * len(next_bigs)
            return np.random.choice(base + next_bigs, p=ps)




if __name__ == "__main__":
    x = ThreesEmulator()
    print(x.b.board)
    print(sorted(list(x.b.values)))

