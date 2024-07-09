import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# Encryption settings
key = b'Sixteen byte key'  # Must be 16, 24, or 32 bytes long
cipher = AES.new(key, AES.MODE_CBC)

def encrypt_message(message):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(message.encode(), AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return base64.b64encode(cipher.iv + encrypted_message).decode()

def decrypt_message(encrypted_message):
    encrypted_message = base64.b64decode(encrypted_message)
    iv = encrypted_message[:16]
    encrypted_message = encrypted_message[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size)
    return decrypted_message.decode()

def server():
    host = '0.0.0.0'
    port = 65432
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()

    print("Server listening...")

    conn, addr = s.accept()
    print(f"Connected by {addr}")

    while True:
        encrypted_data = conn.recv(1024)
        if not encrypted_data:
            break
        decrypted_data = decrypt_message(encrypted_data.decode())
        print(f"Received: {decrypted_data}")
        response = encrypt_message(f"Echo: {decrypted_data}")
        conn.send(response.encode())

    conn.close()

if __name__ == "__main__":
    iv = b'1234567890123456'  # Initialization vector
    server()
