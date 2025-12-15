import socket
import struct
import sys
import os


def recv_exactly(sock, n):
    """Читает ровно n байт из сокета. Блокирует, пока не получит все."""
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise RuntimeError("Сервер закрыл соединение")
        buf += chunk
    return buf


def send_two_rinex(host: str, port: int, base_file: str, rover_file: str):
    # Исправление 1: Проверяем оба файла
    if not os.path.isfile(base_file):
        print(f"Ошибка: файл не найден — {base_file}")
        return
    if not os.path.isfile(rover_file):
        print(f"Ошибка: файл не найден — {rover_file}")
        return

    # Исправление 2: Читаем оба файла
    with open(base_file, 'rb') as f:
        base_data = f.read()
    base_filename = os.path.basename(base_file)

    with open(rover_file, 'rb') as f:
        rover_data = f.read()
    rover_filename = os.path.basename(rover_file)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # --- Отправка базового файла ---
        s.sendall(struct.pack('>I', len(base_filename)))
        s.sendall(base_filename.encode('utf-8'))
        s.sendall(struct.pack('>Q', len(base_data)))
        s.sendall(base_data)

        # --- Отправка файла ровера ---
        s.sendall(struct.pack('>I', len(rover_filename)))
        s.sendall(rover_filename.encode('utf-8'))
        s.sendall(struct.pack('>Q', len(rover_data)))
        s.sendall(rover_data)

        # --- Приём ответа ---
        prefix = recv_exactly(s, 4)

        if prefix == b"OK::":
            size_bytes = recv_exactly(s, 8)
            result_size = struct.unpack('>Q', size_bytes)[0]
            result = recv_exactly(s, result_size)
            print("\n=== Результат обработки ===")
            print(result.decode('utf-8'))

        elif prefix.startswith(b"ERR"):
            rest = s.recv(1024)
            full_error = (prefix + rest).decode('utf-8', errors='replace')
            print("Сервер вернул ошибку:", full_error)

        else:
            print("Некорректный ответ от сервера:", repr(prefix))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Использование: python client.py <base.obs> <rover.obs>")
        sys.exit(1)
    send_two_rinex('192.168.1.215', 9999, sys.argv[1], sys.argv[2])