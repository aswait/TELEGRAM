
def info_message(hotel: dict, period: str) -> str:
    string = f"🏨 Название отеля: {hotel['name']}"\
             f"\n🌎 Адрес: {hotel['address']}"\
             f"\n🌐 Сайт: {hotel['url']}"\
             f"\n📌 Открыть в Google maps: {hotel['map']}"\
             f"\n🚉 Расстояние от центра: {hotel['distance']} км"\
             f"\n💲 Цена за сутки: {hotel['price']} USD"\
             f"\n💵 Цена за период: {round(hotel['price'] * int(period), 2)} USD"\
             f"\n🛎 Рейтинг: {hotel['rating']}"\
             f"\n🧳 Рейтинг по мнению посетителей: {hotel['review']}"

    return string
