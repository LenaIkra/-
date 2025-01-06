import pika
import json
import pandas as pd
from pathlib import Path
from datetime import datetime

# Инициализируем файл логирования
log_file = Path("./logs/metric_log.csv")

if not log_file.exists():
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'w') as f:
        f.write("id,y_true,y_pred,absolute_error\n")

# Словарь для временного хранения данных
data_store = {}

# Функция для записи метрики в файл
def log_metric(message_id, y_true, y_pred):
    absolute_error = abs(y_true - y_pred)
    with open(log_file, 'a') as f:
        f.write(f"{message_id},{y_true},{y_pred},{absolute_error}\n")
    print(f"Метрика записана: id={message_id}, y_true={y_true}, y_pred={y_pred}, absolute_error={absolute_error}")

# Обработчик сообщений из очереди y_true
def callback_y_true(ch, method, properties, body):
    message = json.loads(body)
    message_id = message['id']
    y_true = message['body']
    if message_id in data_store and 'y_pred' in data_store[message_id]:
        y_pred = data_store[message_id]['y_pred']
        log_metric(message_id, y_true, y_pred)
        del data_store[message_id]
    else:
        data_store.setdefault(message_id, {})['y_true'] = y_true

# Обработчик сообщений из очереди y_pred
def callback_y_pred(ch, method, properties, body):
    message = json.loads(body)
    message_id = message['id']
    y_pred = message['body']
    if message_id in data_store and 'y_true' in data_store[message_id]:
        y_true = data_store[message_id]['y_true']
        log_metric(message_id, y_true, y_pred)
        del data_store[message_id]
    else:
        data_store.setdefault(message_id, {})['y_pred'] = y_pred

try:
    # Создаём подключение к серверу RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очереди
    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')

    # Подписываемся на очереди
    channel.basic_consume(queue='y_true', on_message_callback=callback_y_true, auto_ack=True)
    channel.basic_consume(queue='y_pred', on_message_callback=callback_y_pred, auto_ack=True)

    # Запускаем режим ожидания сообщений
    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()

except Exception as e:
    print(f'Ошибка при подключении к очереди: {e}')
