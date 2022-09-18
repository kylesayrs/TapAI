import sys
import numpy as np

from data import animal_cards
from models.loader import loadModel # issue is here

data_source = "wikipedia"
model_name = "naive_bayes"
model = load_model(model_name, animal_cards, data_source)

confidences = model.predict(sys.argv[1])

if np.all(confidences == confidences[0]): # If all equal confidence
    choice = np.random.choice(animal_cards, 1)[0]
else:
    choice = animal_cards.cards[np.argmax(confidences)]

print(choice)
