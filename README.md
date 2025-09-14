# Phase 1: Hello World + Project Setup

## What Changed

- Created Python virtual environment
- Added `requirements.txt` with core dependencies (TensorFlow, NumPy, Gradio)
- Created hello world `app.py` to verify everything works
- Added `.gitignore` after nearly pushing 600MB of venv to Git

## Virtual Environment Setup

**Requires Python 3.9.** I ran `python3 --version` on my Mac and got 3.9.6, which is the system Python that came with macOS. TensorFlow 2.15 doesn't support Python 3.12+, so if you've got a newer Python you'll need to install an older one.

If you're on macOS and only have Python 3.12, you can install an older version with `brew install python@3.11` and then use `python3.11 -m venv venv` instead.

The command `python3 -m venv venv` basically keeps all the packages separate from your main Python stuff. The first `venv` is the module name, second is the folder name. I had to Google "how to create python virtual environment" because I'd never done this before. Activating with `source venv/bin/activate` puts `(venv)` in the terminal prompt so you know it's working. On Windows the activation command would be different but I'm on macOS so using the Unix version.

First time I ran the activate command I was in the wrong directory and got "no such file or directory". Wasted a few minutes before I realised I needed to `cd` into the project folder first. Obvious but yeah.

## Dependencies

Listed everything in `requirements.txt`, one package per line with `==` to lock the versions:

- `tensorflow==2.15.0` (neural networks)
- `numpy` (array operations)
- `gradio==4.36.1` for the web UI (needed in later phases)

`pip install -r requirements.txt` took ages - TensorFlow alone installed 200+ sub-packages. Went and made tea while it ran. Got a few warnings about pip being outdated but the install worked fine. The venv folder ended up at about 600MB, which I wasn't expecting at all from three packages.

## The Hello World Script

```python
def main():
    """Print welcome message to verify setup works."""
    print("Welcome to MNIST Digit Recognition!")
    print("Project initialised successfully.")
```

Two print statements, just enough to confirm Python and the dependencies are working. I used a docstring (triple quotes) rather than a `#` comment because I looked it up and docstrings show up in `help()`, which is the proper way to do it for functions. Regular `#` comments are for inline notes.

One thing that caught me out: running `python app.py` outside the venv gave errors about Python 2 vs 3. Had to use `python3 app.py` explicitly. Inside the activated venv, both `python` and `python3` work, but outside you need `python3` on macOS. Tripped me up for a few minutes before I checked which Python was actually running.

## The .gitignore

Nearly pushed the 600MB venv folder to Git before realising that would be a terrible idea. The venv has every installed package and its compiled files, which are specific to your machine and shouldn't be shared. Created `.gitignore` to exclude `venv/`, `__pycache__/`, `.DS_Store`, and the `.keras` cache folder. Should've done this first really - don't want to be pushing hundreds of megabytes to a repo. Anyone cloning can just recreate the venv from `requirements.txt`, which is the whole point of having that file.

## Why I Did It This Way

### Hiding That Annoying Warning

```python
import warnings
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')
```

This warning kept showing up every time I ran the script because macOS uses LibreSSL instead of OpenSSL, and something in TensorFlow's dependencies doesn't like that. It doesn't actually cause any problems though. Everything still works fine. I used the `message=` bit so it only hides this one specific warning instead of hiding all warnings, because I didn't want to accidentally miss a real problem.

### The `if __name__ == "__main__":` Thing

```python
if __name__ == "__main__":
    main()
```

This just stops `main()` from running if the file gets imported somewhere else. Without it, importing this file would automatically run the hello world message, which would be annoying. I'll be importing between files in later phases so it's good to have this from the start.

### Version Numbers in requirements.txt

I set exact version numbers with `==` so nothing breaks later if a package gets updated. The alternative is `>=` which would let newer versions in, but then stuff might break. Playing it safe for now.

## Project Files

```
gradio_phase1/
├── app.py              # Main script (12 lines)
├── requirements.txt    # Dependencies (3 lines)
├── .gitignore          # Excludes venv/, __pycache__/, .DS_Store
├── README.md           # This file
└── diary.md            # Development journal
```

All files created in this phase. No subdirectories yet, keeping the structure flat for now.

## How to Run

**Requires Python 3.9.**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Expected output:**
```
Welcome to MNIST Digit Recognition!
Project initialised successfully.
```

