import socket
import os
from urllib.parse import urlparse, urljoin

def http_client(host, port, path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
        client_socket.sendall(request.encode('utf-8'))
        response = b""
        
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data
            
    # Возвращаем только тело ответа
    return response.split(b"\r\n\r\n", 1)[1]

def save_image(image_url, directory='images'):
    # Создаем директорию, если ее нет
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Получаем имя файла из URL
    image_name = os.path.basename(image_url)

    # Если путь к файлу не указан, задаем имя по умолчанию
    if not image_name:
        image_name = "image.jpg"

    # Загрузка изображения
    try:
        parsed_url = urlparse(image_url)
        response = http_client(parsed_url.hostname, 80, parsed_url.path)
        with open(os.path.join(directory, image_name), 'wb') as img_file:
            img_file.write(response)
        print(f"Сохранено: {image_name}")
    except Exception as e:
        print(f"Ошибка при загрузке {image_url}: {e}")

def extract_images(html_content):
    # Извлекаем URL всех изображений с помощью регулярного выражения
    import re
    image_urls = re.findall(r'<img\s+[^>]*src="([^"]+)"', html_content.decode('utf-8'))
    return image_urls

def extract_links(html_content):
    # Извлекаем все ссылки на другие страницы
    import re
    links = re.findall(r'href="([^"]+)"', html_content.decode('utf-8'))
    return links

if __name__ == "__main__":
    host = "rokot.ibst.psu"
    port = 80
    path = "/anatoly/"

    response = http_client(host, port, path)
    
    # Сохраняем изображения с основной страницы
    image_urls = extract_images(response)
    for url in image_urls:
        # Проверяем, является ли ссылка абсолютной или относительной
        if not url.startswith("http"):
            url = urljoin(f"http://{host}{path}", url)
        save_image(url)

    # Обрабатываем ссылки на другие страницы и сохраняем изображения с них
    links = extract_links(response)
    for link in links:
        # Проверяем, является ли ссылка абсолютной или относительной
        if not link.startswith("http"):
            link = urljoin(f"http://{host}{path}", link)

        try:
            parsed_url = urlparse(link)
            response = http_client(parsed_url.hostname, 80, parsed_url.path)

            # Извлекаем и сохраняем изображения с текущей страницы
            image_urls = extract_images(response)
            for url in image_urls:
                if not url.startswith("http"):
                    url = urljoin(link, url)
                save_image(url)
        except Exception as e:
            print(f"Ошибка при обработке {link}: {e}")

