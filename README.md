# Phase 5: Make Predictions

## What Changed

- Added prediction functionality to classify digit images
- Added the preprocessing stuff: normalising pixels and adding the batch dimension
- Model loads from Phase 4's saved file and predicts with confidence scores
- Tests on 5 random images each run to check it's actually working

Phase 4 saved the trained model to disk. This phase makes it actually *do* something. It takes an image and tells you what digit it is.

## Understanding the Output

First thing was figuring out what `model.predict()` actually returns. Turns out it gives you an array of 10 numbers, one probability for each digit 0-9, all adding up to 1.0. So if the fourth number (index 3) is 0.85, the model is 85% sure it's a 3. To get the predicted digit you use `argmax()` which finds the index of the highest value. Simple once you know the name, but took me a minute to remember it.

## Two Bugs, Back to Back

**Shape error.** Tried passing a single image to the model and got "expected 3 dimensions, got 2". The model was trained on batches shaped `(60000, 28, 28)` but my image was just `(28, 28)` - no batch dimension. Fix was `np.expand_dims(image, axis=0)` to reshape to `(1, 28, 28)`, a "batch of one". Found another way to do it with `np.newaxis` but expand_dims made more sense to me.

**Normalisation mismatch.** Got predictions working but they were terrible - basically random guesses despite 97% accuracy. Spent a while confused before realising I was feeding raw pixels (0-255) but the model was trained on normalised data (0-1). Added `image.astype('float32') / 255.0` before predicting and everything worked. Frustrating because the model ran fine, it just silently gave garbage. Basically you have to preprocess the same way for training and prediction or you get rubbish results.

## The predict_digit Function

Put it together in `models.py`: normalise, add batch dimension, predict, argmax, calculate confidence percentage. The `verbose=0` flag stops the progress bar per prediction, which was annoying when testing multiple images.

Confidence scores are interesting. Most come back at 99%+ but occasionally you get 85%, which usually means the digit is ambiguous. Doesn't mean it's actually right though. I saw one prediction at 97.8% that was completely wrong. Some digits just look similar.

## Why Two Datasets?

```python
# Raw (0-255) for predictions
(x_train_raw, y_train), (x_test_raw, y_test) = mnist.load_data()
# Normalised (0-1) for training
(x_train, _), (x_test, _) = load_data()
```

Model was trained on normalised data, so predictions need normalisation too. But I load raw data separately so `predict_digit()` handles preprocessing itself, which is what'll happen when someone actually uses the app later.

## Testing

Loaded the saved model from Phase 4 and tested on 5 random images:

```
✓ Image 1: Predicted=7, Actual=7, Confidence=99.8%
✗ Image 2: Predicted=5, Actual=3, Confidence=91.2%
✓ Image 3: Predicted=2, Actual=2, Confidence=98.3%
```

Got 4/5 correct - the wrong one was a 3 predicted as 5, which makes sense for scruffy handwriting. Overall test accuracy: 97.48%, matching training results.

## Why I Did It This Way

### Using `float32` Instead of `float64`

```python
image = image.astype('float32') / 255.0
```

I used `float32` because that's what TensorFlow uses internally. Using a different type might cause problems.

### Converting NumPy Types to Python Types

```python
digit = int(prediction.argmax())
confidence = float(prediction[0][digit]) * 100
```

`argmax()` returns a NumPy type, not a regular Python int. I found that other parts of the code sometimes didn't work with NumPy types, so wrapping them with `int()` and `float()` just makes sure they're normal Python numbers. Easy to forget but it avoids random errors later.

### Why `prediction[0][digit]`

`model.predict()` always gives back a 2D array even when you only give it one image. So `prediction[0]` gets the first (and only) result, and then `[digit]` gets the confidence for the predicted digit. It's because I added the batch dimension with `np.expand_dims` earlier, so the output shape matches the input shape.

## Differences from Phase 4

| Aspect | Phase 4 | Phase 5 |
|--------|---------|---------|
| **Functionality** | Train, save, load | + Make predictions |
| **models.py** | 48 lines | 96 lines (+48) |
| **app.py** | 97 lines | 156 lines (+59) |
| **New functions** | None | `preprocess_image()`, `predict_digit()`, `test_predictions()` |
| **Data loading** | Normalised only | Raw + normalised |
| **Model output** | Accuracy % | Individual predictions with confidence |
