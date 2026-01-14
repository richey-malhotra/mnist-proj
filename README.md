# Phase 20: Error Handling + Input Validation + Drawing Input

## What Changed

- Added `gr.Sketchpad` so users can draw digits on a canvas instead of uploading
- Replaced the radio-button input toggle with proper tabs (Upload vs Draw)
- Proper validation: epochs 1-50, batch size 16-256, empty canvas/upload detection
- Each model now shows a top-5 confidence breakdown, sorted by probability
- Wrapped everything in try/except so users get friendly messages, not Python tracebacks

## Drawing Input with gr.Sketchpad

This was the main feature. `gr.Sketchpad` outputs the same NumPy array format as `gr.Image` uploads, so the existing preprocessing code works without changes. The nice thing is Gradio uses the same numpy format for both, so my preprocessing code just works.

The catch: when you draw, you get white lines on a black background, but MNIST digits are dark on white. So I had to flip the colours.

For blank canvas detection, I check the average brightness across all pixels. If it's above 250 (out of 255), the canvas is basically empty, so there's no point sending that to the model. Shows a "Please draw a digit first" message instead.

## Radio Buttons → Tabs

Originally I tried radio buttons to toggle visibility between upload and draw components. This was buggy - Gradio's visibility toggling with radio buttons caused flickering and state issues. Switched to `gr.Tab` which is way cleaner. Each input method has its own tab and I don't have to mess with showing and hiding stuff.

## Confidence Summary Format

Previously just showed the top predicted digit. Now each model displays its top 5 predictions sorted by confidence:

```
⭐ Deeper CNN: 7 (97.9%) | top → 7:97.9%, 2:0.7%, 1:0.5%, 9:0.4%, 3:0.2%
• Small CNN: 7 (93.1%) | top → 7:93.1%, 2:2.8%, 1:1.6%, 9:1.2%, 0:0.8%
```

The star marks whichever model is most confident. The dictionary ordering was random so I had to sort by probability before displaying. The predictions come out as a 10-element array. I zip with digit labels 0-9, sort descending, take the top 5.

## Phase 14 Deeper CNN Fix

While testing, noticed the Deeper CNN database entry was pointing at a model file that didn't exist - leftover from Phase 14's corruption issue. Had to retrain a clean version and update the database path. The error message was cryptic (TensorFlow deserialization failure), but the fix was straightforward.

## Why I Did It This Way

### Sketchpad Doesn't Just Give You an Image

This confused me for a while. `gr.Sketchpad` doesn't return a simple NumPy array like `gr.Image` does. It returns a dictionary, and the actual image is inside a key called `'composite'`:

```python
if isinstance(drawn_image, dict):
    if 'composite' in drawn_image and drawn_image['composite'] is not None:
        image = drawn_image['composite']
```

I also had to add a check for `isinstance(drawn_image, bool)` because Gradio sometimes sends `False` when you clear the canvas, which is really weird. All of this was figured out through trial and error because the Gradio docs don't explain it properly.

### Returning Blank Images for Errors

```python
blank_image = Image.new('L', (28, 28), 255)
return blank_image, blank_image, "❌ Please upload an image first."
```

When something goes wrong, I can't just return `None` for the image outputs because Gradio expects actual images. So I create a blank white 28×28 image (matching MNIST size) as a placeholder. White because 255 = white in greyscale, so it's obviously empty.

### Marking Failed Predictions With -1

If a model fails to load or predict, I set its confidence to `-1.0` so it sorts to the bottom when the results are ranked. That way errors show up last in the table instead of crashing everything.

### Using Lambdas for the Buttons

```python
upload_predict_button.click(
    fn=lambda img: predict_with_validation("Upload Image", img, None),
    inputs=[image_input], ...
)
```

Both buttons call the same prediction function but I needed to pass a different first argument to each. The lambda does that. Otherwise I'd have to copy-paste the function twice.

### Canvas Size: 280×280

The canvas is 280×280 pixels, which is exactly 10× the MNIST size (28×28). Drawing on a 28×28 canvas would be tiny and unusable. 10× makes it comfortable to draw on, and the maths for shrinking it down is clean.

## File Structure

```
gradio_phase20/
├── app_ui.py          # Main UI (~670 lines, +~160 from Phase 19)
├── utils.py           # Preprocessing function (42 lines)
├── models.py          # Model architectures (unchanged)
├── init_db.py         # Database initialisation (unchanged)
├── requirements.txt   # Dependencies (unchanged)
└── artifacts/
    └── training_history.db
```

## Differences from Phase 19

| Aspect | Phase 19 | Phase 20 |
|--------|----------|----------|
| **Input methods** | Upload only | Upload OR draw (tabs) |
| **Input switching** | Radio buttons | `gr.Tab` components |
| **Validation** | Basic null checks | Epochs, batch size, canvas emptiness |
| **Error messages** | Generic / tracebacks | Specific, helpful messages |
| **Prediction detail** | Top digit only | Top-5 probability distribution |
| **Most confident** | Not shown | Star marker on winning model |
| **app_ui.py** | ~510 lines | ~670 lines (+~160) |
