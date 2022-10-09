from sklearn.feature_extraction.text import CountVectorizer
from catboost import CatBoostClassifier
import pandas as pd
import preprocess
import form_dataframe
import vect_clas


# Первичное генерирование большого датасета для обучения TF-IDF и catboost
def create_full_dataset():
    full_df = form_dataframe.create_df(n_inter=10, n_buh=50, n_audit=50, n_anti=120)
    full_df['title_processed'] = full_df['title'].apply(preprocess.full_preprocess)
    full_df.to_pickle('df_main.pkl')


# Генерирование мини-батча, который и выгружается в папку, и возвращается при вызове функции
def create_mini_batch():
    mini_batch = form_dataframe.create_df()
    mini_batch['title_processed'] = mini_batch['title'].apply(preprocess.full_preprocess)

    vectorizer = get_vectorizer()

    classifier = CatBoostClassifier(border_count=3)
    classifier.load_model("cat_model.cbm", format='cbm')

    mini_batch = add_proba(mini_batch, classifier, vectorizer)

    mini_batch.to_pickle('mini_batch.pkl')

    return mini_batch


def add_proba(x, classifier, vectorizer):

    df = x.copy()
    df['pred'] = df['title_processed'].apply(lambda x: classifier.predict_proba(vectorizer.transform([x])))

    df['buh_proba'] = df['pred'].apply(lambda x: x[0][1])
    df['is_proba'] = df['pred'].apply(lambda x: x[0][2])

    def predict(x):
        if x >= 0.7:
            return 1
        else:
            return 0

    df['buh'] = df['buh_proba'].apply(predict)
    df['is'] = df['is_proba'].apply(predict)

    df.drop(columns=['pred'], inplace=True)

    return df

def get_vectorizer():

    df_main = pd.read_pickle('df_main.pkl')
    vectorizer = vect_clas.fit_tf_idf(df_main)

    return vectorizer

def generate_vect_clas():

    df_main = pd.read_pickle('df_main.pkl')
    vectorizer = get_vectorizer()

    x_vectors = vectorizer.fit_transform(df_main['title_processed'])
    y = df_main['target'].values
    # Classifier
    classifier = vect_clas.fit_class(x_vectors, y)
    # Add Proba
    new = add_proba(df_main, classifier, vectorizer)

    return vectorizer, classifier

# create_full_dataset() -  создание базы данных

# Первый шаг - обновить classifier и vectorizer. К этому шагу уже должен быть составлел файл df_main.pkl (база данных)
# generate_vect_clas()

# Теперь можно создавать мини-батчи (это DataFrame из новостей, который выгрузился в папку со столбцами вероятности
# create_mini_batch()