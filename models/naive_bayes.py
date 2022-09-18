from typing import Optional

import os
import sys
import pickle
import numpy

from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords as NltkStopWords

from data import load_data
from models import Model
from data.cards import all_card_sets

class LemmaTokenizer:
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

lemma_tokenizer = LemmaTokenizer()
nltk_stop_words = ' '.join(NltkStopWords.words('english'))
lemmatized_nltk_stop_words = lemma_tokenizer(nltk_stop_words)

class NaiveBayes(Model):
    def __init__(self, card_set, weights_path: Optional[str] = None):
        self.name = "naive_bayes"
        self.card_set = card_set
        self.weights_path = weights_path


        self._model    = MultinomialNB(alpha=1.0, fit_prior=False)
        self._pipeline = Pipeline(
                           steps=[("counter", CountVectorizer(tokenizer=lemma_tokenizer,
                                                              ngram_range=(1, 2),
                                                              stop_words=lemmatized_nltk_stop_words)),
                                  ("tfidf", TfidfTransformer(smooth_idf=False))])

        if self.weights_path:
            self.load_weights()

    def load_weights(self, weights_path: Optional[str] = None):
        weights_path = weights_path or self.weights_path
        with open(weights_path, "rb") as weights_file:
            [model_state, pipeline_state] = pickle.load(weights_file)

            self._model.__setstate__(model_state)
            self._pipeline.__setstate__(pipeline_state)

            self._pipeline.set_params(counter__tokenizer=lemma_tokenizer)

    def save_weights(self, weights_path):
        weights_path = weights_path or self.weights_path
        with open(weights_path, "wb") as weights_file:
            self._pipeline.set_params(counter__tokenizer=None)

            model_state = self._model.__getstate__()
            pipeline_state = self._pipeline.__getstate__()

            pickle.dump([model_state, pipeline_state], weights_file)

            self._pipeline.set_params(counter__tokenizer=lemma_tokenizer)

    def train(self, x_train, y_train):
        assert len(x_train) == len(y_train)

        x_transformed = self._pipeline.fit_transform(x_train).toarray()
        y_transformed = numpy.array(list(map(self.card_set.cards.index, y_train)))
        assert len(x_transformed) == len(y_transformed)

        self._model = self._model.fit(x_transformed, y_transformed)

    def predict(self, content):
        pred_vec = self._pipeline.transform([content]).toarray()

        if numpy.all((pred_vec == 0)):
            print(f"WARNING: {content} has no recognized words")

        confidence = self._model.predict_proba(pred_vec)[0]

        return confidence
