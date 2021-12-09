import os
import re
import wikipediaapi
import numpy as np
import pandas as pd
from cards import all_card_sets

OUT_DIR = './wiki_data'
CARD_SETS = all_card_sets

COLUMN_NAMES = ['sentence', 'card']
PUNCTUATION_REGEX = r'\.\s+|!\s+|\?\s+|:\s+'

VERBOSE = True

# TODO: Punctionation can sometimes end up at the end of a line and not get removed

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

    for card_set in CARD_SETS:
        out_filename = os.path.join(OUT_DIR, f'{card_set.name}.csv')
        extracted_data = []

        for card in card_set.cards:
            name = card.wiki_name
            if VERBOSE: print(f'Extracting {name}')
            page = wiki_wiki.page(name)
            page_text = page.text

            page_text = page.text.replace('|', '')
            sentences = splitSentences(page_text)

            for sentence in sentences:
                extracted_data.append([sentence, card.name])

        cleaned_df = pd.DataFrame(extracted_data, columns=COLUMN_NAMES)
        cleaned_df.to_csv(out_filename, sep='|', index=False)
