# Phase 6 Development Diary

Now that Phase 5 has predictions working from the command line, I needed a proper interface. Running a script, seeing five results, and then having to edit the code to test again isn't exactly user-friendly. I wanted a web page where someone could actually interact with the model: type something in, click a button, see a result.

I'd already put `gradio==4.36.1` in requirements.txt ages ago. Gradio's made for ML stuff. You just write a Python function and it makes a web page for you. Way easier than building everything from scratch with something like Flask.

## Installing Gradio

First I tried running app_ui.py and got `ModuleNotFoundError: No module named 'gradio'` - bit embarrassing. Gradio was in requirements.txt but I'd never actually installed it because the earlier phases didn't need it. So I ran `pip install -r requirements.txt` again and it pulled down about 30 extra packages (FastAPI, Uvicorn, Hugging Face Hub, loads of stuff I didn't expect). But then it wouldn't actually run - got `ImportError: cannot import name 'HfFolder' from 'huggingface_hub'`. Spent ages Googling this. Pip had installed `huggingface_hub` version 1.0 which removed a function called `HfFolder`, and Gradio 4.36.1 still tries to import it. The fix was adding `huggingface_hub<1.0` to requirements.txt to force an older version. Really annoying - I'd never even heard of huggingface_hub before seeing it in the pip output just now. At least my Python version (3.9.6) wasn't a problem - everything else installed fine.

## Getting the Hello World Running

Didn't want to jump straight to image classification without knowing Gradio works, so I started with the simplest possible thing, a text greeting function. The code's in app_ui.py. It's a `gr.Interface` with a textbox input, textbox output, and a function that takes a name and returns a greeting. Added validation so empty input gets a helpful message instead of "Hello !", plus a title and description so the page looks like it belongs to the project.

When you call `demo.launch()`, it starts a local server on port 7860 and opens your browser. First time it loaded I couldn't believe how clean it looked. Professional layout with labelled boxes, a submit button, all from about ten lines of Python. Typed my name in, hit submit, got the greeting back instantly.

The whole pattern is: user enters something, Gradio calls your function, displays whatever it returns. I initially thought the function would need special decorators or a specific set of arguments but it doesn't. It's just a regular Python function. Gradio handles all the web stuff for you.

Took me a minute to get the `fn=greet` bit - writing `greet` without the brackets doesn't actually call it, it just hands the function itself over to Gradio so Gradio can call it later when someone clicks submit. It's like giving someone a recipe vs actually cooking the food. Looked this up properly and it's called a callback. The idea is actually pretty simple once you get it: instead of calling the function yourself, you hand it to someone else's code and say "here, run this when something happens". You're giving the function away. Gradio holds onto it and then "calls it back" whenever the user clicks Submit. I think the reason callbacks are so common in UI stuff is that you can't predict when a user will click something - you can't just write code that sits there waiting. So you give the framework your function and let it sort out the timing. Bit of a weird concept at first but it makes sense once you see it working.

## Testing

Noticed Gradio created a `flagged/` folder in the project directory - it saves inputs and outputs there when you click the Flag button. Added it to `.gitignore` since it's just local data.

Ran app_ui.py and confirmed the interface loads on localhost:7860. Typed "Harpreet" and got the expected greeting back. Tested empty input - got the validation message. Stopped the server with Ctrl+C, shut down cleanly. One minor annoyance: restarting immediately after Ctrl+C gave "Address already in use" because the port hadn't freed up yet. Just had to wait about 10 seconds.

## Reflection

Honestly expected the web UI to be the hardest part of this project, but Gradio makes it really easy. Only hiccup was forgetting to actually install it even though it was in requirements.txt, the ModuleNotFoundError was a bit embarrassing. Once installed, everything just worked.

The basic idea (function plus inputs plus outputs plus launch) is so simple that the actual coding took about fifteen minutes. The comparison with Phase 5's command-line approach is massive. Instead of run-once scripts I've got a web page that stays running and looks decent and could even be shared over a local network.

Phase 7 should be straightforward: swap the textbox for an image upload and connect it to `predict_digit()` from models.py. The prediction logic's already done. Really glad I went with Gradio.

About an hour total. Most of it was spent on the actual code rather than setup.
