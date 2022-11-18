from collections import Counter, defaultdict
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
  TODO: use a Counter here??
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


def suggest_move_dir(board_arr, next_tiles, n_moves = None, **kwargs):
  #naive suggestions. TODO: step forward more moves if the results are close

  if n_moves is None:
    #this is pretty slow, so step down
    #n_moves = 4 if (board_arr == 0).sum() <= 1 else 3
    n_moves = 4 if (board_arr == 0).sum() <= 0 else 3

  all_counts = Counter()  
  for nt in next_tiles:
    mv_lookup_d = n_move_dfs(board_arr, n_moves, next_tile=nt)
    dircounts = count_full_paths(mv_lookup_d, n_moves)
    all_counts += dircounts
  
  acmc = all_counts.most_common()
  if acmc == []:
    return None
  else:
    return acmc[0][0]

def semiauto_play(game, move_suggestion_func, **kwargs):
  """game: ThreesBoard like object
  move_suggestion_func: func that returns a direction character
  TODO remember how to do argument passing with funcs as args
  
  RETURNS
  list of move tuples 
  """
  moves = []
  # first_board = np.array([[3,1,0,768],[3,0,0,1],[3,2,2,2],[0,0,0,0]])
  # game = ThreesAgent(first_board)
  # midgame_arr = np.array([[0,0,24,6],[1,48,768,2],[6,24,6,3],[12,0,2,2]])
  # game = ThreesAgent(midgame_arr)
  # midgame_arr2 = np.array([[3,12,1,12],[24,12,96,24],[6,384,24,768],[2,12,48,6]])
  # game = ThreesAgent(midgame_arr2)
  while True:
    print('\n')
    print(game.board)

    nexts_inp = input('Next? ')
    if nexts_inp == 'q':
      break
    next_tiles = [int(x) for x in nexts_inp.split(' ')]
    
    #### args hard coded for suggest_move_dir(board_arr, next_tiles)
    dirch = move_suggestion_func(game.board, next_tiles, **kwargs)
    if dirch is None:
      print('No moves available')
      break

    poss_move_inds = list(game.check_move_dirs()[dirch].keys())
    dirprint = {'u':'UP ^', 'd':'DOWN \/', 'l':'LEFT <', 'r':'RIGHT >'}
    print(f'Moving {dirprint[dirch]}')
    print(f'adding {next_tiles[0]} tile at {poss_move_inds}')
    
    next_tile_ind = input('New tile index, (x: chdir, n: chtile) ')
    edited = False
    
    if 'x' in next_tile_ind or 'n' in next_tile_ind:
      edited = True
      if 'x' in next_tile_ind:
        dirch = input('Override move direction? ')

    if 'n' in next_tile_ind or len(next_tiles) > 1:
      nt = input('New tile value? ')
    else:
      nt = next_tiles[0]

    if edited:
      next_tile_ind = input('Redo new tile index? ')

    if next_tile_ind == '':
      if len(poss_move_inds) == 1:
        next_tile_ind = poss_move_inds[0]
      else:
        next_tile_ind = input("Please enter the new tile's index ")

    mvtupfinal = (dirch, int(nt), int(next_tile_ind))
    moved_bool = game.move(*mvtupfinal)
    if not moved_bool:
      print(f'Failed to move {dirch} with tile {nt} into {next_tile_ind}. Try again')
    else:
      moves.append(mvtupfinal)

  return moves



if __name__ == "__main__":
  # almost_out = np.array([[2, 3, 1, 3], [12, 3, 1, 1], [2, 3, 24, 1], [3, 2, 6, 3]])
  # ao_tag = ThreesAgent(almost_out)
  

  # #print(n_move_dfs(almost_out, 5))
  # ao2 = np.array([[48, 192, 384, 1536], [24, 96, 12, 6], [48, 12, 6, 2], [2, 3, 3, 3]])
  # n_moves = 2
  # assert count_full_paths(n_move_dfs(ao2, n_moves, next_tile=None), n_moves) == {'u': 0, 'd': 0, 'l': 10, 'r': 7}
  # assert count_full_paths(n_move_dfs(ao2, n_moves, next_tile=2), n_moves) == {'u': 0, 'd': 0, 'l': 0, 'r': 0}
  

  # midgame_arr2 = np.array([[3,12,1,12],[24,12,96,24],[6,384,24,768],[2,12,48,6]])
  # g2 = ThreesAgent(midgame_arr2)
  # mm = semiauto_play(g2, suggest_move_dir)

  arr20221115 = np.array([[0,1,2,768],[0,2,3,3],[0,0,3,0],[0,1,0,2]])
  arr20221116 = np.array([[1,0,0,768],[3,3,0,2],[1,0,0,0],[2,0,2,3]])
  arr20221117 = np.array([[2,3,2,3072],[0,3,12,768],[192,1,12,384],[3,1,3,96]])
  g = ThreesAgent(arr20221117)
  mm = semiauto_play(g, suggest_move_dir, n_moves=4)