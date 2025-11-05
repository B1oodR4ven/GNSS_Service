import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 8080)
client_socket.bind(server_address)

try:
    message = "privet server"
    client_socket.sendall(message.encode("utf-8"))

    data = client_socket.recv(1024)
    print(f'получен ответ от сервера{data.decode("UTF-8")}')

finally:
    client_socket.close()



