#import numpy as np
from threes import ThreesBoard

class ThreesAnalyzer(ThreesBoard):
  def __init__(self, game_seq, next_tiles):
    """game_seq: N x 4 x 4 np.array, Array of frame arrays
       next_tiles: N x 1 np.array of 'next tile' values
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


  def find_moving_match(self):
    move_dir = None
    found_moving_match = False 
    next_tile_cur = self.next_tiles[self.cur_frame]
    for i in range(self.cur_frame + 1, self.frames.shape[0]):
      for dirch, movetup in self.intermediate_dict.items():
        if (self.frames[i] == movetup[0]).all(): 
          next_tile_i = self.next_tiles[i]
          if next_tile_cur == next_tile_i:
            move_dir = dirch
            found_moving_match = True
            break
          else:
            raise Exception('Next mismatch', self.cur_frame, i)

      if found_moving_match:
        break
    return move_dir, next_tile_cur, i


  def define_move(self):
    dirch, next_tile, moving_frame_ind = self.find_moving_match()
    if not dirch:
      raise Exception('No moving frame found')

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

    for i in range(moving_frame_ind, self.frames.shape[0]):
      for crds in new_coords:
        poss_next_brd = interbrd.copy()
        poss_next_brd[crds] = next_tile
        if (self.frames[i] == poss_next_brd).all():
          self.board = poss_next_brd
          self.cur_frame = i
          self.move_cnt += 1
          self.move_details.append([self.move_cnt, dirch, next_tile, crds, moving_frame_ind, i])
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
