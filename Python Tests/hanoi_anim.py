computer_solve = True
pretty_print = True
print_move = False
print_all_moves = False
print_steps = True

import time

class Towers:
    def __init__(self,height):
        self.height = height
        self.stacks = [[],[],[]]
        for i in range(height,0,-1):
            self.stacks[0].append(i)
    def top(self,stack):
        if len(self.stacks[stack]) > 0:
            return self.stacks[stack][len(self.stacks[stack])-1]
        else:
            return self.height + 1
    def print_stacks(self,prefix=""):
        p_strings = prefix + "\n\n"
        if pretty_print:
            for i in range(self.height,-1,-1):
                p_string = ""
                for j in range(3):
                    p_string += " "
                    if len(self.stacks[j]) < i + 1:
                        p_string += (" " * (self.height)) + "|" + (" " * (self.height))
                    else:
                        block_size = self.stacks[j][i - len(self.stacks[j])]
                        block = "+" + "-" * (block_size - 1) + "|" + "-" * (block_size - 1) + "+"
                        p_string += (" " * (self.height - block_size)) + block + (" " * (self.height - block_size))
                p_strings += p_string + "\n"
            p_strings += ((("=" * (self.height+1)) + "|" + ("=" * (self.height))) * 3) + "=\n\n"
            for i in range(3):
                p_strings += ((" " * (self.height+1)) + str(i+1) + (" " * (self.height)))
            p_strings += "\n"
        else:
            p_strings += "1 : " + str(self.stacks[0]) + "\n"
            p_strings += "2 : " + str(self.stacks[1]) + "\n"
            p_strings += "3 : " + str(self.stacks[2]) + "\n"
        print(p_strings)
    def move(self,m_source,m_target):
        move_success = True
        try:
            source = int(m_source)
            target = int(m_target)
        except:
            source = 0
            target = 0
        if source > 0 and source <= 3 and target > 0 and target <= 3 and source != target:
            if self.top(source-1) < self.top(target-1):
                self.stacks[target-1].append(self.stacks[source-1].pop())
            else:
                move_success = False
        else:
            move_success = False
        return move_success
    def solved(self):
        s_stacks = [[],[],[]]
        for i in range(self.height,0,-1):
            s_stacks[2].append(i)
        return self.stacks == s_stacks

class HanoiSolver:
    def __init__(self,stack_status_func,stack_move_func):
        self.stack_status_func = stack_status_func
        self.stack_move_func = stack_move_func
        self.h_stacks = []
    def solve(self):
        self.moves = []
        start_time = time.time()
        while True:
            self.h_stacks = self.stack_status_func()
            self.stack_sizes = [len(self.h_stacks[0]),0,0]
            self.move_stack(0,2,len(self.h_stacks[0]))
            self.h_stacks = self.stack_status_func()
            self.stack_sizes = [len(self.h_stacks[0]),0,0]
            self.move_stack(2,0,len(self.h_stacks[2]))
        end_time = time.time()
        hours, rem = divmod(end_time-start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        total_time = "{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds)
        if not print_steps:
            self.h_stacks = self.stack_status_func()
        if len(self.moves) > 1:
            print("Solved in %s moves." % len(self.moves))
        else:
            print("Solved in %s move." % len(self.moves))
        print("Solve time: " + total_time)
        if print_all_moves:
            print("Moves:")
            for move in self.moves:
                print(str(move[0]+1) + " > " + str(move[1]+1))
    def move_stack(self,s_s,t_s,block_number):
        time.sleep(0.05)
        temp_stack = list(set([0,1,2])-set([s_s,t_s]))[0]
        if block_number == 1:
            self.stack_move_func(s_s,t_s)
            self.moves.append([s_s,t_s])
            self.move_stack(temp_stack,t_s,self.stack_sizes[temp_stack])
        elif block_number > 1:
            self.move_stack(s_s,temp_stack,block_number-1)
            self.move_stack(s_s,t_s,1)
        self.stack_sizes[s_s] = 0
        self.stack_sizes[t_s] = block_number



if __name__ == "__main__":
    game_size = 0
    got_size = False
    while not got_size:
        try:
            game_size = int(input("Number of blocks: "))
            if game_size > 0 and game_size < 256:
                got_size = True
        except:
            pass
    hanoi = Towers(game_size)
    print("Optimal number of moves: %s" % ((2**game_size)-1))
    if computer_solve:
        def hanoi_status():
            hanoi.print_stacks()
            return hanoi.stacks
        def hanoi_move(s,t):
            hanoi.move(s+1,t+1)
            if print_steps:
                if print_move:
                    hanoi.print_stacks("Move: " + str(s+1) + str(t+1))
                else:
                    hanoi.print_stacks()
        HS = HanoiSolver(hanoi_status,hanoi_move)
        HS.solve()
    else:
        print("Type the source stack and then the target stack to more it to.")
        print("E.g.: 12; move the top block from the first stack to the second stack.")
        hanoi.print_stacks()
        while not hanoi.solved():
            comm = input("Move:")
            try:
                move_good = hanoi.move(comm[0],comm[1])
                if move_good:
                    hanoi.print_stacks()
            except:
                pass
        print("Solved.")
