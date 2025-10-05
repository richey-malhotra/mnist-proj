# Phase 4: Save and Load Trained Models

## What Changed

- Added `save_model()` and `load_model()` functions to models.py
- Created `artifacts/` directory for model files
- Uses `.keras` format (single file, simpler than the older SavedModel way that makes a whole folder)
- Added a yes/no prompt in app.py so you can choose to load the saved model or retrain

## Why This Was Needed

Phase 3's model only existed in memory. All 101,770 trained parameters were lost as soon as the script finished, meaning a 2-minute retrain every time. That gets old fast when you're testing predictions.

## Save Format

Googled "keras save model" and found two options: SavedModel (creates a whole directory with multiple files) and `.keras` (single file, newer). Went with `.keras` because it's simpler - one file instead of a folder structure. It stores everything: architecture, weights, optimiser state, and compilation settings. Once it's loaded you can just use it straight away, don't need to recompile or anything.

The saved file is about 416KB, which seemed surprisingly small for 101k parameters plus all the architecture info.

## How I Set It Up

Created an `artifacts/` directory to keep model files separate from code. Wasn't sure what to call the folder at first - thought about `models/` or `saved/` but a few TensorFlow tutorials I read called saved model files "artifacts", so I went with that. Used `os.makedirs('artifacts', exist_ok=True)` in the save function so it creates the folder if needed without erroring if it already exists. First time using this function. It's handy.

The save and load functions in models.py basically just call `model.save()` and `keras.models.load_model()` and that's it. See models.py for the actual code.

The interactive flow in app.py uses `os.path.exists()` to check if `artifacts/mnist_mlp.keras` exists, then `input().strip().lower()` to handle the user's yes/no choice. Had to add `.strip().lower()` because typing "Y" didn't match "y" initially - case sensitivity on user input is an easy thing to miss.

## Things Worth Explaining

### The `os.makedirs` Issue

```python
def save_model(model, filepath):
    os.makedirs('artifacts', exist_ok=True)
    model.save(filepath)
```

There's a slight problem here that I noticed: the function takes any filepath as an argument but always creates the `'artifacts'` folder specifically. If I ever saved to a different folder it would create `artifacts/` for no reason and then fail because the other folder doesn't exist. It's fine for now since I always save to `artifacts/`, but I should probably fix it at some point to use whatever directory is in the filepath.

### Relative Paths

```python
model_path = 'artifacts/mnist_mlp.keras'
```

This only works if you run `python app.py` from inside the phase folder. If you run it from somewhere else it'll look for `artifacts/` in the wrong place. There are ways to make paths relative to the script's location but I kept it simple for now.

## File Structure

```
gradio_phase4/
├── app.py             # Main script (97 lines, +29 from Phase 3)
├── models.py          # Model architectures + save/load (50 lines, +17)
├── requirements.txt   # Dependencies (unchanged)
└── artifacts/
    └── mnist_mlp.keras  # Saved model (~416KB)
```

## Testing

Tested both paths: save new model and load existing model. Accuracy matched (97.35% before save and after load), so the save/load is working properly. Loading is basically instant (~2 seconds) compared to ~2 minutes for retraining. Massive improvement.

## How to Run

```bash
python app.py
```

On first run: trains and saves the model. On later runs: offers to load or retrain.

## Differences from Phase 3

| Aspect | Phase 3 | Phase 4 |
|--------|---------|---------|
| **Saving the model** | In memory only (lost on exit) | Saved to .keras file |
| **Startup time (with model)** | ~2 minutes (retrain) | ~2 seconds (load) |
| **File count** | 2 Python files | 2 Python files + artifacts/ |
| **User interaction** | None | Load/retrain prompt |
| **New functions** | None | `save_model()`, `load_model()` |
| **New concepts** | None | `os.path.exists()`, `os.makedirs()`, `.strip().lower()` |
