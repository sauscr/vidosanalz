Привет, Меченый! Рад видеть тебя в нашем репозитории. Тут, как в Зоне, всё не так просто, но я помогу тебе запустить наше приложение без лишних мутантов и аномалий. Следуй за мной, и мы вместе преодолеем любые препятствия… или хотя бы настроим проект.

## Как запустить мое приложение на своем компьютере

Имеется .env файл, переменуй .env.example в .env и глянь чего тебе надо изменить

**Важно:** Все действия проводятся в терминале с правами администратора(Windows) в VSCode. Пока что WSL оставим на потом – у нас времени нет, как у сталкера перед рейдом.

### Шаг 1. Создаем виртуальное окружение
Создаём виртуальное окружение рядом с сервером:
```bash
python -m venv venv
```
Отлично, виртуальное окружение создано. Теперь активируем его:
```bash
venv\Scripts\activate
```

Супер, ты в виртуальной зоне. Теперь установим необходимые библиотеки из `requirements.txt`:
```bash
pip install -r requirements.txt
```
Всё, библиотеки установлены. Двигаемся дальше – на сам сервер:
```bash
cd \backend
```

ПРЕЖДЕ ЧЕМ ЗАПУСКАТЬ CELERY, НАДО ЗАПУСТИТЬ DOCKER С REDIS
### Шаг 2. Устанавливаем Docker
 Скачай Docker с [официального сайта](https://www.docker.com/). Если потребуется регистрация – не бойся, это как получать разрешение от Атамана. Загружай всё необходимое.
### Шаг 3. Запускаем Redis в Docker
  (убедись, что ты в папке `\backend`):
   ```bash
   docker run -d -p 6379:6379 --name redis redis
   ```

Мои движения вечны – слова великого человека, продолжаем.

### Шаг 4. Запускаем Celery
```bash
celery -A config worker -l info --pool=solo
```
Еее, Celery в деле!

### Шаг 5. Запускаем сервер Django
Открой новый терминал в VSCode и выполни:
```bash
cd .\backend
python manage.py migrate
python manage.py runserver
```

### Шаг 6. Загружаем видео
Если всё запустилось – поздравляю, ты прошёл первую зону. Теперь открой ещё один терминал и заливай свой видос ~~ip-поток~~:
```bash
cd .\backend
python manage.py capture_stream --url "B:\path\to\video.mp4" --source_type "file" --interval 1
```

После этого у тебя сохранятся кадры с видео ~~придет уведомление~~.

---

Если всё прошло гладко, проект запустился без ошибок. Если возникли трудности, перечитай выше написанное, Меченый. В крайнем случае, пиши мне в Telegram [@sauscr](https://t.me/sauscr), но только по поводу программы. Не предлагай мне консервных банок.

Удачи в Зоне и пусть твой код будет чист, как чернобыльская вода!
