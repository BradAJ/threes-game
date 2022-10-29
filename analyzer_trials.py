from nis import match
from analyzer import ThreesAnalyzer
import numpy as np
from collections import defaultdict

if __name__ == "__main__":
    #npz = np.load('/Users/brad/Downloads/threes_boards_label_arrs_fpaths.npz')
    # npz = np.load('/Users/brad/Downloads/oct17_threes_boards_label_arrs_fpaths.npz')
    # nextsdata = np.load('/Users/brad/Downloads/oct17_threes_next_tile_label_arrs.npz')
    # next_tiles = nextsdata['next_tiles']
    # game_arrs = npz['label_arrs']
    
    npz = np.load('/Users/brad/Downloads/oct27_board_next_tile_arrs.npz')
    game_arrs = npz['board_arrs']
    next_tiles = npz['next_arrs']
    
    

    
    game_seq = [game_arrs[0]]
    frame_nos = [0]
    nexts_seq = [next_tiles[0]]
    for iminus,arr in enumerate(game_arrs[1:]):
        if not (arr == game_seq[-1]).all():
            game_seq.append(arr)
            frame_nos.append(iminus + 1)
            nexts_seq.append(next_tiles[iminus + 1])

    nontrans = list(filter(lambda x: (game_seq[x] != -1).all(), range(len(game_seq))))
    # frame_scores = {}
    # for i in range(len(nontrans)-1):
    #     game_ind = nontrans[i]
    #     next_nontrans_ind = nontrans[i+1]
    #     game = ThreesAnalyzer(game_seq[game_ind].reshape([1,4,4]))
    #     game_d = game.intermediate_dict
    #     dnonneg = {}
    #     for j in range(game_ind+1, next_nontrans_ind):
    #         dout = {dch:(game_seq[j].reshape([4,4]) == arrs[0]).sum() for dch,arrs in game_d.items()}
    #         dnonneg[j] = dout
    #     frame_scores[game_ind] = dnonneg

    # #print(frame_scores)
    # # for i in range(6380,6408):
    # #     print(game_seq[i].reshape([4,4]))
    # # print("""6401: {6402: {'u': 12, 'd': 6, 'l': 12, 'r': 6}, 6403: {'u': 11, 'd': 5, 'l': 11, 'r': 7}, 6404: {'u': 11, 'd': 5, 'l': 11, 'r': 6}}""")
    # # print(frame_nos[6401])
    # # print(npz['fpaths'][frame_nos[6402]])

    # frame_perfects = {}
    # transperfs_next = defaultdict(list)
    # for fno, mv_d in frame_scores.items():
    #     perf_match = False
    #     for sc_d in mv_d.values():
    #         for dirch, dirsc in sc_d.items():
    #             if dirsc == 16:
    #                 perf_match = True
    #                 tmatchgame = ThreesAnalyzer(np.array(game_seq[fno]).reshape([1,4,4]))
    #                 interarr, newtileinds = tmatchgame.intermediate_dict[dirch][1:]
    #                 for k in range(fno, len(game_seq)):
    #                     if k > fno + 100:
    #                         break
    #                     poss_next_arr = game_seq[k].reshape([4,4])
    #                     if (poss_next_arr == interarr).sum() == 15:
    #                         diffarr = poss_next_arr != interarr
    #                         transperfs_next[fno].append([k, poss_next_arr[diffarr][0], np.nonzero(diffarr), dirch])


    #     frame_perfects[fno] = perf_match

    # #print(len(frame_perfects))
    # #print(sum(frame_perfects.values()))

    # #print(transperfs_next)

    # next_goods = defaultdict(list)
    # for fno, matches_info in transperfs_next.items():
    #     if len(matches_info) > 1 and matches_info[0][1] == -1:
    #         for info2 in matches_info[1:]:
    #             if info2[2] == matches_info[0][2]:
    #                 lcon = info2[-1] == 'l' and info2[2][1] == 3
    #                 rcon = info2[-1] == 'r' and info2[2][1] == 0
    #                 ucon = info2[-1] == 'u' and info2[2][0] == 3 
    #                 dcon = info2[-1] == 'd' and info2[2][0] == 0
    #                 if lcon or rcon or ucon or dcon:
    #                     next_goods[fno].append(info2)

    # #print(next_goods)

    # ##Only 99 of the 637 possibilities [oct17] make it thru this last test. Not great, but can
    # ##use these as a start for gathering next tile info.

    # for fno,infolist in next_goods.items():
    #     for framedata in infolist:
    #         if framedata[1] > 3:
    #             #print(fno, framedata)
    #             print(npz['fpaths'][frame_nos[fno]])

    # game = ThreesAnalyzer(np.array(game_seq), next_tiles=np.array(nexts_seq))
    # jump_ind = 0
    # while True:
    #     move_bool = game.define_move() #(next_tiles, frame_nos)
    #     if not move_bool:
    #         if game.cur_frame < jump_ind:
    #             game.board = game.frames[jump_ind]
    #             game.cur_frame = jump_ind
    #             game.move_cnt += 1000
    #             game.get_intermediate_dict()
    #             print(game.find_moving_match())
    #         else:
    #             break

    # print(game.move_details)


    

    # pslice = slice(545,551)
    # print(frame_nos[pslice])
    # print(nexts_seq[pslice])
    # print(game_seq[pslice.stop-1].reshape([4,4]))
    # print(game.define_move())
    # print(game.find_moving_match())
    # #print(np.where(np.array(nexts_seq) > 3))
    # for i, arr in enumerate(np.array(game_seq)[pslice.stop:]):
    #     if (arr != -1).all():
    #         print(i + pslice.stop) 
    #         break
    seen_inds = -1
    start_stops = []
    nontrans_inds = []
    for i, j in enumerate(nontrans):
        if j > seen_inds:
            game2 = ThreesAnalyzer(np.array(game_seq[j:]), next_tiles=np.array(nexts_seq[j:]))
            while True:
                move_bool = game2.define_move(nexts_use_max_on_board=True) #(next_tiles, frame_nos)
                if not move_bool:
                    break
            start_stops.append([j, game2.cur_frame + j])
            nontrans_inds.append(i)
            #print(start_stops[-1])
            print([j, frame_nos[j], i], ',')
            seen_inds = game2.cur_frame + j
    print('\n')
    print(nontrans_inds)
    # for ss in start_stops:
    #     if ss[1] - ss[0] > 200:
    #         print(ss)
    #print(start_stops)
    #         print(frame_nos[j + game2.cur_frame])

    # print(game2.move_details)
    
    # #print(game2.find_moving_match())
    # print(game2.define_move())


                    

