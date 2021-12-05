import termtables
import numpy as np

from models.loader import loadModel

class TapAI():

    def __init__(self, card_set, model_name, grid_shape=(3, 3)):
        print('Starting game')
        print(f'Using card set "{card_set.name}"...')
        print(f'Loading model {model_name}...')

        self.grid_shape = grid_shape
        self.card_set = card_set
        self.num_cards = grid_shape[0] * grid_shape[1]
        assert len(self.card_set.cards) == self.num_cards

        self.model = loadModel(model_name, self.card_set)

    def printBoard(self):
        cards = np.array(self.card_set.cards)
        grid = termtables.to_string(cards.reshape(self.grid_shape))
        print(grid)

    def run(self):
        while True:
            self.printBoard()
            try:
                a_input = input('Player A: ')
            except EOFError:
                break
            self.guessCard(a_input)

    def guessCard(self, a_input):
        confidences = self.model.predict(a_input)
        print(confidences)

        if np.all(confidences == confidences[0]): # If all equal confidence
            choice = np.random.choice(self.card_set.cards, 1)[0]
        else:
            choice = self.card_set.cards[np.argmax(confidences)]
        print(choice)

        return choice
