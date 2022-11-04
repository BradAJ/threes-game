#import numpy as np
from threes import ThreesBoard
from collections import defaultdict

class ThreesAnalyzer(ThreesBoard):
  """Data from a Threes game consists of the 4x4 game board of tiles in 
  {1, 2, 3, 6, 12, ..., 6144} and a next tile indicator. Thus a game can be
  saved with 17 elements for each move. In principle there is no intermediate
  state between moves, but in practice the visuals for the game show the tiles
  in motion. Screen captures of game play are dominated by the motion and 
  merging of tiles.
  
  The ThreesAnalyzer class takes as input Nx4x4 and Nx1 arrays of frames
  from a screen cap (see ingest_threes_screencap.py for video to array
  conversions) and reduces these frames to a sequence of moves. By 
  convention when a tile is 'in motion' it occupies two places on the
  board, both these places are labeled as -1, while completely empty
  places are labeled 0.
  
  Common usage:
  >game = ThreesAnalyzer(game_seq_array, next_tiles_array)
  >while True:
    moved_bool = game.define_move()
    if not moved_bool:
      break
  
  """
  def __init__(self, game_seq, next_tiles):
    """game_seq: N x 4 x 4 np.array, Array of frame arrays
       next_tiles: N x 1 np.array of 'next tile' values
                   NOTE: The code assumes next_tiles >3 are always shown as 
                   trios on screen e.g. 6/12/24. Where the highest tile is
                   the placeholder. This assumption will cause problems if 
                   highest tile on board is <=96.
    """
    self.frames = game_seq.reshape([game_seq.shape[0], 4, 4])
    super().__init__(init_arr=self.frames[0, :, :])
    if self.frames.shape[0] != next_tiles.shape[0]:
      raise ValueError('game_seq and next_tiles dim mismatch:', self.frames.shape[0], next_tiles.shape[0])
    else:
      self.next_tiles = next_tiles

    self.cur_frame = 0
    self.move_cnt = 0
    self.move_details = [['move num', 'move dir', 'next tile', 'next tile coords', 'moving frame num', 'current frame num']]
    self.get_intermediate_dict()


  def get_intermediate_dict(self):
    if self.cur_frame >= self.frames.shape[0]:
      return False
    d_out = {}
    for dirch in ['u', 'd', 'l', 'r']:
      ib = self.get_intermediate_board(dirch, return_moving=True)
      d_out[dirch] = [ib[2], ib[0], ib[1]]

    self.intermediate_dict = d_out


  def find_moving_match(self, nexts_use_max_on_board=True):
    """Given a current board, attempt all four moves {'u', 'd', 'l', 'r'} 
    and try to match these with a subsequent frame based on the combination
    of tiles that stay still and those that move and would therefore be labeled 
    as -1.

    PARAMETERS
    nexts_use_max_on_board: bool. See self.define_move() for details

    RETURNS
    tuple of 3: direction character, next tile value, frame number of match
      or if it fails: None, None, None
    """
    move_dir = None
    found_moving_match = False 
    next_tile_cur = self.next_tiles[self.cur_frame]
    for i in range(self.cur_frame + 1, self.frames.shape[0]):
      for dirch, movetup in self.intermediate_dict.items():
        #arrays match AND the set of indices for next tile is not empty
        if len(movetup[2]) > 0 and (self.frames[i] == movetup[0]).all(): 
          next_tile_i = self.next_tiles[i]
          if next_tile_cur == next_tile_i:
            move_dir = dirch
            found_moving_match = True
            break
          else:
            print('Next mismatch', self.cur_frame, i, next_tile_cur, next_tile_i)
            if nexts_use_max_on_board and next_tile_cur > 3 and next_tile_i > 3:
              move_dir = dirch
              found_moving_match = True
              break

            return None, None, None

      if found_moving_match:
        break
    return move_dir, next_tile_cur, i


  def define_move(self, nexts_use_max_on_board=True):
    """Attempt to match a move given the current board and next tile indicator
    and subsequent frames. If successful returns True.
    
    PARAMETERS
    nexts_use_max_on_board: bool.
      NOTE 
      Due to data coming from screen captures, when next_tile > 3 the image 
      reads are error prone due to rarity. A way around this is when a trio of 
      big tiles is shown that's easy to detect, so can search all possible big 
      tiles based on the constraint that the largest possible next_tile is:
      max_tile_on_board / 8.
      e.g. if max_tile_on_board == 768 then the big tile set for such a game is:
      {6, 12, 24, 48, 96} 
      if 1536 then ^^.union({192}) and so on. 
      If nexts_use_max_on_board:
        search these sets
      else:
        search the trio implied by the predictions (where the max of the trio
        is the placeholder)

    RETURNS
      bool
    """
    dirch, next_tile, moving_frame_ind = self.find_moving_match(nexts_use_max_on_board=nexts_use_max_on_board)
    if not dirch:
      ####raise Exception('No moving frame found', dirch, self.cur_frame)
      return False

    interbrd, new_tile_inds = self.intermediate_dict[dirch][1:]
    #TODO: clean up repeated code (also used in super.move)
    if dirch == 'l':
      new_coords = [(new_ind, 3) for new_ind in new_tile_inds]
    elif dirch == 'd':
      new_coords = [(0, new_ind) for new_ind in new_tile_inds]
    elif dirch == 'r':
      new_coords = [(new_ind, 0) for new_ind in new_tile_inds]
    else: #dirch == 'u'
      new_coords = [(3, new_ind) for new_ind in new_tile_inds]

    poss_next_brds = defaultdict(list)
    for crds in new_coords:
      # See NOTE on next_tiles > 3 in __init__
      if next_tile < 24: 
        all_nexts = [next_tile]
      else:
        if nexts_use_max_on_board:
          max_on_board = self.board.max()
          bigs = [6 * 2 ** y for y in range(10)]
          all_nexts = filter(lambda x: x <= max_on_board / 8, bigs)
        else:
          all_nexts = [int(next_tile / denom) for denom in [1, 2, 4]]
      for nt in all_nexts:
        poss_next_brd = interbrd.copy()
        poss_next_brd[crds] = nt
        poss_next_brds[nt].append([poss_next_brd, crds])

    for i in range(moving_frame_ind, self.frames.shape[0]):
      for next_tile_div, next_brd_crds_l in poss_next_brds.items():
        for poss_next_brd, crds in next_brd_crds_l:
          if (self.frames[i] == poss_next_brd).all():
            self.board = poss_next_brd
            self.cur_frame = i
            self.move_cnt += 1
            self.move_details.append([self.move_cnt, dirch, next_tile_div, crds, moving_frame_ind, i])
            self.get_intermediate_dict()
            return True

    return False


if __name__ == '__main__':
  pass
# TODO these tests use older version w/o the next_tile arg. Update to new version
#   from numpy import array

#   seq_l = [array([  0,   1,   2, 768,   0,   3,   0,   3,   2,   2,   0,   0,   0,
#           0,   2,   3]),
#  array([  0,  -1,  -1, 768,   0,  -1,  -1,   3,  -1,  -1,  -1,   0,   0,
#           0,   2,   3]),
#  array([  0,   0,  -1, 768,   0,   0,   3,   3,   0,   2,   2,   0,   0,
#           0,   2,   3]),
#  array([ -1,   0,  -1, 768,   0,   0,   3,   3,   0,   2,   2,   0,   0,
#           0,   2,   3]),
#  array([  1,   0,  -1, 768,   0,   0,   3,   3,   0,   2,   2,   0,   0,
#           0,   2,   3]),
#  array([  1,   0,  -1, 768,   0,  -1,  -1,   3,   0,  -1,  -1,  -1,   0,
#           0,  -1,  -1]),
#  array([  1,   0,  -1, 768,   0,   2,   2,  -1,   0,  -1,   2,  -1,   0,
#           0,  -1,  -1]),
#  array([  1,   0,  -1, 768,   0,   2,   2,  -1,   0,   0,   2,   3,   0,
#           0,   0,   0]),
#  array([  1,   0,  -1, 768,   0,   2,   2,   3,   0,   0,   2,   3,   0,
#           0,   0,   0]),
#  array([  1,   0,  -1, 768,   0,   2,   2,   3,   0,   0,   2,   3,   0,
#           0,  -1,   0]),
#  array([  1,   0,  -1, 768,   0,   2,   2,   3,   0,   0,   2,   3,   0,
#           0,   1,   0])]

#   game = ThreesAnalyzer(array(seq_l).reshape([len(seq_l), 4, 4]))

#   game.define_move()
#   deets1 = [[None, None, None, None], [1, 'r', -1, -1], [1, 'r', -1, -1], [1, 'r', -1, -1], [1, 'r', -1, -1], [1, 'r', 1, (0, 0)]]
#   assert game.move_details == deets1

#   game.define_move()
#   assert game.move_details == deets1 + [[2, 'u', -1, -1], [2, 'u', -1, -1], [2, 'u', -1, -1], [2, 'u', -1, -1], [2, 'u', -1, -1], [2, 'u', -1, -1], [2, 'u', 1, (3, 2)]]
