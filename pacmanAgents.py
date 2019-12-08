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
        self.managerAgent = ManagerAgent(Agent)
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        self.managerAgent.registerInitialState(state)
        action = self.managerAgent.getAction(state)
        return action


class ManagerAgent(Agent):
    def registerInitialState(self, state):
        self.dodgingGhostAgent = DodgingGhostAgent(Agent)
        self.BFSAgent = BFSAgent(Agent)
        # self.hillClimberAgent = HillClimberAgent(Agent)
        self.dodgingGhostAgent.registerInitialState(state)
        self.BFSAgent.registerInitialState(state)
        # self.hillClimberAgent.registerInitialState(state)
        return

    def getAction(self, state):
        ghostPositions = state.getGhostPositions()
        pacmanPosition = state.getPacmanPosition()

        euclideanDistance = min(getEuclideanDistance(ghostPositions, pacmanPosition))
        ghostOneDistance = self.getBFSDistance(ghostPositions[0], pacmanPosition, state)
        ghostTwoDistance = self.getBFSDistance(ghostPositions[1], pacmanPosition, state)
        BFSDistance = min(ghostOneDistance, ghostTwoDistance)

        if euclideanDistance < 3:
            if BFSDistance < 4:
                return self.dodgingGhostAgent.getAction(state)
            else:
                return self.BFSAgent.getAction(state)
                # return self.hillClimberAgent.getAction(state)
        else:
            return self.BFSAgent.getAction(state)
            # return self.hillClimberAgent.getAction(state)

    def getBFSDistance(self, ghostPosition, pacmanPosition, state):
        mp = state.getWalls()
        n = len(mp[:])
        m = len(mp[0])
        visit = copy.deepcopy(mp)
        for i in range(n):
            for j in range(m):
                visit[i][j] = False
        visit[pacmanPosition[0]][pacmanPosition[1]] = True
        queue = []
        queue.append((pacmanPosition[0], pacmanPosition[1], 0))
        while len(queue) != 0:
            current_node = queue.pop(0)
            position_x = copy.deepcopy(current_node[0])
            position_y = copy.deepcopy(current_node[1])
            if position_x == ghostPosition[0] and position_y == ghostPosition[1]:
                return current_node[2]
            else:
                if 0 <= position_x - 1 < n and visit[position_x - 1][position_y] is False \
                        and mp[position_x - 1][position_y] is False:
                    visit[position_x - 1][position_y] = True
                    queue.append((position_x - 1, position_y, current_node[2] + 1))
                if 0 <= position_x + 1 < n and visit[position_x + 1][position_y] is False \
                        and mp[position_x + 1][position_y] is False:
                    visit[position_x + 1][position_y] = True
                    queue.append((position_x + 1, position_y, current_node[2] + 1))
                if 0 <= position_y - 1 < m and visit[position_x][position_y - 1] is False \
                        and mp[position_x][position_y - 1] is False:
                    visit[position_x][position_y - 1] = True
                    queue.append((position_x, position_y - 1, current_node[2] + 1))
                if 0 <= position_y + 1 < m and visit[position_x][position_y + 1] is False \
                        and mp[position_x][position_y + 1] is False:
                    visit[position_x][position_y - 1] = True
                    queue.append((position_x, position_y + 1, current_node[2] + 1))


class BFSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # initialize
        mp = state.getWalls()
        n = len(mp[:])
        m = len(mp[0])
        visit = copy.deepcopy(mp)
        for i in range(n):
            for j in range(m):
                visit[i][j] = False
        pacman_position = state.getPacmanPosition()
        visit[pacman_position[0]][pacman_position[1]] = True
        pellets = state.getPellets()
        capsules = state.getCapsules()
        queue = []
        legal = state.getLegalPacmanActions()
        for action in legal:
            if action is Directions.WEST:
                position_x = pacman_position[0] - 1
                position_y = pacman_position[1]
                visit[position_x][position_y] = True
                queue.append((position_x, position_y, Directions.WEST))
            elif action is Directions.EAST:
                position_x = pacman_position[0] + 1
                position_y = pacman_position[1]
                visit[position_x][position_y] = True
                queue.append((position_x, position_y, Directions.EAST))
            elif action is Directions.NORTH:
                position_x = pacman_position[0]
                position_y = pacman_position[1] + 1
                visit[position_x][position_y] = True
                queue.append((position_x, position_y, Directions.NORTH))
            elif action is Directions.SOUTH:
                position_x = pacman_position[0]
                position_y = pacman_position[1] - 1
                visit[position_x][position_y] = True
                queue.append((position_x, position_y, Directions.SOUTH))
            else:
                queue.append((pacman_position[0], pacman_position[1], Directions.STOP))
        next_action = Directions.STOP
        while len(queue) != 0:
            current_node = queue.pop(0)
            position_x = copy.deepcopy(current_node[0])
            position_y = copy.deepcopy(current_node[1])
            if (position_x, position_y) in pellets or (position_x, position_y) in capsules:
                next_action = current_node[2]
                break
            else:
                if 0 <= position_x - 1 < n and visit[position_x - 1][position_y] is False \
                        and mp[position_x - 1][position_y] is False:
                    visit[position_x - 1][position_y] = True
                    queue.append((position_x - 1, position_y, current_node[2]))
                if 0 <= position_x + 1 < n and visit[position_x + 1][position_y] is False \
                        and mp[position_x + 1][position_y] is False:
                    visit[position_x + 1][position_y] = True
                    queue.append((position_x + 1, position_y, current_node[2]))
                if 0 <= position_y - 1 < m and visit[position_x][position_y - 1] is False \
                        and mp[position_x][position_y - 1] is False:
                    visit[position_x][position_y - 1] = True
                    queue.append((position_x, position_y - 1, current_node[2]))
                if 0 <= position_y + 1 < m and visit[position_x][position_y + 1] is False \
                        and mp[position_x][position_y + 1] is False:
                    visit[position_x][position_y - 1] = True
                    queue.append((position_x, position_y + 1, current_node[2]))

                    # (the next states, the first action the pacman going to take, depth)
        return next_action


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
        actionList = []
        for i in range(0, 5):
            actionList.append(Directions.STOP)
        tempState = copy.deepcopy(state)
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
                else:
                    break
            if tempState is None:
                break
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


class DodgingGhostAgent(Agent):
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
