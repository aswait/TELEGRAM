Это телеграм бот, с помощью которого можно получать информацию об отелях, в работе использует Rapid Api.   
   
___  

#### Используемые библиотеки:  
        pyTelegramBotAPI 4.10.0  
        python-dotenv 1.0.0
        peewee 3.16.0
        loguru 0.6.0
        python-telegram-bot-calendar 1.0.5
Все библиотеки устанавливаются из файла ```requirements.txt```

___
### Бот состоит из следующих пакетов:  
        config_data - содержит конфигурационные настройки, такие как API key, token для telegram бота и остальные настройки.
        api - пакет для работы c API
        database - содержит процедуры для работы с БД.
        keyboards - содержит клавиатцуры для бота
        states - здесь прописаны состояния для диалога пользователя с ботом

___
### Начало работы:
Для запуска бота необходим установленный интерпретатор Python версии 3.9 все остальные пакеты в requirements.txt. Нужен файл .env куда нужно сохранить RAPIDAPI_KEY и токен от вашего бота.