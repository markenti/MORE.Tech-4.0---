import parser_func
import pandas as pd
import numpy as np


def create_df(n_inter=1, n_buh=1, n_audit=1, n_anti=1):
    # Интерфакс
    inter_url = 'https://www.interfax.ru/news/'

    interfax_df = parser_func.get_last_N_days_interfax(inter_url=inter_url, n=n_inter)
    interfax_df['target'] = 0
    interfax_df.drop_duplicates(inplace=True)

    # buh.ru

    buh_url = 'https://buh.ru/news/uchet_nalogi/?PAGEN_1='

    buh_df = parser_func.get_last_N_pages_buh(buh_url=buh_url, n=n_buh)
    buh_df['target'] = 1
    buh_df.drop_duplicates(inplace=True)

    # audit-it.ru

    audit_url = 'https://www.audit-it.ru/news/account/'

    audit_df = parser_func.get_last_N_pages_audit(audit_url=audit_url, n=n_audit)
    audit_df['target'] = 1
    audit_df.drop_duplicates(inplace=True)

    # anti-malware.ru

    anti_url = 'https://www.anti-malware.ru/news?page='

    anti_df = parser_func.get_last_N_pages_anti(anti_url=anti_url, n=n_anti)
    anti_df['target'] = 2
    anti_df.drop_duplicates(inplace=True)

    # Финальный датасет

    df = pd.DataFrame()
    df = pd.concat([df, interfax_df, buh_df, audit_df, anti_df])

    df.drop_duplicates(subset='title', inplace=True)
    df.drop_duplicates(subset='link', inplace=True)
    df.set_index(np.array([i for i in range(len(df))]), inplace=True)

    return df
