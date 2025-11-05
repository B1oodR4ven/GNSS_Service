import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 8080)
server_socket.bind(server_address)

server_socket.listen(1)
print(f'sever zapushen na {server_address}')
while True:
    #принимаем входящие
    client_socket, client_address = server_socket.accept()
    print(f'подключен клиент{client_address}')
    try:
        #получаем данные от клиента
        data = client_socket.recv(1024)
        if data:
            print(f'получено{data.decode("UTF-8")}')
            response = "Привет от сервера"
            client_socket.sendall(response.encode("utf-8"))

    finally:
        client_socket.close()