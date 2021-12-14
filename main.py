# test commit

from interface.console_interface import TapAI
from data.cards import animal_cards, vegetable_cards, avatar_cards

if __name__ == '__main__':
    #game = TapAI(animal_cards, 'naive_embeddings')
    game = TapAI(animal_cards, 'naive_bayes')
    game.run()
