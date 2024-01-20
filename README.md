
![Static Badge](https://img.shields.io/badge/python_version-3.8%7C3.9%7C3.10%7C3.11%7C3.12-brightgreen?style=for-the-badge&logo=python)
![Static Badge](https://img.shields.io/badge/django_version-4.2.9-brightgreen?style=for-the-badge&logo=django)

## Сайт "Куда пойти"
![scrinshot](static/img/live_screenshot.gif)
### Описание проекта

Сервис для отображения локаций на карте, а также добавления описания и фотографий к ним.

### Основные возможности проекта
- Создание, удаление и редактирование локаций на карте с использованием интерфейса администратора;
- Добавление картинок к локациям;
- Возможность выбора очередности показа картинок.


### Как запустить проект:

Для запуска проекта на локальной машине у вас должны быть установлены Python, git.

Клонируйте репозиторий:
```
git clone git@github.com:nucluster/where_to_go.git
```

Измените свою текущую рабочую директорию:
```
cd where_to_go
```
Создайте и активируйте виртуальное окружение, установите зависимости:
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Создайте .env файл следующего содержания:
```
DEBUG=True
SECRET_KEY=[ваш_секретный_ключ]
ALLOWED_HOSTS=
``` 
>DEBUG: _Логическое значение, которое включает/выключает режим отладки. Если ваше приложение выдает исключение, когда DEBUG имеет значение True, Django отобразит подробную обратную трассировку, включая множество метаданных о вашей среде, например все определенные на данный момент настройки Django (из settings.py)._

>SECRET_KEY: _Секретный ключ для конкретной установки Django. Он используется для обеспечения криптографической подписи и должен быть установлен на уникальное, непредсказуемое значение._

>ALLOWED_HOSTS: _Список строк, представляющих имена хостов/доменов, которые может обслуживать этот сайт Django. Это мера безопасности для предотвращения атак по заголовку HTTP-хоста, которые возможны даже при многих, казалось бы, безопасных конфигурациях веб-сервера._

Примените миграции:
```
python manage.py migrate
```

Создайте суперпользователя Django:
```
python manage.py createsuperuser
```
Для создания тестового суперпользователя можно воспользоваться командой:
```
python manage.py superuser
```
Будет создан суперпользователь login: admin, password: 12345.

Для загрузки данных из json-файлов в БД:
```
python manage.py load_places [путь к папке с файлами локаций]
```
Формат файла локации:
```json
{
    "title": "Экскурсионная компания «Легенды Москвы»",
    "imgs": [
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/4f793576c79c1cbe68b73800ae06f06f.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/7a7631bab8af3e340993a6fb1ded3e73.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/a55cbc706d764c1764dfccf832d50541.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/65153b5c595345713f812d1329457b54.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/0a79676b3d5e3b394717b4bf2e610a57.jpg",
        "https://raw.githubusercontent.com/devmanorg/where-to-go-places/master/media/1e27f507cb72e76b604adbe5e7b5f315.jpg"
    ],
    "description_short": "Неважно, живёте ли вы в Москве всю жизнь или впервые оказались в столице, составить ёмкий, познавательный и впечатляющий маршрут по городу — творческая и непростая задача. И её с удовольствием берёт на себя экскурсионная компания «Легенды Москвы»!",
    "description_long": "<p>Экскурсия от компании «Легенды Москвы» — простой, удобный и приятный способ познакомиться с городом или освежить свои чувства к нему. Что выберете вы — классическую или необычную экскурсию, пешую прогулку или путешествие по городу на автобусе? Любые варианты можно скомбинировать в уникальный маршрут и создать собственную индивидуальную экскурсионную программу.</p><p>Компания «Легенды Москвы» сотрудничает с аккредитованными экскурсоводами и тщательно следит за качеством экскурсий и сервиса. Автобусные экскурсии проводятся на комфортабельном современном транспорте. Для вашего удобства вы можете заранее забронировать конкретное место в автобусе — это делает посадку организованной и понятной.</p><p>По любым вопросам вы можете круглосуточно обратиться по телефонам горячей линии.</p><p>Подробности узнавайте <a class=\"external-link\" href=\"https://moscowlegends.ru \" target=\"_blank\">на сайте</a>. За обновлениями удобно следить <a class=\"external-link\" href=\"https://vk.com/legends_of_moscow \" target=\"_blank\">«ВКонтакте»</a>, <a class=\"external-link\" href=\"https://www.facebook.com/legendsofmoscow?ref=bookmarks \" target=\"_blank\">в Facebook</a>.</p>",
    "coordinates": {
        "lng": "37.64912239999976",
        "lat": "55.77754550000014"
    }
}
```
Для загрузки данных из json-файла по ссылке:
```
python manage.py load_place [ссылка]
```
Фотографии локаций будут подгружаться по ссылке.

Для загрузки и сохранении фотографий на локальный компьютер:
```
python manage.py dwnld_images
```
Файлы фотографий будут сохранены в папку media с нумерацией порядкового номера фотографии локации и названием локации на транслите.
Пример:
```
media/places/ostankinskaya-telebashnya_3.jpg
```
Запуск:
```
python manage.py runserver
```

Работающий сайт доступен по адресу:

https://jasgzym9t.eu.pythonanywhere.com/
 
