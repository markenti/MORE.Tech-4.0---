import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, concat
from tqdm import tqdm
import datetime


def get_day_news(url):
    inter_df = DataFrame()
    for i in range(1, 10):

        response = requests.get(url + str(i))
        soup = BeautifulSoup(response.text, 'lxml')
        items = None

        if items == soup.find(class_='an').find_all('a'):
            break

        items = soup.find(class_='an').find_all('a')

        def get_right_link(x):

            if 'www' in x:
                return x
            else:
                return 'https://interfax.ru' + x

        links = [get_right_link(item.get('href')) for item in items]
        titles = [item.find('h3').get_text().strip() for item in items]

        inter_df = concat([inter_df, DataFrame({'title': titles, 'link': links})])

    return inter_df


def get_last_N_days_interfax(inter_url, n):
    start_date, end_date = datetime.date.today() - datetime.timedelta(days=n), datetime.date.today()
    delta = end_date - start_date
    interfax_df = DataFrame()

    dates = [str(start_date + datetime.timedelta(days=i))[:4] + '/'
             + str(start_date + datetime.timedelta(days=i))[5:7] + '/'
             + str(start_date + datetime.timedelta(days=i))[8:10] for i in range(delta.days + 1)]

    for date in tqdm(dates):
        interfax_df = concat([interfax_df, get_day_news(inter_url + date + '/all/page_')])

    return interfax_df


def get_last_N_pages_buh(buh_url, n):
    buh_df = DataFrame()

    for i in tqdm(range(1, n + 1)):
        url = buh_url + str(i)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        items = soup.find(class_="tab-pane fade active").find_all('a')[:-7]
        links = ['https://buh.ru' + item.get('href') for item in items]
        titles = [item.get_text().strip() for item in items]

        buh_df = concat([buh_df, DataFrame({'title': titles, 'link': links})])

    return buh_df


def get_last_N_pages_audit(audit_url, n):
    audit_df = DataFrame()

    for i in tqdm(range(1, n + 1)):
        response = requests.get(audit_url + str(i))
        soup = BeautifulSoup(response.text, 'lxml')

        items = soup.find(class_='news-list').find_all('a')
        links = ['https://audit-it.ru' + item.get('href') for item in items]
        titles = [item.get_text().strip() for item in items]

        audit_df = concat([audit_df, DataFrame({'title': titles, 'link': links})])

    return audit_df


def get_last_N_pages_anti(anti_url, n):
    anti_df = DataFrame()

    for i in tqdm(range(1, n + 1)):
        response = requests.get(anti_url + str(i))
        soup = BeautifulSoup(response.text, 'lxml')

        items = soup.find_all('h2')[:-2]
        links = ['https://anti-malware.ru' + item.find('a').get('href') for item in items]
        titles = [item.find('a').get_text().strip() for item in items]

        anti_df = concat([anti_df, DataFrame({'title': titles, 'link': links})])

    return anti_df
