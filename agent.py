from collections import defaultdict
import numpy as np
from threes import ThreesBoard

class ThreesAgent(ThreesBoard):
  def __init__(self, init_arr):
    super().__init__(init_arr=init_arr)
    self.init_board = self.board.copy()
    self.max_tile = self.board.max()
    big_tiles = [6 * 2 ** y for y in range(10)]
    next_bigs = set(filter(lambda x: x <= self.max_tile / 8, big_tiles))
    self.new_tile_set = {1, 2, 3}.union(next_bigs)


  def check_move_dirs(self):
    """Look one move ahead. If a specific new tile at is playable at a given 
    location return that tile and location info.

    RETURNS
    dict of the form {'dir': {'new_tile_coord': [new_tile_values]}}
    """
    move_scores = {}
    for dirch in self.move_coords:
      ind_scores = defaultdict(list)
      ib, open_inds = self.get_intermediate_board(dirch)
      if len(open_inds) > 0:
        for ind in open_inds:
          for nt in self.new_tile_set:
            self.move(dirch, nt, ind, new_board=ib)
            if self.can_play():
              ind_scores[ind].append(nt)
            self.reset_board()
        
        move_scores[dirch] = ind_scores

      else:
        move_scores[dirch] = {}
    
    return move_scores


  def reset_board(self):
    self.board = self.init_board.copy()


  def look_ahead_n_moves(self, n=5, n_so_far=0, path_accum=[], parent=None):
    #print(len(path_accum))
    if n_so_far == n:
      return path_accum

    for dirch, move_d in self.check_move_dirs().items():
      for coord, vals in move_d.items():
        for val in vals:
          move_info = (dirch, val, coord)
          self.move(*move_info)
          path_accum.append({parent: move_info})
          self.look_ahead_n_moves(n, n_so_far+1, path_accum, (parent, move_info))

    return path_accum


if __name__ == "__main__":
  almost_out = np.array([[2, 3, 1, 3], [12, 3, 1, 1], [2, 3, 24, 1], [3, 2, 6, 3]])
  ao_tag = ThreesAgent(almost_out)
  mvs_list_of_tups = ao_tag.look_ahead_n_moves()
  lmlot = len(mvs_list_of_tups)
  print(lmlot)
  assert lmlot == 48771