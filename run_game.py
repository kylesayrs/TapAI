import os
from dotenv import load_dotenv

from interface.console_interface import TapAI
from data.cards import animal_cards, vegetable_cards, avatar_cards
from models import load_model

load_dotenv()

if __name__ == '__main__':
    model_name = "naive_bayes"
    card_set = animal_cards
    data_source = "wikipedia"

    model = load_model(model_name, card_set, data_source)

    game = TapAI(model, card_set)
    game.run()
