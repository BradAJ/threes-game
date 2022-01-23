from threes import ThreesBoard
import numpy as np

class ThreesEmulator:
    def __init__(self, init_arr=None, p_bigtile=0.04):
        """For init_arr: see ThreesBoard. For p_bigtile: see .gen_next_tile"""
        self.b = ThreesBoard(init_arr=init_arr)
        self.p_bigtile = p_bigtile

    
    def gen_next_tile(self):
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
            big_p = self.p_bigtile / len(next_bigs)
            base_p = (1 - self.p_bigtile) / 3.
            ps = [base_p] * 3 + [big_p] * len(next_bigs)
            return np.random.choice(base + next_bigs, p=ps)


    def play_randomly(self):
        dirs = ['u', 'd', 'l', 'r']
        while self.b.can_play():
            np.random.shuffle(dirs)
            for d_try in dirs:
                new_b, moved_inds = self.b.get_intermediate_board(d_try)
                if len(moved_inds) > 0:
                    break
            
            new_ind = np.random.choice(list(moved_inds))
            new_tile = self.gen_next_tile()
            self.b.move(d_try, new_tile, new_ind, new_board=new_b)

        return self.b.get_score()



if __name__ == "__main__":
    #x = ThreesEmulator()
    #print(x.b.board)
    #print(x.play_randomly())

    scores = []
    for _ in range(10000):
        x = ThreesEmulator()
        scores.append(x.play_randomly())
    
    print(scores)
    print('')
    print(max(scores))

