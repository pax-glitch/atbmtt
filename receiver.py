import os
import json
import base64
from flask import flash, redirect
from datetime import datetime
from Crypto.Cipher import DES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA512
from Crypto.Signature import pkcs1_15

def unpad(data):
    return data.rstrip(b' ')

def send_ack(message):
    ack = {
        "status": "ACK",
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open("responses/ack.json", "w", encoding="utf-8") as f:
        json.dump(ack, f, indent=2, ensure_ascii=False)
    flash("✅ " + message, "success")
    return redirect('/receiver')

def send_nack(message):
    nack = {
        "status": "NACK",
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open("responses/nack.json", "w", encoding="utf-8") as f:
        json.dump(nack, f, indent=2, ensure_ascii=False)
    flash("❌ " + message, "danger")
    return redirect('/receiver')

def receive(request):
    try:
        uploaded_packet = request.files['packet']
        sender_pubkey_file = request.files['sender_pubkey']
        receiver_privkey_file = request.files['receiver_privkey']

        if not uploaded_packet or not sender_pubkey_file or not receiver_privkey_file:
            return send_nack("Thiếu file packet hoặc khóa")

        packet_data = json.load(uploaded_packet)

        # Đọc khóa
        sender_pubkey = RSA.import_key(sender_pubkey_file.read())
        receiver_privkey = RSA.import_key(receiver_privkey_file.read())

        # Giải mã session key
        enc_session_key = base64.b64decode(packet_data['enc_session_key'])
        rsa_cipher = PKCS1_v1_5.new(receiver_privkey)
        session_key = rsa_cipher.decrypt(enc_session_key, None)
        if not session_key:
            return send_nack("Không giải mã được Session Key - Có thể sai khóa")

        # Kiểm tra chữ ký metadata
        metadata = f"{packet_data['filename']}|{packet_data['timestamp']}|{len(packet_data['packets'])}".encode()
        metadata_hash = SHA512.new(metadata)
        metadata_sig = base64.b64decode(packet_data['metadata_sig'])
        try:
            pkcs1_15.new(sender_pubkey).verify(metadata_hash, metadata_sig)
        except (ValueError, TypeError):
            return send_nack("Không xác minh được chữ ký metadata")

        # Giải mã từng phần
        decrypted_parts = []
        for i, pkt in enumerate(packet_data['packets']):
            try:
                iv = base64.b64decode(pkt["iv"])
                cipher = base64.b64decode(pkt["cipher"])
                sig = base64.b64decode(pkt["sig"])
                hash_hex = pkt["hash"]

                # Kiểm tra hash
                sha = SHA512.new(iv + cipher)
                if sha.hexdigest() != hash_hex:
                    return send_nack(f"Phần {i+1}: Hash không khớp - Dữ liệu bị thay đổi")

                # Kiểm tra chữ ký
                try:
                    pkcs1_15.new(sender_pubkey).verify(sha, sig)
                except (ValueError, TypeError):
                    return send_nack(f"Phần {i+1}: Sai chữ ký số")

                # Giải mã
                cipher_des = DES.new(session_key, DES.MODE_CBC, iv)
                plain = unpad(cipher_des.decrypt(cipher))
                decrypted_parts.append(plain)

            except Exception as e:
                return send_nack(f"Phần {i+1}: Lỗi xử lý: {str(e)}")

        # Ghép và lưu file
        output_path = os.path.join("received", "assignment.txt")
        with open(output_path, "wb") as f:
            for part in decrypted_parts:
                f.write(part)

        return send_ack("Nhận và giải mã file thành công! Đã lưu assignment.txt")

    except Exception as e:
        return send_nack("Lỗi toàn cục: " + str(e))
