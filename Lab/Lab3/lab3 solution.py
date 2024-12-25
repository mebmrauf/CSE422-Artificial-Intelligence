import random

# Part - 01
def alphaBetaPruningPart01(depth, player, alpha, beta):
    if depth == 5:
        return random.choice([-1, 1])

    if player == 0:
        maxVal = -float('inf')
        for i in range(2):
            eval = alphaBetaPruningPart01(depth + 1, 1, alpha, beta)
            maxVal = max(maxVal, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        return maxVal
    else:
        minVal = float('inf')
        for i in range(2):
            eval = alphaBetaPruningPart01(depth + 1, 0, alpha, beta)
            minVal = min(minVal, eval)
            beta = min(beta, eval)
            if alpha >= beta:
                break
        return minVal


def mortalKombat(startingPlayer):
    scorpionWins, subzeroWins, roundWinners = 0, 0, []
    current, next = startingPlayer, 1 - startingPlayer

    for i in range(3):
        result = alphaBetaPruningPart01(0, current, -float('inf'), float('inf'))

        if result == -1:
            roundWinners.append("Scorpion")
            scorpionWins += 1
        else:
            roundWinners.append ("Sub-Zero")
            subzeroWins += 1
        
        if scorpionWins == 2 or subzeroWins == 2:
            break
            
        current, next = next, current

    if scorpionWins > subzeroWins:
        winner = "Scorpion"
    else:
        winner = "Sub-Zero"
    
    return winner, len(roundWinners), roundWinners


# Part - 02
def alphaBetaPruningPart02(depth, isMaximizing, alpha, beta, scores, index=0):
    if depth == 3:
        return scores[index]

    if isMaximizing:
        maxEval = -float('inf')
        for i in range(2):
            eval = alphaBetaPruningPart02(depth + 1, False, alpha, beta, scores, index * 2 + i)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if alpha >= beta:
                break
        return maxEval
    else:
        minEval = float('inf')
        for i in range(2):
            eval = alphaBetaPruningPart02(depth + 1, True, alpha, beta, scores, index * 2 + i)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if alpha >= beta:
                break
        return minEval

def pacmanGame(c):
    scores = [3, 6, 2, 3, 7, 1, 2, 0]

    # Without Dark Magic (Alpha-Beta Pruning)
    rootVal = alphaBetaPruningPart02(0, True, -float('inf'), float('inf'), scores)

    # With Dark Magic
    leftSubtree = max(scores[0:4]) - c
    rightSubtree = max(scores[4:8]) - c

    if leftSubtree > rightSubtree:
        magicVal = leftSubtree
        direction = "left"
    else:
        magicVal = rightSubtree
        direction = "right"

    if magicVal > rootVal:
        print(f"The new minimax value is {magicVal}. Pacman goes {direction} and uses dark magic.")
    else:
        print(f"The minimax value is {rootVal}. Pacman does not use dark magic.")

# Part - 01 Input & Output
startingPlayer = int(input("Select Player 0: Scorpion, 1: Sub-Zero >>> "))

winner, totalRound, roundWinners = mortalKombat(startingPlayer)

print("Part - 01")
print(f"Game Winner: {winner}")
print(f"Total Rounds Played: {totalRound}")
for i in range(totalRound):
    print(f"Winner of Round {i+1}: {roundWinners[i]}")

# Part - 02 Input & Output
cost1 = 2
cost2 = 5

print("\nPart - 02")
print("Case 1:")
pacmanGame(cost1)
print("Case 2:")
pacmanGame(cost2)