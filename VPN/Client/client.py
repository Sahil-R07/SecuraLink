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

def client():
    host = '127.0.0.1'
    port = 65432
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    while True:
        message = input("Enter message to send: ")
        encrypted_message = encrypt_message(message)
        s.send(encrypted_message.encode())

        response = s.recv(1024)
        print(f"Received from server: {decrypt_message(response.decode())}")

if __name__ == "__main__":
    iv = b'1234567890123456'  # Initialization vector
    client()
