# Phase 6: Hello World Gradio Interface

## What Changed

- Created first web interface using Gradio
- Simple text demo: name input, greeting output
- New file `app_ui.py`, where all UI code lives from now on
- Gradio builds HTML/CSS/JavaScript automatically from Python

Phase 5 had predictions working from the command line, but running a script, seeing five results, and editing code to test again isn't user-friendly. Wanted a web page where someone could interact with the model properly.

## Installing Gradio

Gradio was in requirements.txt from Phase 1 but I'd never actually installed it because earlier phases didn't need it. Running app_ui.py gave `ModuleNotFoundError: No module named 'gradio'`, so I ran `pip install -r requirements.txt` again and it pulled down about 30 extra packages (FastAPI, Uvicorn, Hugging Face Hub, loads of unexpected stuff). But then when I tried to run my app I got `ImportError: cannot import name 'HfFolder' from 'huggingface_hub'`. Took me a while to figure out - turns out pip installed `huggingface_hub` version 1.0, which removed something called `HfFolder` that Gradio 4.36.1 still needs. Had to add `huggingface_hub<1.0` to requirements.txt to force pip to install an older version. Annoying that a package I never even asked for can break everything.

## The Hello World

Didn't want to jump straight to image classification without knowing Gradio works. Started with the simplest possible thing, a function that takes a name and returns a greeting:

```python
demo = gr.Interface(
    fn=greet,
    inputs=gr.Textbox(label="Your Name"),
    outputs=gr.Textbox(label="Greeting"),
    title="MNIST Digit Recognition - Hello World"
)
demo.launch()
```

The whole pattern is: user enters something, Gradio calls your function, displays whatever it returns. I initially thought the function would need special decorators or something, but it's just a regular Python function. Gradio sorts out all the web stuff for you.

When it worked, I was surprised how clean it looked. Professional layout with labelled boxes, a submit button, all from about ten lines of Python.

## Testing

Interface loads on localhost:7860. Typed "Harpreet", got the greeting back. Tested empty input - validation message works. Also tested refreshing the page mid-session and everything resets cleanly, nothing left over from before.

One minor annoyance: restarting immediately after Ctrl+C gave "Address already in use" because the port hadn't freed up. Just had to wait ~10 seconds or kill the process. Later learned you can pass `server_port=7861` to use a different port, but for now the wait wasn't a big deal.

## How It Works

### Why Gradio?

I looked at Flask and Django but they seemed like way too much work because you'd have to build the whole UI yourself with HTML and JavaScript. Streamlit was another option but Gradio is made for ML stuff and already has things like image uploads and charts built in, which I knew I'd need later. Basically Gradio lets me focus on the Python code and it handles all the web stuff automatically.

### Empty Input Check

```python
if not name or name.strip() == "":
    return "Hello! Please enter your name."
```

Two checks - `not name` catches if it's `None` (which Gradio sends if you never type anything), and `.strip() == ""` catches if you just type spaces. Had to put the `not name` check first because calling `.strip()` on `None` would crash.

### Testing Gradio on Its Own First

`app_ui.py` doesn't import anything from `models.py` in this phase, even though `models.py` exists in the folder. I wanted to make sure Gradio actually worked before trying to connect it to the model. Easier to figure out what's wrong that way.

## File Structure

```
gradio_phase6/
├── app_ui.py          # Gradio web interface (43 lines)
├── models.py          # Model architectures (unchanged from Phase 5)
├── requirements.txt   # Dependencies (Gradio already listed)
└── artifacts/
    └── mnist_mlp.keras
```

## How to Run

```bash
python app_ui.py
```

Opens browser automatically at http://localhost:7860. Stop with Ctrl+C.

## Differences from Phase 5

| Aspect | Phase 5 | Phase 6 |
|--------|---------|---------|
| **Interface** | Command-line | Web UI (Gradio) |
| **User interaction** | Terminal input | Browser-based |
| **New file** | - | app_ui.py (43 lines) |
| **UI framework** | None | Gradio |
| **Purpose** | Demo predictions in terminal | Test Gradio before adding predictions |
