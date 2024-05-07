
def manhattanDistance(xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

class Agents:
    def getNextAction(self,gameState):
        pass
    
class BasePolicy(Agents):
    def getNextAction(self,gameState):
        spiderPos = gameState.getSpidersPositions().copy()
        fliesPos = gameState.getFliesPositions().copy()
        minDistances = []
        # Calculating the manhattan distance from all the possible next states to all the flies 
        for spider in spiderPos:
            legalActions = gameState.getLegalActions(spider)
            distances = [(dir,manhattanDistance(vec,fvec)) for dir,vec in legalActions for fvec in fliesPos]
            # Find the minimum distance
            minDistances.append(min(distances, key=lambda x: x[1]))
        return [dir for dir,dist in minDistances]

class OrdinaryRollout(Agents):
    # u = min[g(x,u1,u2) + J(f(x,u1,u2))] 
    def getNextAction(self,gameState):
        spiderPos = gameState.getSpidersPositions().copy()
        fliesPos = gameState.getFliesPositions().copy()

        legalActions = [gameState.getLegalActions(spider) for spider in spiderPos]
        # Generating all the possible outcomes
        possibleMoves = []
        for y in legalActions:
            if not possibleMoves:
                possibleMoves = [[z] for z in y]
            else:
                possibleMoves = [x+[z] for x in possibleMoves for z in y] 
        
        # print(possibleMoves)
        # u = min[g(x,u1,u2) + J(f(x,u1,u2))] = min[g(x,u1,u2)] + min[J(f(x,u1,u2))]
        costs = []
        for moves in possibleMoves:
            # print(moves)
            fliesTargeted = []
            minNodes = []
            fliesPosCopy = fliesPos.copy()
            for move in moves:
                distances = [((move[0],manhattanDistance(move[1],fvec),fvec,move[1])) for fvec in fliesPosCopy]
                # print(distances)
                if distances:
                    minDist = min(distances, key=lambda x: x[1])
                    fliesTargeted.append(minDist[2])
                    minNodes.append(minDist)
                    # fliesPosCopy.remove(minDist[2])

            # print(minNodes)
            costForActionPair=0
            for actions in minNodes:
                fliesTargetedCopy = fliesTargeted.copy()
                fliesTargetedCopy.remove(actions[2])

                fliesPosCopy = fliesPos.copy()
                
                try:
                    [fliesPosCopy.remove(x) for x in fliesTargetedCopy]
                except: 
                    # Already not present in list
                    pass

                # print("Current action: ",actions)
                # print("Other agented targeted flies: ",fliesTargetedCopy)
                # print("Remaining flies: ",fliesPosCopy)

                costApproximation = self.costApproximation(actions[3],fliesPosCopy)
                # actions[1]+=costApproximation
                costForActionPair+=actions[1]
                costForActionPair+=costApproximation
            # costs.append([() for ])
            # print(costForActionPair,end="\n\n")
            costs.append(([nodes[0] for nodes in minNodes],costForActionPair))


        # print(costs)
        minimization = min(costs,key=lambda x: x[1])
        # print(minimization)

        return minimization[0]
        

    def costApproximation(self,currentPos,fliesPos):  
        cost = 0
        a=fliesPos.copy()
        while a:
            distances = [(manhattanDistance(currentPos,flyPos),flyPos) for flyPos in a]
            nearestFly = min(distances, key=lambda x: x[0])
            cost+=nearestFly[0]
            a.remove(nearestFly[1])
            currentPos = nearestFly[1]
        return cost


class MultiAgentRollout(Agents):
    
    def getNextAction(self,gameState):
        spiderPos = gameState.getSpidersPositions().copy()
        fliesPos = gameState.getFliesPositions().copy()

        # controls = []  
        # for spider in spiderPos:
            
        # legalActions = [gameState.getLegalActions(spider) for spider in spiderPos]
        # print(legalActions)

        basePolicyControls = []  
        fliesTargeted = []  
        i=0 # current control in consideration
        for i in range(len(spiderPos)):
                distances = [(dir,manhattanDistance(vec,fvec),fvec) for dir,vec in gameState.getLegalActions(spiderPos[i]) for fvec in fliesPos]
                basePolicyControls.append(min(distances,key=lambda x: x[1]))
        
        # print(basePolicyControls)
        for i in range(len(spiderPos)):
            # print("Calculation For spider ",i)
            legalActions = gameState.getLegalActions(spiderPos[i])
            
            remainingFlies = fliesPos.copy()
            # print(remainingFlies)
            # Flies targeted by each agent 
            # Future = by base policy
            # Past = by calculation
            for j in range(len(basePolicyControls)):
                if j!=i:
                    dir, cost, nearestFly = basePolicyControls[j]
                    if nearestFly in remainingFlies: remainingFlies.remove(nearestFly)

            # calculating Q factors
            QFactors = [(dir,manhattanDistance(vec,fvec),self.costApproximation(fvec,fliesPos),fvec) for dir,vec in legalActions for fvec in  remainingFlies]  
            # print("QFactors For spider ",i,QFactors)

            if QFactors:
                minQFactor = min(QFactors,key=lambda x: x[1]+x[2])
            
            # Updating current control
                basePolicyControls[i] = (minQFactor[0],minQFactor[1],minQFactor[3])
            # print("Agent ",i,"Control finalized updated basepolicy:",basePolicyControls,"\n")

        return [dir for dir,_,_ in basePolicyControls]



    def costApproximation(self,currentPos,fliesPos):  
        cost = 0
        a=fliesPos.copy()
        while a:
            distances = [(manhattanDistance(currentPos,flyPos),flyPos) for flyPos in a]
            nearestFly = min(distances, key=lambda x: x[0])
            cost+=nearestFly[0]
            a.remove(nearestFly[1])
            currentPos = nearestFly[1]
        return cost


