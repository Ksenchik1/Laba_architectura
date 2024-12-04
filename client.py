import socket

client = socket.socket()
hostname = socket.gethostname()
port = 17085

try:
    client.connect((hostname, port))
except ConnectionRefusedError:
    print("Не удалось подключиться к серверу. Сервер может быть закрыт.")
    client.close()
    exit()

while True:
    try:
        message = input("Введите текст (введите 'close' для выхода): ")
        if message.strip() == '':
            print("Вы не можете отправить пустую строку. Пожалуйста, введите данные.")
            continue
        client.send(message.encode())

        if message.lower() == 'close':
            print("Закрытие соединения с сервером.")
            data = client.recv(1024)
            print("Сервер отправил:", data.decode())
            break

        try:
            data = client.recv(1024)
        except OSError as e:
            print("Соединение с сервером было прервано: ", e)
            break

        if not data:
            print("Сервер разорвал соединение.")
            break

        print("Сервер отправил:", data.decode())
    except OSError as e:
        print("Ошибка при отправке сообщения:", e)
        break

client.close()
