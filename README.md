This AI agent implements a probabilistic approach to solve the Minesweeper game. The agent combines deterministic logic rules with probability-based heuristics to make informed decisions about which cells to uncover.

Key Features:

Probabilistic Reasoning: Calculates the likelihood of mines in each cell.  
Rule-Based Deduction: Identifies guaranteed safe moves and certain mines.  
Constraint Satisfaction: Processes hints to satisfy neighboring cell constraints.  
Queue-Based Frontier Management: Maintains and prioritizes a frontier of known safe cells.  
Heuristic Decision Making: When certainty isn't possible, selects tiles with lowest mine probability.  

AI Methods Used:

Knowledge Representation: Maintains an internal board state.  
Constraint Satisfaction: Applies rules based on numbered tile constraints.  
Probability Theory: Calculates tile danger levels when certainty isn't possible.  
Queue-Based Frontier Management: Efficiently tracks and processes the frontier of exploration.  
Heuristic Search: Uses best-first approach by choosing lowest-risk tiles.  

How It Works:

The AI keeps track of the game state in a 2D board.  
For each revealed number, it updates knowledge about surrounding cells.  
When a cell has a number matching its unrevealed neighbors, all are flagged as mines.  
When a cell has a number matching its flagged neighbors, all other neighbors are marked safe.  
For uncertain situations, probabilities are calculated for each unrevealed cell.  
The cell with the lowest probability of containing a mine is selected.  

Performance:

100% of 1000 beginner 5x5 worlds with 1 mine.  
75% of 1000 easy 8x8 worlds with 10 mines.  
69% of 1000 intermediate 16x16 worlds with 40 mines.  
9% of 1000 expert 16x30 worlds with 99 mines.  
