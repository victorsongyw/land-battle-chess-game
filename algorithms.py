
######## This file contains all the algorithms that the game uses

from pieceClasses import *


#### finding all posts that are legal moves given a selected piece

railroadPosts = set()
# this set contains all posts that are on the railroad
for i in range(1, 11):
    railroadPosts.add((i, 0))
    railroadPosts.add((i, 4))
for i in range(0, 5):
    railroadPosts.add((1, i))
    railroadPosts.add((5, i))
    railroadPosts.add((6, i))
    railroadPosts.add((10, i))

# finding all legal moves for a selected piece
def isLegal(board, selected):
    (a, b) = selected
    valid = set()
    # landmines and pieces in headquarters cannot move
    if board[a][b].piece.order == 10 or isinstance(board[a][b], Headquarters):
        return valid

    # searching adjacent moves with one step
    for (c, d) in [(a-1, b), (a+1, b), (a, b-1), (a, b+1)]:
        if 0 <= c <= 11 and 0 <= d <= 4 and (board[c][d].piece == None or \
        (board[c][d].piece.side != board[a][b].piece.side and \
        not isinstance(board[c][d], Camp))): # pieces in camps are protected from attack
            valid.add((c, d))
    for (c, d) in [(a-1, b-1), (a-1, b+1), (a+1, b-1), (a+1, b+1)]:
        if 0 <= c <= 11 and 0 <= d <= 4 and isinstance(board[c][d], Camp) and board[c][d].piece == None:
            valid.add((c, d))
    # Camps reach out to every diagonal direction as well
    if isinstance(board[a][b], Camp):
        for (c, d) in [(a-1, b-1), (a-1, b+1), (a+1, b-1), (a+1, b+1)]:
            if 0 <= c <= 11 and 0 <= d <= 4:
                if board[c][d].piece == None or \
                (board[c][d].piece.side != board[a][b].piece.side and not isinstance(board[c][d], Camp)):
                    valid.add((c, d))
    # the front line only has three access roads; the other two are invalid
    if (a, b) in [(5, 1), (6, 1), (5, 3), (6, 3)]:
        valid.discard((5, 1))
        valid.discard((6, 1))
        valid.discard((5, 3))
        valid.discard((6, 3))

    # searching moves enabled by railroads
    if (a, b) in railroadPosts:
        # finding railroad path for Sappers (Sappers can make turns on railroads)
        if board[a][b].piece.order == 1:
            lst = []
            if (a, b) in [(5, 1), (5, 3), (6, 1), (6, 3)]:
                lst = findSprPaths(a, b-1, a, b, board, lst) + findSprPaths(a, b+1, a, b, board, lst)
            else:
                lst = findSprPaths(a-1, b, a, b, board, lst) + findSprPaths(a+1, b, a, b, board, lst) + \
                        findSprPaths(a, b-1, a, b, board, lst) + findSprPaths(a, b+1, a, b, board, lst)
            for (i, j) in lst:
                valid.add((i, j))
        # finding railroad path for regular pieces
        else: 
            # finding vertical railroad paths
            if (b == 0 or b == 4) and 1 <= a <= 10:
                (c, d) = (a, b)
                c += 1
                while (1 <= c <= 10 and board[c][d].piece == None):
                    c += 1
                    if c <= 10 and (board[c][d].piece == None or board[c][d].piece.side != board[a][b].piece.side):
                        valid.add((c, d))
                (c, d) = (a, b)
                c -= 1
                while (1 <= c <= 10 and board[c][d].piece == None):
                    c -= 1
                    if c >= 1 and (board[c][d].piece == None or board[c][d].piece.side != board[a][b].piece.side):
                        valid.add((c, d))
            # finding horizontal railroad paths
            if a == 5 or a == 6 or a == 1 or a == 10:
                (c, d) = (a, b)
                d += 1
                while (0 <= d <= 4 and board[c][d].piece == None):
                    d += 1
                    if d <= 4 and (board[c][d].piece == None or board[c][d].piece.side != board[a][b].piece.side):
                        valid.add((c, d))
                (c, d) = (a, b)
                d -= 1
                while (0 <= d <= 4 and board[c][d].piece == None):
                    d -= 1
                    if d >= 0 and (board[c][d].piece == None or board[c][d].piece.side != board[a][b].piece.side):
                        valid.add((c, d))

    valid.discard((a, b)) # make sure the self position is not included
    return valid

# recursively finding railroad paths for Sappers
def findSprPaths(a, b, i, j, board, lst):
    # base cases
    if (a, b) not in railroadPosts:
        return []
    elif (a, b) in lst:
        return []
    elif board[a][b].piece != None: 
        # railroad path is blocked by a piece
        if board[a][b].piece.side != board[i][j].piece.side:
            return [(a, b)]
        else:
            return []

    # recursive cases
    elif (a, b) in [(5, 1), (5, 3), (6, 1), (6, 3)]:
        lst.append((a, b))
        return [(a, b)] + findSprPaths(a, b-1, i, j, board, lst) + findSprPaths(a, b+1, i, j, board, lst)
    else:
        lst.append((a, b))
        return [(a, b)] + findSprPaths(a-1, b, i, j, board, lst) + findSprPaths(a+1, b, i, j, board, lst) + \
                findSprPaths(a, b-1, i, j, board, lst) + findSprPaths(a, b+1, i, j, board, lst)



#### making moves

# determine if game is over
def isOver(board):
    Aok, Bok = False, False
    for x in range(12):
        for y in range(5):
            if board[x][y].piece != None:
                if board[x][y].piece.side == "A" and Aok == False:
                    if isLegal(board, (x, y)) != set():
                        Aok = True
                elif board[x][y].piece.side == "B" and Bok == False:
                    if isLegal(board, (x, y)) != set():
                        Bok = True
    if Aok == False:
        return "B"
    elif Bok == False:
        return "A"
    else:
        return None



# two pieces make contact (and updates the game-over check)
def contactWithGameOverCheck(a, b, i, j, data):
    if data.board[a][b].piece.order == 0:
        data.winner = data.board[i][j].piece.side
    elif data.board[i][j].piece.order == 0:
        data.winner = data.board[a][b].piece.side
    contact(a, b, i, j, data.board)
    if isOver(data.board) != None:
        data.winner = isOver(data.board)

# two pieces make contact
def contact(a, b, i, j, board):
    # Bombs co-destroy any enemy piece
    if board[a][b].piece.order == None or board[i][j].piece.order == None or \
    board[a][b].piece.order == board[i][j].piece.order:
        board[a][b].piece = None
        board[i][j].piece = None
    # Sappers can capture landmines
    elif board[a][b].piece.order == 1 and board[i][j].piece.order == 10:
        board[i][j].piece = board[a][b].piece
        board[a][b].piece = None
    # other pieces react according to their order
    elif board[a][b].piece.order > board[i][j].piece.order:
        board[i][j].piece = board[a][b].piece
        board[a][b].piece = None
    else:
        board[a][b].piece = None


#### AI algorithm using minimax with heuristics and alpha-beta pruning

# get the largest value piece of the two sides (excluding the Flag)
def getLargestPiece(board):
    largestA, largestB = 0, 0
    for x in range(12):
        for y in range(5):
            if board[x][y].piece != None and board[x][y].piece.order != 0: # excluding the Flags
                try:
                    if board[x][y].piece.side == "A" and board[x][y].piece.value > largestA:
                        largestA = board[x][y].piece.value
                    elif board[x][y].piece.side == "B" and board[x][y].piece.value > largestB:
                        largestB = board[x][y].piece.value
                except:
                    pass
    return (largestA, largestB)


# calculate the score of the current board (positive if orange/upper/AI side is at advantage)
def getBoardScore(board):
    score = 0
    if board[0][1].piece != None and board[0][1].piece.order == 0:
        orangeFlag = "left"
    else:
        orangeFlag = "right"
    if board[11][1].piece != None and board[11][1].piece.order == 0:
        blueFlag = "left"
    else:
        blueFlag = "right"

    largestA, largestB = getLargestPiece(board)
    for x in range(12):
        for y in range(5):
            if board[x][y].piece != None:
                if board[x][y].piece.side == "A":
                    try:
                        score += board[x][y].piece.value # different pieces have different values
                    except: 
                        # Bombs do not have fixed values; their value is calculated as 1/3 of the largest opponent's piece
                        score += largestB / 3
                else:
                    try:
                        score -= board[x][y].piece.value
                    except:
                        score -= largestA / 3

                # taking up camps are a plus
                if x <= 5:
                    if isinstance(board[x][y], Camp) and board[x][y].piece.side == "B":
                        score -= 5
                    # camps that are just above the flag is even more valuable
                    if orangeFlag == "left":
                        if (x, y) == (2, 1) and board[x][y].piece.side == "B":
                            score -= 10
                    else:
                        if (x, y) == (2, 3) and board[x][y].piece.side == "B":
                            score -= 10
                else:
                    if isinstance(board[x][y], Camp) and board[x][y].piece.side == "A":
                        score += 5
                    # camps that are just above the flags are even more valuable
                    if blueFlag == "left":
                        if (x, y) == (9, 1) and board[x][y].piece.side == "A":
                            score += 10
                    else:
                        if (x, y) == (9, 3) and board[x][y].piece.side == "A":
                            score += 10
    return score


# AI move seeks to maximize the board score
def AIMove(board, maxDepth, depth=0, alpha=-100000, beta=100000):
    assert(alpha < beta)
    currentScore = getBoardScore(board)
    if currentScore > 1000 or currentScore < -1000: 
        # This means the game has ended (a flag has been captured)
        return (None, currentScore)
    elif depth == maxDepth:
        return (None, currentScore)
    else:
        bestMove = None
        bestScore = -10000
        for x in range(11, -1, -1):
            for y in range(5):
                if board[x][y].piece != None and board[x][y].piece.side == 'A':
                    for (a, b) in isLegal(board, (x, y)):
                        # non-Flag pieces in headquarters does not need to be captured
                        if (a, b) in [(0, 1), (0, 3), (11, 1), (11, 3)] and board[a][b].piece.order == 0:
                            return ((x, y, a, b), 1000)
                        else:
                            # store move
                            fromPost = board[x][y].piece
                            toPost = board[a][b].piece
                            # make move
                            if board[a][b].piece == None:
                                board[a][b].piece = board[x][y].piece
                                board[x][y].piece = None
                            else:
                                contact(x, y, a, b, board)
                            move, moveScore = PlayerMove(board, maxDepth, depth+1, alpha, beta)
                            # undo move
                            board[x][y].piece = fromPost
                            board[a][b].piece = toPost

                            if moveScore > bestScore:
                                bestScore = moveScore
                                bestMove = (x, y, a, b)
                                # pruning
                                alpha = max(alpha, bestScore)
                                if (alpha >= beta):
                                    return (bestMove, bestScore)
        return (bestMove, bestScore)

# Player move seeks to minimize the board score
def PlayerMove(board, maxDepth, depth=0, alpha=-100000, beta=100000):
    assert(alpha < beta)
    currentScore = getBoardScore(board)
    if currentScore > 1000 or currentScore < -1000:
        # This means the game has ended (a flag has been captured)
        return (None, currentScore)
    elif depth == maxDepth:
        return (None, currentScore)
    else:
        bestMove = None
        bestScore = 10000
        for x in range(12):
            for y in range(5):
                if board[x][y].piece != None and board[x][y].piece.side == 'B':
                    for (a, b) in isLegal(board, (x, y)):
                        # non-Flag pieces in headquarters does not need to be captured
                        if (a, b) in [(0, 1), (0, 3), (11, 1), (11, 3)] and board[a][b].piece.order == 0: 
                            return ((x, y, a, b), -1000)
                        else:
                            # store move
                            fromPost = board[x][y].piece
                            toPost = board[a][b].piece
                            # make move
                            if board[a][b].piece == None:
                                board[a][b].piece = board[x][y].piece
                                board[x][y].piece = None
                            else:
                                contact(x, y, a, b, board)
                            move, moveScore = AIMove(board, maxDepth, depth+1, alpha, beta)
                            # undo move
                            board[x][y].piece = fromPost
                            board[a][b].piece = toPost
                            
                            if moveScore < bestScore:
                                bestScore = moveScore
                                bestMove = (x, y, a, b)
                                # pruning
                                beta = min(beta, bestScore)
                                if (alpha >= beta):
                                    return (bestMove, bestScore)
        return (bestMove, bestScore)




