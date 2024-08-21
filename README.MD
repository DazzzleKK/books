# Книженции и запросы

## Features
- 4 функции для получения книг и авторов
- Тесты

## Usage
- `pip install -r req.txt`.
- `python manage.py migrate`.
- `python manage.py shell`.
```
  >>> from books.queries.shortcuts import get_books_after_date, get_authors_with_most_books, get_authors_profits, get_python_books
  >>> get_books_after_date()
  >>> get_authors_with_most_books()
  >>> get_authors_profits()
  >>> get_python_books()
  ```

## Tests
- Для корректной работы тестов необходимо отключить скрипт наполнения базы в миграции
- 52 строка [0002_auto_20240820_1155.py](books%2Fbooks_queries%2Fmigrations%2F0002_auto_20240820_1155.py)