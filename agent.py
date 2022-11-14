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
            premove_board = self.board.copy()
            self.move(dirch, nt, ind, new_board=ib)
            if self.can_play():
              ind_scores[ind].append(nt)
            self.board = premove_board
        
        move_scores[dirch] = ind_scores

      else:
        move_scores[dirch] = {}
    
    return move_scores


  def reset_board(self):
    self.board = self.init_board.copy()


####### SEARCH SCRIPT FUNCS (outside ThreesAgent cls)####
def n_move_dfs(init_arr, n, next_tile=None):
  """init_arr: np.array [4,4] Threes board
  n: int, number of moves to attempt in a single path
  next_tile: None or int, if specified, require that the first move insert that
    tile value. NOTE: Search paths will only start with this value, but other values
    with are included in output dict for that first move only. For example if
    next_tile = 3 the output dict might have: 
    {0: (('r', 1, 0), []), 1: (('r', 2, 0), []), 3: (('r', 3, 0), []), ...}
    The entries at 0 and 1 are included for completeness but no subsequent entries
    will ever have 0 or 1 as their starting point if next_tile=3

  RETURNS
  dict {index number:(move tuple [see .move() method], [list of ancestor indexes])}
  """
  ag = ThreesAgent(init_arr)

  mv_lookup = {}
  unseen = []
  for i, mvtup in enumerate(parse_move_dirs_dict(ag.check_move_dirs())):
    mv_lookup[i] = (mvtup, [])

    if (next_tile is None) or (next_tile == mvtup[1]):
      unseen.append(i)
  i += 1

  while len(unseen) > 0:
    new_mvind = unseen.pop()
    mvtup, old_mv_inds = mv_lookup[new_mvind]
    mvseq = old_mv_inds + [new_mvind]

    if len(mvseq) < n:
      ag = ThreesAgent(init_arr)
      for mvind in mvseq:
        mved_bool = ag.move(*mv_lookup[mvind][0])
        if not mved_bool:
          bad_tups = [(jj, mv_lookup[jj][0]) for jj in mvseq]

          raise Exception(f'Failed to move current, from ancestors, {mvind}, {bad_tups}')
      
      for next_mvtup in parse_move_dirs_dict(ag.check_move_dirs()):
        mv_lookup[i] = next_mvtup, mvseq
        unseen.append(i)
        i += 1
    else:
      continue

  return mv_lookup


def parse_move_dirs_dict(mv_d):
  mv_tups = []
  for dirch, coord_val_d in mv_d.items():
    for coord, vals in coord_val_d.items():
      for val in vals:
        mv_tups.append((dirch, val, coord))
  return mv_tups


def count_full_paths(mv_lookup, n, ignore_big_tiles=True):
  """
  mv_lookup: dict, returned by n_moves_dfs
    e.g. 1529: (('r', 24, 3), [0, 1160])
  n: int, number of moves specified in n_moves_dfs
  ignore_big_tiles: bool, only count paths of length n if the added tiles are <=3

  RETURNS
  dict
  """
  cnt_d  = {x: 0  for x in ['u', 'd', 'l', 'r']}
  for mvtup, mvinds in mv_lookup.values():
    if (len(mvinds) + 1 == n):
     if (not ignore_big_tiles) or (mvtup[1] <= 3):
      cnt_d[mv_lookup[mvinds[0]][0][0]] += 1
  return cnt_d






if __name__ == "__main__":
  almost_out = np.array([[2, 3, 1, 3], [12, 3, 1, 1], [2, 3, 24, 1], [3, 2, 6, 3]])
  ao_tag = ThreesAgent(almost_out)
  
  

  # mvs_list_of_tups = ao_tag.look_ahead_n_moves()
  # lmlot = len(mvs_list_of_tups)
  # #print(lmlot)
  #assert lmlot == 48771

  #print(mvs_list_of_tups)

  #print(ao_tag.check_move_dirs())





  #print(n_move_dfs(almost_out, 5))
  ao2 = np.array([[48, 192, 384, 1536], [24, 96, 12, 6], [48, 12, 6, 2], [2, 3, 3, 3]])
  n_moves = 2
  assert count_full_paths(n_move_dfs(ao2, n_moves, next_tile=None), n_moves) == {'u': 0, 'd': 0, 'l': 10, 'r': 7}
  assert count_full_paths(n_move_dfs(ao2, n_moves, next_tile=2), n_moves) == {'u': 0, 'd': 0, 'l': 0, 'r': 0}
  

#### IPYTHON TESTING
"""
n_moves = 4
game = ThreesAgent(np.array([[2,24,12,48], [3, 12, 24, 192], [6, 12, 384, 2], [2, 12, 1, 1536]]))
game.move('d', 3, 1)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.move('r', 1, 1)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.move('u', 1, 0)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
n_moves = 4
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.board
game.move('l', 1, 3)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=None), n_moves, ignore_big_tiles=False)
game.move('d', 12, 0)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=2), n_moves)
game.move('r', 2, 1)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('u', 3, 0)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.move('d', 1, 0)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('d', 3, 0)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=2), n_moves)
game.move('u', 2, 0)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('l', 3, 1)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('d', 3, 1)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=2), n_moves)
game.move('l', 2, 0)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('u', 3, 1)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
count_full_paths(n_move_dfs(game.board, 5, next_tile=3), 5)
game.move('l', 3, 2)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=2), n_moves)
game.move('d', 2, 1)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=2), n_moves)
game.move('u', 2, 3)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.move('l', 1, 3)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('l', 3, 3)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('u', 1, 3)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.move('l', 1, 1)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.move('d', 1, 3)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=2), n_moves)
game.move('u', 2, 2)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.move('d', 1, 2)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.move('r', 1, 3)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.move('r', 1, 3)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=2), n_moves)
game.move('u', 2, )
game.move('u', 2, 0)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=2), n_moves)
game.move('r', 2, 3)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('u', 3, 1)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=2), n_moves)
game.move('l', 2, 2)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('r', 3, 3)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=2), n_moves)
game.move('d', 2, 2)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('l', 3, 3)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('d', 3, 0)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.move('d', 1,3)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.move('r', 1, 1)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('d', 3, 0)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=2), n_moves)
count_full_paths(n_move_dfs(game.board, 5, next_tile=2), 5)
game.board
game.move('l', 2, 0)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=2), n_moves)
game.move('u', 2, 3)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('l', 3, 3)
game.board
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=None), n_moves, ignore_big_tiles=False)
game.move('l', 12, 1)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('u', 3, 3)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.move('l', 1, 3)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=2), n_moves)
game.move('u', 2, 3)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=2), n_moves)
game.move('r',2,3)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.move('l',1,2)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=3), n_moves)
game.move('u', 3, 3)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=1), n_moves)
game.move('d', 1, 0)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=None), n_moves, ignore_big_tiles=False)
##count_full_paths(n_move_dfs(game.board, n_moves, next_tile=48), n_moves, ignore_big_tiles=False)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=48), n_moves)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=96), n_moves)
count_full_paths(n_move_dfs(game.board, n_moves, next_tile=192), n_moves)
game.move('r', 48, 3)
game.board
game2 = ThreesAgent(np.array([[      1,  768, 0,   0],
       [   6, 1536,    3,    2],
       [  12,    6,   24,    3],
       [      3,   12,   12, 48]])
       )
###oops!
game2.board
count_full_paths(n_move_dfs(game2.board, n_moves, next_tile=3), n_moves)
game2.move('r', 3, 3)
count_full_paths(n_move_dfs(game2.board, n_moves, next_tile=1), n_moves)
game2.move('u', 1, 2)
count_full_paths(n_move_dfs(game2.board, n_moves, next_tile=1), n_moves)
game2.move('l', 1, 1)
count_full_paths(n_move_dfs(game2.board, n_moves, next_tile=3), n_moves)
game2.move('d',3,2)
game2.board
count_full_paths(n_move_dfs(game2.board, n_moves, next_tile=1), n_moves)
n_moves = 3
game2.move('r',1,2)
count_full_paths(n_move_dfs(game2.board, n_moves, next_tile=2), n_moves)
game.board
history

"""
#### This worked better than expected. Playing agent could use count_full_paths
#### with something like n_moves = 4 if (game.board == 0).sum() == 0 or 1 and
#### n_moves = 3 if ^^ > 1...