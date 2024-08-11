import pandas as pd
from sklearn.cluster import KMeans
import numpy as np

# Идея: разделить выборку на 7 кластеров (по сходству пользователей). 
# Плюс, подготовка таблицы для поиска рекомендаций

def get_find_cluster(df_clean):
    """
    Кластеризация выборки на 7 кластеров (по сходству пользователей) с помощью алгоритма KMeans.
    Подготовка данных для поиска рекомендаций
    Возвращает датафрейм с указанием номера кластера, исполнителя, трека, общее количество трека исполнителя в кластере, общее количество повторов исполнителя в кластере.
    Аргумент:
        df_clean: DataFrame. Очищенные данные.
    """
    # Составляется матрица призаков на основе очищенных данных
    matrix = df_clean.pivot_table(values=['trackname'],index=['user_id'],columns=['artistname'], aggfunc='count').fillna(0)
    # производим деление матрицы на матрицу для составления бинарной классификации
    matrix = (matrix/matrix).fillna(0).astype("int8")
    
    # обучаем модель с разделением на 7 кластеров
    KM_model = KMeans(n_clusters=7, random_state=42, max_iter=700)
    cluster_labels = KM_model.fit_predict(matrix)

    # добавление в датафрейм меток кластеров, далее выделяем нужные столбцы датафрейма из матрицы признаков в отдельные списки
    # на основе списков составляем датафрейм, чтобы после слить его с исходной таблицей (ключ user_id)
    user_clusters = matrix.reset_index()[['user_id']]
    user_clusters['cluster'] = cluster_labels
    user = list(user_clusters['user_id'])
    cluster = list(user_clusters['cluster'])
    
    # слияние исходного датафрейма с наименованиями кластеров 
    df_result = df_clean.merge(pd.DataFrame({'user_id': user, 'cluster': cluster}), how= 'left', on= 'user_id')[['user_id', 'artistname', 'trackname', 'cluster']]

    # подсчет кол-ва треков исполнителя в каждом кластере
    group = df_result.groupby(['cluster', 'artistname', 'trackname']).count().reset_index().rename(columns={'user_id': 'count_tracks'})

    # Подсчет количества раз добавления артиста в каждом кластере:
    # group.groupby(['cluster', 'artistname'])[['count_tracks']].sum().reset_index().rename(columns= {'count_tracks': 'count_artist'})

    # слияние таблицы с подсчетом кол-ва треков и таблицы с подсчетом кол-ва раз добавленных артистов
    df_recom = group.merge(group.groupby(['cluster', 'artistname'])[['count_tracks']].sum().reset_index().rename(columns= {'count_tracks': 'count_artist'}), 
                                        how='left', on=['cluster', 'artistname'])

    return df_recom