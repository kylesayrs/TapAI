import os
import sys
import pickle
import numpy as np
import pandas as pd

from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords as NltkStopWords

sys.path.append('..')
from data.cards import all_card_sets

class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

lemma_tokenizer = LemmaTokenizer()
nltk_stop_words = ' '.join(NltkStopWords.words('english'))
lemmatized_nltk_stop_words = lemma_tokenizer(nltk_stop_words)

class SVMClassifer():

    def __init__(self, card_set, pretrained=True):
        self.card_set = card_set
        self.weight_path = os.path.join(Path(__file__).parent, f'../weights/svm_weights_{self.card_set.name}.weights')

        self._model    = LinearSVC(alpha=1.0, fit_prior=False)
        self._pipeline = Pipeline(
                           steps=[('counter', CountVectorizer(tokenizer=lemma_tokenizer,
                                                              ngram_range=(1, 2),
                                                              stop_words=lemmatized_nltk_stop_words)),
                                  ('tfidf', TfidfTransformer(smooth_idf=False))])

        if pretrained:
            self.loadWeights()

    def loadWeights(self):
        weights_file = open(self.weight_path, 'rb')

        [model_state, pipeline_state] = pickle.load(weights_file)

        self._model.__setstate__(model_state)
        self._pipeline.__setstate__(pipeline_state)

        self._pipeline.set_params(counter__tokenizer=lemma_tokenizer)

        weights_file.close()

    def saveWeights(self):
        weights_file = open(self.weight_path, 'wb')

        self._pipeline.set_params(counter__tokenizer=None)

        model_state    = self._model.__getstate__()
        pipeline_state = self._pipeline.__getstate__()

        pickle.dump([model_state, pipeline_state], weights_file)

        self._pipeline.set_params(counter__tokenizer=lemma_tokenizer)

        weights_file.close()

    def train(self):
        data = pd.read_csv(f'../data/wiki_data/{self.card_set.name}.csv', sep='|')

        X = self._pipeline.fit_transform(data['sentence']).toarray()
        y = np.array(list(map(self.card_set.cards.index, data['card'])))
        assert len(X) == len(y)

        self._model = self._model.fit(X, y)

    def predict(self, content):
        pred_vec = self._pipeline.transform([content]).toarray()

        if np.all((pred_vec == 0)):
            print(f'WARNING: {content} has no recognized words')

        confidence = self._model.predict_proba(pred_vec)[0]

        return confidence

if __name__ == '__main__':
    for card_set in all_card_sets:
        print(f'Training {card_set.name}')
        model = SVMClassifer(card_set=card_set, pretrained=False)
        model.train()
        model.saveWeights()
