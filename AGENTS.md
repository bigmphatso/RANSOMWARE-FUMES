# AGENTS.md

Guidance for coding agents working in this repository.

## Project Overview

This repository is an assignment/lab project about ransomware behavior. It contains Python scripts that demonstrate file encryption, file restoration, ransom-note generation, and one unrecoverable destructive routine. Treat all code here as controlled educational material only.

Main files:

- `ware.inf0.txt` - brief project description.
- `Dev Files/fumes/recoverable/fumes_e.py` - Fernet-based encryption demo that writes `.locked` files and ransom notes.
- `Dev Files/fumes/recoverable/fumes_d.py` - paired decryption demo that restores `.locked` files using `key.txt`.
- `Dev Files/fumes/recoverable/fumes.v1.py` - earlier in-place encryption version.
- `Dev Files/fumes/recoverable/*.txt` - procedural notes for encryption and decryption.
- `Dev Files/fumes/unrecoverable/fumes.py` - destructive demo that overwrites file contents and deletes itself.
- `Test Folder/Test/` - sample target files for local lab testing.

## Safety Rules

- Do not run any ransomware script against real user data.
- Do not run `Dev Files/fumes/unrecoverable/fumes.py` unless the user explicitly asks and confirms they understand it destroys files. Prefer not to run it at all.
- Do not make the destructive or ransom functionality more operational, stealthy, portable, evasive, or deployable.
- Keep all examples constrained to disposable test folders inside this repository.
- Do not add real payment addresses, real contact details, persistence, privilege escalation, obfuscation, spreading behavior, or external command-and-control behavior.
- If modifying scripts, prefer transforming them into harmless simulations: dry-run mode, manifest output, copy-based fixtures, explicit confirmation prompts, and clear educational labeling.

## Development Notes

- Python is the only application language currently present.
- The recoverable scripts require `cryptography` for `Fernet`.
- There is no package metadata, virtual environment definition, or test runner configuration yet.
- Existing paths are Windows-style hard-coded strings such as `Ransomwares\Test Folder\Test`; they do not match the current Linux workspace layout.
- The repository currently has no root `.gitignore`.

## Recommended Improvements

- Add a `requirements.txt` with `cryptography`.
- Replace hard-coded target paths with CLI arguments that only accept paths under a known lab directory.
- Add a mandatory dry-run default and require an explicit flag for write operations.
- Add path validation to prevent accidental traversal outside `Test Folder/Test`.
- Write keys and generated notes into a dedicated lab output directory, not the project root.
- Add tests around file selection, skip rules, encryption/decryption round trips, and note generation.
- Replace realistic ransom language with clearly marked educational text.
- Remove or quarantine the unrecoverable script, or rewrite it as a non-destructive simulator.

## Working Practices

- Before editing, inspect the relevant file and preserve unrelated user changes.
- Use `rg`/`rg --files` for repo searches.
- Use `apply_patch` for manual edits.
- Keep changes small and scoped to the user's request.
- When reviewing, lead with safety and data-loss risks.
- When reporting line references, use current line numbers from `nl -ba`.

## Verification

For safe changes, prefer these checks:

- Static syntax check: `python -m py_compile <file.py>`
- Unit tests if a test suite is added.
- Dry-run output against files under `Test Folder/Test`.

Avoid verification steps that encrypt, overwrite, delete, or rename user files unless the user explicitly authorizes a disposable fixture run.
