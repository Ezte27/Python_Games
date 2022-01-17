class GameState():
    def __init__(self):
        self.board = [ 
        ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["--", "--", "--", "--", "--", "--", "--", "--"],
        ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.moveFunctions = {"P": self.getPawnMoves, "R": self.getRookMoves,
                              "N": self.getKnightMoves, "B": self.getBishopMoves,
                              "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.whiteToMove=True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.currentCastlingRights = castleRights(True, True, True, True)
        self.castleRightsLog = [castleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove # Switch turns
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
        
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + move.promotionChoice
        
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][move.endCol+1]
                self.board[move.endRow][move.endCol+1] = "--"
            else:
                self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-2]
                self.board[move.endRow][move.endCol-2] = "--"
        
        self.updateCastleRights(move)
        self.castleRightsLog.append(castleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove # Switch turns
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRights = castleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = "--"
                else:
                    self.board[move.endRow][move.endCol-2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--"

    def updateCastleRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.bks = False

    def getValidMoves(self):
        moves = self.getAllPossibleMoves()
        tempCastleRights = castleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        for i in range(len(moves)-1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        self.currentCastlingRights = tempCastleRights
        return moves
    
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])
    
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == "w" and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves) # calls the get moves function and adds the parameters
        return moves
    
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--": # one square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0: # Captures to the left
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r, c), (r-1, c-1), self.board))
            if c+1 <= 7: # Captures to the left
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r, c), (r-1, c+1), self.board))
        elif not self.whiteToMove:
            if self.board[r+1][c] == "--": # one square pawn advance
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0: # Captures to the left
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r, c), (r+1, c-1), self.board))
            if c+1 <= 7: # Captures to the left
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r, c), (r+1, c+1), self.board))

    def getRookMoves(self, r, c, moves):
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1)) # up, down, left, right
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0<= endRow < 8 and 0<= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    def getKnightMoves(self, r, c, moves):
        knightMoves = [(-2, 1), (-2, -1), (2, 1), (2, -1), (-1, 2), (1, 2), (1, -2), (-1, -2)]
        enemyColor = "b" if self.whiteToMove else "w"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0<= endRow < 8 and 0<= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                elif endPiece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                    
    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (1, 1), (1, -1), (-1, 1)) # upLeft, downRight, downLeft, upRight
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break
    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)
    def getKingMoves(self, r, c, moves):
        kingMoves = ((1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1))
        enemyColor = "b" if self.whiteToMove else "w"
        for m in kingMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece == "--":
                    moves.append(Move((r, c), (endRow, endCol), self.board))
                elif endPiece[0] == enemyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return 
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueenSideCastleMoves(r, c, moves)
    
    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == "--" and self.board[r][c+2] == "--" and self.board[r][c+3][1] == "R":
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r,c), (r, c+2), self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == "--" and self.board[r][c-2] == "--" and self.board[r][c-3] == "--" and self.board[r][c-4][1] == "R":
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r,c), (r, c-2), self.board, isCastleMove=True))

class castleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.wqs = wqs
        self.bks = bks
        self.bqs = bqs

class Move():

    ranksToRows = {"1": 7,"2": 6,"3": 5,"4": 4,
                   "5": 3,"6": 2,"7": 1,"8": 0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0,"b": 1,"c": 2,"d": 3,
                   "e": 4,"f": 5,"g": 6,"h": 7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, startSQ, endSQ, board, isCastleMove=False):
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        self.isPawnPromotion = False
        self.promotionChoice = "Q"
        if (self.pieceMoved == "wP" and self.endRow == 0) or (self.pieceMoved == "bP" and self.endRow == 7):
            self.isPawnPromotion = True
        self.isCastleMove = isCastleMove
    
    def __eq__(self, other): # Overriding the equals method for functions
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
