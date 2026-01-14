# Phase 20 Development Diary

## Drawing Input

This was the feature I'd been putting off since early on. Gradio has a built-in `gr.Sketchpad` component which made it straightforward - it outputs the same numpy array format as image uploads so it works with the existing preprocessing code without any changes.

Originally tried using radio buttons to switch between upload and draw modes with visibility toggles, but that caused weird type mismatches in the callbacks. Switched to separate tabs instead (Upload tab and Draw tab) which is cleaner anyway.

Both the Upload and Draw tabs need to call `predict_with_validation()` but with different arguments. Didn't want to write two separate wrapper functions just for that so I used lambdas - `fn=lambda img: predict_with_validation("Upload Image", img, None)`. A lambda is basically a mini function you write right there without giving it a name. The `lambda img:` bit means it takes `img` as input and the rest is what it does. Honestly found the syntax confusing the first time I saw it but once I realised it's just a one-line `def` it made sense.

One problem: drawn digits come out as dark-on-light but MNIST expects light-on-dark. Had to add an inversion step. Also needed to detect empty drawings - ended up checking average pixel brightness, if it's above 250 the canvas is basically blank.

## Validation and Error Handling

Went through the app and added proper validation everywhere I could think of:
- Training params: epochs 1-50, batch size 16-256
- Empty image checks for both upload and draw
- "No trained models found" message instead of crash when database is empty
- try/except around all prediction logic

The error messages are specific now rather than generic Python tracebacks. Things like "Please draw a digit on the canvas first" instead of just crashing.

## Confidence Summary

Added a compact confidence breakdown to each model's prediction - shows the top 5 digit probabilities so you can tell whether the model is sure (one value dominating) or uncertain (several close values). Looks like:

`Deeper CNN: 7 (97.9%) | top → 7:97.9%, 2:0.7%, 1:0.5%, 9:0.4%, 3:0.2%`

Also sorted the output by confidence so the most certain model appears first, with a star next to the winner. Considered a bar chart or heatmap for this but it felt like overkill - the text version is enough to see how sure the model is and it doesn't take up loads of space.

## Problems

The Deeper CNN database entry pointed at a model file that didn't exist (leftover from Phase 14's corruption issue). Had to patch the row. Also the initial output order was random because dictionaries don't guarantee order - fixed with sorting.

For the sorting I used `sorted(model_rows, key=lambda m: m['confidence'], reverse=True)` - the `key=` bit tells Python what to sort by, which here is a lambda that grabs the confidence from each dict. `reverse=True` makes it highest-first. The probability breakdown line is a bit mad: `sorted(enumerate(probs), key=lambda x: x[1], reverse=True)[:5]`. `enumerate()` pairs each probability with its position (which digit it is), sort by probability, then `[:5]` takes the top 5. Lot going on in one line but couldn't work out a cleaner way to do it.

## Testing

Drew all 10 digits (0-9), tested empty canvas detection, tried switching between tabs, checked probability formatting. The drawing feature is actually fun to use - way more satisfying than hunting for digit images to upload.

Took about 4 hours. The drawing part was quick, but checking all the different inputs adds up.
