import os
AVAILABLE_MODELS = ["naive_embeddings", "naive_bayes"]

def load_model(model_name, card_set, data_source="wikipedia"):
    assert model_name in AVAILABLE_MODELS

    if model_name == "naive_embeddings":
        from models import NaiveEmbeddings
        return NaiveEmbeddings(card_set)

    if model_name == "naive_bayes":
        from models import NaiveBayes
        weights_path = os.path.join(
            os.environ.get("WEIGHTS_PATH", "weights"),
            "_".join([model_name, data_source, card_set.name]) + ".weights"
        )
        return NaiveBayes(card_set, weights_path=weights_path)
