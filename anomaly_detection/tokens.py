import sys
import pandas as pd
import numpy as np
import re
import string
from collections import Counter
import tqdm
import pickle

import spacy

class NLPVectorizor():
    def __init__(self, max_sentence_size=70, debug=True):
        self.max_sentence_size = max_sentence_size
        self.debug = debug

        self.nlp = spacy.load('en_core_web_sm')
        punct = re.escape(string.punctuation.replace("'", '').replace("'", ''))
        infix_re = re.compile(f'''[{punct}]''')
        self.nlp.tokenizer = spacy.tokenizer.Tokenizer(self.nlp.vocab, infix_finditer=infix_re.finditer)

        self.removed_words = []
        self.vocab_dict = {'': 0, 'UNK': 1}
        self.vocab_file_path = 'vocab.bin'
        self.removed_words_file_path = 'removed_words.pkl'
        self.vocab_dict_file_path = 'vocab_dict.pkl'

    def transform(self, sentences):
        # Clean data
        if self.debug: print('Preprocessing data...')
        sentences_cleaned = self.preprocess(sentences)

        # Tokenize
        if self.debug: print('Tokenizing data...')
        sentences_tokens = list(map(self.tokenize, tqdm.tqdm(sentences_cleaned)))

        # Filter removed words
        if self.debug: print('Removing words'); print(f'len_removed_words: {len(self.removed_words)}')
        i = 0
        for sentence_tokens in tqdm.tqdm(sentences_tokens):
            sentences_tokens[i] = list(filter(lambda w: not w in self.removed_words, sentence_tokens[:self.max_sentence_size * 2]))
            i += 1

        # Create encodings
        if self.debug: print('Encoding sentences')
        sentence_encodings = list(map(self.encodeTokens, sentences_tokens))

        return sentence_encodings

    def fit(self, sentences, min_df=0.0001, max_df=1.0):
        # Clean data
        if self.debug: print('Preprocessing data...')
        sentences_cleaned = self.preprocess(sentences)

        # Tokenize
        if self.debug: print('Tokenizing data...')
        sentences_tokens = list(map(self.tokenize, tqdm.tqdm(sentences_cleaned)))

        # Delete infrequent words
        if self.debug: print('Deleting infrequent words...')
        word_counts, self.removed_words = self.filterByFreq(sentences_tokens, min_df=min_df, max_df=max_df)

        # Create vocabulary
        if self.debug: print('Creating vocabulary...')
        self.vocab_dict = self.createVocabDict(word_counts)

    def encodeTokens(self, tokens):
        unk_index = self.vocab_dict['UNK']
        encoding = np.zeros(self.max_sentence_size, dtype=int)

        sentence_encoding = np.array([self.vocab_dict.get(word, unk_index) for word in tokens])

        sentence_len = min(self.max_sentence_size, len(sentence_encoding))
        encoding[:sentence_len] = sentence_encoding[:sentence_len]

        return encoding, sentence_len

    def createVocabDict(self, word_counts):
        vocab_dict = {'': 0, 'UNK': 1}
        for word in tqdm.tqdm(word_counts):
            vocab_dict[word] = len(vocab_dict)

        return vocab_dict

    def filterByFreq(self, sentences_tokens, min_df=0.0, max_df=1.0):
        word_counts = Counter()
        for sentence_tokens in sentences_tokens:
            word_counts.update(sentence_tokens)

        num_total_words = sum(word_counts.values())
        removed_words = []
        for word in tqdm.tqdm(list(word_counts)):
            if word_counts[word] < num_total_words * min_df or \
               word_counts[word] > num_total_words * max_df:
                removed_words.append(word)
                del word_counts[word]

        return word_counts, removed_words

    def tokenize(self, sentence):
        return [token.text for token in self.nlp.tokenizer(sentence)]

    def preprocess(self, sentences, lower=True, punct=True, numbers=True):
        match_punct = re.escape(string.punctuation)
        match_num = '0-9'

        total_match = 'a-zA-Z'
        if punct:
            total_match += match_punct
        if numbers:
            total_match += match_num

        total_regex = re.compile(f'[^{total_match}]+')

        def _preprocess(sentence):
            try:
                sentence = total_regex.sub(' ', sentence)
            except KeyboardInterrupt:
                sys.exit(0)
            except:
                return ''

            if lower:
                sentence = sentence.lower()

            return sentence

        return list(map(_preprocess, tqdm.tqdm(sentences)))

    def save(self):
        self.nlp.vocab.to_disk(self.vocab_file_path)
        pickle.dump(self.removed_words, open(self.removed_words_file_path, 'wb'))
        pickle.dump(self.vocab_dict, open(self.vocab_dict_file_path, 'wb'))

    def load(self):
        self.nlp.vocab.from_disk(self.vocab_file_path)
        self.removed_words = pickle.load(open(self.removed_words_file_path, 'rb'))
        self.vocab_dict = pickle.load(open(self.vocab_dict_file_path, 'rb'))


if __name__ == '__main__':
    '''
    messages = [
        "hello NLP world. it's me, the boy %(*#)ˆ∆",
        "here comes the boy, hello boy 5. welcome. there he is. he is here",
        "i.don't;know?how&to*press(space",
        "the the the the the the the the the the the the the the the the the",
        "the the the the the the the the the the the the the the the the the",
        "the the the the the the the the the the the the the the the the the",
        "the the the the the the the the the the the the the the the the the",
        "leftmost is the best most 0rmsdbs97a nealon"
    ]
    '''
    data_df = pd.read_csv('trumptweets.csv')
    messages = data_df['content'][:1000]

    #'''
    nlp_vectorizor = NLPVectorizor()
    nlp_vectorizor.fit(messages)
    #nlp_vectorizor.save()
    #'''

    #'''
    #nlp_vectorizor.load()
    message_tokens = nlp_vectorizor.transform(messages)
    #'''
