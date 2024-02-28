# Learning Platform

Этот проект представляет собой онлайн-платформу для обучения, разработанную на основе Django и Django REST Framework.

## Установка

1. Клонируйте репозиторий с помощью команды:

```
git clone https://github.com/your_username/Learning-Platform.git
```

2. Перейдите в каталог проекта:

```
cd Learning-Platform
```

3. Создайте и активируйте виртуальное окружение:

```
python -m venv venv
source venv/bin/activate # для MacOS/Linux
venv\Scripts\activate # для Windows
```

4. Установите зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

5. Примените миграции:

```
python manage.py migrate
```

## Запуск

Запустите сервер разработки Django:

```
python manage.py runserver
```

После этого проект будет доступен по адресу http://127.0.0.1:8000/.

## Использование API

API предоставляет следующие эндпоинты:

- `/api/available-products/` - получение списка доступных продуктов
- `/api/product-lessons/<product_id>/` - получение уроков продукта по его идентификатору