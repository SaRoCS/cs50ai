import math
import os
import string
import sys

import nltk

FILE_MATCHES = 1
SENTENCE_MATCHES = 1

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    text = {}

    for dir, _, files in os.walk(directory):
        for file in files:
            with open(os.path.join(dir, file)) as f:
                text[file] = f.read()

    return text


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # list of words to remove
    remove = nltk.corpus.stopwords.words("english") + list(string.punctuation)
    # tokenize and filter
    words = [x.lower() for x in nltk.tokenize.word_tokenize(document)]
    words = [x for x in words if x not in remove]

    return words



def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = {}
    words = set()
    # get all words
    for document in documents:
        words.update(documents[document])
    # for every word count how many docs it is in and calculate idf
    for word in words:
        count = 0

        for document in documents:
            if word in documents[document]:
                count += 1

        idfs[word] = math.log(len(documents) / count)

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = {}

    for file in files:
        file_tfidf = 0
        for word in query:
            # word frequency * idf
            file_tfidf += files[file].count(word) * idfs[word]

        tf_idfs[file] = file_tfidf

    top = list(tf_idfs.keys())
    top.sort(reverse=True, key=lambda x:tf_idfs[x])

    return top[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    res = {}

    for sentence in sentences:
        res[sentence] = {}
        sent_mwm = 0
        count = 0
        # add idf of query words in doc and count word freq
        for word in query:
            if word in sentences[sentence]:
                sent_mwm += idfs[word]
                count += sentence.count(word)

        res[sentence]["mwm"] = sent_mwm
        # query density
        res[sentence]["den"] = count / len(sentences[sentence])

    top = list(res.keys())
    top.sort(reverse=True, key=lambda x:(res[x]["mwm"], res[x]["den"]))

    return top[:n]


if __name__ == "__main__":
    main()
