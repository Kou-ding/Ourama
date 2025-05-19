Test# Ourama (王ラマ)
A hybrid digital/physical Roguelike, RPG, Deckbuilder, Co-op game that livens up its boardgame basis by making it interactive and adding graphics to the mix.

## Tutorial
Replicate the conda environment required to run the game:
```bash
# create venv based on environment.yml
conda env create -f environment.yml
# activate environment
conda activate ouevn
```
Run the game:
```bash
python3 game.py
```

## Manual
Ourama is a turn-based game in which the player utilizes cards to defeat opponents.  

### Player Classes 
At the start of the game players choose one of 4 main classes.
- Knight
- Assassin
- Tank
- Healer

### Cards
Cards have energy and one additional attribute:
- energy: It is the amount of energy required the play the card.  
- attack: Attacks the monster on behalf of the player.
- shield: Shields the player from incoming damage.
- heal: Heals the player.
- add_energy: Increases the player's energy for the current round.
- add_max_health: Increases the player's max health.

### Game Logic
- Players have their own deck.
- Each turn they draw two cards.
- They can play as many cards as their energy tank allows.
- Cards that have been used return to the bottom of the deck 
- When the the used card get at the top of the deck, we perform a deck shuffle. 
- After a non-boss encounter each player can add 1 out of 3 card to their deck.
- If all the players die before the Boss is defeated, it's Game Over.
- If the players manage to defeat the Boss they win the game.
