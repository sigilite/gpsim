# gpsim
Simulator for a Grand Prix tournament of Magic: the Gathering

This program initializes a bunch of 'player' objects with different 'deck' types and then runs an entire 15-round tournament in which they are paired against each other & play best-of-3 games. The pairings are accomplished using the standard tournament rules for large Magic: the Gathering tournaments; in particular, a player is always paired against an opponent who they have not played against previously, and who has the same match record as they do (if possible).

Each match is a best-of-3 games, and in this program each game is assigned a random winner and a random length of time. Both the winner and the time taken are weighted by what decks each player is using (for example, two slow decks facing each other are likely to take more time than two fast ones). Just as in actual Magic: the Gathering tournaments, if the players run out of time before finishing their match, it terminates in a draw (unless one player is already ahead on games, in which case they are the winner).

After 15 rounds, the 8 players with the best records are declared as the "Top 8" players, and their player IDs and deck types
are printed to the terminal.
