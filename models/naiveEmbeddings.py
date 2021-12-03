import numpy as np

EMBEDDING_FILE_PATH = 'pretrained_weights/glove.6B.50d.txt'

class naiveEmbeddings():

    def __init__(self, cards):
        self.embeddings_dict = self.loadEmbeddingsDict(EMBEDDING_FILE_PATH)
        self.cards = cards

        # TODO: Normalization words

    def loadEmbeddingsDict(self, file_path, max=None):
        embeddings_dict = {}

        with open(file_path) as embedding_file:
            for i, line in enumerate(embedding_file):
                values = line.split(' ')
                word = values[0]
                vector = np.asarray(values[1:], np.float32)
                embeddings_dict[word] = vector

                if (not max is None) and i > max:
                    break

        return embeddings_dict

    def getWordEmbeddings(self, words):
        embeddings = []
        for word in words:
            try:
                embeddings.append(self.embeddings_dict[word])
            except KeyError as e:
                print(f'Warning: {word} not in embeddings dict')
                continue

        return embeddings

    def predict(self, content):
        words = content.split(' ')
        print(words)

        card_embeddings = [self.embeddings_dict[card] for card in self.cards]
        word_embeddings = self.getWordEmbeddings(words)
        card_scores = []
        for card_embedding in card_embeddings:

            score = 0
            for word_embedding in word_embeddings:
                distance =  np.linalg.norm(word_embedding - card_embedding)
                distance -= np.linalg.norm(word_embedding - self.embeddings_dict['a'])
                distance -= np.linalg.norm(word_embedding - self.embeddings_dict['the'])
                score += distance

            card_scores.append(score)

        print(card_scores)
        print(np.argmin(card_scores))
        print(self.cards[np.argmin(card_scores)])
        return self.cards[np.argmin(card_scores)]
