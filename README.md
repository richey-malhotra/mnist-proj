# Phase 2: Load MNIST Dataset

## What Changed

- Added MNIST dataset loading with `mnist.load_data()`
- Created `load_data()` function that loads the dataset and prints info about it
- Updated `main()` to load data and print statistics
- Output shows shapes, value ranges, and sample labels

## Finding MNIST

Googled "MNIST dataset python" and found it's built right into Keras, so no separate download needed. MNIST stands for "Modified National Institute of Standards and Technology". It's apparently super famous - everyone uses it for learning neural networks. Handwritten digits that got scanned in years ago.

The dataset has 60,000 training images and 10,000 test images, each 28×28 pixels in greyscale. Labels are just integers 0-9 for which digit it is. The train/test split is so you can check the model actually learned and isn't just memorising, which makes sense I guess.

28×28 is really tiny compared to modern photos, but that's enough for digit recognition. The whole thing is only ~11MB. Modern image datasets are gigabytes.

## The Nested Tuple

The return value confused me at first:

```python
(x_train, y_train), (x_test, y_test) = mnist.load_data()
```

It returns two tuples - one for training, one for testing. Each has images (x) and labels (y). Initially tried indexing into the result manually like `data[0][0]`, which worked but looked messy. The unpacking syntax is much cleaner once you wrap your head around it.

## Understanding the Data

`x_train.shape` gives `(60000, 28, 28)`, which is 60,000 separate 28×28 grids. Pixel values range 0-255 (standard greyscale: 0 is black, 255 is white). Will need to normalise these to 0-1 by dividing by 255 later, but for now just wanted to see what's there.

Data comes back as NumPy arrays. `.shape` checks dimensions, `.min()` / `.max()` for value ranges. NumPy is basically what TensorFlow uses underneath for all the number crunching.

First run pauses while it downloads (~11MB). After that it loads from cache instantly. Not sure where exactly the cached data lives on disk but it works.

## Testing

Ran `app.py`, got the expected output. Shapes match documentation, pixel range is 0-255, first 10 labels are `[5 0 4 1 9 2 1 3 1 4]`. Interesting that they're not sorted. Everything worked first time after figuring out the tuple unpacking.

## How It Works

### Import Path

```python
from tensorflow.keras.datasets import mnist
```

I used `tensorflow.keras` rather than just installing `keras` as a separate package. Since TensorFlow 2, Keras is basically included inside TensorFlow, so importing it this way means it'll definitely work with whatever TensorFlow version I've got installed. Using a separate `keras` package could cause weird version mismatches.

### The Function Prints and Returns

`load_data()` both prints the statistics and returns the data. It's a bit messy because I've read that functions are supposed to just do one thing, but I always want to see the stats when loading so it made sense to combine them. The data gets unpacked inside the function for printing and then packed back up for returning, which is a bit unnecessary but keeps things simple.

## Differences from Phase 1

| Aspect | Phase 1 | Phase 2 |
|--------|---------|---------|
| **Functionality** | Print hello world | Load and inspect MNIST data |
| **Imports** | None | tensorflow.keras.datasets |
| **Functions** | main() | main(), load_data() |
| **Output** | 2 lines | Dataset statistics |
| **Data downloaded** | None | ~11MB MNIST dataset |
| **Total lines (app.py)** | 12 | 33 (+21 lines) |
