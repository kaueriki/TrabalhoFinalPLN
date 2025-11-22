from collections import Counter
import math


def calcular_bow(corpus_tokens):
    bow_global = Counter()

    for tokens in corpus_tokens:
        bow_global.update(tokens)

    return bow_global


def calcular_tfidf(corpus_tokens):
    total_docs = len(corpus_tokens)

    df = Counter()
    for tokens in corpus_tokens:
        df.update(set(tokens))

    tfidf_global = {}

    for tokens in corpus_tokens:
        tf = Counter(tokens)
        for palavra, freq in tf.items():
            idf = math.log((total_docs + 1) / (df[palavra] + 1)) + 1
            score = freq * idf

            if palavra not in tfidf_global or score > tfidf_global[palavra]:
                tfidf_global[palavra] = score

    return tfidf_global


def calcular_bow_tfidf(preprocess_output):
    tokens = preprocess_output["tokens"]

    bow = calcular_bow(tokens)
    tfidf = calcular_tfidf(tokens)

    return bow, tfidf
