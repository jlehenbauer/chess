# Chess

## Motivation
Who's never thought "it would be fun to write a chess engine, right?" This is that. But that also requires a way to play chess, which is where this project begins.

## Progress
So far, a 2D array is created to hold the pieces. Each piece has their own class, and the `board_standard()` function creates a board with the appropriate pieces. The `move(notation)` function has been started, but right now is only defined for pawns, and will allow them to move any distance forward.

## TODO:
 - Consider a better method for movement
 - Decide where to parse chess notation (i.e. parse, then call `move()` or parse within `move()`)
 - Write movement for other pieces
 - Write checks within piece class to verify valid movement