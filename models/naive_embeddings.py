import numpy as np
from transformers import PreTrainedTokenizer

class NaiveEmbeddings():
    def __init__(self, card_set):
        self.cards = card_set.cards
        self.embeddings_dict = self.load_embeddings_dict(EMBEDDING_FILE_PATH)
        self.card_embeddings = self.get_card_embeddings(self.cards)
        # TODO: Normalize for frequently used card words

    def load_embeddings_dict(self, file_path, max=None):
        embeddings_dict = {}

        with open(file_path) as embedding_file:
            for i, line in enumerate(embedding_file):
                values = line.split(" ")
                word = values[0]
                vector = np.asarray(values[1:], np.float32)
                embeddings_dict[word] = vector

                if (not max is None) and i > max:
                    break

        return embeddings_dict

    def get_card_embeddings(self, cards):
        embeddings = []
        for card in cards:
            embeddings.append(self.embeddings_dict[card.name])

        return embeddings

    def get_word_embeddings(self, words):
        embeddings = []
        for word in words:
            try:
                embeddings.append(self.embeddings_dict[word])
            except KeyError as e:
                print(f"Warning: {word} not in embeddings dict")
                continue

        return embeddings

    def predict(self, content):
        content = content.lower()
        words = content.split(" ")

        word_embeddings = self.get_word_embeddings(words)
        card_scores = []
        for card_embedding in self.card_embeddings:

            score = 0
            for word_embedding in word_embeddings:
                score += np.linalg.norm(word_embedding - card_embedding)

            card_scores.append(score)

        confidences = 1.0 - (card_scores / np.max(card_scores))
        return confidences
