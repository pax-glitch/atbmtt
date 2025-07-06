from Crypto.PublicKey import RSA
import os

os.makedirs("keys", exist_ok=True)

def generate_keypair(name):
    key = RSA.generate(1024)
    with open(f"keys/{name}_private.pem", "wb") as f:
        f.write(key.export_key())
    with open(f"keys/{name}_public.pem", "wb") as f:
        f.write(key.publickey().export_key())

generate_keypair("sender")
generate_keypair("receiver")
print("✅ Đã tạo 4 khóa trong thư mục 'keys/'")
