# 1. Подключить базовый образ Python 3.9
FROM python:3.9

# 2. Задать рабочую директорию
WORKDIR /usr/src/app

# 3. Скопировать содержимое папки src в рабочую директорию
COPY src/ .

# 4. Скопировать файл с зависимостями
COPY requirements.txt .

# 5. Установить все необходимые зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 6. Запустить скрипт для работы сервиса
CMD ["python", "plot.py"]
