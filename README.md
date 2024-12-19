# Tetris Autoplayer

This project consists of a Tetris AI auto player which will try to maximize the score on a Tetris game with a given number of blocks, taking a heuristic approach with two move considerations to try and choose the move which the AI considers best according to some heuristics.

The heuristics which have been used in the current version of the auto player are:

-	Aggregate column height
-	Difference in column height
-	Maximum column height
-	Number of completed rows
-	Number of holes
-	Number of wells
-	Column where the block is placed

This version of the auto player tries to maximize the Tetrises (4-line clearings) as this considerably increases the score compared to clearing the lines individually. However, there is also a danger zone where any line clearings are positively rewarded, to try to control the stack as much as possible.

## How to achieve Tetrises?
The approach which has been taken to achieve and reward 4-line clearings, maximizing therefore the score, is creating a uniform stack trying to leave the rightmost column blank, where holes are severely penalized (the AI only places a block in a way which creates a whole if it is completely necessary and there is no option to place the block such that it does not create any holes. This stack will be created until the AI receives an I block, which is placed in the empty column to clear four lines at the same time.

Even though the AI will try to avoid clearing lines if these are not Tetrises and will try to avoid placing blocks in the rightmost column, which is being left clear for I blocks, it is not an strictly enforced heuristic, and a block can be potentially placed in that position if doing so in any others will negatively affect or damage the stack.

## Two Block Considerations
To take account more of the possibilities and make the AI less greedy in its choices, I have decided to implement two move considerations. This means that the AI not only places the current block in every possible position and scores each of them but does the same with the next block as well, providing a more accurate prediction as to which is the best move in each situation. Nevertheless, the scoring of the board after the current board has been placed has a slightly higher weighting than the scoring of the board when the next block has been placed.

## Further Improvements (Genetic Algorithm)
To further improve the quality of the Tetris auto player, I have decided to implement a genetic algorithm to find the better weights for each of the heuristics being considered to score boards to maximize the average performance of the auto player. My genetic algorithm works in the following way:

1.	It starts with a population of 20 chromosomes (sets of weights)
2.	Runs a Tetris auto player on 10 different seeds with each of the chromosomes, saving the average performance for each of the chromosomes
3.	Filters the best-performing chromosomes and reproduces them to create newer chromosomes (new generation)
4.	Mutates the new generation of chromosomes to add some randomly generated values, based on a probability of mutation of 10%
5.	Does the same steps on the new generation

To ensure accurate weights, the genetic algorithm has been run for 50 generations.

## Example Gameplay

<video width="600" controls>
  <source src="example_gameplay.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>
