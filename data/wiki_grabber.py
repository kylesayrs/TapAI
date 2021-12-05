import re
import wikipediaapi
import numpy as np
import pandas as pd
from cards import animal_cards, vegetable_cards

OUT_FILENAME = './wiki_data.csv'
CARDS = np.concatenate((animal_cards, vegetable_cards))

COLUMN_NAMES = ['sentence', 'card']
PUNCTUATION_REGEX = r'\.\s+|!\s+|\?\s+|:\s+'

VERBOSE = True

def splitSentences(text):
    all_sentences = []

    for line in text.split('\n'):
        if len(line) <= 0: continue                     # Remove spacer lines

        sentences = re.split(PUNCTUATION_REGEX, line)
        if len(sentences) == 1: continue                # Remove lines with only
        for sentence in sentences:                      # one split (titles)
            if len(sentence) == 0: continue
            all_sentences.append(sentence)

    return all_sentences

if __name__ == '__main__':
    wiki_wiki = wikipediaapi.Wikipedia(language='en',
                                 extract_format=wikipediaapi.ExtractFormat.WIKI)

    extracted_data = []

    for name in CARDS:
        if VERBOSE: print(f'Extracting {name}')
        page = wiki_wiki.page(name)
        page_text = page.text

        page_text = page.text.replace('|', '')
        sentences = splitSentences(page_text)

        for sentence in sentences:
            extracted_data.append([sentence, name])

    cleaned_df = pd.DataFrame(extracted_data, columns=COLUMN_NAMES)
    cleaned_df.to_csv(OUT_FILENAME, sep='|', index=False)
