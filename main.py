# test commit

from interface.console_interface import TapAI
from data.cards import animal_cards

if __name__ == '__main__':
    game = TapAI(animal_cards, 'naive_embeddings')
    game.printBoard()
    while True:
        game.playerATurn()
