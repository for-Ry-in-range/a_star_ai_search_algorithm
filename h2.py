from h1 import *
import sys 
import heapq


def linear_conflict(board, goal):
    """Count linear conflicts in rows and columns"""
    conflicts = 0
    
    # CHECK ROWS 
    for row in range(3):
        for col in range(3):
            val = board[row][col]
            if val == 0:
                continue 
            goal_row, goal_col = find_tile(goal, val)
            if row == goal_row:
                for col2 in range(col + 1, 3):
                    val2 = board[row][col2]
                    if val2 == 0:
                        continue 
                    goal_row2, goal_col2 = find_tile(goal, val2)
                    
                    if goal_row2 == row and goal_col2 < goal_col:
                        conflicts += 1
                        
    # CHECK COLUMNS 
    for col in range(3):
        for row in range(3):
            val = board[row][col]
            if val == 0:
                continue 
            
            goal_row, goal_col = find_tile(goal, val)
            if col == goal_col:
                for row2 in range(row + 1, 3):
                    val2 = board[row2][col]
                    if val2 == 0:
                        continue 
                    goal_row2, goal_col2 = find_tile(goal, val2)
                    
                    if goal_col2 == col and goal_row2 < goal_row:
                        conflicts += 1
    
    return conflicts
            
            
            

def h2_heuristic(board, goal):
    """h2 = h1 + 2 * number of linear conflicts"""
    return manhattan(board, goal) + 2 * linear_conflict(board, goal)
    

def a_star(start, goal):
    """Returns the depth, total nodes, moves, and f values"""
    start_h = h2_heuristic(start, goal)
    
    start_node = Node(start, 0,start_h)
    open_list = []
    closed = set()
    heapq.heappush(open_list, start_node)
    total_nodes = 1

    # Go through unexpanded nodes, in order of f value
    while open_list:
        current = heapq.heappop(open_list)
        if current.board == goal:
            moves, f_values = reconstruct_path(current)
            return len(moves), total_nodes, moves, f_values
        closed.add(flatten(current.board))
        for move, new_board in get_neighbors(current.board):
            new_flat = flatten(new_board)
            if new_flat in closed:
                continue
            g = current.g + 1
            h = h2_heuristic(new_board, goal)
            new_node = Node(new_board, g, h, current, move)
            heapq.heappush(open_list, new_node)
            total_nodes += 1

    return None  # Solution not found


def main():
    # Ensure the correct amount of parameters
    if len(sys.argv) != 3:
        print("Use this format: python3 h2.py <input.txt> <output.txt>")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    start, goal = read_input(input_file)
    depth, total_nodes, moves, f_values = a_star(start, goal)
    write_output(output_file, start, goal, depth, total_nodes, moves, f_values)

if __name__ == "__main__":
    main()
