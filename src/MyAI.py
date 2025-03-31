# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================
from AI import AI
from Action import Action
from queue import Queue
import random

class MyAI(AI):
    def __init__(self, rows, cols, totalMines, startX, startY):
        self.rows, self.cols = cols, rows
        self.totalMines = totalMines
        self.currentX, self.currentY = startX, startY
        self.exploredCount = 0
        self.totalSafeCells = (rows * cols) - totalMines
        
        self.safeQueue = Queue()
        self.visitedCells = set()
        self.tileProbabilities = {}
        
        self.adjacentCells = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),         (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        # Initialize board with -100 (unexplored)
        self.board = [[-100] * self.cols for _ in range(self.rows)]

    def isValid(self, x, y):
        return 0 <= x < self.rows and 0 <= y < self.cols

    def getNeighbors(self, x, y):
        # Returns (unrevealed neighbors, flagged neighbors)
        unrevealed = []
        flagged = []
        
        for dx, dy in self.adjacentCells:
            newX, newY = x + dx, y + dy
            if self.isValid(newX, newY):
                if self.board[newX][newY] == -100:  # Unrevealed
                    unrevealed.append((newX, newY))
                elif self.board[newX][newY] == -1:   # Flagged
                    flagged.append((newX, newY))
        return unrevealed, flagged

    def calculateTileProbabilities(self):
        """
        Calculate probability of mines for each unexplored tile
        """
        self.tileProbabilities.clear()
        
        for x in range(self.rows):
            for y in range(self.cols):
                if self.board[x][y] > 0:  # Tiles with hints
                    unrevealed, flagged = self.getNeighbors(x, y)
                    
                    # Remaining mines to be placed
                    remaining_mines = self.board[x][y] - len(flagged)
                    
                    # Calculate probability for each unrevealed neighbor
                    if unrevealed:
                        prob = remaining_mines / len(unrevealed)
                        for tile in unrevealed:
                            if tile not in self.tileProbabilities:
                                self.tileProbabilities[tile] = prob
                            else:
                                # Average probabilities from multiple sources
                                self.tileProbabilities[tile] = (self.tileProbabilities[tile] + prob) / 2

    def selectBestMove(self):
        """
        Select the best move based on probabilistic reasoning
        """
        self.calculateTileProbabilities()
        
        # Prioritize moves from safe queue
        if not self.safeQueue.empty():
            return self.safeQueue.get()
        
        # If probabilities calculated, choose lowest probability tile
        if self.tileProbabilities:
            best_tile = min(self.tileProbabilities, key=self.tileProbabilities.get)
            return best_tile
        
        # Fallback to random unexplored tile
        unexplored = [(x, y) for x in range(self.rows) for y in range(self.cols) if self.board[x][y] == -100]
        return random.choice(unexplored) if unexplored else None

    def getAction(self, number: int) -> Action:
        # Update curr cell's state
        self.board[self.currentX][self.currentY] = number
        self.visitedCells.add((self.currentX, self.currentY))
        
        if self.exploredCount == self.totalSafeCells:
            return Action(AI.Action.LEAVE, 1, 1)

        # If number is 0, all neighbors are safe
        if number == 0:
            unrevealed, _ = self.getNeighbors(self.currentX, self.currentY)
            for cell in unrevealed:
                if cell not in self.safeQueue.queue:
                    self.safeQueue.put(cell)

        # Advanced hint processing
        for x in range(self.rows):
            for y in range(self.cols):
                if self.board[x][y] > 0:  # If it has a hint/number
                    unrevealed, flagged = self.getNeighbors(x, y)
                    
                    # If unrevealed count equals the number, all must be mines -> flag
                    if len(unrevealed) > 0 and len(unrevealed) + len(flagged) == self.board[x][y]:
                        flagging_tile = unrevealed[0]
                        self.board[flagging_tile[0]][flagging_tile[1]] = -1  # Mark as flagged
                        self.currentX, self.currentY = flagging_tile
                        return Action(AI.Action.FLAG, self.currentX, self.currentY)
                    
                    # If flagged count equals the number, all other neighbors are safe
                    if len(flagged) == self.board[x][y] and len(unrevealed) > 0:
                        for cell in unrevealed:
                            if cell not in self.safeQueue.queue:
                                self.safeQueue.put(cell)

        # Select best move
        next_move = self.selectBestMove()
        
        if next_move:
            self.currentX, self.currentY = next_move
            self.exploredCount += 1
            return Action(AI.Action.UNCOVER, self.currentX, self.currentY)
        
        # No moves left
        return Action(AI.Action.LEAVE, 1, 1)
 