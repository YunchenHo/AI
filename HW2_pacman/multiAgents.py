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
    return currentGameState.getScore() # pacman.py 中的 GameState.getScore() 已經包含了吃食物、時間懲罰、吃鬼獎勵等因素，直接回傳


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
    MinimaxAgent：
    使用 Minimax 演算法在搜尋樹中找出 Pacman 的最佳行動。

    - Pacman（agentIndex=0）是 MAX 玩家，目標是最大化分數。
    - 所有鬼魂（agentIndex>=1）是 MIN 玩家，假設會選擇讓 Pacman 最差的動作。
    - 搜尋深度由 self.depth 決定，depth=1 代表 Pacman 走一步 + 所有鬼魂各走一步。
    - 葉節點（終止狀態或達到最大深度）由 self.evaluationFunction 評分。
    - 支援任意數量的鬼魂，每個 depth 層包含一個 MAX 層（Pacman）和多個 MIN 層（每隻鬼各一層）。
    """

    # minimax 是核心遞迴函式
    # 根據當前 agentIndex 和 depth 來決定是 MAX 還是 MIN 節點，並返回該節點的分數
    def minimax(self, state, agentIndex, depth):
        
        # 終止條件1：遊戲已結束（贏或輸），直接回傳評估分數
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)
        
        # 終止條件2：輪到 Pacman 且已達到最大搜尋深度，回傳葉節點評估分數
        if agentIndex == 0 and depth == self.depth:
            return self.evaluationFunction(state)

        # 計算下一個行動的 agent：(目前index+1) 對總agent數取餘數，超過就回到 Pacman(0)
        nextAgent = (agentIndex + 1) % state.getNumAgents()
        # 只有當下一個 agent 是 Pacman（代表一輪結束）時，depth 才 +1
        if nextAgent == 0:
            nextDepth = depth + 1  
        else:
            nextDepth = depth

        # Pacman 的回合（MAX 節點）：選擇所有子節點中分數最大的
        if agentIndex == 0:
            bestValue = float('-inf') # 初始化為負無限大，確保任何值都能更新
            for action in state.getLegalActions(0): # 遍歷 Pacman 所有合法動作
                childState = state.getNextState(0, action) # 產生執行這個動作後的子狀態
                value = self.minimax(childState, nextAgent, nextDepth)  # 這個子狀態傳給下一層遞迴
                bestValue = max(bestValue, value) # 保留最大值（MAX 玩家選最好的）
            return bestValue 
            # 如果我是 Pacman，我會選最好的那步，所以這個state的價值就是那個最大分數。

        # 鬼魂的回合（MIN 節點）：選擇所有子節點中分數最小的
        else:
            bestValue = float('inf') # 初始化為正無限大，確保任何值都能更新
            for action in state.getLegalActions(agentIndex): # 遍歷該鬼魂所有合法動作
                childState = state.getNextState(agentIndex, action) # 產生執行這個動作後的子狀態
                value = self.minimax(childState, nextAgent, nextDepth) # 這個子狀態傳給下一層遞迴
                bestValue = min(bestValue, value) # 保留最小值（MIN 玩家選最差的）
            return bestValue 
            # 如果我是鬼魂，我會選讓 Pacman 最慘的那步，所以這個state的價值就是那個最小分數。
    
    # 子節點的 return bestValue → 變成父節點的 value → 父節點再拿去比較更新 bestValue 

    
    # getAction 是 Minimax 的頂層，為分數→動作的轉換層
    # 裡面會呼叫 minimax 來評估每個動作的分數，最後回傳分數最高的動作執行
    def getAction(self, gameState):
        bestAction = None # 記錄目前最佳動作，初始為 None（尚未找到）
        bestScore = float('-inf') # 記錄目前最高分數，初始為負無限大

        # 遍歷 Pacman 所有合法動作（相當於 MAX 節點的頂層展開）
        for action in gameState.getLegalActions(0):
            childState = gameState.getNextState(0, action) # 產生 Pacman 執行動作後的子狀態
            score = self.minimax(childState, agentIndex=1, depth=0) # 從鬼魂回合開始遞迴（depth=0）
            if score > bestScore: # 若此動作的分數更高，更新最佳動作
                bestScore = score
                bestAction = action

        return bestAction # 回傳分數最高的動作



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Alpha-Beta Pruning Agent：
    在 Minimax 的基礎上加入剪枝機制，大幅減少需要展開的節點數，但結果與 Minimax 完全相同。

    - alpha：MAX 玩家（Pacman）目前已保證能拿到的最低分。
    - beta：MIN 玩家（鬼魂）目前已保證能壓到的最高分。
    - MAX 節點剪枝條件：當 v > beta，代表鬼魂不會選這條路（已有更好的選擇），直接放棄。
    - MIN 節點剪枝條件：當 v < alpha，代表 Pacman 不會選這條路（已有更好的選擇），直接放棄。
    - Pruning 使用不等號（> 和 <），不在等號時剪枝。
    - 子節點按照 getLegalActions 的原始順序處理，不能重新排序。
    """

    # alphabeta 是核心遞迴函式，邏輯與 Minimax 相同，但加入 alpha 和 beta 參數來進行剪枝
    def alphabeta(self, state, agentIndex, depth, alpha, beta):
        # 終止條件1：遊戲已結束（贏或輸），直接回傳評估分數
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        # 終止條件2：輪到 Pacman 且已達到最大搜尋深度，回傳葉節點評估分數
        if agentIndex == 0 and depth == self.depth:
            return self.evaluationFunction(state)

        # 計算下一個行動的 agent 與深度（邏輯與 Minimax 相同）
        nextAgent = (agentIndex + 1) % state.getNumAgents()
        if nextAgent == 0:
            nextDepth = depth + 1
        else:
            nextDepth = depth

        # Pacman 的回合（MAX 節點）
        if agentIndex == 0:
            bestValue = float('-inf') # 初始化為負無限大
            for action in state.getLegalActions(0):
                childState = state.getNextState(0, action)
                # 傳遞 alpha, beta 給子節點，讓子節點能進行剪枝
                value = self.alphabeta(childState, nextAgent, nextDepth, alpha, beta) 
                bestValue = max(bestValue, value)
                # beta剪枝：Pacman 所選的節點分數已高於鬼魂保證能壓到的最高分（beta），鬼魂不會選這條路
                if bestValue > beta: 
                    return bestValue
                alpha = max(alpha, bestValue) # 更新 alpha：Pacman 找到更好的選擇
            return bestValue

        # 鬼魂的回合（MIN 節點）
        else:
            bestValue = float('inf') # 初始化為正無限大
            for action in state.getLegalActions(agentIndex):
                childState = state.getNextState(agentIndex, action)
                # 傳遞 alpha, beta 給子節點，讓子節點能進行剪枝
                value = self.alphabeta(childState, nextAgent, nextDepth, alpha, beta)
                bestValue = min(bestValue, value)
                # alpha剪枝：鬼魂所選的節點分數已低於 Pacman 保證能拿到的最低分（alpha），Pacman 不會選這條路
                if bestValue < alpha:
                    return bestValue
                beta = min(beta, bestValue) # 更新 beta：鬼魂找到更能壓低分數的選擇
            return bestValue


    # getAction 是 Alpha-Beta 的頂層，為分數→動作的轉換層
    # 裡面會呼叫 alphabeta 來評估每個動作的分數，最後回傳分數最高的動作執行
    def getAction(self, gameState):
        bestAction = None
        bestScore = float('-inf')
        alpha = float('-inf') # 初始 alpha = -∞，Pacman 尚未找到任何保證分數
        beta = float('inf') # 初始 beta = +∞，鬼魂尚未找到任何壓制分數

        # 頂層展開 Pacman 的所有合法動作（相當於 MAX 節點）
        for action in gameState.getLegalActions(0):
            childState = gameState.getNextState(0, action)
            score = self.alphabeta(childState, agentIndex=1, depth=0, alpha=alpha, beta=beta)
            if score > bestScore: # 若此動作更好，更新最佳動作
                bestScore = score
                bestAction = action
            alpha = max(alpha, score) # 頂層也要更新 alpha，讓後續子節點能正確剪枝

        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    ExpectimaxAgent：
    改良自 Minimax，適合對抗「非最優對手」（例如隨機行動的鬼魂）。

    - Pacman（MAX 節點）的邏輯與 Minimax 完全相同，選擇最大值。
    - 鬼魂改為「Chance 節點」，不再假設鬼魂選最壞的，而是假設鬼魂均勻隨機選動作。
    - Chance 節點的值 = 所有子節點分數的平均值（期望值）。
    - 因為鬼魂不是最優對手，Expectimax 的 Pacman 行為比 Minimax 更大膽。
    - 無法使用 Alpha-Beta Pruning（Chance 節點的期望值必須看完所有子節點才能確定）。
    """

    # expectimax 是核心遞迴函式，邏輯與 Minimax 相似
    # 但鬼魂改為 Chance 節點，計算所有子節點分數的平均值（期望值）
    def expectimax(self, state, agentIndex, depth):
        # 終止條件1：遊戲已結束（贏或輸），直接回傳評估分數
        if state.isWin() or state.isLose():
            return self.evaluationFunction(state)

        # 終止條件2：輪到 Pacman 且已達到最大搜尋深度，回傳葉節點評估分數
        if agentIndex == 0 and depth == self.depth:
            return self.evaluationFunction(state)

        # 計算下一個行動的 agent 與深度（邏輯與 Minimax 相同）
        nextAgent = (agentIndex + 1) % state.getNumAgents()
        if nextAgent == 0:
            nextDepth = depth + 1
        else:
            nextDepth = depth

        # Pacman 的回合（MAX 節點）：與 Minimax 完全相同，選最大值
        if agentIndex == 0:
            bestValue = float('-inf') # 初始化為負無限大
            for action in state.getLegalActions(0):
                childState = state.getNextState(0, action)
                value = self.expectimax(childState, nextAgent, nextDepth)
                bestValue = max(bestValue, value) # 選擇分數最高的動作
            return bestValue

        # 鬼魂的回合（Chance 節點）：計算所有子節點分數的平均值（期望值）
        else:
            totalValue = 0 # 累加所有子節點的分數
            actions = state.getLegalActions(agentIndex)
            if len(actions) == 0: # 若無合法動作，回傳 0
                return 0
            for action in actions:
                childState = state.getNextState(agentIndex, action)
                value = self.expectimax(childState, nextAgent, nextDepth)
                totalValue += value # 累加每個動作的分數
            averageValue = totalValue / len(actions) # 除以動作數量，得到期望值
            return averageValue


    # getAction 是 Expectimax 的頂層，為分數→動作的轉換層
    # 裡面會呼叫 expectimax 來評估每個動作的分數，最後回傳分數最高的動作執行
    def getAction(self, gameState):
        bestAction = None # 記錄目前最佳動作
        bestScore = float('-inf') # 記錄目前最高分數

        # 遍歷 Pacman 所有合法動作（頂層 MAX 節點展開）
        for action in gameState.getLegalActions(0):
            childState = gameState.getNextState(0, action)
            score = self.expectimax(childState, agentIndex=1, depth=0)  # 從鬼魂回合開始遞迴
            if score > bestScore: # 若此動作的期望分數更高，更新最佳動作
                bestScore = score
                bestAction = action

        return bestAction # 回傳期望分數最高的動作


# 調整各項評分權重，讓 Pacman 更積極地追食物，吃 capsule 製造 scared 狀態，同時更謹慎地避開鬼魂
def betterEvaluationFunction(currentGameState):
    """
    改良版的評估函式，評估當前遊戲狀態(而非動作)的優劣。

    設計考量：
    1. 食物距離：引導 Pacman 靠近食物，每顆食物都給予距離倒數的加分，最近食物再額外加分。
    2. 鬼魂處理：
       - scaredTimer > 5（鬼魂仍處於 scared 狀態且時間充裕）：給予大量固定獎勵（100分），
         鼓勵 Pacman 維持讓鬼魂 scared 的狀態（吃 capsule），但不強迫追鬼以避免計時器歸零的風險。
       - 鬼魂正常且距離 <= 2：大幅扣分，距離越近扣越多，避免近距離危險。
       - 鬼魂正常且距離 > 2：輕微扣分，引導 Pacman 不要朝鬼魂方向移動。
    3. Capsule 距離：靠近能量豆加分，讓 Pacman 主動去吃 capsule 製造 scared 狀態。
    """
    # 基礎分數：當前遊戲狀態的分數（包含已吃食物、時間懲罰、吃鬼獎勵等）
    score = currentGameState.getScore()

    # 取得 Pacman 目前位置
    pacPosition = currentGameState.getPacmanPosition()

    # 取得所有剩餘食物的座標列表
    findFood = currentGameState.getFood()
    foodList = []
    for x in range(findFood.width): # 遍歷地圖所有 x 座標
        for y in range(findFood.height): # 遍歷地圖所有 y 座標
            currentFood = findFood[x][y] # 取得該格是否有食物（True/False）
            if currentFood == True: # 若有食物，記錄其座標
                foodList.append((x, y))

    # 食物距離評分：對每顆食物加上距離倒數，並額外獎勵最近的食物
    if foodList:
        nearestFood = float('inf') # 記錄最近食物距離，初始為正無限大
        for food in foodList:
            currentFood = manhattanDistance(pacPosition, food) # 計算到該食物的曼哈頓距離
            score += 3.0 / currentFood # 每顆食物都加分，距離越近加越多
            if currentFood < nearestFood: # 更新最近食物距離
                nearestFood = currentFood
        score += 6.0 / nearestFood # 對最近的食物額外加分，強化靠近行為

    # 鬼魂距離評分：根據 scaredTimer 分兩種情況處理
    ghostStates = currentGameState.getGhostStates()
    for ghost in ghostStates:
        ghostPosition = ghost.getPosition() # 取得鬼魂座標
        ghostScaredTime = ghost.scaredTimer # 取得 scared 剩餘時間
        ghostDistance = manhattanDistance(pacPosition, ghostPosition) # 計算與鬼魂的距離
        if ghostDistance > 0: # 避免除以零
            if ghostScaredTime > 5:
                score += 100.0 # scared 時間充裕：給予大量獎勵，鼓勵維持此狀態
                               # ghostScaredTime 大於 5 時，給予大量分數獎勵，Pacman 可以安全地吃掉鬼魂
                               # 但當小於 5 時，不再有獎勵，讓Pacman不要再靠近鬼魂
            elif ghostDistance <= 2:
                score -= 2.0 / ghostDistance # 正常鬼魂且非常近：大幅扣分，緊急避開
            else:
                score -= 1.5 / ghostDistance # 正常鬼魂但距離較遠：輕微扣分，保持警覺

    # Capsule 距離評分：靠近能量豆加分，引導 Pacman 去吃 capsule 以製造 scared 狀態
    capsuleList = currentGameState.getCapsules()
    for capsule in capsuleList:
        capsuleDistance = manhattanDistance(pacPosition, capsule) # 計算到能量豆的距離
        score += 1.0 / capsuleDistance # 距離越近加越多分

    return score # 回傳綜合評估分數

# Abbreviation
better = betterEvaluationFunction

"""
補充概念：

葉節點 
→ evaluationFunction() 算分
→ return 分數給上層
→ 上層 max/min 比較
→ 再 return 給更上層
→ 一路推回頂層
→ getAction() 選最佳動作
"""