import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import color
from skimage.transform import rescale
from sklearn.decomposition import PCA
from sklearn.neighbors import KNeighborsClassifier


def frame_subset2pcs_or_jpgs(movie_path, base_jpg_fname=None, mean_diff=3, pca_objs=None):
  """Given a path to a video file of a screen capture of a Threes game, break this
  into a series of jpg files (if base_jpg_fname is supplied). 
  
  Generally, holding each frame image as an array in memory is too costly. However,
  each frame contains a great deal of info as pixels that are irrelevant to 
  identifying the Threes game board and next tile. The current pipeline
  downscales the relevant regions of the image and then reduces dimensionality
  with PCA. This is a MUCH smaller representation of the image. So pretrained
  sklearn PCA objects are accepted to apply these transformations, and thus
  maintain and return a representation of each frame in memory.

  PARAMETERS
  movie_path: str
  base_jpg_fname: None or str
  mean_diff: int or float, limit of mean difference between saved frame and 
                current frame to be considered *same*. Slices of screen and
                looking only at GREEN channel are HARD CODED.
  pca_objs: None or pair of sklearn PCA objects: (game_board, next_tile)
  
  RETURNS
  None or pair: (list of board PCs, list of next tile PCs)
  """
  row_slice = slice(310, 1500)
  col_slice = slice(100, 790)

  vidcap = cv2.VideoCapture(movie_path)
  success, old_frame = vidcap.read()

  count = 0
  saved = 0
  game_pcs_l = []
  next_pcs_l = []
  while success:
    count += 1
    success, frame = vidcap.read()
    if success:
      diff = frame[row_slice, col_slice, 1] - old_frame[row_slice, col_slice, 1]
      if diff.mean() > mean_diff:
        if base_jpg_fname:
          if count < 100:
            print('writing', count)
          cv2.imwrite(f"{base_jpg_fname}_{count}.jpg", old_frame)

        #convert from BGR to RGB
        frame4pcs = cv2.cvtColor(old_frame, cv2.COLOR_BGR2RGB)
        if pca_objs:
          game_pcs, next_pcs = get_game_next_tile_pcs(frame4pcs, *pca_objs)
          game_pcs_l.append(game_pcs)
          next_pcs_l.append(next_pcs)

        old_frame = frame
        saved += 1
  print('Count, Saved', count, saved)
  return game_pcs_l, next_pcs_l


def next_tile_downscale_grn_chan(img):
  # channel 1 pulls green channel from RGB arr, assumes imgs are cropped to:
  # slice(323, 433), slice(345, 545)
  return rescale(img[:, :, 1], .2).ravel()


def tile2smallgray(tile_arr):
  #convert above arrays to lists of (55, 40)-shape arrays
  #by converting to grayscale and cropping and downscaling
  row_crop = slice(1, 221) #crop two rows
  col_crop = slice(3, 163) #crop 7 columns
  gray_crop = color.rgb2gray(tile_arr[row_crop, col_crop, :])
  return rescale(gray_crop, .25)


def screen_img2Xarr(img):
  row_u = 606
  width = 167
  col_l = 109
  height = 222

  tiles = []
  for i in range(4):
    for j in range(4):
      tile_r_slice = slice(row_u+i*height, row_u+(i+1)*height)
      tile_c_slice = slice(col_l+j*width, col_l+(j+1)*width)
      tile_img = img[tile_r_slice, tile_c_slice, :]
      small = tile2smallgray(tile_img)
      #X_board[4*i + j, :] = small.ravel()
      tiles.append(small.ravel())
  return np.array(tiles)


def get_game_next_tile_pcs(img_or_fpath, game_pca, next_pca):
  """img_or_fpath: np.array or str (if str then: open with plt.imread)"""
  next_tile_rows = slice(323, 433)
  next_tile_cols = slice(345, 545)

  if type(img_or_fpath) is str:
    img = plt.imread(fpath)
  else:
    img = img_or_fpath
  board_scaled = screen_img2Xarr(img)
  next_scaled = next_tile_downscale_grn_chan(img[next_tile_rows, next_tile_cols, :])

  return game_pca.transform(board_scaled), next_pca.transform(next_scaled[np.newaxis, :])


if __name__ == "__main__":

  game_training_data = np.load('/content/threes_tiles_X_y_arrs4sklearn.npz')
  X = game_training_data['X']
  y = game_training_data['y']
  game_pca = PCA(n_components=20)
  X_xform = game_pca.fit_transform(X)
  game_one_nn = KNeighborsClassifier(n_neighbors=1)
  game_one_nn.fit(X_xform, y)


  next_training = np.load('/content/next_tile_labels_arrs_v1.npz')
  next_y = next_training['labels']
  next_cropped_imgs = next_training['arrs']
  next_X_scaled = np.array([next_tile_downscale_grn_chan(img) for img in next_cropped_imgs])
  next_pca = PCA(n_components=2)
  next_onenn = KNeighborsClassifier(n_neighbors=1)
  next_X_xform = next_pca.fit_transform(next_X_scaled)
  next_onenn.fit(next_X_xform, next_y)




