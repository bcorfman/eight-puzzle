__author__ = 'brandon_corfman'
from const import UP, DOWN, LEFT, RIGHT, NUM_TILES
from search import Problem, astar_search, Node, FIFOQueue

def manhattan_distance(idx1, idx2):
    row1, col1 = idx1 / 3, idx1 % 3
    row2, col2 = idx2 / 3, idx2 % 3
    return abs(row1 - row2) + abs(col1 - col2)

def breadth_first_count_nodes_at_depth(problem, depth=28):
    node = Node(problem.initial)
    node_count = 1
    frontier = FIFOQueue()
    explored = set()
    frontier.append(node)
    old_depth = 1
    while frontier:
        node = frontier.pop()
        explored.add(node.state)
        if node.depth != old_depth:
            old_depth = node.depth
            print node.depth
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                if node.depth == depth + 1:
                    return node_count
                if node.depth == depth:
                    node_count += 1
                frontier.append(child)
    return None


class EightPuzzleProblem(Problem):
    def __init__(self, initial, goal):
        Problem.__init__(self, initial, goal)

    def actions(self, state):
        blank_idx = state.index('0')
        leftmost_in_row = blank_idx / 3 * 3
        rightmost_in_row = leftmost_in_row + 2
        # actions are valid if they don't go outside the grid
        if blank_idx + UP >= 0:
            yield UP
        if blank_idx + LEFT >= leftmost_in_row:
            yield LEFT
        if blank_idx + RIGHT <= rightmost_in_row:
            yield RIGHT
        if blank_idx + DOWN < NUM_TILES:
            yield DOWN

    def result(self, state, action):
        blank_idx = state.index('0')  # where is the blank tile located?
        swap_idx = blank_idx + action
        if swap_idx < blank_idx:
            return '%s%s%s%s%s' % (state[0:swap_idx], state[blank_idx], state[swap_idx+1:blank_idx],
                                   state[swap_idx], state[blank_idx+1:])
        else:
            return '%s%s%s%s%s' % (state[0:blank_idx], state[swap_idx], state[blank_idx+1:swap_idx],
                                   state[blank_idx], state[swap_idx+1:])

    def h(self, node):
        return sum((manhattan_distance(i, self.goal.index(s)) for i, s in enumerate(node.state) if s != '0'))


def main():
    problem = EightPuzzleProblem('164870325', '012345678')
    print len(astar_search(problem).solution())
    problem = EightPuzzleProblem('817456203', '012345678')
    print len(astar_search(problem).solution())
    problem = EightPuzzleProblem('012345678', '000000000')
    print breadth_first_count_nodes_at_depth(problem)

if __name__ == '__main__':
    main()
