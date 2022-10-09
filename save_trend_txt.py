import trends
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

def get_trend(prof):

    """"
    prof = ['is', 'buh']
    """"

    df = pd.read_pickle('df_main.pkl')
    cnt_vectorizer = CountVectorizer(ngram_range=(1, 3))

    # Внимание: в нижней строчке заменить target на принятое тобой решение
    result = trends.get_all_trends(df.loc[df[prof] == 1], cnt_vectorizer)
    list_of_trends = trends.get_good_trends(result)

    return list_of_trends
