import socket
import ssl
import threading

# Thông tin server
server_address = ('localhost', 12345)

def receive_data(ssl_socket):
    try:
        while True:
            data = ssl_socket.recv(1024)
            if not data:
                break
            print("\nNhận:", data.decode('utf-8')) # Added newline for better display with input prompt
    except Exception as e:
        print(f"\nLỗi khi nhận dữ liệu: {e}")
    finally:
        ssl_socket.close()
        print("Kết nối đã đóng.")

# Tạo socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tạo SSL context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT) # Changed to PROTOCOL_TLS_CLIENT
context.verify_mode = ssl.CERT_NONE  # Change this according to your needs (for self-signed certs, CERT_NONE is often used)
context.check_hostname = False # Change this according to your needs (for localhost or self-signed, often False)

# Thiết lập kết nối SSL
# For client, server_hostname should match the CN in the server's certificate
ssl_socket = context.wrap_socket(client_socket, server_hostname='localhost')

try:
    ssl_socket.connect(server_address)
    print("Đã kết nối tới server.")

    # Bắt đầu một luồng để nhận dữ liệu từ server
    receive_thread = threading.Thread(target=receive_data, args=(ssl_socket,))
    receive_thread.daemon = True # Allow main thread to exit even if this thread is running
    receive_thread.start()

    # Gửi dữ liệu lên server
    while True:
        message = input("Nhập tin nhắn: ")
        ssl_socket.send(message.encode('utf-8'))

except KeyboardInterrupt:
    print("\nĐã ngắt kết nối bởi người dùng.")
except Exception as e:
    print(f"Lỗi kết nối: {e}")
finally:
    ssl_socket.close() # Ensure socket is closed on exit