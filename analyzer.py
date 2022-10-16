#import numpy as np
from threes import ThreesBoard

class ThreesAnalyzer(ThreesBoard):
  def __init__(self, game_seq, first_board=None):
    """game_seq: N x 4 x 4 np.array, Sequence of frame arrays
    first_board: 4 x 4 np.array or None, initialize ThreesBoard class
                 If None, take this from game_seq[0, :, :] (first frame)
    """
    ###if game_seq.shape[1] == 16:
    self.frames = game_seq.reshape([game_seq.shape[0], 4, 4])

    if first_board is None:
      first_board = self.frames[0, :, :]
    super().__init__(init_arr=first_board)

    self.cur_frame = 0
    self.move_cnt = 0
    self.move_details = [[None, None, None, None]]
    self.get_intermediate_dict()


  def define_move(self):
    #check for single perfect match in moving frames (not intermediates)
    possible_dirs = []
    for dirch, scores in self.score_next_frame().items():
      if scores[0] == 16:
        possible_dirs.append(dirch)

    if len(possible_dirs) == 1:
      mv_dir = possible_dirs[0]
      self.move_cnt += 1
      self.move_details.append([self.move_cnt, mv_dir, -1, -1])
      self.cur_frame += 1
      new_tile_d = self.get_new_tile(mv_dir)

      finalize_move = False
      # perfect new board after a perfect move match
      if new_tile_d['match_cnt'] == 16:
        finalize_move = True
      else:
        # OR the only mismatches are where frame has a -1
        # might be too permissive if frame has a lot of -1s?
        frame = self.frames[new_tile_d['frame_num']]
        if (frame[frame != new_tile_d['brd']] == -1).all():
          finalize_move = True

      if finalize_move:
        self.board = new_tile_d['brd']
        #move history housekeeping:
        frame_info = []
        for i in range(self.cur_frame, new_tile_d['frame_num']):
          frame_info.append([self.move_cnt, mv_dir, -1, -1])

        frame_info.append([self.move_cnt, mv_dir, new_tile_d['val'],
                           new_tile_d['coords']])
        self.move_details.extend(frame_info)
        self.cur_frame = new_tile_d['frame_num']
        self.get_intermediate_dict()

    else: #num dirs !=1
      print('poss', possible_dirs)




  def get_new_tile(self, dirch, print_board_and_frame=False):
    """#new_tile_d contains a match count assuming, mv_dir, and new_tile_info[:2]
      #it may take several frames before this guess is made, new_tile_info[2]
      #gives the frame number where the comparison with the board is made
      #so decide what to do when matching is imperfect:

    dirch: character in {'u', 'd', 'l', 'r'}

    returns: dict w/ keys: 'val', 'coord', 'brd', 'frame_num', 'match_cnt'"""
    mv_brd, inter_brd, new_tile_inds = self.intermediate_dict[dirch]

    #TODO: clean up repeated code (also used in super.move)
    if dirch == 'l':
      new_coords = [(new_ind, 3) for new_ind in new_tile_inds]
    elif dirch == 'd':
      new_coords = [(0, new_ind) for new_ind in new_tile_inds]
    elif dirch == 'r':
      new_coords = [(new_ind, 0) for new_ind in new_tile_inds]
    else: #dirch == 'u'
      new_coords = [(3, new_ind) for new_ind in new_tile_inds]

    new_tile_val = None
    step = 0
    new_tile_coords = []
    while new_tile_val is None:
      step += 1
      for coord in new_coords:
        possible_new_tile = self.frames[self.cur_frame + step][coord]
        if possible_new_tile != inter_brd[coord]:
          if possible_new_tile == -1:
            if mv_brd[coord] != -1:
              #location of new tile found, but not its value
              new_tile_coords.append(coord)
            # else:
            #   continue
              #can't say anything for sure
          else:
            #warning: this could get overwritten in multiple mismatches
            new_tile_val = possible_new_tile
            new_tile_coords.append(coord)

    if len(set(new_tile_coords)) > 1:
      raise Exception('Ambiguous situation at frame, step:',self.cur_frame, step)
    else:
      #possible completed move:
      new_brd = inter_brd.copy()
      new_brd[new_tile_coords[0]] = new_tile_val
      match_cnt = (new_brd == self.frames[self.cur_frame + step]).sum()

      if print_board_and_frame:
        print('ThreesBoard Moved')
        print(new_brd)
        print('Frame')
        print(self.frames[self.cur_frame + step])
        raise Exception('Mismatched update above.')

      return {'val':new_tile_val, 'coords':new_tile_coords[0], 'brd':new_brd,
              'frame_num':self.cur_frame + step, 'match_cnt':match_cnt}



  def score_next_frame(self):
    if not self.intermediate_dict:
      return False

    match_scores = {}
    for dirch, arrsinds in self.intermediate_dict.items():
      scs = [(arr == self.frames[self.cur_frame + 1, :]).sum() for arr in arrsinds[:2]]
      match_scores[dirch] = scs

    return match_scores


  def get_intermediate_dict(self):
    if self.cur_frame >= self.frames.shape[0]:
      return False
    d_out = {}
    for dirch in ['u', 'd', 'l', 'r']:
      ib = self.get_intermediate_board(dirch, return_moving=True)
      d_out[dirch] = [ib[2], ib[0], ib[1]]

    self.intermediate_dict = d_out



if __name__ == '__main__':
  from numpy import array

  seq_l = [array([  0,   1,   2, 768,   0,   3,   0,   3,   2,   2,   0,   0,   0,
          0,   2,   3]),
 array([  0,  -1,  -1, 768,   0,  -1,  -1,   3,  -1,  -1,  -1,   0,   0,
          0,   2,   3]),
 array([  0,   0,  -1, 768,   0,   0,   3,   3,   0,   2,   2,   0,   0,
          0,   2,   3]),
 array([ -1,   0,  -1, 768,   0,   0,   3,   3,   0,   2,   2,   0,   0,
          0,   2,   3]),
 array([  1,   0,  -1, 768,   0,   0,   3,   3,   0,   2,   2,   0,   0,
          0,   2,   3]),
 array([  1,   0,  -1, 768,   0,  -1,  -1,   3,   0,  -1,  -1,  -1,   0,
          0,  -1,  -1]),
 array([  1,   0,  -1, 768,   0,   2,   2,  -1,   0,  -1,   2,  -1,   0,
          0,  -1,  -1]),
 array([  1,   0,  -1, 768,   0,   2,   2,  -1,   0,   0,   2,   3,   0,
          0,   0,   0]),
 array([  1,   0,  -1, 768,   0,   2,   2,   3,   0,   0,   2,   3,   0,
          0,   0,   0]),
 array([  1,   0,  -1, 768,   0,   2,   2,   3,   0,   0,   2,   3,   0,
          0,  -1,   0]),
 array([  1,   0,  -1, 768,   0,   2,   2,   3,   0,   0,   2,   3,   0,
          0,   1,   0])]

  game = ThreesAnalyzer(array(seq_l).reshape([len(seq_l), 4, 4]))

  game.define_move()
  deets1 = [[None, None, None, None], [1, 'r', -1, -1], [1, 'r', -1, -1], [1, 'r', -1, -1], [1, 'r', -1, -1], [1, 'r', 1, (0, 0)]]
  assert game.move_details == deets1

  game.define_move()
  assert game.move_details == deets1 + [[2, 'u', -1, -1], [2, 'u', -1, -1], [2, 'u', -1, -1], [2, 'u', -1, -1], [2, 'u', -1, -1], [2, 'u', -1, -1], [2, 'u', 1, (3, 2)]]
