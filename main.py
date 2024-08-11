import pandas as pd
import find_cluster
import recommendation
import parser

def recom_music(text):
    """
    Возвращает список рекомендованных треков и исполнителей.
    Включает в себя функции: pars_message(text),  get_find_cluster(df_clean), get_recommendation(lst, data_recom).
    Аргумент:
        text: text message
    """
    # считываем датасет
    df_clean = pd.read_csv('Z_dataset_clean.csv')

    # Запускаем парсер входных данных и проверяем наличие их в датасете
    lst = parser.pars_message(text)
    if len(lst) == 1:
        if lst[0] not in df_clean['artistname'].values:
            raise TypeError('Cannot find' + lst[0] + 'in the dataset')
        
    elif len(lst) == 2:
        if lst[0] not in df_clean['artistname'].values:
            raise TypeError('Cannot find' + lst[0] + 'in the dataset')
        elif lst[1] not in df_clean['trackname'].values:
            raise TypeError('Cannot find' + lst[1] + 'in the dataset')

    # Запускаем функцию по разбиению на кластеры данных
    data_recom = find_cluster.get_find_cluster(df_clean)

    # Запускаем функцию по поиску рекомендаций
    recom_lst = recommendation.get_recommendation(lst, data_recom)
    return recom_lst