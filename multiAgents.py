# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Actions, Directions
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

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        FoodDist = []       # Lists to store food and ghost distances
        GhostsDist = []
        result = 0
        Food = newFood.asList()
        
        num = childGameState.getNumAgents()
        for i in range(1,num):
            GhostsDist.append(manhattanDistance(newPos,childGameState.getGhostPosition(i))) #get distance from ghost positions
        
        for food in Food:
            FoodDist.append(manhattanDistance(newPos,food))     #get distance from every food
        

        for food in FoodDist:
            if food < 2:                        # getting closer to food gives us a better score
                result += 1
            elif food >= 2 and food < 10:
                result += 0.2                   # we give alot less if the foods are further away
            else:
                result += 0.1                   # and half that if food is too far away
        for dist in GhostsDist:
            if dist == 0:
                result = float("-inf")          # if we reach a ghost we lose so we don't want that
        for dist in GhostsDist:
            if dist <= 4:
                result -= len(FoodDist)*10      # if the ghost is close the result will depend on how many food we have left
                                                # if we still have lots of food deduct alot so don't get risky but if there are 
                                                # few left pacman can get more risky        
        


        return childGameState.getScore() + result

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
    Your minimax agent (question 2)
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
        "*** YOUR CODE HERE ***"
        
        GhostNo = gameState.getNumAgents() - 1      

        
        def maxvalue(gameState,depth):          # defining the max function
            pacActions = gameState.getLegalActions(0)   # get the pacman actions

            if gameState.isWin() or gameState.isLose() or depth == self.depth: #if we won/lost/found max depth return the value but no action 
                return (self.evaluationFunction(gameState),None)
            
            Action = None
            value = float("-inf")       # start at -inf and no action
            for action in pacActions:
                
                newvalue = minvalue(gameState.getNextState(0,action),1,depth )  # for each action get the minimum value of next state (1st ghost playing) 
                if newvalue[0]>value:                                           # and get the highest possible value
                    value = newvalue[0]
                    Action = action

            return (value,Action)                       #return the highest of the min values and action required
                

            

        def minvalue(gameState,agent,depth):    # defining min function
            
            ghostActions = gameState.getLegalActions(agent) # get the possible actions of the current ghost

            
            if  gameState.isWin() or gameState.isLose() or depth == self.depth:    # if is win/lose or found max depth return current value and no action
                return (self.evaluationFunction(gameState),None)
            value = float("inf")                                            # start at +inf and no action
            Action = None

            
            for action in ghostActions:     # for each possible action
                if(agent == GhostNo): # if this is the last ghost
                    newvalue = maxvalue(gameState.getNextState(agent,action),depth+1) # get the max value of the next state increasing depth by 1
                else:               # else 
                    newvalue = minvalue(gameState.getNextState(agent,action),agent+1,depth) # get the min value of next state for the next ghost
                
                if newvalue[0] < value:        # keep the minimum value of the next possible actions
                    value = newvalue[0]
                    Action = action  

            return (value,Action)               # return that value and action

        return(maxvalue(gameState,0)[1]) # return the max action starting at depth 0 will increment up to given depth = self.depth 
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        GhostNo = gameState.getNumAgents() - 1
        def maxAB(gameState,depth,a,b):         # this is exactly the same as minimax function but has less computation time
            pacActions = gameState.getLegalActions(0)

            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return (self.evaluationFunction(gameState),None)
            
            Action = None
            value = float("-inf")
            for action in pacActions:
                
                newvalue = minAB(gameState.getNextState(0,action),1,depth,a,b)
                if newvalue[0]>value:
                    value = newvalue[0]
                    Action = action
                    if value>b:             # only difference here is checking if the new value is greater than our current b (the min value we have so far)
                        return (value,Action) # if so we allways pick this value
                    a = max(a,value)          # set a to be the max between previus a and the new value

            return (value,Action)

        def minAB(gameState,agent,depth,a,b):   # same as minimax
            ghostActions = gameState.getLegalActions(agent)

            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return (self.evaluationFunction(gameState),None)
            value = float("inf")
            Action = None

            
            for action in ghostActions:
                if(agent == GhostNo): 
                    newvalue = maxAB(gameState.getNextState(agent,action),depth+1,a,b) 
                else: 
                    newvalue = minAB(gameState.getNextState(agent,action),agent+1,depth,a,b)
                
                if newvalue[0] < value:
                    value = newvalue[0]
                    Action = action
                    if value<a:     # if the value is less than a (max value we have so far) we allways pick this value
                        return (value,Action)
                    b = min(b,value) # set be to be max of previous b and new value

            return (value,Action)



        return maxAB(gameState,0,float("-inf"),float("inf"))[1]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        GhostNo = gameState.getNumAgents() - 1


        def expectimax(gameState,depth):    # expectimax works the same as minimax but instread the minvalue function is diferent
            pacActions = gameState.getLegalActions(0)

            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return (self.evaluationFunction(gameState),None)
            
            Action = None
            value = float("-inf")
            for action in pacActions:
                
                newvalue = randomGhostValue(gameState.getNextState(0,action),1,depth )
                if newvalue>value:
                    value = newvalue
                    Action = action

            return (value,Action)


        def randomGhostValue(gameState,agent,depth):

            ghostActions = gameState.getLegalActions(agent)

            
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return (self.evaluationFunction(gameState))
            
            value = 0 # here since it is required that every action has the same possibility we don't need an action from the ghosts part
            
            for action in ghostActions: # for every action in the ghostActions
                if(agent == GhostNo): # if it's the last ghost 
                    newvalue = expectimax(gameState.getNextState(agent,action),depth+1) # increment depth +1 and get the expectimax value of pacman
                    value+= 1/len(ghostActions)*newvalue[0]     # increase the value by newvalue/possible actions
                else: 
                    newvalue = randomGhostValue(gameState.getNextState(agent,action),agent+1,depth)
                    value+= 1/len(ghostActions)*newvalue  # same for other ghosts but calling randomGhostValue instead
            return value

        
        return expectimax(gameState,0)[1]       # return the expectimax action

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    
    DESCRIPTION: First of all we need to get the data about the specific Gamestate

    At start the most important thing is staying alive. So we reduce alot of points if Pacman is 1 
    move away from a ghost.
    Then decrease a little bit if the ghost is quite close so pacman doesn't stay realy close but 
    shouldn't be "afraid" to go closer if there is still food around.
    Finally we award few points if the ghosts are far away.

    Moving to food distances part:
    At start any food remaining uneaten is worth 10 points so we deduct that 
    from our score.
    Then for any food still uneaten the furthest the food the more points we deduct.This is because if
    pacman eats the closeby food, he will then remain there being "afraid" of the ghost still giving him 
    points while he keeps distance.
    So this way expanding a state where he has moved closer to the furthest foods will give him a higher score,
    eating the close foods while moving towards there increasing his score.

    Finally Capsules and scared ghosts:
    Scared ghosts are very important to be eaten since they give 200 points each.
    Capsules on the other hand don't give points but enable this bonus for a short period of time.
    So we add 100 points from any state where the scared ghost is 2 moves away(we know the depth of the search
    will be 2 so pacman will instantly find the scared ghost and reach it).
    Still awarding 20 points if the ghost is 3-6 moves away that means  we would probably get
    to the < 3 state in around 2-3 moves.
    Being more than 6 moves away from a scared ghost deducts points.
    So since this is important we "encourage" Pacman to eat the capsules by deducting 50 points at any state the capsules remain
    uneaten
    """
    
    "*** YOUR CODE HERE ***"
    PacPos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood().asList()
    Ghosts = currentGameState.getGhostStates()
    GhostNo = currentGameState.getNumAgents() -1
    Capsules = currentGameState.getCapsules()

    #print(ScaredTimers)
    result = 0

    FoodDist = [] #food distance
    CapsuleDist = [] # capsule distance
    ScaredGhostsDist = []   # scared ghost distances
    ActiveGhostDist = []    # active ghost distances


    #getting ghost and scared ghost distances
    
    for i in range(0,GhostNo):
        if Ghosts[i].scaredTimer:
            ScaredGhostsDist.append(manhattanDistance(PacPos,currentGameState.getGhostPosition(i+1)))
        else:
            ActiveGhostDist.append(manhattanDistance(PacPos,currentGameState.getGhostPosition(i+1)))

    # getting food distance
    for food in Food:
        FoodDist.append(manhattanDistance(PacPos,food))

    #getting capsule distances

    for capsule in Capsules:
        CapsuleDist.append(manhattanDistance(PacPos,capsule))
    
    # staying more than 1 point away from a ghost is very important
    for distance in ActiveGhostDist:
        if distance < 2:
            result -= 100
        if distance < 7 :
            result -= 10
        else:
            result += 10
    
    # eating a ghost is really important it gives 200 points
    for distance in ScaredGhostsDist:
        if distance < 3:
            result += 100
        if distance < 7:
            result += 20
        else:
            result -= 10
    
    # food is worth 10 points 
    result -= 10*len(Food)

    for dist in FoodDist: # having food uneaten is bad for our score
        if dist < 2:
            result -= 10
        if dist < 7:
            result -= 15
        else:
            result -= 20  # the furthest away it is the worse cause we waste time standing

    # quite important to get capsules as after that will can eat ghosts
    result -= 50*len(Capsules)



    return currentGameState.getScore() + result
    util.raiseNotDefined()    

# Abbreviation
better = betterEvaluationFunction
