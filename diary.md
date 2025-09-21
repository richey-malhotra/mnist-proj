# Phase 2 Development Diary

Load the MNIST dataset and understand its structure. With the venv and dependencies from Phase 1 all working, it's time to actually get some data in. Want to see what the data actually looks like: how many images, what size, what format the labels are in.

## Finding Out About MNIST

Googled "MNIST dataset python" and found it's built into Keras. Apparently it's super famous. Everyone uses it for learning neural networks. MNIST stands for "Modified National Institute of Standards and Technology". Handwritten digits that got scanned in years ago.

The dataset has 60,000 training images and 10,000 test images, each 28x28 pixels in greyscale. Labels are just 0-9 for which digit it is. The train/test split is so you can check if the model actually learned rather than just memorising.

## Loading the Data

The import is simple: `from tensorflow.keras.datasets import mnist`. The `load_data()` function returns a weird nested tuple structure that confused me at first:

```
(x_train, y_train), (x_test, y_test) = mnist.load_data()
```

It's returning two tuples - one for training, one for testing. Each has images (x) and labels (y). Initially I tried indexing into the result manually like `data[0][0]`, which worked but looked messy. The unpacking syntax is way cleaner once you get your head round it.

When I printed `x_train.shape` and saw `(60000, 28, 28)` I had to think about what that meant. First number is how many images, second and third are the pixel dimensions. So it's 60,000 separate 28x28 grids. Pixel values range from 0 to 255, which is standard for images, 0 is black, 255 is white. I'll need to normalise these to 0-1 later by dividing by 255, but for now just wanted to see what's there.

First time I ran it, there was a pause while it downloaded (~11MB). After that it loads from cache instantly, which is nice.

## Testing

Ran `app.py`, got the expected output. Shapes match the documentation, pixel range is 0-255, and the first 10 labels are a mix of digits `[5 0 4 1 9 2 1 3 1 4]`. Interesting that they're not sorted. Everything worked first time after I figured out the tuple unpacking.

## What I Learned

The dataset is organised into separate train/test splits, images are tiny (28x28) compared to normal photos, labels are just integers, and pixel values are raw 0-255 not normalised yet. The data comes back as NumPy arrays. You can use `.shape` to check dimensions and `.min()` / `.max()` for value ranges. NumPy is basically what TensorFlow uses underneath for all the number crunching.

The `(x_train, y_train), (x_test, y_test)` pattern seems to be standard for ML datasets. Will probably see this structure again with other datasets.

More interesting than Phase 1. Actually getting real data loaded feels like progress. The dataset is way smaller than I expected. 28x28 pixels is really tiny. But that's enough for digit recognition. Seeing actual label values like `[5 0 4 1 9 2 1 3 1 4]` makes it feel more real than just abstract arrays.

Didn't expect the download on first run - glad it caches though. Also surprised the whole thing is only 11MB. Modern image datasets are gigabytes so this is nothing by comparison. Still not sure exactly where the cached data gets stored on disk but it works, so I'm not going to worry about it.
