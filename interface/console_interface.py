import termtables
import numpy as np

from models.loader import loadModel

class TapAI():

    def __init__(self, cards, model_name, grid_shape=(3, 3)):
        print('Starting game')
        print(f'Loading model {model_name}...')
        assert len(cards) == 9
        self.cards = cards
        self.model = loadModel(model_name, self.cards)

        self.current_cards = np.random.choice(self.cards, grid_shape[0] * grid_shape[1])

    def printBoard(self):
        grid = termtables.to_string(self.cards.reshape((3, 3)))
        print(grid)

    def run(self):
        print('run')

    def playerATurn(self):
        a_input = input('Player A: ')
        confidences = self.model.predict(a_input)
        print(confidences)
        print(self.cards[np.argmax(confidences)])
