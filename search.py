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
from game import Directions
from typing import List

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




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    exploration_stack = util.Stack()
    
    start_state = problem.getStartState()
    exploration_stack.push((start_state, []))
    visited_nodes = set()
    
    while not exploration_stack.isEmpty():
        current_state, action_path = exploration_stack.pop()
        
        if problem.isGoalState(current_state):
            return action_path
            
        if current_state not in visited_nodes:
            visited_nodes.add(current_state)
            for next_state, action, step_cost in problem.getSuccessors(current_state):
                if next_state not in visited_nodes:
                    new_path = action_path + [action]
                    exploration_stack.push((next_state, new_path))
                    
    return [] # Return empty list if no path is found

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    exploration_queue = util.Queue()
    
    start_state = problem.getStartState()
    exploration_queue.push((start_state, []))
    visited_nodes = set()
    
    while not exploration_queue.isEmpty():
        current_state, action_path = exploration_queue.pop()
        
        if problem.isGoalState(current_state):
            return action_path
            
        if current_state not in visited_nodes:
            visited_nodes.add(current_state)
            for next_state, action, step_cost in problem.getSuccessors(current_state):
                if next_state not in visited_nodes:
                    new_path = action_path + [action]
                    exploration_queue.push((next_state, new_path))        
    return []

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    exploration_pq = util.PriorityQueue()
    
    start_state = problem.getStartState()
    # queue -> (current_state, path_of_actions, cumulative_cost)
    exploration_pq.push((start_state, [], 0), 0)
    
    visited_nodes = set()
    
    while not exploration_pq.isEmpty():
        current_state, action_path, current_cost = exploration_pq.pop()
        
        if problem.isGoalState(current_state):
            return action_path
            
        if current_state not in visited_nodes:
            visited_nodes.add(current_state)
            
            for next_state, action, step_cost in problem.getSuccessors(current_state):
                if next_state not in visited_nodes:
                    new_path = action_path + [action]
                    new_cumulative_cost = current_cost + step_cost
                    
                    # PriorityQueue -> priority = cumulative cost
                    exploration_pq.push((next_state, new_path, new_cumulative_cost), new_cumulative_cost)  
    return []

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # priority queue -> f(n) = g(n) + h(n)
    open_list = util.PriorityQueue()
    start_loc = problem.getStartState()
    
    # queue -> (current_state, path_of_actions, cumulative_g_cost)
    # priority -> 0 + heuristic
    initial_f_cost = 0 + heuristic(start_loc, problem)
    open_list.push((start_loc, [], 0), initial_f_cost)
    best_costs_so_far = {start_loc: 0}
    
    while not open_list.isEmpty():
        curr_loc, moves, g_cost = open_list.pop()
        
        if problem.isGoalState(curr_loc):
            return moves
            
        if best_costs_so_far.get(curr_loc, float('inf')) >= g_cost:
            
            for next_loc, action, step_cost in problem.getSuccessors(curr_loc):
                new_g_cost = g_cost + step_cost
                
                if new_g_cost < best_costs_so_far.get(next_loc, float('inf')):
                    best_costs_so_far[next_loc] = new_g_cost
                    new_moves = moves + [action]
                    f_cost = new_g_cost + heuristic(next_loc, problem)
                    open_list.push((next_loc, new_moves, new_g_cost), f_cost)    
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
