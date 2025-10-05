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
---

## Phase 3 — Train First MLP Model

### What I tested

Ran the training script a few times to make sure it actually works and the accuracy goes up.

### Tests

| # | What I tried | Type | Expected | Actual | Pass? |
|---|---|---|---|---|---|
| 1 | Train MLP with 5 epochs | Normal | Accuracy improves each epoch | Started at 89.3%, ended at 97.1% | Yes |
| 2 | Train MLP with 10 epochs | Normal | Higher accuracy than 5 epochs | Got 97.8% — slightly better | Yes |
| 3 | Check model outputs 10 classes | Normal | Output shape is (None, 10) | model.summary() showed (None, 10) | Yes |
| 4 | Run training without normalising the data | Erroneous | Should still work but worse accuracy | Accuracy stuck at around 11% — basically random | Yes (but bad) |
| 5 | Train with batch_size=1 | Boundary | Should work but very slow | Worked but took about 15 minutes for 1 epoch. Way too slow | Yes |

### Bugs found

**Forgot to normalise the pixel values.** The first time I ran it the accuracy was about 11% and I couldn't work out why. Spent ages checking the model architecture before I realised the input data was 0-255 instead of 0-1. Dividing by 255.0 fixed it immediately — accuracy jumped to 90%+ on the first epoch. Felt stupid but at least I know why normalisation matters now.

### What I learned

The val_accuracy is more important than training accuracy because that's on data the model hasn't seen. If training accuracy is way higher than val accuracy that means it's memorising rather than actually learning (overfitting). Mine were pretty close so I think it's OK.
---

## Phase 4 — Save and Load Trained Models

### What I tested

Made sure models save properly and load back with the same predictions.

### Tests

| # | What I tried | Type | Expected | Actual | Pass? |
|---|---|---|---|---|---|
| 1 | Save model after training | Normal | .keras file appears in artifacts/ | File created, 1.2MB | Yes |
| 2 | Load saved model and predict | Normal | Same predictions as before saving | Predictions matched exactly | Yes |
| 3 | Try loading a model that doesn't exist | Erroneous | Should get an error | Got FileNotFoundError — makes sense | Yes |
| 4 | Save two models, load each separately | Boundary | Both files exist and load correctly | Both loaded fine, predictions different because different training runs | Yes |

### Bugs found

**Model file path was hardcoded.** I had the path as just `model.keras` which saved it in the project root. Moved it to `artifacts/model.keras` and added the artifacts folder to the project. Not really a bug but it was messy having model files in the root directory.
