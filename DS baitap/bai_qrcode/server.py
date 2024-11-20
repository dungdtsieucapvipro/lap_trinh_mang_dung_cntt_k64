import socket
import qrcode
from io import BytesIO

HOST = '127.0.0.1'  
PORT = 12345        

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Server is listening on {HOST}:{PORT}...")

while True:
    conn, addr = server.accept()
    print(f"Connected by {addr}")
    try:
        
        data = conn.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"Received data: {data}")

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        
        conn.send(len(img_io.getvalue()).to_bytes(4, 'big'))
        
        conn.sendall(img_io.getvalue())
        print("QR code sent!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
