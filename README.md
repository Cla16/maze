# maze
## A maze generator written in Python3

Generates mazes using a backtracking implementation then converts those mazes into a png file.

Plan is to include multiple maze solving algorithms as well as support for the creation of braid and combo mazes

Thanks Guido Draheim whose conversion of python to PNG code serves as the base for the conversion between the generated mazes and .png files

## Quick use case

Once you have the repo cloned, run python3 maze_generator.py -s [size of NxN maze to be generated] -d [downwards-bias] -l [left-bias] -r[right-bias] -u -[up-bias]

## Questions and concerns

If you see anyway to improve either the readability or performance of the code, please open up a PR! There are definitely improvements to be made.
