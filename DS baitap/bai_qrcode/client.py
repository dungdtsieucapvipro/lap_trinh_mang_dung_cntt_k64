import socket
from PIL import Image
from io import BytesIO

# Thông tin kết nối server
HOST = '127.0.0.1'  # Địa chỉ IP server
PORT = 12345        # Cổng giao tiếp

# Kết nối đến server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Gửi dữ liệu
data_to_send = input("Enter text or URL to generate QR code: ")
client.send(data_to_send.encode('utf-8'))

# Nhận kích thước dữ liệu từ server
data_size = int.from_bytes(client.recv(4), 'big')
print(f"Expecting {data_size} bytes of data...")

# Nhận ảnh QR từ server
img_data = b""
while len(img_data) < data_size:
    packet = client.recv(1024)
    if not packet:
        break
    img_data += packet

# Hiển thị ảnh mã QR
if img_data:
    img = Image.open(BytesIO(img_data))
    img.show()
else:
    print("No data received!")

# Đóng kết nối
client.close()
