from display import display_grid

numbers = ["1","2","3","4","5","6","7","8","9"]
letters = ["A","B","C","D","E","F","G","H","I"]

test_sodoku =  [["1", "", "","4", "", "","7", "", ""],
                [ "","5", "", "","8", "", "","2", ""],
                [ "", "","9", "", "","3", "", "","6"],
                [ "", "","4", "", "","7", "", "","1"],
                ["5", "", "","8", "", "","2", "", ""],
                [ "","9", "", "","3", "", "","6", ""],
                [ "", "","5", "", "","8", "", "","2"],
                ["6", "", "","9", "", "","3", "", ""],
                [ "","1", "", "","4", "", "","7", ""]]

blank_sodoku = [["","","","","","","","",""],
                ["","","","","","","","",""],
                ["","","","","","","","",""],
                ["","","","","","","","",""],
                ["","","","","","","","",""],
                ["","","","","","","","",""],
                ["","","","","","","","",""],
                ["","","","","","","","",""],
                ["","","","","","","","",""]]

sodoku_1 =     [["1","","","","6","3","","2",""],
                ["","","3","","7","","","",""],
                ["","6","2","9","","","","","3"],
                ["2","5","","","","8","4","3",""],
                ["6","","","4","3","2","","","9"],
                ["","","8","7","","","","6","1"],
                ["4","2","","","5","9","8","7",""],
                ["","","","8","","","1","",""],
                ["","9","","1","","","","4","5"]]

sodoku_2 =     [["","","6","5","","","2","7",""],
                ["","4","","","","","","3",""],
                ["9","","","","4","3","6","","1"],
                ["","","1","","","9","","","3"],
                ["","3","4","6","","5","","",""],
                ["2","","","3","","","4","","5"],
                ["1","","5","9","3","","","","7"],
                ["","","","","","","","2",""],
                ["","8","9","","5","","3","",""]]

sodoku_3 =     [["9","","","","4","3","8","",""],
                ["","","","6","8","","","",""],
                ["","","","","","","1","","7"],
                ["","2","","","","9","","","3"],
                ["5","8","","","","","","4","1"],
                ["1","","","8","","","","7",""],
                ["8","","6","","","","","",""],
                ["","","","","6","1","","",""],
                ["","","4","3","2","","","","6"]]


class cell:
    def __init__(self,value=""):
        self.value = ""
        self.inital=False
        self.done = False
        self.possible = numbers.copy()
        if value in numbers:
            self.inital=True
            self.value = value
            self.done = True
            self.possible = []

    def strip_possible(self, row, column, square, x, y):
        if not self.done:
            #print("STRIP: " + letters[x] + numbers[y])
            possible = self.possible.copy()
            for i in range(len(possible)):
                number = possible[i]
                if number in row or number in column or number in square:
                    self.possible.remove(number)
            assert len(self.possible) > 0, ("No possible solutions for " +
                letters[x] + numbers[y])

    def remove_values(self, values):
        for number in values:
            if number in self.possible:
                self.possible.remove(number)

    def propose(self, row, column, square, x, y):
        if not self.done:
            #print("PROPOSE: " + letters[x] + numbers[y])
            assert len(self.possible) > 0, ("No possible solutions for " +
                letters[x] + numbers[y])
            if len(self.possible) == 1:
                self.value = self.possible[0]
                self.done = True
                self.possible = []
            else:
                proposed = []
                for number in self.possible:
                    row_index = x % 3
                    column_index = y % 3
                    square_index = (y % 3) + (3 * (x % 3))
                    row_only = True
                    column_only = True
                    square_only = True
                    for i in range(9):
                        if (number in row[i].possible or row[i].value == number) and i != row_index:
                            row_only = False
                        if (number in column[i].possible or column[i].value == number) and i != column_index:
                            column_only = False
                        if (number in square[i].possible or square[i].value == number) and i != square_index:
                            square_only = False
                    if row_only or column_only or square_only:
                        proposed.append(number)
                assert len(proposed) <= 1, ("Multiple solutions for " +
                    letters[x] + numbers[y] + ": " + str(proposed))
                if len(proposed) == 1:
                    self.value = proposed[0]
                    self.done = True
                    self.possible = []

def get_values(grid):
    value_grid = []
    for i in range(9):
        value_row = []
        for j in range(9):
            cell_value = grid[i][j].value
            if cell_value != "":
                value_row.append(cell_value)
            else:
                value_row.append(" ")
        value_grid.append(value_row)
    return value_grid

def get_possible(grid):
    value_grid = []
    for i in range(9):
        value_row = []
        for j in range(9):
            cell_value = grid[i][j].possible
            if cell_value != "":
                value_row.append(cell_value)
            else:
                value_row.append(" ")
        value_grid.append(value_row)
    return value_grid

def check_solution(values):
    valid = True
    for i in range(3):
        # Check row i
        row = values[i].copy()
        for k in range(row.count(" ")):
            row.remove(" ")
        if len(row) != len(set(row)):
            valid = False
            break

        # Check column i
        column = get_column(values, i).copy()
        for k in range(column.count(" ")):
            column.remove(" ")
        if len(column) != len(set(column)):
            valid = False
            break

        for j in range(3):
            # Check square (j,i)
            square = get_square(values, j, i).copy()
            for k in range(square.count(" ")):
                square.remove(" ")
            if len(square) != len(set(square)):
                valid = False
                break
        if not valid:
            break
    return valid

def check_complete(values):
    valid = True
    for i in range(3):
        # Check row i
        row = values[i].copy()
        row.sort()
        if numbers != row:
            valid = False
            break
        # Check column i
        column = get_column(values, i).copy()
        column.sort()
        if numbers != column:
            valid = False
            break
        for j in range(3):
            # Check square (j,i)
            square = get_square(values, j, i).copy()
            square.sort()
            if numbers != square:
                valid = False
                break
        if not valid:
            break
    return valid

def get_column(grid, i):
    return [row[i] for row in grid]

def get_square(grid, x, y):
    values = []
    x_offset = 3 * (x // 3)
    y_offset = 3 * (y // 3)
    for i in range(3):
        for j in range(3):
            values.append(grid[j+y_offset][i+x_offset])
    return values

def solve(input_table):
    cell_grid = []
    max_iterations = 0
    for j in range(9):
        cell_row = []
        for i in range(9):
            cell_row.append(cell(input_table[j][i]))
            if cell_row[i].value == "":
                max_iterations += 1
        cell_grid.append(cell_row)
    print("Max Iterations: " + str(max_iterations))
    values = get_values(cell_grid)
    print("Initial Values")
    display_grid(values)
    iteration = 0
    stop = False
    assert check_solution(values), "Impossible Sodoku"
    inp = input("Continue?")
    while inp != "quit" and iteration < max_iterations and not stop:
        iteration += 1
        print("Iteration: " + str(iteration))
        # Remove invalid possibilities
        for j in range(9):
            for i in range(9):
                row = values[j]
                column = get_column(values, i)
                square = get_square(values, i, j)
                cell_grid[j][i].strip_possible(row, column, square, i, j)
        # Link duplicate cells (remove possibilities) repeat until changes propogated
        for f in range(3):
            # Rows
            for j in range(9):
                row = cell_grid[j]
                possibilities = []
                for c in row:
                    if not c.done:
                        c_possible = c.possible.copy()
                        c_possible.sort()
                        possibilities.append(c_possible)
                repeats = []
                for p in possibilities:
                    duplicates = possibilities.count(p)
                    assert duplicates <= len(p), ("Impossible number of " +
                        "duplicate possibilities: Row " + numbers[j] +
                        " : " + str(possibilities))
                    if duplicates == len(p) and not p in repeats and duplicates > 1:
                        repeats.append(p)
                for _i in range(len(repeats)):
                    r1_set = set(repeats[_i])
                    for _j in range(_i+1,len(repeats)):
                        r2_set = set(repeats[_j])
                        assert len(r1_set.intersection(r2_set)) == 0, (
                            "Common numbers between duplicate possibilites: Row " +
                            numbers[j] + " : " + str(possibilities) + " : " + str(repeats))
                for r in repeats:
                    for c in row:
                        if not c.done:
                            c_possible = c.possible.copy()
                            c_possible.sort()
                            if c_possible != r:
                                c.remove_values(r)
            # Columns
            for i in range(9):
                column = get_column(cell_grid, i)
                possibilities = []
                for c in column:
                    if not c.done:
                        c_possible = c.possible.copy()
                        c_possible.sort()
                        possibilities.append(c_possible)
                repeats = []
                for p in possibilities:
                    duplicates = possibilities.count(p)
                    assert duplicates <= len(p), ("Impossible number of " +
                        "duplicate possibilities: Column " + letters[i] +
                        " : " + str(possibilities))
                    if duplicates == len(p) and not p in repeats and duplicates > 1:
                        repeats.append(p)
                for _i in range(len(repeats)):
                    r1_set = set(repeats[_i])
                    for _j in range(_i+1,len(repeats)):
                        r2_set = set(repeats[_j])
                        assert len(r1_set.intersection(r2_set)) == 0, (
                            "Common numbers between duplicate possibilites: Column " +
                            letters[i] + " : " + str(possibilities) + " : " + str(repeats))
                for r in repeats:
                    for c in column:
                        if not c.done:
                            c_possible = c.possible.copy()
                            c_possible.sort()
                            if c_possible != r:
                                c.remove_values(r)
            # Squares
            for j in range(3):
                for i in range(3):
                    square = get_square(cell_grid, i*3, j*3)
                    possibilities = []
                    for c in square:
                        if not c.done:
                            c_possible = c.possible.copy()
                            c_possible.sort()
                            possibilities.append(c_possible)
                    repeats = []
                    for p in possibilities:
                        duplicates = possibilities.count(p)
                        assert duplicates <= len(p), ("Impossible number of " +
                            "duplicate possibilities: Square " + letters[i] +
                            numbers[j-1] + " : " + str(possibilities))
                        if duplicates == len(p) and not p in repeats and duplicates > 1:
                            repeats.append(p)
                    for _i in range(len(repeats)):
                        r1_set = set(repeats[_i])
                        for _j in range(_i+1,len(repeats)):
                            r2_set = set(repeats[_j])
                            assert len(r1_set.intersection(r2_set)) == 0, (
                                "Common numbers between duplicate possibilites: Square " +
                                letters[i] + numbers[j-1] + " : " + str(possibilities) + " : " + str(repeats))
                    for r in repeats:
                        for c in square:
                            if not c.done:
                                c_possible = c.possible.copy()
                                c_possible.sort()
                                if c_possible != r:
                                    c.remove_values(r)

        # Copy single possibilities into cell, or put unique possibilities into cell
        for j in range(9):
            for i in range(9):
                row = cell_grid[j]
                column = get_column(cell_grid, i)
                square = get_square(cell_grid, i, j)
                cell_grid[j][i].propose(row, column, square, i, j)
        values = get_values(cell_grid)
        display_grid(values)
        assert check_solution(values), "Solving Failed"
        if check_complete(values):
            suffix = ""
            if iteration > 1:
                suffix = "s"
            print("Solved in " + str(iteration) + " iteration" + suffix + "  :D")
            stop = True
        else:
            pass
            #inp = input("Continue?")
    if not stop:
        print("Unable to solve in " + str(iteration) + " iterations  :(")
    print()
    return values

if __name__ == "__main__":
    solve(sodoku_1)
    solve(sodoku_2)
    solve(sodoku_3)
