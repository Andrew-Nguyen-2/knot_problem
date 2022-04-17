import os

import numpy as np

from solution import *


class Point:

    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"x={self.x}, y={self.y}, c={self.c}"


class Path:

    def __init__(self, case):
        self.path = []
        self.strands = []
        start_index = -1
        for i in range(len(case)):
            if case[i][0] == "-":
                start_index = i
                break

        end_index = -1
        for i in range(len(case)):
            if case[i][-1] == "-":
                end_index = i
                break
        
        current = Point(start_index, 0, '-')
        end = Point(end_index, len(case[0]) - 1, '-')
        direction = "r"

        size = (len(case), len(case[0]))
        self.size = size

        while current != end:
            self.path.append(current)
            if current.c == '-':
                if direction == "r":
                    next_x = current.x
                    next_y = current.y + 1
                    next_c = case[next_x][next_y]
                    current = Point(next_x, next_y, next_c)
                    continue
                else:
                    next_x = current.x
                    next_y = current.y - 1
                    next_c = case[next_x][next_y]
                    current = Point(next_x, next_y, next_c)
                    continue

            if current.c == '|':
                if direction == "u":
                    next_x = current.x + 1
                    next_y = current.y
                    next_c = case[next_x][next_y]
                    current = Point(next_x, next_y, next_c)
                    continue
                else:
                    next_x = current.x - 1
                    next_y = current.y
                    next_c = case[next_x][next_y]
                    current = Point(next_x, next_y, next_c)
                    continue

            if current.c == "+":
                if direction == "u" or direction == "d":
                    if case[current.x][current.y + 1] == '-':
                        next_x = current.x
                        next_y = current.y + 1
                        next_c = case[next_x][next_y]
                        current = Point(next_x, next_y, next_c)
                        direction = "r"
                        continue
                    else:
                        next_x = current.x
                        next_y = current.y - 1
                        next_c = case[next_x][next_y]
                        current = Point(next_x, next_y, next_c)
                        direction = "l"
                        continue
                if direction == "l" or direction == "r":
                    if case[current.x + 1][current.y] == '|':
                        next_x = current.x + 1
                        next_y = current.y
                        next_c = case[next_x][next_y]
                        current = Point(next_x, next_y, next_c)
                        direction = "u"
                        continue
                    else:
                        next_x = current.x - 1
                        next_y = current.y
                        next_c = case[next_x][next_y]
                        current = Point(next_x, next_y, next_c)
                        direction = "d"
                        continue

            if current.c == "I":
                if direction == "u":
                    next_x = current.x + 1
                    next_y = current.y
                    next_c = case[next_x][next_y]
                    current = Point(next_x, next_y, next_c)
                    continue
                if direction == "d":
                    next_x = current.x - 1
                    next_y = current.y
                    next_c = case[next_x][next_y]
                    current = Point(next_x, next_y, next_c)
                    continue
                if direction == "r":
                    next_x = current.x
                    next_y = current.y + 1
                    next_c = case[next_x][next_y]
                    current = Point(next_x, next_y, next_c)
                    continue
                if direction == "l":
                    next_x = current.x
                    next_y = current.y - 1
                    next_c = case[next_x][next_y]
                    current = Point(next_x, next_y, next_c)
                    continue
                    
            if current.c == "H":
                if direction == "u":
                    next_x = current.x + 1
                    next_y = current.y
                    next_c = case[next_x][next_y]
                    current = Point(next_x, next_y, next_c)
                    continue
                if direction == "d":
                    next_x = current.x - 1
                    next_y = current.y
                    next_c = case[next_x][next_y]
                    current = Point(next_x, next_y, next_c)
                    continue
                if direction == "r":
                    next_x = current.x
                    next_y = current.y + 1
                    next_c = case[next_x][next_y]
                    current = Point(next_x, next_y, next_c)
                    continue
                if direction == "l":
                    next_x = current.x
                    next_y = current.y - 1
                    next_c = case[next_x][next_y]
                    current = Point(next_x, next_y, next_c)
                    continue

            if current.c == ".":
                raise Exception("Bad traversal")


        self.path.append(end)
        self.calculate_strands()


    def __str__(self):
        path_string = [" " * self.size[1] + '\n' for i in range(self.size[0])]
        for point in self.path:
            path_string[point.x] = path_string[point.x][:point.y] + point.c + path_string[point.x][point.y + 1:]
        path_string = "".join(path_string)
        return path_string

    
    def calculate_strands(self):
        point_index = 0
        current = self.path[point_index]
        end = self.path[-1]
        direction = "r"

        strand_index = 0
        current_index = 0
        self.strands = []

        while current != end:
            current_index += 1
            if current.c == '-':
                point_index += 1
                current = self.path[point_index]
                continue

            if current.c == '|':
                point_index += 1
                current = self.path[point_index]
                continue

            if current.c == "+":
                if direction == "u" or direction == "d":
                    if self.path[point_index].y < self.path[point_index + 1].y:
                        point_index += 1
                        current = self.path[point_index]
                        direction = "r"
                        continue
                    else:
                        point_index += 1
                        current = self.path[point_index]
                        direction = "l"
                        continue
                if direction == "l" or direction == "r":
                    if self.path[point_index].x > self.path[point_index + 1].x:
                        point_index += 1
                        current = self.path[point_index]
                        direction = "u"
                        continue
                    else:
                        point_index += 1
                        current = self.path[point_index]
                        direction = "d"
                        continue

            if current.c == "I":
                if direction in "ud":
                    point_index += 1
                    current = self.path[point_index]
                    continue
                if direction in "rl":
                    self.strands.append(self.path[strand_index:current_index])
                    strand_index = current_index
                    point_index += 1
                    current = self.path[point_index]
                    continue
 
            if current.c == "H":
                if direction in "ud":
                    self.strands.append(self.path[strand_index:current_index])
                    strand_index = current_index
                    point_index += 1
                    current = self.path[point_index]
                    continue
                if direction in "rl":
                    point_index += 1
                    current = self.path[point_index]
                    continue

        self.strands.append(self.path[strand_index:current_index])



    def show_strands(self):
        print("------Strands------")
        for strand in self.strands:
            path_string = [" " * self.size[1] + '\n' for i in range(self.size[0])]
            for point in strand:
                path_string[point.x] = path_string[point.x][:point.y] + point.c + path_string[point.x][point.y + 1:]
            path_string = "".join(path_string)
            print(path_string)
        print("------------------")


    def resolve_r1_moves(self):
        last_crossing = Point(-1, -1, "undefined")
        crossing_indexes = []
        for i, point in enumerate(self.path):
            if point.c in "HI":
                if point == last_crossing:
                    # Have an r1 move
                    crossing_indexes.append((prev_index, i))
                last_crossing = point
                prev_index = i
                
        for start_index, end_index in crossing_indexes:
            self.path = self.path[:start_index] + [Point(self.path[start_index].x, self.path[start_index].y, "+")] + self.path[end_index + 1:]
         
        return len(crossing_indexes) != 0

    def resolve_r2_moves(self):
        self.calculate_strands()

        have_r2 = False

        if len(self.strands) < 2:
            return

        for i in range(len(self.strands) - 1):
            c1 = self.strands[i][-1]
            c2 = self.strands[i + 1][-1]

            for i, strand in enumerate(self.strands):
                if c1 in strand and c2 in strand:
                    over_strand, start_cross, end_cross = i, c1, c2
                    have_r2 = True
                    break

        # Need to resolve the diagram now

        return have_r2

            



    def calc_alexander(self):
        # Follow path until reach crossing
        # 
        point_index = 0
        current = self.path[point_index]
        end = self.path[-1]
        direction = "r"

        strand_index = 0
        current_index = 0

        while current != end:
            current_index += 1
            if current.c == '-':
                point_index += 1
                current = self.path[point_index]
                continue

            if current.c == '|':
                point_index += 1
                current = self.path[point_index]
                continue

            if current.c == "+":
                if direction == "u" or direction == "d":
                    if self.path[point_index].y < self.path[point_index + 1].y:
                        point_index += 1
                        current = self.path[point_index]
                        direction = "r"
                        continue
                    else:
                        point_index += 1
                        current = self.path[point_index]
                        direction = "l"
                        continue
                if direction == "l" or direction == "r":
                    if self.path[point_index].x > self.path[point_index + 1].x:
                        point_index += 1
                        current = self.path[point_index]
                        direction = "u"
                        continue
                    else:
                        point_index += 1
                        current = self.path[point_index]
                        direction = "d"
                        continue

            if current.c == "I":
                if direction in "ud":
                    point_index += 1
                    current = self.path[point_index]
                    continue
                if direction in "rl":
                    point_index += 1
                    current = self.path[point_index]
                    continue
 
            if current.c == "H":
                if direction in "ud":
                    point_index += 1
                    current = self.path[point_index]
                    continue
                if direction in "rl":
                    point_index += 1
                    current = self.path[point_index]
                    continue

        return -1


    def calc_alexander(self):
        self.calculate_strands()
        
        # TODO Play around with symbolic solver. Idea is to calculate matrix with symbols, and create alex polynomial from it


if __name__ == "__main__":
	print("yesy")
