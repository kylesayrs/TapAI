from models.naiveEmbeddings import naiveEmbeddings

AVAILABLE_MODELS = ['naive_embeddings']

def loadModel(model_name, cards):
    assert model_name in AVAILABLE_MODELS

    if model_name == 'naive_embeddings':
        return naiveEmbeddings(cards)
