import csv
import wikipediaapi
from cards import animal_cards

OUT_FILENAME = './wiki_animals.csv'
HEADERS = ['name', 'summary', 'content']

if __name__ == '__main__':
    wiki_wiki = wikipediaapi.Wikipedia(language='en',
                                 extract_format=wikipediaapi.ExtractFormat.WIKI)

    csvfile = open(OUT_FILENAME, 'w')
    writer = csv.writer(csvfile)
    writer.writerow(HEADERS)

    for name in animal_cards:
        page = wiki_wiki.page(name)
        writer.writerow([name, page.summary, page.text])

    csvfile.close()
