# Chess

## Motivation
Who's never thought "it would be fun to write a chess engine, right?" This is that. But that also requires a way to play chess, which is where this project begins.

## Progress
So far, a 2D array is created to hold the pieces. Each piece has their own class, and the `board_standard()` function creates a board with the appropriate pieces. The `move(notation)` function enables (valid) movement of all pieces, including taking those that belong to the opponent, by taking in and parsing move chess notation from the command line.

## TODO:
 - Consider a better method for movement
 - Use some normal board notation like FEN
