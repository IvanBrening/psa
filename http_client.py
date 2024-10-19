import socket

def http_client(host, port, path):
    # Создаем TCP-сокет
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Подключаемся к серверу
        client_socket.connect((host, port))

        # Формируем HTTP-запрос
        request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"

        # Отправляем запрос на сервер
        client_socket.sendall(request.encode())

        # Получаем ответ от сервера
        response = b""
        while True:
            # Читаем данные из сокета
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

    # Декодируем ответ и возвращаем его
    return response.decode()

# Задаем параметры подключения
host = "rokot.ibst.psu"
port = 80
path = "/anatoly/"

# Загружаем страницу
response = http_client(host, port, path)
print(response)

