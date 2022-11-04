# threes-game
Emulator and Analyzer for the mobile game [Threes](https://asherv.com/threes/).

I, personally, enjoy playing Threes because the rules are simple but encompass
a very large space of game play, like Chess or Go. Unlike these games, there is 
no adversary in Threes. The uncertainty in playing comes from an element of
randomness. (If you are unfamiliar with the game play, the link above goes to a 
quick tutorial). 

The player has rough/aggregate control of the position each tile on the board, 
but every move generates a new tile. Usually the player knows the value of this
new tile, but not exactly where it will be placed. The move direction (up,
down, left, or right) defines which edge of the board will accept the new tile,
e.g. moving tiles up makes room at the bottom. This logic is straightforward
and is captured with the .move() method in the threes.ThreesBoard class.

The details of the randomness with which new tiles are generated and placed
are internal to game. For example a common challenge in game play is having a
board with many 1s which must be matched with 2s. So one possible question
of randomness is: does the number of 1s on the board have any effect on the
probability of a 2 being the next tile? 

ThreesEmulator assumes that the randomness of the game is fairly simple,
and is based on unscientific comparisons with the actual game play. (It,
for example, does not account for the number of 1s on board when
generating a new tile.) When using the emulator it is not obvious to me
that it is a significantly different "game space" than the true game.
However, this is based only on intuition.

In order to make a detailed comparison, one needs a record of game play
of the true game. I generate this by taking a screen recording of my
phone while I play. ingest_threes_screencap.py is a script that takes 
such a video file and attempts to reduce the data to a 4x4 array 
representation of the board for each frame of the video. Currently this
uses PCA and kNearest Neighbors (the training data I use is available upon
request).

The sequence of arrays from the movie frames will be mostly redundant (such 
as when I'm thinking about the next move and nothing is happening on screen).
Even when redundant frames are filtered out, frames showing the tiles in 
motion or merging that make the game intuitive to play by swiping my 
thumb are irrelevant to the numerical representation of the state of the game.
ThreesAnalyzer contains code to deduce the sequence of moves in a game, based
on the video frame arrays. [This is a work-in-progress]

