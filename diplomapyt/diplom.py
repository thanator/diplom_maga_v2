import os
import subprocess
import xml.sax

import mwparserfromhell
from gensim import corpora
from gensim.corpora import Dictionary, MmCorpus
from gensim.models import TfidfModel, LsiModel
from gensim.utils import simple_preprocess
from np.magic import np

from WikiXmlHandler import WikiXmlHandler
from lsi.BoWCorpus import BoWCorpus
from sqlhelper.sqlhelper import readFromDb
from utils.TextFormatter import format_text, get_normal_form_of_word
import warnings

warnings.simplefilter("ignore", category=UserWarning)

data_path = 'ruwiki-20190520-pages-meta-current1.xml-p4p204179.bz2'

status = dict()


def main():
    dbList = readFromDb()
    status['start'] = "Started..."
    # Чтение из архива bz2, Запускает подпроцесс bzcat.
    #
    #
    badDocs = get_docs(data_path, 100)
    goodDocs = docs_to_docs_with_unique_words(badDocs)

    with open('file.txt', 'w') as the_file:
        for stroka in goodDocs:
            the_file.write(stroka + os.linesep)

    # goodDocs = list()
    # f = open("file.txt", "r")
    # goodDocs = f.read().splitlines()
    # print(goodDocs)

    listOfLists = getting_list_of_list_from_docs(goodDocs)
    # dictionary = Dictionary(listOfLists)
    # bow_corpus = BoWCorpus(goodDocs, dictionary)
    # #
    # dictionary.save('mydict.pkl')  # save dict to disk
    # MmCorpus.serialize('bow_corpus.mm', bow_corpus)

    # loaded_dict = Dictionary()
    #
    # corpus = MmCorpus('bow_corpus.mm')

    # Корпус слов
    # bow_corpus = BoWCorpus(listOfDocs, dictionary)
    # for line in bow_corpus:
    #     print(line)

    # Словарь слов
    # dictionary = Dictionary(listOfListsOfWords)

    # print(dictionary.token2id)

    # TFIDF
    # mydict = Dictionary([simple_preprocess(line) for line in goodDocs])
    # corpus = [mydict.doc2bow(simple_preprocess(line)) for line in goodDocs]
    # # Show the Word Weights in Corpus
    # for doc in corpus:
    #     print([[mydict[id], freq] for id, freq in doc])
    # tfidf = TfidfModel(corpus, smartirs='ntc')
    # # Show the TF-IDF weights
    # for doc in tfidf[corpus]:
    #     print([[mydict[id], np.around(freq, decimals=2)] for id, freq in doc])

    # LSI
    dct = Dictionary(listOfLists)
    corpus = [dct.doc2bow(line) for line in listOfLists]
    lsi_model = LsiModel(corpus=corpus, id2word=dct, num_topics=7, decay=0.5)
# View Topics
    from pprint import pprint
    pprint(lsi_model.print_topics(-1))


# [5][3]

def get_docs(path: str, docCount: int = 10) -> list:
    status['docs'] = "Getting docs..."
    log_status()
    handler = WikiXmlHandler()
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)
    for line in subprocess.Popen(['bzcat'],
                                 stdin=open(path),
                                 stdout=subprocess.PIPE).stdout:
        try:
            parser.feed(line)
        except StopIteration:
            break

        if len(handler.pages) > docCount:
            break
    listOfDocks = list()
    for page in handler.pages:
        if len(page) >= 3:
            wiki = mwparserfromhell.parse(page[3])
            log_status()
            print("Parsing " + str(handler.pages.index(page)) + " from " + str(len(handler.pages)) + " pages")
            textPage1 = wiki.strip_code(normalize=True, collapse=True, keep_template_params=False)
            listOfDocks.append(format_text(textPage1))

            status['docs'] = "Docs loaded..."
            log_status()
    return listOfDocks


def docs_to_docs_with_unique_words(docList) -> list:
    listOfDocs = list()
    status['words'] = "Words processing"
    for doc in docList:
        slova = format_text(doc).split()
        wordNumber = 0
        listSlov = list()
        newDoc = ""
        for slovo in slova:
            wordNumber = wordNumber + 1
            log(docList.index(doc), len(docList) - 1, wordNumber, len(slova))
            slovo = get_normal_form_of_word(slovo)
            newDoc = newDoc + " " + slovo
            # listSlov.append(slovo)
        # listOfListsOfWords.append(listSlov)
        listOfDocs.append(newDoc)
    status['words'] = "Words processed"
    log_status()
    return listOfDocs


def getting_list_of_list_from_docs(listOfDocs):
    lisOfLists = list(list())
    status['words'] = "Words processing"
    for doc in listOfDocs:
        slova = format_text(doc).split()
        wordNumber = 0
        listSlov = list()
        newDoc = ""
        for slovo in slova:
            wordNumber = wordNumber + 1
            log(listOfDocs.index(doc), len(listOfDocs) - 1, wordNumber, len(slova))
            newDoc = newDoc + " " + slovo
            listSlov.append(slovo)
        lisOfLists.append(listSlov)
    status['words'] = "Words processed"
    log_status()
    return lisOfLists


def log(pageNumber, pages, wordNumber, slova):
    log_status()
    print(str(pageNumber) + " from " + str(pages) + " pages, " + str(
        wordNumber) + " from " + str(slova) + " slov")


def log_status():
    subprocess.call('clear' if os.name == 'posix' else 'cls')

    for key in status.keys():
        print('\n' + key + ": " + status.get(key))


if __name__ == '__main__':
    main()
