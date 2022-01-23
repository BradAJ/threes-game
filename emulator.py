import re
from threes import ThreesBoard
import numpy as np

class ThreesEmulator:
    def __init__(self, init_arr=None, p_bigtile=0.04):
        """For init_arr: see ThreesBoard. For p_bigtile: see .gen_next_tile"""
        self.b = ThreesBoard(init_arr=init_arr)
        self.p_bigtile = p_bigtile
        self.next_tile = None
        self.recording = []

    
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
            self.next_tile = np.random.choice(base)
        else:
            bigs =  [3 * 2**i for i in range(1, 12)]
            next_bigs = bigs[:bigs.index(maxtile) - 2]
            big_p = self.p_bigtile / len(next_bigs)
            base_p = (1 - self.p_bigtile) / 3.
            ps = [base_p] * 3 + [big_p] * len(next_bigs)
            self.next_tile = np.random.choice(base + next_bigs, p=ps)


    def gen_next_hint(self):
        """big tiles are obscured with a group of three possibles for games
        with the max on board tile >=192 generate these hints. for consistency
        always return a list.
        """
        if self.next_tile is None:
            self.gen_next_tile()
        next_tile = self.next_tile
        if next_tile < 6:
            return [next_tile]
        
        maxtile = self.b.board.max()
        constrained_bigs = {48:[6], 96:[6, 12]}
        if maxtile in constrained_bigs:
            return constrained_bigs[maxtile]
        
        bigs =  [3 * 2**i for i in range(1, 12)]
        ind = bigs.index(next_tile)
        if ind == 0:
            lo_ind = 0
        elif ind == 1:
            lo_ind = np.random.choice([0, 1])
        else:
            lo_ind = np.random.choice(range(ind-2, ind+1))
        
        return bigs[lo_ind:lo_ind+3]


    def record_game(self):
        #move_dirs = []
        u_s = '\x1b[A'
        d_s = '\x1b[B'
        l_s = '\x1b[D'
        r_s = '\x1b[C'
        
        inp = ''
        while inp != 'q':
            print(self.gen_next_hint())
            print(self.b.board)
            inp = input('? ')
            if inp == u_s:
                dir = 'u'
            elif inp == d_s:
                dir = 'd'
            elif inp == l_s:
                dir = 'l'
            elif inp == r_s:
                dir = 'r'
            else:
                break
            
            #move_dirs.append(dir)

            moved_bool = self.step(dir, record_step=True)
            if not moved_bool:
                print(self.b.get_score())
        return self.recording

        
    def step(self, dir, record_step=True):
        new_b, moved_inds = self.b.get_intermediate_board(dir)
        if len(moved_inds) > 0:
            new_ind = np.random.choice(list(moved_inds))
            if self.next_tile is None:
                self.gen_next_tile()
            moved_bool = self.b.move(dir, self.next_tile, new_ind, new_board=new_b)
            if moved_bool and record_step:
                self.recording.append([dir, self.next_tile, new_ind])        
            self.next_tile = None
        else:
            moved_bool = False
        
        return moved_bool



    def play_randomly(self):
        dirs = ['u', 'd', 'l', 'r']
        while self.b.can_play():
            np.random.shuffle(dirs)
            for dir in dirs:
                moved_bool = self.step(dir)
                if moved_bool:
                    break

        return self.b.get_score()



if __name__ == "__main__":
    x = ThreesEmulator()
    #print(x.b.board)
    print(x.play_randomly())

    # scores = []
    # for _ in range(10000):
    #     x = ThreesEmulator()
    #     scores.append(x.play_randomly())
    
    # print(scores)
    # print('')
    # print(max(scores))

    x = ThreesEmulator()
    print(x.record_game())

