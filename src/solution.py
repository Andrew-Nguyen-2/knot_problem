import numpy as np

# test_input_knotted = [
#     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '+', '-', '-', '-', '-', '-', '-', '+', '.', '.', '.', '.'],
#     ['.', '.', '.', '|', '.', '.', '.', '.', '.', '.', '|', '.', '.', '.', '.'],
#     ['.', '.', '.', '|', '.', '.', '.', '+', '-', '-', 'H', '-', '-', '-', '-'],
#     ['.', '.', '.', '|', '.', '.', '.', '|', '.', '.', '|', '.', '.', '.', '.'],
#     ['-', '-', '-', 'I', '-', '-', '-', 'H', '-', '-', '+', '.', '.', '.', '.'],
#     ['.', '.', '.', '|', '.', '.', '.', '|', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '+', '-', '-', '-', '+', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
# ]
#
# test_input_straightened = [
#     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '+', '-', '-', '-', '-', '-', '-', '+', '.', '.', '.', '.'],
#     ['.', '.', '.', '|', '.', '.', '.', '.', '.', '.', '|', '.', '.', '.', '.'],
#     ['.', '.', '.', '|', '.', '.', '.', '+', '-', '-', 'I', '-', '-', '-', '-'],
#     ['.', '.', '.', '|', '.', '.', '.', '|', '.', '.', '|', '.', '.', '.', '.'],
#     ['-', '-', '-', 'I', '-', '-', '-', 'H', '-', '-', '+', '.', '.', '.', '.'],
#     ['.', '.', '.', '|', '.', '.', '.', '|', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '+', '-', '-', '-', '+', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
# ]
#
# test_input_knotted2 = [
#     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '+', '-', '-', '-', '-', '-', '-', '+', '.', '.', '.', '.'],
#     ['.', '.', '.', '|', '.', '.', '.', '.', '.', '.', '|', '.', '.', '.', '.'],
#     ['.', '.', '.', '|', '.', '.', '.', '+', '-', '-', 'I', '-', '-', '-', '-'],
#     ['.', '.', '.', '|', '.', '.', '.', '|', '.', '.', '|', '.', '.', '.', '.'],
#     ['-', '-', '-', 'H', '-', '-', '-', 'I', '-', '-', '+', '.', '.', '.', '.'],
#     ['.', '.', '.', '|', '.', '.', '.', '|', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '+', '-', '-', '-', '+', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
# ]
#
# test_input_straightened2 = [
#     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '+', '-', '-', '-', '-', '-', '-', '+', '.', '.', '.', '.'],
#     ['.', '.', '.', '|', '.', '.', '.', '.', '.', '.', '|', '.', '.', '.', '.'],
#     ['.', '.', '.', '|', '.', '.', '.', '+', '-', '-', 'H', '-', '-', '-', '-'],
#     ['.', '.', '.', '|', '.', '.', '.', '|', '.', '.', '|', '.', '.', '.', '.'],
#     ['-', '-', '-', 'H', '-', '-', '-', 'I', '-', '-', '+', '.', '.', '.', '.'],
#     ['.', '.', '.', '|', '.', '.', '.', '|', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '+', '-', '-', '-', '+', '.', '.', '.', '.', '.', '.', '.'],
#     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
# ]


def load_data():
    f = open("input_cases", "r")
    knots = []
    for x in f:
        row = []
        for val in x:
            row.append(val)
        if len(row) > 0:
            knots.append(row)

    for i in range(len(knots)):
        knots[i] = knots[i][:-1]

    knots_cleaned = []
    column_lengths = []

    for i in knots:
        if i[0].isdigit():
            val = i[0]
            if i[1].isdigit():
                val = i[0] + i[1]
            column_lengths.append(val)

    for i in column_lengths:
        col = int(i)
        knot = knots[:col+1]
        knots = knots[col+1:]
        knots_cleaned.append(knot)


    for i in range(len(knots_cleaned)):
        knots_cleaned[i] = knots_cleaned[i][1:]

    return knots_cleaned


class Solve:

    def __init__(self, string_input):
        self.string_input = np.array(string_input)
        self.start_index = self.find_start()
        self.states = []
        self.num_intersections = np.count_nonzero(self.string_input == "H") + np.count_nonzero(self.string_input == "I")

    def find_start(self):
        left_column = self.string_input[:, 0]
        i = np.where(left_column == "-")
        return [i[0][0], 0]

    def get_next(self, index, prev_index):
        valid_continue = ["-", "|", "H", "I", "+"]
        # check if on left edge
        if index[1] == 0:
            above = [index[0] - 1, index[1]]
            right = [index[0], index[1] + 1]
            below = [index[0] + 1, index[1]]
            if self.string_input[above[0]][above[1]] in valid_continue and above != prev_index:
                return above
            if self.string_input[below[0]][below[1]] in valid_continue and below != prev_index:
                return below
            if self.string_input[right[0]][right[0]] in valid_continue and right != prev_index:
                return right
        # check if on top edge
        if index[0] == 0:
            left = [index[0], index[1] - 1]
            right = [index[0], index[1] + 1]
            below = [index[0] + 1, index[1]]
            if self.string_input[left[0]][left[1]] in valid_continue and left != prev_index:
                return left
            if self.string_input[below[0]][below[1]] in valid_continue and below != prev_index:
                return below
            if self.string_input[right[0]][right[0]] in valid_continue and right != prev_index:
                return right
        # check if on right edge
        if index[0] == 8:
            above = [index[0] - 1, index[1]]
            left = [index[0], index[1] - 1]
            below = [index[0] + 1, index[1]]
            if self.string_input[above[0]][above[1]] in valid_continue and left != prev_index:
                return left
            if self.string_input[below[0]][below[1]] in valid_continue and below != prev_index:
                return below
            if self.string_input[above[0]][above[1]] in valid_continue and above != prev_index:
                return above
        # check if on bottom edge
        if index[0] == 14:
            above = [index[0] - 1, index[1]]
            left = [index[0], index[1] - 1]
            right = [index[0], index[1] + 1]
            if self.string_input[above[0]][above[1]] in valid_continue and above != prev_index:
                return above
            if self.string_input[left[0]][left[1]] in valid_continue and left != prev_index:
                return left
            if self.string_input[right[0]][right[0]] in valid_continue and right != prev_index:
                return right

        above = [index[0] - 1, index[1]]
        left = [index[0], index[1] - 1]
        right = [index[0], index[1] + 1]
        below = [index[0] + 1, index[1]]
        previous_string = self.string_input[prev_index[0]][prev_index[1]]
        current_string = self.string_input[index[0]][index[1]]
        intersections = ["I", "H"]
        if self.string_input[above[0]][above[1]] in valid_continue and above != prev_index:
            if current_string == "+" or previous_string == "|" or previous_string in intersections:
                return above
            if self.string_input[left[0]][left[1]] not in valid_continue and \
                    self.string_input[right[0]][right[1]] not in valid_continue:
                return above
        if self.string_input[left[0]][left[1]] in valid_continue and left != prev_index:
            if current_string == "+" or previous_string == "-" or previous_string in intersections:
                return left
            if self.string_input[above[0]][above[1]] not in valid_continue and \
                    self.string_input[below[0]][below[1]] not in valid_continue:
                return left
        if self.string_input[right[0]][right[0]] in valid_continue and right != prev_index:
            if current_string == "+" or previous_string == "-" or previous_string in intersections:
                return right
            if self.string_input[above[0]][above[1]] not in valid_continue and \
                    self.string_input[below[0]][below[1]]:
                return right
        if self.string_input[below[0]][below[1]] in valid_continue and below != prev_index:
            if current_string == "+" or previous_string == "|" or previous_string in intersections:
                return below
            if self.string_input[left[0]][left[1]] not in valid_continue and \
                    self.string_input[right[0]][right[1]] not in valid_continue:
                return below

    def iterate_string(self):
        curr = self.start_index
        prev = self.start_index
        i = 0

        while i < self.num_intersections:
            current_string_value = self.string_input[curr[0]][curr[1]]
            previous_string_value = self.string_input[prev[0]][prev[1]]

            if previous_string_value == "-" and current_string_value == "H":
                self.states.append("over")
                i += 1
            if previous_string_value == "-" and current_string_value == "I":
                self.states.append("under")
                i += 1
            if previous_string_value == "|" and current_string_value == "H":
                self.states.append("under")
                i += 1
            if previous_string_value == "|" and current_string_value == "I":
                self.states.append("over")
                i += 1

            tmp = curr
            curr = self.get_next(tmp, prev)
            prev = tmp

    def output(self):
        knot = False
        for i in range(1, len(self.states)):
            if self.states[i] != self.states[i-1]:
                knot = True
            if self.states[i] == self.states[i-1]:
                knot = False

        if knot:
            return "knotted"
        else:
            return "straightened"


if __name__ == "__main__":
    # knotted = Solve(test_input_knotted)
    # straightened = Solve(test_input_straightened)
    # knotted2 = Solve(test_input_knotted2)
    # straightened2 = Solve(test_input_straightened2)
    #
    # knotted.iterate_string()
    # print(knotted.output())
    #
    # straightened.iterate_string()
    # print(straightened.output())
    #
    # knotted2.iterate_string()
    # print(knotted2.output())
    #
    # straightened2.iterate_string()
    # print(straightened2.output())
    knots = load_data()
    for i in knots:
        solution = Solve(i)
        solution.iterate_string()
        print(solution.output())
