def pars_message(text):
    """
    Обработка входных данных. Поиск разделителя.
    Возвращает список с одни элементом (исполнителем) или двумя (исполнитель + трек).
    Аргумент:
        text message
    """
    qгery = text
    pars = qгery.split(' ; ')
    return pars