# no_time_to_listen

Телеграмм бот, использующий обученную модель vosk для перевода голосовых сообщений в текст.

https://t.me/NoTimeToListenBot

Для установки необходим Python версии 3.11

## Установка

- Скачайте проект с репозитория 
  ```sh 
  git clone https://github.com/shinumerde/no_time_to_listen
  ```
- Перейдите в папку проекта
  ```sh
  cd no_time_to_listen
  ```
- Установите зависимости
  ```sh
  pip install -r requirements.txt
  ```
- Зарегистрируйте своего бота в
  ```sh
  https://t.me/BotFather
  ```
- Полученный API токен подставьте вместо переменной API_TOKEN в app.py либо используйте .env файл с переменной API_TOKEN
