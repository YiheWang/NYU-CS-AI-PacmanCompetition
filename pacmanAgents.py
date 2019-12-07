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


class CompetitionAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write your algorithm Algorithm instead of returning Directions.STOP
        return Directions.STOP


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
