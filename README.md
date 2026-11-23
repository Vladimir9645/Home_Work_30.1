# Home_Work_30.1

Учебный LMS-проект на Django и Django REST Framework. Реализованы курсы, уроки, кастомная авторизация по email и API для управления платежами.

## Стек технологий

- Python 3.11+
- Django 6.1
- Django REST Framework
- django-filter
- SQLite (разработка)

## Возможности

- Управление курсами и уроками (CRUD через API).
- Кастомная модель пользователя с входом по email.
- Учёт платежей (курс/урок, сумма, способ оплаты).
- API с фильтрацией и сортировкой.
- Вложенные сериализаторы: в ответе курса сразу виден список уроков и их количество.

## Структура проекта

## Структура проекта

```
Home_Work_30.1/
├── config/                 # Настройки и главный urls
│   ├── settings.py
│   └── urls.py
├── lms/                    # Курсы и уроки
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── users/                  # Пользователи, платежи, фильтры
│   ├── models.py
│   ├── serializers.py
│   ├── filters.py
│   ├── views.py
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── create_payments.py
├── media/                  # Загружаемые файлы
└── README.md
```

## Как запустить

1. Установи зависимости:
   ```bash
   pip install django djangorestframework django-filter

