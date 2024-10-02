from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        def minimax(depth,agentID,state): # define a function to do recursive
            if state.isWin() | state.isLose(): # current state is already win lose 
                return self.evaluationFunction(state) # return current evaluation value
            if depth == self.depth: # reach the required depth
                return self.evaluationFunction(state) # return current evaluation value
            action = state.getLegalActions(agentID) # get the current state action with agent ID
            if agentID == 0: # agent is 0 => then is pacman
                tmp_score = float("-INF") # set a max value with the min num
                for acts in action: # go through all action
                    next_state = state.getNextState(agentID,acts) # get the action's next state
                    tmp_score = max(minimax(depth,agentID + 1,next_state),tmp_score)
                    # if the minimax return value is larger than tmp_score, change tmp_score
                return tmp_score # return the max value in this action
            else: # agent is not 0 => then is ghost
                min_score = float("INF") # set a min value with the max num
                for acts in action: # go through all action
                    next_state = state.getNextState(agentID,acts) # get the action's next state
                    if agentID + 1 >= state.getNumAgents(): # all agents choose action
                        min_score = min(minimax(depth + 1,0,next_state),min_score)
                        # if the minimax return value is smaller than min_score, change min_score
                        # since all agents has moves, depth + 1
                    else:
                        min_score = min(minimax(depth,agentID + 1,next_state),min_score)
                        # if the minimax return value is smaller than min_score, change min_score
                return min_score # return the min value in this action
        
        best = float("-INF") # set a max value with the min num
        move = None # define a variable to store action
        if gameState.isWin() | gameState.isLose() | self.depth == 0:
            return None # if already win/lose or reach required depth, do nothing
        for act in gameState.getLegalActions(0): # go through all actions
            next = gameState.getNextState(0,act) # get the action's next state
            score = minimax(0,1,next) # find out it's minimax value
            if score > best: # choose the max one 
                best = score # store its value
                move = act # store its action
        return move # return the action found
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        def alphabeta(depth,agentID,state,alpha,beta): # define a function to do recursive
            if state.isWin() | state.isLose(): # current state is already win lose 
                return self.evaluationFunction(state) # return current evaluation value
            if depth == self.depth: # reach the required depth
                return self.evaluationFunction(state) # return current evaluation value
            action = state.getLegalActions(agentID) # get the current state action with agent ID
            if agentID == 0: # agent is 0 => then is pacman
                tmp_score = float("-INF") # set a max value with the min num
                for acts in action: # go through all action
                    next_state = state.getNextState(agentID,acts) # get the action's next state
                    tmp_score = max(alphabeta(depth,agentID + 1,next_state,alpha,beta),tmp_score)
                    # if the minimax return value is larger than tmp_score, change tmp_score
                    if tmp_score > beta: 
                        return tmp_score # return if current value is larger than beta
                    alpha = max(tmp_score,alpha) # update alpha with the max value in this action
                return tmp_score # return the max value in this action
            else: # agent is not 0 => then is ghost
                min_score = float("INF") # set a min value with the max num
                for acts in action: # go through all action
                    next_state = state.getNextState(agentID,acts) # get the action's next state
                    if agentID + 1 >= state.getNumAgents(): # all agents choose action
                        min_score = min(alphabeta(depth + 1,0,next_state,alpha,beta),min_score)
                        # if the minimax return value is smaller than min_score, change min_score
                        # since all agents has moves, depth + 1
                    else:
                        min_score = min(alphabeta(depth,agentID + 1,next_state,alpha,beta),min_score)
                        # if the minimax return value is smaller than min_score, change min_score
                    if min_score < alpha: 
                        return min_score # return if current value is smaller than alpha
                    beta = min(min_score,beta) # update beta with the min value in this action
                return min_score # return the min value in this action
        
        best = float("-INF") # set a max value with the min num
        alpha = float("-INF") # set alpha to the minimal, then later update its value
        beta = float("INF") # set beta to the maximal, then later update its value
        move = None # define a variable to store action
        if gameState.isWin() | gameState.isLose() | self.depth == 0:
            return None # if already win/lose or reach required depth, do nothing
        for act in gameState.getLegalActions(0): # go through all actions
            next = gameState.getNextState(0,act) # get the action's next state
            score = alphabeta(0,1,next,alpha,beta) # find out it's minimax value
            if score > best: # choose the max one 
                best = score # store its value
                move = act # store its action
            alpha = max(score,alpha) # in here, need to update alpha
        return move # return the action found
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        def expectimax(depth,agentID,state): # define a function to do recursive
            if state.isWin() | state.isLose(): # current state is already win lose 
                return self.evaluationFunction(state) # return current evaluation value
            if depth == self.depth: # reach the required depth
                return self.evaluationFunction(state) # return current evaluation value
            action = state.getLegalActions(agentID) # get the current state action with agent ID
            if agentID == 0: # agent is 0 => then is pacman
                tmp_score = float("-INF") # set a max value with the min num
                for acts in action: # go through all action
                    next_state = state.getNextState(agentID,acts) # get the action's next state
                    tmp_score = max(expectimax(depth,agentID + 1,next_state),tmp_score)
                    # if the minimax return value is larger than tmp_score, change tmp_score
                return tmp_score # return the max value in this action
            else: # agent is not 0 => then is ghost
                val = 0. # variable to sum up all action value
                count = 0 # counting the numbers of the value
                for acts in action: # go through all action
                    count = count + 1 # the number of the value add 1
                    next_state = state.getNextState(agentID,acts) # get the action's next state
                    if agentID + 1 >= state.getNumAgents(): # all agents choose action
                        val += expectimax(depth + 1,0,next_state) 
                        # sum up the action value
                        # since all agents has moves, depth + 1
                    else:
                        val += expectimax(depth,agentID + 1,next_state) # sum up the action value
                return val/count # return the expection
        
        best = float("-INF") # set a max value with the min num
        move = None # define a variable to store action
        if gameState.isWin() | gameState.isLose() | self.depth == 0:
            return None # if already win/lose or reach required depth, do nothing
        for act in gameState.getLegalActions(0): # go through all actions
            next = gameState.getNextState(0,act) # get the action's next state
            score = expectimax(0,1,next) # find out it's minimax value
            if score > best: # choose the max one 
                best = score # store its value
                move = act # store its action
        return move # return the action found
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)      
    pac_pos = currentGameState.getPacmanPosition() # get pacman's position
    food_list = currentGameState.getFood().asList() # get the food list
    score = currentGameState.getScore() # get current score
    ghost_state = currentGameState.getGhostStates() # get the ghosts' state

    remain_cap = len(currentGameState.getCapsules()) # calculate remain capsules
    remian_food = len(food_list) # calculate remain food
    score -= 15 * remian_food # remain more, score is less
    score -= 30 * remain_cap # remain more, score is less

    for food in food_list: # go through all food
        dis = manhattanDistance(pac_pos,food) # calculate the distance
        if dis < 3: # according the the distance to decide the weight
            score -= 1 * dis
        else:
            score -= 0.5 * dis

    for ghost in ghost_state: # go through all ghost
        dis = manhattanDistance(pac_pos,ghost.getPosition())
        # calculate the distance
        # since the ghost is in state type, need to use getPosition() to get the position
        if dis < 3: # according the the distance to decide the weight
            score -= 20 * dis
        else:
            score -= 10 * dis
    
    return score
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction
