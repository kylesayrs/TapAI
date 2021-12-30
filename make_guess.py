import sys

import numpy as np

from models.loader import loadModel # issue is here

from data.cards import animal_cards

model_name = "naive_embeddings"

model = loadModel(model_name, animal_cards)

confidences = model.predict(sys.argv[1])

if np.all(confidences == confidences[0]): # If all equal confidence
    choice = np.random.choice(animal_cards, 1)[0]
else:
    choice = animal_cards.cards[np.argmax(confidences)]

print(choice)

