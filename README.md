# Phase 14: Multi-Model Prediction Comparison

## What Changed

- Added `get_best_models()` to find the highest-accuracy model per architecture
- Replaced single-model prediction with `predict_with_comparison()`
- Predictions from all architectures shown side by side
- Added consensus check: do all models agree on the digit?
- Wrapped model loading in try/except after a corrupted file issue

So this phase was meant to be straightforward: add multi-model prediction comparison. But when I actually looked at my code from Phase 13, I realised I'd built the wrong thing. The plan said "comparison", meaning automatically run all three architectures and show results side by side. What I actually had was a single-model prediction where you just pick which model to use. Completely different feature so had to scrap the old predict function and start again.

The rewrite was cleaner than what I had before, so at least something good came out of it. `get_best_models()` queries the database for the highest-accuracy run per architecture (Phase 12's database schema made this pretty easy), then `predict_with_comparison()` loads each best model, runs the prediction, and shows all the results together.

## How the Comparison Works

The flow is: `get_best_models()` looks through the database for each architecture and finds the run with the highest validation accuracy. It checks the file actually exists on disk before including it. I added that after running into the corrupted model problem.

Then `predict_with_comparison()` preprocesses the uploaded image once using Phase 13's `preprocess_image()`, and loops through every best model to get predictions. At the end there's a consensus check:

```python
if len(set(predictions)) == 1:
    results.append("All models agree on " + str(predictions[0]))
else:
    results.append("Models predict different digits")
```

I think this is satisfyingly simple - just throw all the predictions into a set and if there's only one unique value, they all agree.

## The Corrupted Model File

MLP and Deeper CNN loaded fine, but the Small CNN threw a file-not-found error even though `os.path.exists()` returned True. The file was there, 4.2MB, looked normal. Keras just couldn't read it - I think it was saved with a different TensorFlow version. Spent about 20 minutes trying different things before giving up and just retraining a new Small CNN. The new model saved and loaded perfectly.

So basically, just because a file exists doesn't mean Keras can actually open it. That's why `predict_with_comparison()` wraps every `load_model()` call in try/except now. If one model file is bad, it shows an error for that architecture but the others still work.

## Why I Did It This Way

### `ORDER BY val_accuracy DESC LIMIT 1`

```python
cursor.execute('''
    SELECT model_filename, val_accuracy
    FROM training_runs WHERE model_id = ?
    ORDER BY val_accuracy DESC LIMIT 1
''', (model_id,))
```

To find the best model per architecture, I just sort by accuracy descending and take the first row. Simple SQL, no complicated grouping. Phase 12's database schema already stores validation accuracy per run so this was easy to add.

### File Existence Check Before Loading

```python
if os.path.exists(f'artifacts/{filename}'):
    best_models[arch] = (filename, result[1])
```

After the corrupted model incident I added `os.path.exists()` in `get_best_models()`. If the best model's file is missing or deleted, it just skips that architecture and prints a warning. Better than crashing the whole comparison because one file went bad.

### Consensus with `set()`

```python
if len(set(predictions)) == 1:
```

To check if all models agree, I put their predictions in a set. Sets remove duplicates, so if they all predicted the same digit the set has length 1. I wasn't sure if there was a better way to do this but it works and it's readable.
