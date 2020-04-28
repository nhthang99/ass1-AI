# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import heapq

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

class Node:
    def __init__(self, state, path, cost):
        self.state = state
        self.path = path
        self.cost = cost
    
    def __str__(self):
        return "Node(state={}, path={}, cost={})".format(self.state, self.path, self.cost)

class CustomPriorityQueue(util.PriorityQueue):
    def __init__(self):
        super().__init__()
    
    def update(self, item, priority):
        # If item already in priority queue with higher priority, update its priority and rebuild the heap.
        # If item already in priority queue with equal or lower priority, do nothing.
        # If item not in priority queue, do the same thing as self.push.
        assert(isinstance(item, Node))
        for index, (p, c, i) in enumerate(self.heap):
            if i.state == item.state:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

class GraphSearch:
    def __init__(self, problem, fringe, heuristic=None):
        self.problem = problem
        self.fringe = fringe
        self.closed = []
        self.heuristic = heuristic

    def __getStartNode(self):
        return Node(self.problem.getStartState(), [], 0)

    def getActions(self):
        startNode = self.__getStartNode()
        # Depth First Search And Breath First Search
        if not isinstance(self.fringe, util.PriorityQueue):
            self.fringe.push(startNode)
        # Uniform Cost Search
        elif not self.heuristic:
            self.fringe.push(startNode, 0)
        # A* Search
        else:
            self.fringe.push(startNode, self.heuristic(startNode.state, self.problem))

        while not self.fringe.isEmpty():
            node = self.fringe.pop()

            if self.problem.isGoalState(node.state):
                return node.path
            
            if node.state not in self.closed:
                self.closed.append(node.state)
                self.__expand(node)
                

    def __expand(self, node):
        suceessors = self.problem.getSuccessors(node.state)
        for child_state, child_path, child_cost in suceessors:
            childNode = Node(child_state, node.path + [child_path], node.cost + child_cost)
            # Depth First Search And Breath First Search
            if not isinstance(self.fringe, util.PriorityQueue):
                self.fringe.push(childNode)
            # Uniform Cost Search
            elif not self.heuristic:
                self.fringe.update(childNode, node.cost + child_cost)
            # A* Search
            else:
                self.fringe.update(childNode, node.cost + child_cost + self.heuristic(childNode.state, self.problem))


def depthFirstSearch(problem):
    "*** YOUR CODE HERE ***"
    fringe = util.Stack()
    return GraphSearch(problem, fringe).getActions()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    fringe = util.Queue()
    return GraphSearch(problem, fringe).getActions()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # fringe = util.PriorityQueue()
    fringe = CustomPriorityQueue()
    return GraphSearch(problem, fringe).getActions()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # fringe = util.PriorityQueue()
    fringe = CustomPriorityQueue()
    return GraphSearch(problem, fringe, heuristic).getActions()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
