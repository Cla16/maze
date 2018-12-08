import sys
from random import randint
import zlib
import struct
import argparse

class Maze:
    
    def __init__(self, maze_size):
       self.maze = [[1 for col in range(maze_size)] for row in range(maze_size)]
       self.entrance = randint(maze_size // 4, maze_size * 3 // 4)
    
    def show_maze(self):
        for row in range(len(self.maze)):
            print(self.maze[row])

    def generate_entrances(self):
        self.maze[0][self.entrance] = 0

    def generate_paths_backtrack(self, maze_size, up_bias, down_bias, left_bias, right_bias):
        curr_row = 1 
        curr_col = self.entrance
        self.maze[curr_row][curr_col] = 0
        visited_cells = []

        while not curr_row == maze_size - 1:
            visited_cells.append([curr_row, curr_col])
            possible_moves = []
            possible_moves += down_bias * [[curr_row - 1, curr_col]]
            possible_moves += up_bias * [[curr_row + 1, curr_col]]
            possible_moves += right_bias * [[curr_row, curr_col + 1]] 
            possible_moves += left_bias * [[curr_row, curr_col - 1]]
            viable_moves = []
            
            for i in range(len(possible_moves)):
                if possible_moves[i] not in visited_cells:
                	if possible_moves[i][0] > 0 and possible_moves[i][0] < maze_size and possible_moves[i][1] >= 0 and possible_moves[i][1] < maze_size:
                		viable_moves.append(possible_moves[i])
            
            good_moves = []

            for i in range(len(viable_moves)):
                num_of_zeroes = 0
                if [viable_moves[i][0] + 1, viable_moves[i][1]] in visited_cells:
            	    num_of_zeroes += 1
                if [viable_moves[i][0] - 1, viable_moves[i][1]] in visited_cells:
            	    num_of_zeroes += 1
                if [viable_moves[i][0], viable_moves[i][1] + 1] in visited_cells:
                    num_of_zeroes += 1	
                if [viable_moves[i][0], viable_moves[i][1] - 1] in visited_cells:
            	    num_of_zeroes += 1
                if num_of_zeroes <= 1:
               	    good_moves.append(viable_moves[i])

            if good_moves != []:
                move = good_moves[randint(0, len(good_moves) - 1)] 
                curr_row = move[0]
                curr_col = move[1]
                self.maze[curr_row][curr_col] = 0
            
            else: 
                new_spot = randint(0, len(visited_cells) - 1)
                curr_row = visited_cells[new_spot][0]
                curr_col = visited_cells[new_spot][1]

def get_args():
    parser = argparse.ArgumentParser(description = "Take in arguments to define maze")
    parser.add_argument("-s", "--maze_size", help = "set the maze_size", required = True, type = int, default = 10)
    parser.add_argument("-r", "--right_bias", help = "define how biased the maze is towards moving to the right", required = False, type = int, default = 1)
    parser.add_argument("-l", "--left_bias", help = "define how biased the maze is towards moving to the left", required = False, type = int, default = 1)
    parser.add_argument("-u", "--up_bias", help = "define how biased the maze is towards moving up", required = False, type = int, default = 1)
    parser.add_argument("-d", "--down_bias", help = "define how biased the maze is towards moving down", required = False, type = int, default = 1)
    return parser.parse_args()


def makeGrayPNG(data, height = None, width = None, path = "white"):
    def I1(value):
        return struct.pack("!B", value & (2**8-1))
    def I4(value):
        return struct.pack("!I", value & (2**32-1))
    
    # compute width & height from data if not explicit
    if height is None:
        height = len(data) # rows
    if width is None:
        width = 0
        for row in data:
            if width < len(row):
                width = len(row)
    if path == "white":
    	for i in range(height):
    		for j in range(width):
    			if data[i][j] == 0 and (i == 0 or i == height - 1):
    				data[i][j] = 127
    			elif data[i][j] == 0 :
    				data[i][j] = 255
    else:
    	for i in range(height):
    		for j in range(width):
    			if data[i][j] == 0 and (i == 0 or i == height - 1):
    				data[i][j] = 127
    			elif data[i][j] == 0 :
    				data[i][j] = 255

    # generate these chunks depending on image type
    makeIHDR = True
    makeIDAT = True
    makeIEND = True
    png = b"\x89" + "PNG\r\n\x1A\n".encode('ascii')
    if makeIHDR:
        colortype = 0 # true gray image (no palette)
        bitdepth = 8 # with one byte per pixel (0..255)
        compression = 0 # zlib (no choice here)
        filtertype = 0 # adaptive (each scanline seperately)
        interlaced = 0 # no
        IHDR = I4(width) + I4(height) + I1(bitdepth)
        IHDR += I1(colortype) + I1(compression)
        IHDR += I1(filtertype) + I1(interlaced)
        block = "IHDR".encode('ascii') + IHDR
        png += I4(len(IHDR)) + block + I4(zlib.crc32(block))
    if makeIDAT:
        raw = b""
        for y in range(height):
            raw += b"\0" # no filter for this scanline
            for x in range(width):
                c = b"\0" # default black pixel
                if y < len(data) and x < len(data[y]):
                    c = I1(data[y][x])
                raw += c
        compressor = zlib.compressobj()
        compressed = compressor.compress(raw)
        compressed += compressor.flush() #!!
        block = "IDAT".encode('ascii') + compressed
        png += I4(len(compressed)) + block + I4(zlib.crc32(block))
    if makeIEND:
        block = "IEND".encode('ascii')
        png += I4(0) + block + I4(zlib.crc32(block))
    return png

if __name__ == "__main__":
    
    args = get_args()
    x = Maze(maze_size = args.maze_size)
    x.generate_entrances()
    x.generate_paths_backtrack(maze_size = args.maze_size, up_bias = args.up_bias, down_bias = args.down_bias, right_bias = args.right_bias, left_bias = args.down_bias)
    
    photo = makeGrayPNG(x.maze)

    file = open("pngmaze.png", "wb")

    file.write(photo)
    file.close()