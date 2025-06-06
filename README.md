# goit-pythonweb-hw-06

## Встановлення та запуск

### 1. Встановіть залежності
```
poetry install
```

Активуйте віртуальне середовище
```
poetry shell
```

### 2. Налаштування змінних середовища

Створіть файл `.env` у корені проекту (можете скопіювати з `.env.example`):


### 3. Запуск PostgreSQL через Docker

```bash
docker-compose up -d
```

### 4. Застосування міграцій

```bash
alembic upgrade head
```

### 5. Заповнення бази тестовими даними

```bash
python seed.py
```

### 6. Тестування запитів

```bash
python my_select.py
```
