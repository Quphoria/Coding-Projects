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

sodoku_4 =     [["","","2","","","1","","",""],
                ["","6","8","","","","","","3"],
                ["","","","","8","6","","9",""],
                ["9","","","","","2","","8","6"],
                ["8","","4","","","","1","","2"],
                ["5","2","","8","","","","","9"],
                ["","8","","1","4","","","",""],
                ["1","","","","","","9","2",""],
                ["","","","7","","","5","",""]]

sodoku_5 =     [["8","","3","","","","4","","7"],
                ["","","","","","7","","1",""],
                ["6","2","","4","","","","",""],
                ["","","5","","4","","","",""],
                ["","","","9","","5","3","",""],
                ["","","","","","","5","",""],
                ["","9","","2","","","","","8"],
                ["","3","","5","","8","","2","1"],
                ["","","","","1","","","","3"]]

class cell:
    def __init__(self,x,y,value=""):
        self.x = x
        self.y = y
        self.coord = letters[x] + numbers[y]
        self.row_index = x % 3
        self.column_index = y % 3
        self.square_index = (y % 3) + (3 * (x % 3))
        self.value = ""
        self.inital=False
        self.done = False
        self.possible = numbers.copy()
        if value in numbers:
            self.inital=True
            self.value = value
            self.done = True
            self.possible = []

    def strip_possible(self, row, column, square):
        if not self.done:
            #print("STRIP: " + letters[x] + numbers[y])
            possible = self.possible.copy()
            for i in range(len(possible)):
                number = possible[i]
                if number in row or number in column or number in square:#
                    self.possible.remove(number)
            assert len(self.possible) > 0, ("No possible solutions for " + self.coord)

    def remove_values(self, values):
        for number in values:
            if number in self.possible:
                self.possible.remove(number)

    def clear_unless_group(self, values):
        assert len(self.possible) > 0, ("No possible solutions for " + self.coord)
        possible = self.possible.copy()
        p_set = set(possible)
        v_set = set(values)
        if len(p_set.intersection(v_set)) == len(values):
            self.possible = values.copy()
        else:
            for number in possible:
                if number in values:
                    self.possible.remove(number)
        assert len(self.possible) > 0, ("No possible group solutions for " +
            self.coord + " : " + str(possible) + " : " + str(values))

    def propose(self, row, column, square):
        if not self.done:
            #print("PROPOSE: " + letters[x] + numbers[y])
            assert len(self.possible) > 0, ("No possible solutions for " + self.coord)
            if len(self.possible) == 1:
                self.value = self.possible[0]
                self.done = True
                self.possible = []
            else:
                proposed = []
                for number in self.possible:
                    row_only = True
                    column_only = True
                    square_only = True
                    for i in range(9):
                        if (number in row[i].possible or row[i].value == number) and i != self.row_index:
                            row_only = False
                        if (number in column[i].possible or column[i].value == number) and i != self.column_index:
                            column_only = False
                        if (number in square[i].possible or square[i].value == number) and i != self.square_index:
                            square_only = False
                    if row_only or column_only or square_only:
                        proposed.append(number)
                assert len(proposed) <= 1, ("Multiple solutions for " +
                    self.coord + " : " + str(proposed))
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
            value_row.append(cell_value)
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
    for i in range(9):
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
    for i in range(3):
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

def check_duplicates(group, error_suffix):
    #print("CHK_DUP: " + error_suffix)
    possibilities = []
    for c in group:
        if not c.done:
            c_possible = c.possible.copy()
            c_possible.sort()
            possibilities.append(c_possible)
    repeats = []
    for p in possibilities:
        duplicates = possibilities.count(p)
        assert duplicates <= len(p), ("Impossible number of " +
            "duplicate possibilities: " + error_suffix +
            " : " + str(possibilities))
        if duplicates == len(p) and not p in repeats and duplicates > 1:
            repeats.append(p)
    for i in range(len(repeats)):
        r1_set = set(repeats[i])
        for j in range(i+1,len(repeats)):
            r2_set = set(repeats[j])
            assert len(r1_set.intersection(r2_set)) == 0, (
                "Common numbers between duplicate possibilites: " +
                error_suffix + " : " + str(possibilities) + " : " + str(repeats))
    for r in repeats:
        for c in group:
            if not c.done:
                c_possible = c.possible.copy()
                c_possible.sort()
                if c_possible != r:
                    c.remove_values(r)

def strip_duplicates(group, error_suffix):
    #print("STP_DUP: " + error_suffix)
    frequencies = {"1":0, "2":0, "3":0, "4":0, "5":0,
                    "6":0, "7":0, "8":0, "9":0}
    possibilities = []
    cells = []
    for c in group:
        if not c.done:
            cells.append(c)
            c_possible = set(c.possible)
            for number in c_possible:
                frequencies[number] += 1
            possibilities.append(c_possible)
    for f in frequencies.copy():
        if frequencies[f] == 0:
            del frequencies[f]
    sub_groups = {"1":set(), "2":set(), "3":set(), "4":set(), "5":set(),
                    "6":set(), "7":set(), "8":set(), "9":set()}
    for f in frequencies:
        for p in range(len(possibilities)):
            if f in possibilities[p]:
                sub_groups[f].add(p)
    if len(sub_groups) > 1:
        groups = []
        common_numbers = []
        i = 1
        while len(sub_groups) > 2 and i < 9:
            i += 1
            groups.append([])
            common_numbers.append([])
            for s in sub_groups:
                if len(sub_groups[s]) == i:
                    if sub_groups[s] in groups[i-2]:
                        common_numbers[i-2][groups[i-2].index(sub_groups[s])].append(s)
                    else:
                        groups[i-2].append(sub_groups[s])
                        common_numbers[i-2].append([s])
        length_groups = {"1":[], "2":[], "3":[], "4":[], "5":[],
                        "6":[], "7":[], "8":[], "9":[]}
        for i in range(len(groups)):
            for j in range(len(groups[i])):
                length_groups[str(len(common_numbers[i][j]))].append([groups[i][j], common_numbers[i][j]])
        old_length_groups = {}
        length_groups_data = True
        while old_length_groups != length_groups and length_groups_data:
            old_length_groups = length_groups.copy()
            updated_ids = False
            for g in length_groups:
                for i in reversed(range(len(length_groups[g]))):
                    assert len(length_groups[g][i][0]) > 0, ("No more possibilities for: "
                        + str(length_groups[g][i][1]))
                    if len(length_groups[g][i][0]) == len(length_groups[g][i][1]):
                        #print("COMMON", length_groups[g][i][0], length_groups[g][i][1])
                        cell_list = length_groups[g][i][0]
                        possibility_list = length_groups[g][i][1]
                        del length_groups[g][i]
                        for k in cell_list:
                            cells[k].clear_unless_group(possibility_list)
                            for h in length_groups:
                                for j in range(len(length_groups[h])):
                                    if k in length_groups[h][j][0]:
                                        length_groups[h][j][0].remove(k)
                                        updated_ids = True
                if updated_ids:
                    break

            length_groups_data = False
            for g in length_groups:
                if len(length_groups[g]) > 0:
                    length_groups_data = True
                    break

            if length_groups_data:
                lg_copy = length_groups.copy()
                length_groups = {"1":[], "2":[], "3":[], "4":[], "5":[],
                                "6":[], "7":[], "8":[], "9":[]}
                for g in lg_copy:
                    for i in range(len(lg_copy[g])):
                        gp = str(len(lg_copy[g][i][0]))
                        length_groups[gp].append(lg_copy[g][i])


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
            cell_row.append(cell(i, j, input_table[j][i]))
            if cell_row[i].value == "":
                max_iterations += 1
        cell_grid.append(cell_row)
    #print("Max Iterations: " + str(max_iterations))
    values = get_values(cell_grid)
    print("Initial Values")
    display_grid(values)
    iteration = 0
    stop = False
    assert check_solution(values), "Impossible Sodoku"
    inp = ""
    inp = input("Continue?")
    print("-----SOLVING-----")
    while inp != "quit" and iteration < max_iterations and not stop:
        iteration += 1
        print()
        print("Iteration: " + str(iteration))
        # Remove invalid possibilities
        for j in range(9):
            for i in range(9):
                row = values[j]
                column = get_column(values, i)
                square = get_square(values, i, j)
                cell_grid[j][i].strip_possible(row, column, square)
        # Link duplicate cells (remove possibilities) repeat until changes propogated
        # Rows
        for j in range(9):
            row = cell_grid[j]
            check_duplicates(row, "Row " + numbers[j])
        # Columns
        for i in range(9):
            column = get_column(cell_grid, i)
            check_duplicates(column, "Column " + letters[i])
        # Squares
        for j in range(3):
            for i in range(3):
                square = get_square(cell_grid, i*3, j*3)
                check_duplicates(square, "Square " + letters[i] + numbers[j-1])
        # In groups, check for pairs, with extra numbers in possible, and remove all except the pair
        if iteration == 20 or True:
            # Rows
            for j in range(9):
                row = cell_grid[j]
                strip_duplicates(row, "Row " + numbers[j])
            # Columns
            for i in range(9):
                column = get_column(cell_grid, i)
                strip_duplicates(column, "Column " + letters[i])
            # Squares
            for j in range(3):
                for i in range(3):
                    square = get_square(cell_grid, i*3, j*3)
                    strip_duplicates(square, "Square " + letters[i] + numbers[j-1])
        # Copy single possibilities into cell, or put unique possibilities into cell
        for j in range(9):
            for i in range(9):
                row = cell_grid[j]
                column = get_column(cell_grid, i)
                square = get_square(cell_grid, i, j)
                cell_grid[j][i].propose(row, column, square)
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
    print("METRO EASY")
    solve(sodoku_1)
    print("METRO MODERATE")
    solve(sodoku_2)
    print("METRO CHALLENGING")
    solve(sodoku_3)
    print("HARD")
    solve(sodoku_4)
    print("VERY HARD")
    solve(sodoku_5)
    input("Continue?")
