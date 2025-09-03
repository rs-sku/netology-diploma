# Дипломная работа профессии "Python-разработчик"

## Руководство по запуску
1. Клонировать репозиторий: `git clone git@github.com:SkuratovichRS/netology_diploma.git`
2. Создать виртуальное окружение: `python -m venv .venv`
3. Активировать виртуальное окружение: `source venv/bin/activate` (На виндовс: `venv\Scripts\activate`)
4. Установить зависимости: pip install -r `requirements.txt`
5. Создать `.env` с переменными из `.env.example`
6. Запустить БД: `docker compose up -d`
7. Применить миграции: `python manage.py migrate` 
8. Запустить сервис: `python manage.py runserver`