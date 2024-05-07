from spider import *
from fly import *
import os 
import time
from graphics import GameVisualizer
class Directions:
    NORTH = 'North'
    SOUTH = 'South'
    EAST = 'East'
    WEST = 'West'
    STOP = 'Stop'
class Actions:
    _directions = {Directions.WEST:  (0, -1),
                Directions.STOP:  (0, 0),
                Directions.EAST:  (0, 1),
                Directions.NORTH: (-1, 0),
                Directions.SOUTH: (1, 0)}
    
    _directionsAsList = [('West', (0, -1)), ('Stop', (0, 0)), ('East', (0, 1)), ('North', (-1, 0)), ('South', (1, 0))]

    def directionToVector(direction):
        dx, dy = Actions._directions[direction]
        return (dx, dy)
    directionToVector = staticmethod(directionToVector)

    def getPossibleActions(gridSize,pos):
        possible = []
        x, y = pos
        for dir, vec in Actions._directionsAsList:
            dx, dy = vec
            next_y = y + dy
            next_x = x + dx
            if next_x > -1 and next_x < gridSize and next_y > -1 and next_y <gridSize:
                possible.append([dir,(next_x,next_y)])
        return possible
    getPossibleActions = staticmethod(getPossibleActions)

    def getSuccessor(position, action):
        dx, dy = Actions.directionToVector(action)
        x, y = position
        return (x + dx, y + dy)
    getSuccessor = staticmethod(getSuccessor)

class Agent:
    def __init__(self) -> None:
        self.pos = (0,0)
    def updatePos(self,newPos):
        pass
    def whoAmI(self,newPos):
        pass
    def currentPos(self):
        pass

class Spider(Agent):
    def __init__(self,initPos=(0,0)) -> None:
        self.pos = initPos

    def updatePos(self,newPos):
        self.pos = newPos
    
    def whoAmI(self):
        return 'S'
    def currentPos(self):
        return self.pos


class Fly(Agent):
    def __init__(self,initPos=(0,0)) -> None:
        self.pos = initPos
    def updatePos(self,newPos):
        self.pos = newPos
    def whoAmI(self):
        return 'F'
    def currentPos(self):
        return self.pos

class Layout:
    def __init__(self, gridSize=10,spiders=[(0,5),(0,5)],flies=[(0,0)]):
        self.gridSize = gridSize
        self.grid = [['.' for _ in range(gridSize)] for _ in range(gridSize)]
        self.spiders = spiders
        self.flies = flies
        self.placeFlies()
        self.placeSpiders()
        self.numSpiders = len(spiders)
        self.numFlies = len(flies)

    def placeSpiders(self):
        # Initial placement of two spiders at the top row, fourth square from the right
        for i in self.spiders:
            self.grid[i[0]][i[1]] = 'S'

    def placeFlies(self):
        for i in self.flies:
            self.grid[i[0]][i[1]] = 'F'

    def printLayout(self):
        for row in self.grid:
            print(' '.join(row))

    def updatePos(self,whose,prevPos,newPos):
        self.grid[prevPos[0]][prevPos[1]]='.'
        if whose=='S':
            if self.grid[newPos[0]][newPos[1]]=='F':
                self.grid[newPos[0]][newPos[1]]=whose
                self.numFlies-=1
                self.flies.remove((newPos[0],newPos[1]))
                # self.spiders
            else:
                self.grid[newPos[0]][newPos[1]]=whose
        if whose=='F':
            self.flies.remove((prevPos[0],prevPos[1]))
            if self.grid[newPos[0]][newPos[1]]=='S':
                self.numFlies-=1
            else:
                self.grid[newPos[0]][newPos[1]]=whose
                self.flies.append((newPos[0],newPos[1]))

    def getSpiderPositions(self):
        return self.spiders
    def getFliesPositions(self):
        return self.flies

    def getGridStatus(self):
        return self.grid


class GameStateData:
    def __init__(self,gridSize,agents) -> None:
        self.agents = agents
        self.end = False
        self.gridSize = gridSize

class GameState:
    def __init__(self,gridSize,agents) -> None:
        self.data = GameStateData(gridSize,{'S':[ Spider(s) for s in agents['S']],'F':[ Fly(f) for f in agents['F']]})
        self.layout = Layout(gridSize,agents['S'],agents['F'])

    def getLegalActions(self,pos):
        return Actions.getPossibleActions(self.data.gridSize,pos)

    def isEnd(self):
        return self.layout.numFlies==0

    def getNextStage(self):
        pass

    def generateSucssorState(self,agentIndex,action):
        # print("Agent Index: ",agentIndex)
        # print("Action: ",action)
        if agentIndex == 0:
            self.spiderApplyAction(action)            
        else:
            self.flyApplyAction(action)
        
        return self.layout.getGridStatus()

    def getSpidersPositions(self):
        return [s.currentPos() for s in self.data.agents['S']]
    def getFliesPositions(self):
        return self.layout.getFliesPositions()


    def spiderApplyAction(self,action):
        GameDynamics.move(self.data.agents['S'],self,action)

    def flyApplyAction(self,action):
        GameDynamics.move(self.data.agents['F'],self,action)



class GameDynamics:
    def move(agent:Agent,gamestate:GameState,directions:list[Directions]):
        for agent,direction in zip(agent,directions):
            # print("Updating Agent: ",agent,"Direction: ",direction)
            currentPos=agent.currentPos()
            newPos=Actions.getSuccessor(currentPos,direction)

            gamestate.layout.updatePos(agent.whoAmI(),currentPos,newPos)
            agent.updatePos(newPos)
    move = staticmethod(move)
            

class Game:
    class Agents:
        BasePolicy=BasePolicy()
        OrdinaryRollout=OrdinaryRollout()
        MultiAgentRollout=MultiAgentRollout()

    def __init__(self,gridSize,spiders,flies,cellSize=50,speed=0.1,graphics=True) -> None:
        self.gameState = GameState(gridSize,{'S':spiders,'F':flies})

        self.gameVisualizer = GameVisualizer(gridSize, cellSize, self.gameState.layout.grid)
        self.gameStateHistory = [[inner_list[:] for inner_list in self.gameState.layout.grid.copy()]] # adding initial state
        self.timeElapsed = 0

        self.graphics = graphics
        self.speed = speed
    def update_graphics(self):
        if self.timeStep<len(self.gameStateHistory):
            self.gameVisualizer.update_state(self.gameStateHistory[self.timeStep],self.timeStep,self.timeElapsed)
            self.gameVisualizer.after(int(self.speed*1000),self.update_graphics)
            self.timeStep+=1
        else: 
            self.timeStep=0
            time.sleep(0.5)
            self.gameVisualizer.update_state(self.gameStateHistory[self.timeStep],self.timeStep,self.timeElapsed)
            self.gameVisualizer.after(int(self.speed*1000),self.update_graphics)


    def visualize(self):
        self.timeStep = 0
        self.update_graphics()
        self.gameVisualizer.mainloop()

    def isEnd(self):
        return self.gameState.isEnd()

    def run(self,spiderAgent:Agents):
        if not self.graphics:
            self.gameState.layout.printLayout()

        agentKeys=list(self.gameState.data.agents.keys())
        agentIndex=0
        
        i = 0
        start = time.time()
        while not self.isEnd():
            agents = self.gameState.data.agents[agentKeys[agentIndex]]
            # Spider agent ['S']
            if agentIndex == 0:
                action = spiderAgent.getNextAction(self.gameState)
            # Fly agent ['F']
            else:
                action = RandomChoice().getNextAction(self.gameState)

            nextState = self.gameState.generateSucssorState(agentIndex,action)

            self.gameStateHistory.append([x[:] for x in nextState])
            
            if not self.graphics:
                os.system('clear')
                print("\nTime step",i)
                self.gameState.layout.printLayout()
                time.sleep(self.speed)
            
            agentIndex+=1
            agentIndex%=len(agentKeys)
            i+=1
            # if i==4:
            #     break
        end = time.time()
        self.timeElapsed = (end-start) * 10**3
        print("The time of execution is :",self.timeElapsed, "ms")
        if self.graphics:            
            self.visualize()



if __name__=="__main__":
    grid_size = 10
    spiders = [(0,5),(0,0)]
    flies = [(9,8),(8,6)]


    game = Game(grid_size,spiders,flies,graphics=True,speed=0.1)
    game.run(Game.Agents.MultiAgentRollout)
