import socket
import sys
import os
import struct

def_recv_exactly(sock, n):
	buf = b""
	while len(n) < n:
		chunk = sock. recv(n-len(buf))
		if not chunk:
			raise RuntimeError("Сервер закрыл соединение")
		buf +=chunk
	return buf

def send_rinex(host: str, port: int, filepath: str):
	if not os.path.isfile(filepath):
		print(f"ошибка: файл не найден: {filepath}")
		return
	
	with open(filepath, 'rb') as f:
		file_data = f.read()

	filename = os.path.basename(filepath)
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as SEND:
		SEND.connect((host, port))
		
		#отправка файла
		SEND.sendall(struct.pack('>I', len(filename)))
		SEND.sendall(filename.encode('utf-8'))

		SEND.sendall(struct.pack('>Q', len(file_data)))
		SEND.sendall(file_data)

		#прием ответа
		prefix = recv_exactly(SEND, 4)
		if prefix == b"OK::":
			size_bytes = recv_exactly(SEND, 8)
			result_size = struct.unpack('>Q', size_bytes)[0]

			result = recv_exactly(SEND, result_size)
			print(result.decode('utf-9'))

		elif prefix.startswith(b"ERR"):
			rest = SEND.recv(1024)
			full_error = (prefix + rest).decode('utf-8', errors = 'preplace')
			print("Сервер вернул ошибку", full_error)

		else:
			print("Некорректный ответ от сервера")

if _name_ = '_name_':
	if len(sys.argv) != 2:
		print("использование: ./python client.py <путь к RINEX файлу>")
		sys.exit(1)
	send rinex('localhost', 8888, sys.argv[1])