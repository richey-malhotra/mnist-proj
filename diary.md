# Phase 1 Development Diary

## Session Goal

Get the project set up from scratch. Virtual environment, install packages, and make sure everything actually runs. Just a simple hello world to prove Python and the dependencies work.

## Setting Up the Virtual Environment

Googled how to set up a virtual environment since I'd never done one. It basically keeps all the packages in their own folder so they don't mess with system Python.

Command is `python3 -m venv venv`. The first `venv` is the module name, second is what I'm calling the folder. A bit confusing but that's what everyone seems to call it. Important thing is the Python version. I checked mine - `python3 --version` shows 3.9.6, which is the system Python that came with my Mac. TensorFlow 2.15 doesn't work with 3.12 or newer, which I found out from the TensorFlow docs. Lucky my Mac already had 3.9 or I'd have been messing around trying to install an older Python.

After creating it, nothing happened. Turns out you have to "activate" it with `source venv/bin/activate`, then the terminal shows `(venv)` at the start of the prompt. That's how you know it's working. On Windows it would be different but I'm on macOS so using the Unix version.

## Installing Dependencies

Needed to figure out what packages to install. For this project I need TensorFlow (neural networks), NumPy (array operations), and Gradio (web interface). Listed them in `requirements.txt`, one per line. You can specify versions with `==` to lock them.

Ran `pip install -r requirements.txt` and it took AGES. TensorFlow especially. It downloaded something like 200+ packages. Left it installing for a bit. Got a few warnings about pip being outdated but the install worked fine.

## Hello World

Created `app.py` with just a main function that prints a welcome message and confirms the project initialised. See the README for the actual code. It's literally two print statements. First tried `python app.py` but got an error about Python 2 vs 3. Had to use `python3 app.py` instead. Later found out in the venv it doesn't matter (both work) but outside it you need python3 on macOS.

## Problems I Hit

First time I tried `source venv/bin/activate` I was in the wrong directory. Got "no such file or directory". Obvious in hindsight but wasted a few minutes.

Also wasn't sure if the docstring at the top of `app.py` needed triple quotes or could be a comment. Googled it and found that triple quotes are for docstrings, `#` for comments. Docstrings are better because they show up in `help()`.

The big surprise was the venv folder size. After installing everything it was like 600MB. I nearly pushed it to Git before realising that would be a terrible idea. Created a `.gitignore` file to exclude the `venv/` directory, plus `__pycache__/` and the `.keras` cache folder. Should've done that first really. Don't want to be pushing hundreds of megabytes to a repo.

## Testing

Created the venv, activated it, installed requirements, ran the script. All worked after I sorted the directory thing. Output was exactly what I expected: welcome message and confirmation line.

## What I Learned

Virtual environments keep dependencies separate, which makes sense - if I need different TensorFlow versions for different projects they won't conflict. The `requirements.txt` format is pretty simple, just package names and optional versions, so someone else can replicate the setup easily. Starting with hello world before adding complexity is way less overwhelming than trying to do everything at once.

Not sure why TensorFlow needs that many sub-dependencies, counted over 200 packages. Probably has to do with all the different operations it supports but seems like a lot. Also wondering if I really need exact versions in requirements.txt or if `>=` would be fine. Playing it safe for now.

## Reflection

Simpler than I expected. Main challenge was the venv commands. The install took a while but that's just waiting. Good to have something working before adding more stuff - Phase 2 will load the actual MNIST data which should be more interesting.

About an hour all in, maybe a bit over because I'd never done the venv thing before. Would be faster next time.

## Notes for Next Phase

Phase 2 needs to load MNIST data. From a quick Google, Keras has it built in with `tensorflow.keras.datasets.mnist.load_data()`. Should be straightforward. Will need to understand the shape of the data, like how many images, what dimensions, what the labels look like.
