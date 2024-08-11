import pandas as pd
from sklearn.cluster import KMeans
import numpy as np

def get_recommendation(lst, df_recom):
    """
    Подбор рекомендаций музыки по входной информации: артист / артист+песня.
    Аргументы:
        lst: list с указанием артиста / артиста+песни
        df_recom: DataFrame с указанием номера кластера, исполнителя, трека, общее количество трека исполнителя в кластере, общее количество повторов исполнителя в кластере
    """
    if len(lst) == 1: # поиск рекомендации только по исполнителю
        # выявление кластера, где максимально содержится запрошенный исполнитель
        nomber = df_recom[df_recom.artistname == lst[0]]
        nomber_cluster = int(nomber[nomber.count_artist == nomber.count_artist.max()]['cluster'].unique())

        # выделяем необходимый кластер. Производим выборку 10 треков. Объединяем артиста и его трек в один столбец с разделителем " - "
        df_recom = df_recom[df_recom.cluster == nomber_cluster].sample(n=10)
        df_recom['artist - track'] = df_recom['artistname'] + ' - ' + df_recom['trackname']
        lst_recomm = df_recom['artist - track'].tolist()
        return lst_recomm

    elif len(lst) == 2: # поиск рекомендации по по исполнителю и треку
        # выявление кластера, где максимально содержится запрошенный трек и исполнитель
        nomber_1 = df_recom[(df_recom.artistname == lst[0]) & (df_recom.trackname == lst[1])]
        nomber_cluster_1 = int(nomber_1[(nomber_1.count_tracks == nomber_1.count_tracks.max()) & (nomber_1.count_artist == nomber_1.count_artist.max())]['cluster'].unique())

        # выделяем необходимый кластер. Производим выборку 10 треков. Объединяем артиста и его трек в один столбец с разделителем " - "
        df_recom = df_recom[df_recom.cluster == nomber_cluster_1].sample(n=10)
        df_recom['artist - track'] = df_recom['artistname'] + ' - ' + df_recom['trackname']
        lst_recomm = df_recom['artist - track'].tolist()
        return lst_recomm
