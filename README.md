Вот стилизованный README.md в формате Markdown:

```markdown
# Travel Bot 🌍✈️

Telegram-бот для планирования путешествий с интеграцией картографических сервисов


## 🚀 Запуск
```bash
docker-compose up --build -d
```


## 🗃️ База данных
- Реализован паттерн **Repository** для работы с PostgreSQL
- Миграции через Alembic 

## 📦 Внешние зависимости
### Картография
- **Folium** - генерация интерактивных карт с пользовательским стилем
- **Selenium** - конвертация HTML-карт в PNG (headless Chrome)
- **OpenStreetMap** - поиск локаций и геокодирование
- **OSRM** - построение оптимальных маршрутов между точками

## 🐳 Docker-окружение
```yaml
services:
  bot:           # Основное приложение (Python)
  bot_db:        # PostgreSQL база данных
  chrome:        # Headless Chrome для рендеринга
  selenium-hub:  # Selenium Grid оркестратор
```

## 🛠️ Функционал
| Компонент          | Описание                                                                 |
|--------------------|-------------------------------------------------------------------------|
| 👤 Профиль         | Создание/редактирование пользовательских данных                         |
| 🗺 Путешествия     | Управление поездками с привязкой к датам                               |
| 🗺 Маршруты       | Автоматическая генерация оптимальных путей между точками (OSRM)        |
| 📎 Вложения        | Прикрепление файлов и заметок к поездкам                               |
| 🖼 Карты           | Визуализация маршрутов через Folium + экспорт в PNG                    |

## ⚙️ Dockerfile
```dockerfile
FROM python:3.11-slim
# Установка зависимостей
RUN apt-get update && apt-get install -y ...
# Копирование и установка Python-пакетов
COPY requirements.txt .
RUN pip install -r requirements.txt
# Запуск приложения
CMD ["python", "main.py"]
```


