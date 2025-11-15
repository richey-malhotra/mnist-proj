# Phase 10: Show Training Progress

## What Changed

- Training function now uses `yield` instead of `return` (Python generators)
- One epoch at a time instead of `model.fit(epochs=N)` all at once
- Epoch-by-epoch progress visible in the UI
- Added `verbose=0` to suppress Keras console output

## The Problem

Phase 8's training gave you no feedback at all - click "Start Training" and the UI completely freezes for 90 seconds. Set 10 epochs and you're just staring at nothing with no idea whether it's working or crashed. Googled "gradio show progress during function" and found the answer: Python generators.

## How Generators Fix It

A normal function runs and returns at the end, but yield lets it send back a value and carry on from where it stopped. Gradio detects generator functions automatically, and each `yield` updates the output component immediately. You don't need to set anything up, just swap `return` for `yield` and it works.

The idea of `yield` pausing a function halfway through and then carrying on was new to me. Had to read the Python docs to understand it properly, but once I got it, it was actually pretty easy to add.

## The Epoch Loop

Instead of `model.fit(epochs=5)` (trains all at once, no control), I loop manually:

```python
all_results = []
for epoch in range(epochs):
    history = new_model.fit(..., epochs=1, verbose=0)
    train_acc = history.history['accuracy'][0] * 100
    all_results.append(f"Epoch {epoch+1}/{epochs}: {train_acc:.2f}%")
    yield "\n".join(all_results)
```

Since `epochs=1`, the history arrays have exactly one element, so `[0]` gets that single value.

The **building-up thing** was important. Each `yield` needs to show ALL previous epochs plus the current one, not just the latest. My first version replaced the text each time so you'd see "Epoch 1: 91%" then it would vanish and become "Epoch 2: 94%". Fixed by keeping a running list and joining everything together on each yield.

`verbose=0` suppresses Keras's own progress bars in the terminal. Since we're showing our own messages in the UI, having Keras also printing clutters things up.

## Testing

Trained with 5 epochs. I clicked the button, immediately saw "Starting training..." appear (confirms it's doing something), then after ~15 seconds the first epoch result appeared, then the second, and so on. Watching accuracy climb epoch by epoch is way more informative than just getting a final number. Can actually see if it's improving or plateauing.

Total training time is the same (each epoch still takes about 15 seconds) but it feels completely different when you can see progress.

Only downside: you can't cancel training once it's started. It runs to completion. At least you know it's working, though.

## The Tricky Bits

### Yielding at Different Points

The generator yields three times basically: once at the start ("Starting training...") so you know the button actually did something, then once after each epoch with the results, and once at the end with a summary after saving. That way the user always has some feedback about what's going on.

### Training Also Prints to the Terminal

Each epoch gets both printed to the terminal and yielded to the UI. The terminal output is useful if I'm debugging and want to see what's happening in the terminal while the app runs.

### The Model Only Saves at the End

```python
# Save model after all epochs (outside the loop)
save_model(new_model, model_path)
```

If training gets interrupted halfway through (like closing the browser), the in-progress model is lost because it only saves after all epochs finish. I could save after each epoch but that seemed like overkill for this.
