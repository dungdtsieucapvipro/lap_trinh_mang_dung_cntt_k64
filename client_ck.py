import socket

# Tạo socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Kết nối đến server
client_socket.connect(('localhost', 65432))

# Gửi mã chứng khoán
stock_symbol = input('Nhập mã chứng khoán: ')
client_socket.sendall(stock_symbol.encode())

# Nhận kết quả từ server
data = client_socket.recv(4096).decode()
print('Thông tin mã chứng khoán:')
print(data)

# Đóng kết nối
client_socket.close()
