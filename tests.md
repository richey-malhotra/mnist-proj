# Testing Log
## Phase 1 — Initial Setup

### What I tested

Just checked that Python and TensorFlow installed properly and the hello world script runs.

### Tests

| # | What I tried | Type | Expected | Actual | Pass? |
|---|---|---|---|---|---|
| 1 | Run app.py | Normal | Prints "Hello World" | It printed it | Yes |
| 2 | Import tensorflow in Python shell | Normal | No errors | Imported fine, version 2.15.0 | Yes |
| 3 | Import numpy | Normal | No errors | Imported fine | Yes |

### Bugs found

None — there's nothing to break yet. Just making sure my environment works before I start building stuff.
---

## Phase 2 — Load MNIST Dataset

### What I tested

Loaded the dataset and checked the shapes and values look right.

### Tests

| # | What I tried | Type | Expected | Actual | Pass? |
|---|---|---|---|---|---|
| 1 | Load MNIST dataset | Normal | No errors, data loads | Loaded in about 2 seconds | Yes |
| 2 | Check training set shape | Normal | (60000, 28, 28) | Correct | Yes |
| 3 | Check test set shape | Normal | (10000, 28, 28) | Correct | Yes |
| 4 | Check pixel value range | Normal | 0 to 255 | Min was 0, max was 255 | Yes |
| 5 | Check label values | Normal | Integers 0-9 | All values in {0,1,...,9} | Yes |

### Bugs found

Nothing broken. I did notice the images are uint8 which means I'll need to convert to float and normalise later, but that's not a bug — just something to remember.
