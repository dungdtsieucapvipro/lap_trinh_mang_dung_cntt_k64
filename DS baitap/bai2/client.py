import socket

#! Bài 2: Client gửi khoảng a và b để server tìm tất cả các số có tổng các chữ số = 15 trong khoảng từ a đến b

#! TCP - Tuần tự Client
def tcp_sequential_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12380))
    
    a = int(input("Nhập số nguyên a: "))
    b = int(input("Nhập số nguyên b: "))
    client_socket.send(f"{a} {b}".encode())

    data = client_socket.recv(1024).decode()
    print(f"Các số có tổng các chữ số bằng 15 trong khoảng từ {a} đến {b} là: {data}")
    client_socket.close()

#! TCP - Song Song Client
def tcp_parallel_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12381))
    
    a = int(input("Nhập số nguyên a: "))
    b = int(input("Nhập số nguyên b: "))
    client_socket.send(f"{a} {b}".encode())

    data = client_socket.recv(1024).decode()
    print(f"Các số có tổng các chữ số bằng 15 trong khoảng từ {a} đến {b} là: {data}")
    client_socket.close()

#! UDP - Tuần tự Client
def udp_sequential_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    a = int(input("Nhập số nguyên a: "))
    b = int(input("Nhập số nguyên b: "))
    client_socket.sendto(f"{a} {b}".encode(), ("127.0.0.1", 12382))
    
    data, _ = client_socket.recvfrom(1024)
    print(f"Các số có tổng các chữ số bằng 15 trong khoảng từ {a} đến {b} là: {data.decode()}")
    client_socket.close()

#! UDP - Song Song Client
def udp_parallel_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    a = int(input("Nhập số nguyên a: "))
    b = int(input("Nhập số nguyên b: "))
    client_socket.sendto(f"{a} {b}".encode(), ("127.0.0.1", 12383))
    
    data, _ = client_socket.recvfrom(1024)
    print(f"Các số có tổng các chữ số bằng 15 trong khoảng từ {a} đến {b} là: {data.decode()}")
    client_socket.close()

#! Main function to choose the client mode
def main():
    choice = input("Chọn chế độ client (1: TCP tuần tự, 2: TCP song song, 3: UDP tuần tự, 4: UDP song song): ")
    if choice == '1':
        tcp_sequential_client()
    elif choice == '2':
        tcp_parallel_client()
    elif choice == '3':
        udp_sequential_client()
    elif choice == '4':
        udp_parallel_client()
    else:
        print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
