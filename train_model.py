import os

from models import load_model
from data import all_card_sets, load_data

if __name__ == "__main__":
    data_source = "wikipedia"
    model_name =

    for card_set in all_card_sets:
        model = load_model(card_set=card_set, weights_path=None)
        print(f"Training {model.name} on {card_set.name}")

        x_train, y_train = load_data(data_source, card_set.name, split="train")
        model.train(x_train, y_train)

        weights_path = os.path.join(
            os.environ.get("WEIGHTS_PATH", "weights"),
            f"{model.name}_{data_source}_{card_set.name}.weights",
        )
        model.save_weights(weights_path)
