import pandas as pd
import matplotlib.pyplot as plt
import time

# Пути к файлу данных и графику
log_file_path = './logs/metric_log.csv'
output_image_path = './logs/error_distribution.png'

while True:
    try:
        # Чтение данных из metric_log.csv
        data = pd.read_csv(log_file_path)
        
        # Построение гистограммы абсолютных ошибок
        plt.figure(figsize=(10, 6))
        plt.hist(data['absolute_error'], bins=20, color='skyblue', edgecolor='black')
        plt.title('Distribution of Absolute Errors', fontsize=16)
        plt.xlabel('Absolute Error', fontsize=14)
        plt.ylabel('Frequency', fontsize=14)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        
        # Сохранение графика в файл
        plt.savefig(output_image_path)
        plt.close()
        print(f'Гистограмма обновлена: {output_image_path}')
        
        # Задержка между обновлениями
        time.sleep(10)
    except FileNotFoundError:
        print(f'Файл {log_file_path} не найден. Ожидание...')
        time.sleep(10)
    except Exception as e:
        print(f'Ошибка: {e}')
        time.sleep(10)