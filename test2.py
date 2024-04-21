from google_images_download import google_images_download

# Функция для загрузки изображения Казанского собора
def download_kazan_cathedral_image():
    response = google_images_download.googleimagesdownload()

    # Параметры поиска изображений
    search_params = {
        "keywords": "Казанский собор",  # Ключевые слова для поиска
        "limit": 1,  # Количество изображений для загрузки
        "output_directory": "images",  # Папка для сохранения изображений
        "no_directory": True  # Не создавать отдельную папку для каждого запроса
    }

    # Загрузка изображений
    response.download(search_params)

# Загрузка изображения Казанского собора
download_kazan_cathedral_image()
