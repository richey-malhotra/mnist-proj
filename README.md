# Phase 7: Image Upload and Prediction

## What Changed

- Swapped Phase 6's text greeting for a real image classifier
- Added the code to convert uploaded images into MNIST format
- Model loads once at startup so it's not reloading on every prediction
- Output shows predicted digit with confidence percentage

This is the phase where the model from Phase 3, the prediction logic from Phase 5, and the Gradio UI from Phase 6 all come together into one working app.

## PIL vs Pillow

First thing I needed was a way to resize images. Found PIL for working with images, except PIL is ancient and unmaintained - the actual package you install is called Pillow. But you still write `from PIL import Image` in your code. I literally tried `import Pillow` first and it just doesn't work. It's basically a newer version but they kept the old name so existing code still works. Confusing, but bit weird but whatever.

## The Preprocessing Steps

Getting a user's uploaded photo into the shape the model expects turned out to be a longer chain than I thought. Six steps total:

1. **NumPy array → PIL Image**: Gradio passes uploads as NumPy arrays, but PIL handles resizing better
2. **Convert to greyscale** with `.convert('L')`. The 'L' just means grey (I had to look that up), strips RGB channels down to one
3. **Resize to 28×28**: MNIST standard size, uses PIL's default resize method
4. **Back to NumPy array**: the model works with arrays, not PIL objects
5. **Normalise to 0-1**: divide by 255.0, same as Phase 3's training preprocessing
6. **Add batch dimension**: `np.expand_dims(axis=0)` reshapes (28, 28) to (1, 28, 28) because Keras models expect batches

The **order matters** for the greyscale step. If you resize a colour image first, you get (28, 28, 3) because three channels survive the resize. Converting to greyscale before resizing strips it down to a single channel and gives you the (28, 28) shape the model expects.

And yes, I forgot the batch dimension again. Same exact error as Phase 5: "expected 3 dimensions, got 2". At least this time I recognised it immediately.

## The api_name Bug

The app crashed on page load with `TypeError: argument of type 'bool' is not iterable` deep inside gradio_client code. Had to add `api_name=False` to the Interface constructor to fix it. Not a great error message but at least the fix is one extra parameter. This comes back in Phase 8 too.

## Confidence Output

Initially just returned the predicted digit as a bare number, which wasn't very useful - you can't tell whether the model is certain or guessing. Changed it to show digit plus confidence percentage: "Predicted Digit: 7, Confidence: 98.45%". Way better because you can actually see if it's sure or just guessing.

## Testing

Clean MNIST-style digits got 99%+ confidence. A colour phone photo of a handwritten 3 came through at about 87%. The greyscale conversion and resizing handled it, but some quality is obviously lost. Even uploaded a photo of a cat to see what happens, and the model predicted 8 with low confidence. It doesn't know how to reject non-digits, it just picks the closest one and gives it a probability. Worth remembering for later.

## Decisions

### Greyscale Conversion

The code uses PIL's `.convert('L')` to convert colour images to greyscale. There's supposedly a more "proper" way that weights green higher because our eyes are more sensitive to it, but for black-and-white digit images it doesn't really matter. The code also checks if the image is already greyscale and skips the conversion if so.

### Error Handling

```python
try:
    ...
except Exception as e:
    return f"Error: {str(e)}"
```

I wrapped the prediction code in a try/except so if something goes wrong, it shows an error message instead of crashing. I also added a check for `None` in case nothing was uploaded. I just wanted to make sure the app doesn't completely break on bad input.

## Differences from Phase 6

| Aspect | Phase 6 | Phase 7 |
|--------|---------|---------|
| **Interface** | Text greeting | Image classification |
| **Input** | `gr.Textbox` | `gr.Image` |
| **Processing** | String formatting | 6-step preprocessing chain |
| **Model usage** | None | Loaded at startup, used for prediction |
| **Output** | Greeting text | Digit + confidence % |
| **New concept** | Gradio basics | PIL/Pillow, image preprocessing |
