import os
from pathlib import Path
from cryptography.fernet import Fernet

# ── CONFIG ────────────────────────────────────────────
REPO_ROOT        = Path(__file__).resolve().parents[3]
TARGET_DIR       = REPO_ROOT / "Test Folder"
KEY_FILE         = "key.txt"
LOCKED_EXTENSION = ".locked"
NOTE_FILENAME    = "READ_ME.html"   # optional to delete afterward

# ── STEP 1: Load the Fernet key ───────────────────────
def load_key():
    with open(KEY_FILE, "rb") as f:
        return f.read()

# ── STEP 2: Decrypt one file and restore its name ─────
def decrypt_file(path, fernet):
    with open(path, "rb") as f:
        encrypted_data = f.read()
    try:
        data = fernet.decrypt(encrypted_data)
    except Exception as e:
        print(f"[!] Failed to decrypt {path}: {e}")
        return

    # Restore original filename (strip .locked)
    original_path = path[:-len(LOCKED_EXTENSION)]
    with open(original_path, "wb") as f:
        f.write(data)
    os.remove(path)
    print(f"[+] Decrypted: {original_path}")

# ── STEP 3: Walk & decrypt every .locked file ─────────
def decrypt_tree(root_dir, fernet):
    for curr_dir, _, files in os.walk(root_dir):
        for fname in files:
            if not fname.endswith(LOCKED_EXTENSION):
                continue

            full_path = os.path.join(curr_dir, fname)
            decrypt_file(full_path, fernet)

        # Optional: remove ransom note after decryption
        note_path = os.path.join(curr_dir, NOTE_FILENAME)
        if os.path.exists(note_path):
            try:
                os.remove(note_path)
                print(f"[+] Removed note: {note_path}")
            except:
                pass

# ── MAIN ───────────────────────────────────────────────
def main():
    key = load_key()
    fernet = Fernet(key)
    decrypt_tree(TARGET_DIR, fernet)
    print("\n✅ All done! Your files should be restored.")

if __name__ == "__main__":
    main()
