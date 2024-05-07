import random
class Agents:
    def getNextAction(self,gameState):
        pass

class RandomChoice(Agents):
    def getNextAction(self, gameState):
        fliesPos = gameState.getFliesPositions().copy()
        legalActions = [gameState.getLegalActions(fly) for fly in fliesPos] 
        # print(legalActions)
        random_actions = [random.choice(actions) for actions in legalActions]

        return [dir for dir,_ in random_actions]

