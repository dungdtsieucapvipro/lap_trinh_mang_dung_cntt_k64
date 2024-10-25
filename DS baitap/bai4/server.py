import socket
import threading

# Bài 4: Server xử lý tìm số lớn nhất từ dãy số thực do client gửi

def find_max(numbers):
    return max(numbers)

#! TCP - Tuần tự Server
def tcp_sequential_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12376))
    server_socket.listen(5)
    print("TCP Tuần tự Server đang lắng nghe trên cổng 12376...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Kết nối từ {client_address} đã được thiết lập.")
        data = client_socket.recv(1024).decode()
        numbers = list(map(float, data.split()))

        max_number = find_max(numbers)
        response = str(max_number)

        client_socket.send(response.encode())
        client_socket.close()

#! TCP - Song Song Server
def tcp_parallel_server():
    def handle_client(client_socket, client_address):
        print(f"Kết nối từ {client_address} đã được thiết lập.")
        data = client_socket.recv(1024).decode()
        numbers = list(map(float, data.split()))

        max_number = find_max(numbers)
        response = str(max_number)

        client_socket.send(response.encode())
        client_socket.close()
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12377))
    server_socket.listen(5)
    print("TCP Song Song Server đang lắng nghe trên cổng 12377...")

    while True:
        client_socket, client_address = server_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

#! UDP - Tuần tự Server
def udp_sequential_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("127.0.0.1", 12378))
    print("UDP Tuần tự Server đang lắng nghe trên cổng 12378...")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        numbers = list(map(float, data.decode().split()))

        max_number = find_max(numbers)
        response = str(max_number)

        server_socket.sendto(response.encode(), client_address)

#! UDP - Song Song Server
def udp_parallel_server():
    def handle_client(data, client_address, server_socket):
        print(f"Kết nối từ {client_address} đã được thiết lập.")
        numbers = list(map(float, data.decode().split()))

        max_number = find_max(numbers)
        response = str(max_number)

        server_socket.sendto(response.encode(), client_address)
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("127.0.0.1", 12379))
    print("UDP Song Song Server đang lắng nghe trên cổng 12379...")

    while True:
        data, client_address = server_socket.recvfrom(1024)
        client_handler = threading.Thread(target=handle_client, args=(data, client_address, server_socket))
        client_handler.start()

#! Main function to call different servers
def main():
    choice = input("Chọn chế độ server (1: TCP tuần tự, 2: TCP song song, 3: UDP tuần tự, 4: UDP song song): ")
    if choice == '1':
        tcp_sequential_server()
    elif choice == '2':
        tcp_parallel_server()
    elif choice == '3':
        udp_sequential_server()
    elif choice == '4':
        udp_parallel_server()
    else:
        print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
