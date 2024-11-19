import socket
import qrcode
from io import BytesIO

# Khởi tạo server
HOST = '127.0.0.1'  # Địa chỉ IP server
PORT = 12345        # Cổng giao tiếp

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Server is listening on {HOST}:{PORT}...")

while True:
    conn, addr = server.accept()
    print(f"Connected by {addr}")
    try:
        # Nhận dữ liệu từ client
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"Received data: {data}")
        
        # Tạo mã QR
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Lưu QR vào BytesIO
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        # Gửi kích thước dữ liệu trước
        conn.send(len(img_io.getvalue()).to_bytes(4, 'big'))
        
        # Gửi ảnh mã QR
        conn.sendall(img_io.getvalue())
        print("QR code sent!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
