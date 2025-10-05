# Phase 4 Development Diary

## Session Goal

Save trained models to disk so I don't have to retrain every time. Same model from Phase 3, just saved to a file now.

## What I Did

Right now the trained model only exists in memory, so soon as the script finishes, all 101,770 trained parameters are lost and I have to wait 2 minutes to retrain. Annoying.

Googled "keras save model" and found two main formats: SavedModel (directory-based, the older approach) and `.keras` (single file, newer, recommended). Went with `.keras` because it's simpler. One file instead of a whole directory structure. According to the docs it saves everything: architecture, weights, optimiser state, compilation settings. Once it's loaded you can just use it straight away, no need to recompile.

Created an `artifacts/` directory to keep model files separate from code. Called it "artifacts" because that's the term the TensorFlow tutorials use for saved model files - I originally was going to call it `models/` but that could get confused with the `models.py` file. Used `os.makedirs('artifacts', exist_ok=True)` in the save function so it creates the folder if needed without errors if it already exists. The save and load functions in `models.py` are short - they basically just call `model.save()` and `keras.models.load_model()` and that's it. See models.py for the code.

Added a yes/no choice to `app.py`. It checks if `artifacts/mnist_mlp.keras` exists using `os.path.exists()` and asks if you want to load it or train fresh. Had a minor issue with `input()` not handling uppercase, so typing "Y" didn't match "y" until I added `.strip().lower()`. The saved file is about 416KB, which seemed small for 101k parameters plus all the architecture info. Not sure why it's that small but it works.

## Testing

Tested both paths. Save works, load works, accuracy matches (97.35% before and after loading). Loading is basically instant versus 2 minutes for retraining. Also tested the "train fresh" path to make sure it overwrites the old file properly. Done.

## Git and Binary Files

Added the .keras model files to .gitignore. Read online that you shouldn't commit binary files to git because they bloat the repository - git can't diff them properly so it stores the whole file every time, and model files change every time you retrain. The artifacts folder still exists in the repo for the code that references it, but the actual model files stay local. You just retrain when you clone the project. Makes sense since training only takes a couple of minutes anyway.

One annoying thing - git doesn't track empty folders. So even though the `artifacts/` directory exists on my machine, it wouldn't appear in the repo because all the files inside it are gitignored. Found a Stack Overflow answer that said you can put an empty file called `.gitkeep` inside the folder and git will track that, which keeps the folder in the repo. It's not actually a git feature, just a convention people use. The name doesn't matter but `.gitkeep` is what everyone seems to call it.

## What I Learned

First time using `os.path.exists()` and `os.makedirs()`, both simple but useful for any file management. The `.strip().lower()` thing for checking what the user typed is something I'll probably use in every project from now on. Basically, saving and loading the model turns a 2-minute wait into a 2-second load, which makes development way faster since I'm not sitting through training every time I want to test predictions.

## Wrapping Up

Not the most exciting phase but really useful. Didn't actually write much new code but it makes a huge difference - 2 seconds to load vs 2 minutes to train. Still don't really know what the .keras file looks like internally but it works so I'm not going to worry about it.

Maybe 45 minutes? Wasn't keeping track.

## Notes for Next Phase

Phase 5 is making actual predictions, which means loading a single image, preprocessing it, and getting a digit classification out of the model. Looking forward to actually using this thing instead of just training it.
