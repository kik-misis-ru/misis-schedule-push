# МИР МИСиС - Отправка пуш-нотификаций

## Запуск приложения

1. Клонируем репозиторий:
  > git clone https://github.com/kik-misis-ru/misis-schedule-push.git
2. Создам папку для приложения:
  >mkdir misis-push
3. Переходим в папку:
  > cd misis-push
3. Добавляем заполняем .env реальными данными.

4. Создаем виртуальное окружение:
  > python virtualenv venv
5. Активируем виртуальное окружение.
  > venv\Scripts\activate
6. Устанавливаем модули из файла requirements.txt:
  > pip install -r requirements.txt
7. Запускаем приложение:
  >python main.py