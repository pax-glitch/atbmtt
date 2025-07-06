import os
import base64
import json
from flask import flash, redirect
from datetime import datetime
from Crypto.Cipher import DES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA512

def pad(data):
    return data + b' ' * (8 - len(data) % 8)

def send(request):
    file = request.files['file']
    receiver_pubkey_file = request.files['receiver_pubkey']
    if not file or not receiver_pubkey_file:
        flash("❌ Thiếu file hoặc khóa công khai người nhận", "danger")
        return redirect('/sender')

    filename = file.filename
    content = file.read()
    receiver_pubkey = RSA.import_key(receiver_pubkey_file.read())
    sender_privkey = RSA.import_key(open("keys/sender_private.pem").read())

    # Tạo Session Key
    session_key = get_random_bytes(8)
    encrypted_session_key = PKCS1_v1_5.new(receiver_pubkey).encrypt(session_key)

    # Ký metadata
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    metadata = f"{filename}|{timestamp}|3".encode()
    metadata_hash = SHA512.new(metadata)
    metadata_sig = pkcs1_15.new(sender_privkey).sign(metadata_hash)

    # Chia file
    part_size = len(content) // 3
    parts = [content[i*part_size:(i+1)*part_size] for i in range(3)]
    parts[2] += content[3*part_size:]

    packets = []
    for part in parts:
        iv = get_random_bytes(8)
        des_cipher = DES.new(session_key, DES.MODE_CBC, iv)
        ciphertext = des_cipher.encrypt(pad(part))
        sha = SHA512.new(iv + ciphertext)
        signature = pkcs1_15.new(sender_privkey).sign(sha)

        packets.append({
            "iv": base64.b64encode(iv).decode(),
            "cipher": base64.b64encode(ciphertext).decode(),
            "hash": sha.hexdigest(),
            "sig": base64.b64encode(signature).decode()
        })

    packet_json = {
        "filename": filename,
        "timestamp": timestamp,
        "enc_session_key": base64.b64encode(encrypted_session_key).decode(),
        "metadata_sig": base64.b64encode(metadata_sig).decode(),
        "packets": packets
    }

    # Ghi vào file
    output_path = os.path.join("sent", "packet.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(packet_json, f, indent=2)

    flash("✅ Gửi file thành công! Đã lưu gói tin tại sent/packet.json", "success")
    return redirect('/sender')
