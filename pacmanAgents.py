# pacmanAgents.py
# ---------------
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


from pacman import Directions
from game import Agent
import random
import math
import copy


class CompetitionAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        capsules = state.getCapsules()
        # if len(capsules) == 2:
        return Directions.STOP


class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    def mutate(self, current_action, possible):
        random_action = current_action
        while random_action == current_action:
            random_action = possible[random.randint(0, len(possible) - 1)]
        return random_action

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # generate the first seq
        # get all possible actions for pacman
        tempState = copy.deepcopy(state)
        actionList = []
        for i in range(0, 5):
            actionList.append(Directions.STOP)
        for i in range(0, len(actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                legal = tempState.getLegalPacmanActions()
                actionList[i] = legal[random.randint(0, len(legal) - 1)]
                tempState = tempState.generatePacmanSuccessor(actionList[i])
            else:
                break
        highestGameEvaluation = gameEvaluation(state, tempState)

        while tempState is not None:
            newActionList = actionList[:]
            tempState = copy.deepcopy(state)
            # tempState = state.copy()

            for i in range(0, len(newActionList)):
                if tempState is None: break
                if tempState.isWin() + tempState.isLose() == 0:
                    legal = tempState.getLegalPacmanActions()
                    newActionList[i] = legal[random.randint(0, len(legal) - 1)]
                    tempState = tempState.generatePacmanSuccessor(newActionList[i])
                else: break
            if tempState is None: break
            else:
                # else it is not the win state
                newScore = gameEvaluation(state, tempState)
                # judge whether it is a higher climb
                if newScore > highestGameEvaluation:
                    highestGameEvaluation = newScore
                    actionList = newActionList[:]
                else:
                    continue

        return actionList[0]


class DodgingGhost(Agent):
    def registerInitialState(self, state):
        return

    def getAction(self, state):
        actions = state.getLegalPacmanActions()
        actions.append(Directions.STOP)
        bestAction = None
        farthestDistance = 0.0
        # loop to find the farthest euclidean distance between pacman and ghosts
        for action in actions:
            nextState = state.generatePacmanSuccessor(action)
            # find next positions of ghost and pacman
            ghostPositions = nextState.getGhostPositions()
            nextPosition = nextState.getPacmanPosition()
            # get distance, find the closer ghost, and try to keep away from it
            distance = min(getEuclideanDistance(ghostPositions, nextPosition))
            if distance > farthestDistance:
                farthestDistance = distance
                bestAction = action

        # return the action leads to farthest distance from ghost
        return bestAction


def getEuclideanDistance(ghostPositions, pacmanPosition):
    distanceList = []
    for position in ghostPositions:
        distanceList.append(math.sqrt((position[0] - pacmanPosition[0]) ** 2 + (position[1] - pacmanPosition[1]) ** 2))
    return distanceList


def scoreEvaluation(state):
    return state.getScore() + [0, -1000.0][state.isLose()] + [0, 1000.0][state.isWin()]


def gameEvaluation(startState, currentState):
    rootEval = scoreEvaluation(startState)
    currentEval = scoreEvaluation(currentState)
    return (currentEval - rootEval) / 1000.0
