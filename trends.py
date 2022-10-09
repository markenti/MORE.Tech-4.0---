from natasha import Segmenter, NewsMorphTagger, Doc, NewsEmbedding
import numpy as np


def get_all_trends(corpus, vectorizer):
    X = vectorizer.fit_transform(corpus['title']).toarray()

    count = X.shape[0] // 9

    new_freq = np.asarray(X[:count].sum(axis=0)).ravel() / len(X[:count])
    old_freq = np.asarray(X[count:].sum(axis=0)).ravel() / len(X[count:])

    razn = np.array(new_freq - old_freq)
    vocab = np.array(vectorizer.get_feature_names_out())

    return vocab[np.argsort(razn)[-40:]]


def get_good_trends(result):
    segmenter = Segmenter()
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)

    trend = []

    for gram in result:

        doc = Doc(gram)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)
        synt_length = len(doc.tokens)

        if synt_length == 1 and doc.tokens[0].pos == 'NOUN':
            trend.append(gram)

        elif synt_length > 1:
            trend.append(gram)

    return np.array(trend)