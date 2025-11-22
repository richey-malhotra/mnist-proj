# Phase 11: Add Different Model Architectures

## What Changed

- Added `create_small_cnn()` and `create_deeper_cnn()` to `models.py`
- Architecture dropdown in the Training tab
- Users can now choose between MLP, Small CNN, or Deeper CNN
- CNNs use the 2D layout of the image so they get better accuracy

Until now, only Phase 3's MLP was available. It works fine (~97%) but MLPs flatten the image into a long list of pixels and lose the structure of where things are. A pixel at (10, 15) and one at (10, 16) might be neighbours but the MLP doesn't know that. CNNs fix this with small filters that slide across the image and pick up things like edges and corners.

## Learning About CNNs

Spent a while reading the Keras docs on Conv2D. The idea: define a set of filters (say 32) each 3×3 pixels, and each learns to detect a different pattern. First layer picks up edges and corners. Stack a second conv layer on top and it combines those into curves, loops, intersections.

MaxPooling takes 2×2 blocks and keeps the highest value, which shrinks the data and means the network doesn't care as much if the digit is slightly shifted.

## The Reshape Problem

First CNN attempt crashed with "expected 4D input, got 3D". MLP takes flat `(28, 28)` data, but Conv2D needs `(28, 28, 1)` - that extra `1` is the channel dimension (1 for greyscale, 3 for RGB). Fix: add a Reshape layer at the start. Felt obvious afterwards, but the error message wasn't clear about what was missing.

## Small CNN Architecture

```python
model = keras.Sequential([
    layers.Reshape((28, 28, 1), input_shape=(28, 28)),
    layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])
```

One conv layer (32 filters), one pooling, then dense layers. Not much to it but it works.

## Deeper CNN Architecture

```python
model = keras.Sequential([
    layers.Reshape((28, 28, 1), input_shape=(28, 28)),
    layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
    layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Dropout(0.25),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(10, activation='softmax')
])
```

Two conv layers stacked (32 then 64 filters), plus Dropout(0.25) and Dropout(0.5) layers - a regularisation technique to prevent overfitting. More on this in the section below.

## UI Change

Added `gr.Dropdown` with the three choices. Simple if/elif in the training function creates the right model. Had to update imports too. I initially only had `create_mlp`, which gave a NameError for the CNN functions.

## Testing Results

| Architecture | Val Accuracy | Time per Epoch |
|---|---|---|
| MLP | ~97% | ~15s |
| Small CNN | ~98.5% | ~25s |
| Deeper CNN | ~99%+ | ~40s |

CNNs are clearly better, but the downside is training time. The Deeper CNN takes nearly 3× as long. The accuracy gap isn't massive on MNIST but I think CNNs would probably make a bigger difference on harder datasets.

## Problem I Haven't Fixed Yet

All three architectures save to the same model file, so training a Deeper CNN overwrites whatever was there. Can't compare models side by side. Phase 12 fixes this with proper history tracking.

## How It Works

### Why 32 Filters and 3×3?

I went with 32 filters because that's what the Keras examples use for MNIST. 3×3 is the most common kernel size. It's small but it still covers the pixels right around each one. The Deeper CNN goes up to 64 filters in the second layer because deeper layers need to recognise more complicated things so they need more filters.

### Dropout

Dropout randomly switches off neurons during training (25% after the convolution layers and 50% before the output layer). It sounds counterproductive but it basically stops the network from relying on any one neuron too much. The accuracy results show it works, even though it feels like it shouldn't.

## File Structure

```
gradio_phase11/
├── app_ui.py          # Main application (225 lines, +14 from Phase 10)
├── models.py          # 3 architectures (170 lines, +77)
├── requirements.txt   # Dependencies (unchanged)
└── artifacts/
    └── mnist_mlp.keras
```

## Differences from Phase 10

| Aspect | Phase 10 | Phase 11 |
|--------|----------|----------|
| **Architectures** | MLP only | MLP, Small CNN, Deeper CNN |
| **models.py** | 93 lines | 170 lines (+77) |
| **UI Controls** | Epochs, batch size | + Architecture dropdown |
| **Model creation** | Always `create_mlp()` | Conditional based on dropdown |
| **app_ui.py** | 211 lines | 225 lines (+14) |
