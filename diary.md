# Phase 13 (Part 2) Development Diary

## Overview

Quick phase. I was about to start Phase 14 (multi-model comparison) and realised it's going to need the exact same image preprocessing that's already in `predict_uploaded_image()` — about 15 lines of converting uploads to 28×28 greyscale normalised arrays. I was literally about to copy-paste the whole block into a new function when I thought... that's going to be really annoying if I ever need to fix a bug in it, because I'd have to remember to change it in both places.

## What Actually Happened

Selected the preprocessing block in VS Code to copy it, and this little lightbulb icon popped up in the margin. Clicked it and one of the options said "Extract method". Tried it out of curiosity — it pulled the selected code into its own function automatically and replaced the original block with a single function call. That's basically what I was going to do manually, just VS Code did it in about 2 seconds.

Ended up not using the auto-generated version though, because I wanted the function in a separate file rather than just sitting at the top of `app_ui.py`. Created `utils.py` instead. Called it that because I noticed a few Python projects on GitHub use the name "utils" for shared helper functions — short for "utilities". So `models.py` has architecture definitions, `utils.py` has shared helpers, and `app_ui.py` has the UI logic.

Googled "extract method python" afterwards cos I was curious what VS Code was actually doing, and apparently this whole thing of reorganising your code without changing what it does is called "refactoring". There's a proper name for it and everything. Makes sense I suppose — you're not adding features, you're just reshaping the existing code so it's tidier. Feels like the kind of thing that sounds more impressive than it is though. I literally just moved some lines into a different file.

## PIL Type Issue

Only real snag was a PIL type thing. My first version just did `Image.fromarray(image)` directly, but Gradio can pass float32 arrays and PIL's `fromarray` expects uint8. Got a `ValueError` about unhandled data types. The fix was adding type checks — convert to uint8 first if needed, handle both RGB and greyscale inputs, then do the conversion and resize. Three lines of type-checking to avoid crashes on dodgy input.

## Testing

Uploaded a test digit and got the same prediction and confidence as before. Trained a model to make sure that path still works, checked the History tab. Everything working exactly the same, so moving the code didn't break anything. If I've done it right, nobody using the app should notice any difference — and they don't.

## Reflection

This is the kind of change where nothing looks different to the user but the code is better organised. Phase 14 will need `preprocess_image()` for running predictions across multiple saved models, so pulling it out now saves copy-pasting later. If there's ever a bug in the preprocessing, I only have to fix it in one place.

Knocked this out in under an hour. Probably the fastest phase so far — the actual coding was maybe 20 minutes, the rest was testing to make sure nothing broke. The VS Code lightbulb thing was a nice find though. Might look into what other stuff it can do.
