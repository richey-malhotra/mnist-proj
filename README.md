# Phase 17: Image Preview

## What Changed

- Added preprocessing visualisation: original and processed images shown side by side
- Renamed `predict_with_comparison` to `predict_with_preview`
- Function now returns three values: original image, preprocessed 28×28 image, predictions text
- Predict tab layout updated with two image displays alongside results

Before this, uploading an image gave you a prediction, and you had no idea what happened to it. Now you can see exactly what the model receives after preprocessing.

## Why This Matters

It's partly about trust. If someone uploads a photo of a digit and gets a wrong answer, they can see that the 28×28 version looks nothing like what they uploaded. The preprocessing squashes and inverts colours and sometimes the digit becomes unrecognisable. Showing that helps explain why it sometimes gets things wrong.

It's good for debugging too. If a prediction is wrong, you can tell whether the problem is the model or the preprocessing. A digit that looks clear at 28×28 but still gets misclassified = model problem. A digit that's unrecognisable after resizing = preprocessing problem.

## How I Did It

The preprocessed numpy array needs converting back to a PIL Image for display. You multiply by 255 and cast to uint8 since the normalised model input (0-1) isn't directly displayable. Forgot that Gradio Image components want PIL not numpy, spent a few minutes on that.

If something goes wrong, the function returns `None, None, error_message` so the image boxes stay empty and the error appears in the text box. Returning three things at once (image, image, text) worked nicely. I might do it again if I need before/after views.

The preprocessed image looks a bit blocky (28×28 rendered at display size) but that's the point - you see exactly what the model sees, pixels and all.

## Layout

The Predict tab needed rearranging. Image upload and button on the left column, original preview, preprocessed preview, and prediction results stacked on the right. It's a bit cramped but gets the point across.

## Testing

Uploaded a few images, both previews display correctly. Tried an already-28×28 image (preview looks identical, which makes sense). Colour photo of a digit, and the colour disappears in the preprocessed version from the greyscale conversion, which is a nice way to actually see that preprocessing is happening. Quick phase overall.

## Why I Did It This Way

### Reversing Normalisation for Display

```python
img_preprocessed = Image.fromarray((img_array * 255).astype('uint8'))
```

The model input is normalised to 0-1 floats, but PIL and Gradio need 0-255 uint8 for display. Multiplying by 255 reverses the normalisation, then `astype('uint8')` truncates. There's a small precision issue: `0.5 * 255 = 127.5` truncates to `127`. You can't actually see the difference, but technically the displayed image isn't exactly what went in before normalisation.

### `interactive=False` on Display Images

```python
original_image_display = gr.Image(label="Your Uploaded Image", interactive=False)
```

Without `interactive=False`, Gradio shows editing tools (crop, draw, clear) on the preview images, which would confuse people and could mess up what's being shown. They're just for display - the user shouldn't be able to edit them.

### Why Every Return Needs Three Values

Gradio maps each return value to the output boxes in order. If the function returns 2 values instead of 3, Gradio throws an error. That's why every place where something goes wrong carefully returns `None, None, error_message`, so it always returns 3 things to match what Gradio expects. `None` tells Gradio to leave that image box empty.
