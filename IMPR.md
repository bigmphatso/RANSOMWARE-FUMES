# Improvement Suggestions

This project should stay an educational, controlled lab. Improvements should reduce accidental harm, make behavior easier to understand, and improve recovery/testing rather than making the ransomware behavior more operational.

## Safety First

- Remove or quarantine `Dev Files/fumes/unrecoverable/fumes.py`.
- If it must remain, rewrite it as a non-destructive simulator that only logs what it would do.
- Make dry-run mode the default for all scripts.
- Require an explicit flag such as `--write` before any script can rename, delete, encrypt, decrypt, or overwrite files.
- Add a clear confirmation prompt before write operations.
- Prevent scripts from operating outside the repository's `Test Folder`.
- Replace realistic ransom language with clearly marked educational/demo wording.
- Do not add real payment addresses, real contact details, persistence, spreading behavior, stealth, obfuscation, or external network behavior.

## Path Handling

- Avoid absolute machine-specific paths.
- Derive lab paths from the repository root.
- Validate resolved target paths before processing files.
- Refuse to run if the target path is missing, is outside the repo, or is not under `Test Folder`.
- Keep generated files such as notes, manifests, and keys in a predictable lab output location.

## Data Protection

- Do not delete originals until encrypted output has been fully written and verified.
- Avoid overwriting restored files during decryption; check whether the destination already exists.
- Write a manifest of affected files before modifying anything.
- Keep backups or copies of fixtures before any destructive lab run.
- Add clear failure handling for partial writes, missing keys, invalid keys, and permission errors.

## Code Structure

- Split shared constants and path helpers into a common module.
- Replace duplicated file-walking logic with a reusable helper.
- Add command-line arguments for target path, dry-run/write mode, and output paths.
- Use `pathlib.Path` consistently instead of mixing raw strings and `os.path`.
- Remove unused imports.
- Keep function names honest: avoid names like `_encrypt_file` for routines that destroy data.

## Dependencies And Setup

- Add `requirements.txt` with `cryptography`.
- Add a short setup section in `README.md`.
- Add a root `.gitignore` that excludes generated files such as `key.txt`, `READ_ME.html`, `.locked` files, caches, and virtual environments.
- Document that scripts must only be run against disposable test fixtures.

## Testing

- Add unit tests for file selection and skip rules.
- Add tests for path validation.
- Add encryption/decryption round-trip tests using temporary fixture files.
- Add tests to confirm dry-run mode does not modify files.
- Add tests for decryption collision handling when the restored filename already exists.
- Add tests for missing or invalid `key.txt`.

## Documentation

- Add a project `README.md` explaining the educational purpose, safe usage, and risks.
- Document the difference between recoverable encryption and unrecoverable destruction.
- Include a warning that the unrecoverable version destroys file contents permanently.
- Explain where keys, notes, and modified files are written.
- Keep `AGENTS.md` updated when project conventions change.

## Suggested Priority

1. Quarantine or disable the unrecoverable script.
2. Add dry-run mode and path validation.
3. Add `.gitignore` and `requirements.txt`.
4. Add tests around path safety and dry-run behavior.
5. Refactor shared path/file-walking logic.
6. Improve documentation and remove realistic ransom wording.
