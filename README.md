# Phase 8: Tabbed Interface with gr.Blocks

## What Changed

- Migrated from `gr.Interface` to `gr.Blocks`
- Added two tabs: Train and Predict
- MNIST data loads once when the app starts instead of every click
- Added `variant="primary"` for blue buttons and `gr.Markdown` headers

The app went from just doing predictions to something that actually feels useable - you can train a model and test it without touching the terminal.

## Why gr.Blocks?

Phase 7 used `gr.Interface`, which is designed for one function with one set of inputs/outputs. I need both training AND prediction, and Interface literally can't do that. `gr.Blocks` is the answer. It's a different way of building the UI where you put components inside `with` blocks and then connect button clicks to functions afterwards.

The syntax took some getting used to. Instead of passing a function to a constructor, you nest everything in `with` statements:

```python
with gr.Blocks() as demo:
    with gr.Tab("Train"):
        # training components here
    with gr.Tab("Predict"):
        # prediction components here
```

Looks a bit weird with all the nested `with` statements but it kind of matches how the page is laid out: Blocks contains Tabs, Tabs contain Components. You connect button clicks with `button.click(fn=..., inputs=[...], outputs=[...])` after the components are defined.

The jump from ~80 lines (Phase 7) to 194 lines feels big, but most of it is just setting up the buttons and layout.

## Loading Data Once at the Start

Moved MNIST loading out of the training function to the top of the file. Otherwise it would reload the data every time you click Train, which is wasteful and slow. Now it loads once at startup and training starts immediately. Only a small change but it makes a big difference if you're training multiple times.

## Same Bug, Again

The `api_name=False` crash from Phase 7 came back. Same `TypeError: argument of type 'bool' is not iterable`. Had to add it to both button click handlers. At least this time I knew the fix immediately instead of spending ages debugging. Still annoying that it affects Blocks too. I assumed it was Interface-specific.

Also hit a type conversion issue: `gr.Number` returns floats but `model.fit()` wants integer epochs. Quick `int()` cast sorted it.

And at one point I had three Gradio servers running on different ports because I kept forgetting to kill the old ones before restarting. Had to `pkill` everything and start fresh. Need to get in the habit of Ctrl+C before re-running.

## Testing

Trained an MLP for 3 epochs from the UI - ~90 seconds, got ~97% accuracy, same as Phase 3's command-line version. Switched to Predict tab, uploaded a test image, prediction still works. The main issue is the UI looks frozen during training. It just sits there for 90 seconds with no feedback. That needs fixing but it's a later phase problem (Phase 10).

## Things Worth Explaining

### Default Values for the Controls

```python
epochs_input = gr.Number(label="Epochs", value=3, minimum=1, maximum=20, step=1)
batch_size_input = gr.Number(label="Batch Size", value=32, minimum=16, maximum=128, step=16)
```

Epochs defaults to 3 because that's enough for the model to learn on MNIST without taking forever. Max is 20 because it doesn't really improve much beyond that. Batch size defaults to 32 because that's what the tutorials use, and I set min/max so users can't enter something silly.

### The Prediction Model Doesn't Update

The prediction tab loads the model once when the app starts. So if you train a new model, the prediction tab is still using the old one until you restart the app. I know about this but I'll fix it in a later phase.

## File Structure

```
gradio_phase8/
├── app_ui.py          # Main application (194 lines)
├── models.py          # Model architectures (92 lines)
├── requirements.txt   # Dependencies (unchanged)
└── artifacts/
    └── mnist_mlp.keras
```

## How to Run

```bash
pip install -r requirements.txt
python app_ui.py
```

App opens on http://localhost:7860 with Train and Predict tabs.

## Differences from Phase 7

| Aspect | Phase 7 | Phase 8 |
|--------|---------|---------|
| **UI framework** | `gr.Interface` (single function) | `gr.Blocks` (multi-component) |
| **Features** | Prediction only | Training + prediction |
| **Input method** | Image upload | Image upload + number inputs |
| **Tabs** | None | Train, Predict |
| **Lines of code** | ~80 | 194 (+~114) |
| **Data loading** | Inside function | Once at startup |
