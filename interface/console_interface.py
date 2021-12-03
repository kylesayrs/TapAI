import termtables
import numpy as np

from data.cards import animal_cards
from models.loader import loadModel

class TapAI():

    def __init__(self, model_name):
        print('Starting game')
        print(f'Loading model {model_name}...')
        self.cards = animal_cards
        self.model = loadModel(model_name, self.cards)

    def printBoard(self):
        grid = termtables.to_string(self.cards[:9].reshape((3, 3)))
        print(grid)

    def run(self):
        print('run')

    def playerATurn(self):
        a_input = input('Player A: ')
        confidences = self.model.predict(a_input)
        print(confidences)
        print(self.cards[np.argmax(confidences)])
