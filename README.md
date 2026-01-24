# Phase 22: Code Comments and Documentation

## What Changed

- Proper docstrings on all functions across three Python files
- Section markers (`# ===`) to split up the big files so I can find things
- Inline comments explaining **why** not **what**
- The docstring format I found in tutorials, with Args, Returns, and custom sections
- +210 lines of documentation, nothing actually changed in how the app works

Honestly expected this to be boring. It wasn't boring exactly, but it took way longer than I thought. Writing documentation for 900+ lines took ages because I had to actually understand what everything does well enough to explain it. I found that way harder than I expected.

## app_ui.py (~935 → ~1030 lines, +~95)

The big one. First thing was section markers, those `# ===` dividers splitting the file into DATA LOADING, DATABASE FUNCTIONS, TRAINING, PREDICTION, CHARTS, UI LAYOUT. Before this I had to Cmd+F for function names. Now I can just scroll.

The most important docstring was probably `save_training_run()` because it changes the database in ways you wouldn't guess from the function name. Added a custom "Database Changes" section. I made that up because I thought if the function is doing stuff to the database that you can't tell from the name, I should probably write that down.

Also documented `get_training_history()` with a note about using sequential queries instead of JOINs. The actual reason: sequential queries are simpler to debug and I can follow each one on its own. JOINs would probably be faster but with like 50 rows it honestly doesn't matter.

For `train_new_model()` I used "Yields" instead of "Returns" because it's a generator (Phase 10). Small thing but the distinction matters since it's a generator not a normal function.

## models.py (170 → 229 lines, +59)

Added a module header comparing all three architectures: accuracy, speed, when you'd pick each one. Each `create_` function now has the full layer-by-layer breakdown with expected parameter counts. If I forget why I picked one architecture over another I can just check the docstring.

## utils.py (42 → 100 lines, +58)

Short file but the preprocessing steps are important, so numbered step comments:

```python
# Step 1: Convert to PIL Image (handles numpy arrays from Gradio)
# Step 2: Resize to 28×28 (MNIST standard)
# Step 3: Convert to greyscale (the 'L' just means grey, I had to look it up)
# Step 4: Normalise to 0-1 range
# Step 5: Add batch dimension (models expect [batch, height, width])
```

The batch dimension one is worth spelling out because it properly confused me in Phase 5.

## How I Wrote the Comments

Used the docstring format I kept seeing in tutorials, the one with `Args:`, `Returns:`, indented descriptions. Tried to say why I did things a certain way instead of just repeating what the code already says. Like there's no point writing `# add 1 to x` next to `x = x + 1` but if it's `# skip header row` then that's actually useful. For inline comments, things that aren't obvious just from reading the code, like database queries, numpy operations, Gradio quirks. Didn't comment basic Python.

## Line Count Impact

| File | Phase 21 | Phase 22 | Change |
|------|----------|----------|--------|
| app_ui.py | ~935 | ~1030 | +~95 |
| models.py | 170 | 229 | +59 |
| utils.py | 42 | 100 | +58 |
| **Total** | | | **+210 lines** |

## Testing

Ran `python -c "import app_ui"` (and models, utils) to check no docstrings broke the syntax. Tested `help(models.create_mlp)` in the REPL and the formatted output looks right.

## Reflection

Writing the comments made me actually go through my own code properly. Found a couple of places where I'd done something for a reason I'd already half-forgotten - now it's written down. That's really the point: if I come back to this in a few months I'll have no idea what anything does otherwise. Took about 3 hours. Documentation took way longer than I expected.

## Why I Did It This Way

### Some Functions Got Better Docs Than Others

Only `create_mlp()` got the full treatment with parameters, expected accuracy, and layer shapes. The CNN functions got shorter descriptions even though they're more complex. The MLP was the first one I documented so I spent the most time on it. The CNN docstrings just reference the MLP one where the patterns are the same.

### `predict_with_validation()` Has a Rubbish Docstring

It's a 150-line function that does about five different things: input validation, preprocessing, calling multiple models, building a table, error handling. The docstring is two lines. I left it because I just couldn't work out how to summarise it properly, which probably means the function itself is too big and should be split up. Might need to revisit that.

### The Step Comments Are in the Wrong Order

The `utils.py` comments say resize then greyscale, but doing greyscale first would actually be faster because then the resize only works on one colour channel instead of three. It doesn't affect the result either way, but I noticed it while documenting and didn't want to change the code in a phase that's just supposed to be documentation.

### Leftover `preprocess_image` in models.py

`utils.py` and `models.py` both have image preprocessing code. The one in `utils.py` is the one that actually gets used. The one in `models.py` is left over from before I created `utils.py`. It never gets called. I just documented it rather than deleting it since this phase was supposed to be documentation only, not code changes.

## Differences from Phase 21

| Aspect | Phase 21 | Phase 22 |
|--------|----------|----------|
| **Function docstrings** | Basic (1-2 lines) | Detailed (10-20 lines) |
| **Inline comments** | Minimal | Extensive with reasoning |
| **Section markers** | None | Clear sections throughout |
| **Total lines added** | - | +210 (documentation only) |
