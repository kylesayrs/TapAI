import sys
import pickle
import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

sys.path.append("..")
from data.cards import all_card_sets

class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

class naiveBayes():

    def __init__(self, card_set, pretrained=True):
        self.card_set = card_set

        self._model     = MultinomialNB(alpha=1.0, fit_prior=False)
        self._vectorizer = CountVectorizer(tokenizer=LemmaTokenizer())

        if pretrained:
            self.loadWeights()

    def loadWeights(self):
        model_file = open(f'./weights/nb_model_{self.card_set.name}.weights', 'rb')
        vec_file   = open(f'./weights/nb_vec_{self.card_set.name}.weights', 'rb')

        model_state = pickle.load(model_file)
        vec_state   = pickle.load(vec_file)

        self._model.__setstate__(model_state)
        self._vectorizer.__setstate__(vec_state)

    def saveWeights(self):
        model_file = open(f'../weights/nb_model_{self.card_set.name}.weights', 'wb')
        vec_file   = open(f'../weights/nb_vec_{self.card_set.name}.weights', 'wb')

        model_state = self._model.__getstate__()
        vec_state   = self._vectorizer.__getstate__()
        vec_state['tokenizer'] = None

        pickle.dump(model_state, model_file)
        pickle.dump(vec_state, vec_file)

        model_file.close()
        vec_file.close()

    def train(self):
        data = pd.read_csv(f'../data/wiki_data/{self.card_set.name}.csv', sep='|')

        X = self._vectorizer.fit_transform(data['sentence']).toarray()
        y = np.array(list(map(self.card_set.cards.index, data['card'])))
        assert len(X) == len(y)

        self._model = self._model.fit(X, y)

    def predict(self, content):
        pred_vec = self._vectorizer.transform([content]).toarray()

        if np.all((pred_vec == 0)):
            print(f'WARNING: {content} has no recognized words')

        confidence = self._model.predict_proba(pred_vec)[0]

        return confidence

if __name__ == '__main__':
    for card_set in all_card_sets:
        print(f'Training {card_set.name}')
        model = naiveBayes(card_set=card_set, pretrained=False)
        model.train()
        model.saveWeights()
