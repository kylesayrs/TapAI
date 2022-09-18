import os

from data import CardSet

AVAILABLE_MODELS = ["naive_embeddings", "naive_bayes"]

def load_model(
    model_name: str,
    card_set: CardSet,
    data_source: str = "wikipedia"
):
    if model_name == "naive_bayes":
        from .naive_bayes import NaiveBayes
        weights_path = os.path.join(
            os.environ.get("WEIGHTS_PATH", "weights"),
            "_".join([model_name, data_source, card_set.name]) + ".weights"
        )
        return NaiveBayes(card_set, weights_path=weights_path)

    elif model_name == "naive_embeddings":
        from .naive_embeddings import NaiveEmbeddings
        return NaiveEmbeddings(card_set)

    else:
        raise ValueError(
            f"Unknown model name {model_name}, "
            f"available models: {AVAILABLE_MODELS}"
        )
