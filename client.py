import socket
import threading

server_running = True
lock = threading.Lock()
clients = []


def close_server():
    with lock:
        global server_running
        server_running = False
        print("Сервер закрывается...")

        for client in clients:
            client.close()

        server.close()
        print("Сервер закрыт")


def h_client(con, c_id):
    global server_running

    try:
        while server_running:
            data = con.recv(1024)
            if not data:
                print(f"Клиент {c_id} отключился.")
                break

            message = data.decode()
            print(f"Клиент {c_id} ввел: {message}")

            if message.lower() == 'ping':
                response = "Pong"
                con.send(response.encode())
                print(f"Клиент {c_id} получил: {response}")
            elif message.lower() == 'close':
                print(f"Клиент {c_id} запросил закрытие сервера.")
                con.send("Сервер закрывается...".encode())
                close_server()                
                break
            else:
                response = "Мне такое не нравится("
                con.send(response.encode())
                print(f"Клиент {c_id} получил: {response}")
    except ConnectionResetError:
        print(f"Соединение с клиентом {c_id} разорвано.")
    except Exception as e:
        print(f"Произошла ошибка от клиента {c_id}: {e}")
    finally:
        con.close() 


try:
    server = socket.socket()
    hostname = socket.gethostname()
    port = 17085
    ip = socket.gethostbyname(hostname)

    server.bind((hostname, port))
    server.listen(2)
    print("Сервер запущен")
    print(f"Порт: {port}")
    print(f"Хост: {hostname}")
    print(f"Ip: {ip} \n")

    while server_running:
        try:
            client, _ = server.accept()
            clients.append(client)
            c_id = len(clients)
            threading.Thread(target=h_client, args=(client, c_id)).start()
            print(f"Клиент {c_id} подключился.")

        except Exception as e:
            print(f"Ошибка при подключении клиента: {e}")

except OSError as e:
    print(f"Произошла ошибка при создании сервера: {e}")
    exit(1)
