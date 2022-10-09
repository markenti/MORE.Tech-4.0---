from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer


def full_preprocess(text):
    tokenizer = TweetTokenizer()
    tokeniz = lambda text: ' '.join(tokenizer.tokenize(text.lower()))

    stop_words = set(stopwords.words('russian'))

    def delete_stop_words(text):

        filtered_tokens = []
        for token in text.split():
            if token not in stop_words:
                filtered_tokens.append(token)

        return ' '.join(filtered_tokens)

    lemmatize = lambda text: ' '.join([MorphAnalyzer().parse(word)[0].normal_form for word in text.split()])

    text = tokeniz(text)
    text = delete_stop_words(text)

    return lemmatize(text)
