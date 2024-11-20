import socket
from PIL import Image
from io import BytesIO

HOST = '127.0.0.1'  
PORT = 12345     

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

data_to_send = input("Enter text or URL to generate QR code: ")
client.send(data_to_send.encode('utf-8'))

data_size = int.from_bytes(client.recv(4), 'big')
print(f"Expecting {data_size} bytes of data...")

img_data = b""
while len(img_data) < data_size:
    packet = client.recv(1024)
    if not packet:
        break
    img_data += packet

if img_data:
    img = Image.open(BytesIO(img_data))
    img.show()
else:
    print("No data received!")

client.close()
