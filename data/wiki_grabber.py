import csv
import wikipediaapi

OUT_FILENAME = './wiki_animals.csv'
HEADERS = ['name', 'summary', 'content']

NAMES = ['rat', 'ox', 'tiger', 'rabbit', 'dragon', 'snake',
         'horse', 'sheep', 'monkey', 'chicken', 'dog', 'pig']

if __name__ == '__main__':
    wiki_wiki = wikipediaapi.Wikipedia(language='en',
                                 extract_format=wikipediaapi.ExtractFormat.WIKI)

    csvfile = open(OUT_FILENAME, 'w')
    writer = csv.writer(csvfile)
    writer.writerow(HEADERS)

    for name in NAMES:
        page = wiki_wiki.page(name)
        writer.writerow([name, page.summary, page.text])

    csvfile.close()
