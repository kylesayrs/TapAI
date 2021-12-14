AVAILABLE_MODELS = ['naive_embeddings', 'naive_bayes']

def loadModel(model_name, card_set):
    assert model_name in AVAILABLE_MODELS

    if model_name == 'naive_embeddings':
        from models.naiveEmbeddings import naiveEmbeddings
        return naiveEmbeddings(card_set)

    if model_name == 'naive_bayes':
        from models.naiveBayes import naiveBayes
        return naiveBayes(card_set, pretrained=True)
