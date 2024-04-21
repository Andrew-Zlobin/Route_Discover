from bing_image_downloader import downloader
query_string ="Петроградская метро"
downloader.download(query_string, limit=2,  output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)

import json

def process_data(data):
    for item in data:
        title = item.get('title')
        if title:
            # Обработка значения поля title
            # print(title)
            query_string = title
            downloader.download(query_string, limit=2,  output_dir='dataset', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
        if 'children' in item:
            process_data(item['children'])

# Загрузка данных из файла data.json
with open('objectCity.json', 'r') as file:
    data = json.load(file)

# Обработка данных
process_data(data)
