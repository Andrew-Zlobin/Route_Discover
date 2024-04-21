import osmnx as ox
import matplotlib.pyplot as plt
from PIL import Image

def get_image_from_coordinates(latitude, longitude, zoom=15, width=400, height=400):
    # Загрузка изображения карты OpenStreetMap по координатам с помощью osmnx
    graph = ox.graph_from_point((latitude, longitude), dist=100, network_type='all')
    fig, ax = ox.plot_graph(graph, figsize=(6, 6), show=False, close=True, bgcolor='w', node_color='b')

    # Сохранение изображения и его последующее открытие
    image_path = "map.png"
    plt.savefig(image_path, dpi=300, bbox_inches='tight', pad_inches=0.1)
    plt.close(fig)  # Закрываем фигуру после сохранения
    image = Image.open(image_path)
    
    return image

# Координаты Казанского собора в Москве
latitude = 55.7520
longitude = 37.6175

# Получение изображения
image = get_image_from_coordinates(latitude, longitude)

# Отображение изображения
if image:
    image.show()
