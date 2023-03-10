from database.retrieve import retrieve_data


def history_message(user_id: int) -> str:
    info = retrieve_data(user_id)
    message = list()

    for command in info:
        message.append(f"💬 Команда: {command['command']}"
                       f"\n📅 Дата и время ввода: {command['date']}"
                       f"\n🏨 Отели:")
        for hotel in command['hotels']:
            message.append("{} ℹ Название: {}" 
                           "\n{} 🔗 Ссылка: {}".format('\t'*6, hotel['name'], '\t'*6, hotel['url']))
        message.append('\n')

    return '\n'.join(message)
