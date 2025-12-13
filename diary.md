# Phase 15 Development Diary

## What I Was Doing

Adding accuracy charts to the History tab. Phase 12 introduced the History tab with a table of training runs, and it worked fine but it was just numbers - wanted to actually see how accuracy changes per epoch so I could spot patterns like overfitting.

## Schema Extension

Needed a new `metrics` table because each training run has multiple epochs. I briefly thought about storing epoch data as a JSON string inside the existing training_runs table - still not totally comfortable with JSON if I'm honest, the whole format feels a bit fiddly with all the braces and quotes. But more importantly you wouldn't be able to query individual epochs with SQL, you'd just have this big blob of text to deal with. Separate table with run_id, epoch, train_accuracy, val_accuracy. Straightforward.

One decision I'm glad I made early: store raw floats from Keras (like 0.93) and only multiply by 100 for display. Almost stored percentages directly which would've been inconsistent with everything else.

## The Callback

Used a custom Keras callback to write metrics to the database after each epoch. This was my first time writing a Python class from scratch, so I had to look up basically everything. The syntax goes:

```python
class MetricsCallback(keras.callbacks.Callback):
    def __init__(self, run_id):
        super().__init__()
        self.run_id = run_id

    def on_epoch_end(self, epoch, logs=None):
        # save metrics to database here
```

Had to look up every part of this.

`class MetricsCallback(keras.callbacks.Callback)` means I'm creating a new type of thing called MetricsCallback that's based on Keras's existing Callback class. The bit in brackets is inheritance - my class gets all the built-in callback behaviour and I just change the specific parts I care about.

`__init__` is the setup function that runs when you first create one of these objects. The double underscores mean it's a special Python method, not something you'd normally name yourself. `self` is how the object refers to its own data - so `self.run_id = run_id` saves the run ID inside the object so the other methods can use it later. And `super().__init__()` calls the parent class's setup so I don't accidentally break whatever Keras needs to do internally.

`on_epoch_end` is a method I'm overriding - the parent Callback class already has this method but it does nothing by default. By writing my own version, I'm saying "when an epoch finishes, do this instead". Keras calls it automatically during training, which is the same callback idea from Phase 6 - I'm not calling this function myself, Keras calls it for me at the right time.

Honestly the class syntax felt really heavy for what's basically "run this code after each epoch". But I think it makes sense because Keras has loads of different hooks (start of training, end of epoch, end of batch, etc.) and a class keeps them all organised together.

Actually ended up not using the callback class — since I'm already training one epoch at a time from Phase 10, I can just call `save_epoch_metrics()` directly in the loop after each epoch. Simpler and it already works. But glad I learned how callbacks work, it'll probably be useful eventually.

First version saved epochs as 0-based (epoch 0, 1, 2...) which looked weird in the chart. Changed to +1 so it starts at 1 like a normal person would expect.

Also hit an annoying Keras problem - used `logs.get('acc')` instead of `logs.get('accuracy')`. Got NULL values in the database until I printed out the actual log keys and found the right name. Wasted about 5 minutes on that.

## Plotly Charts

Started with `px.line` from Plotly Express but switched to `go.Figure()` with manual traces because I wanted more control over the layout. Added markers on each data point so you can see individual epochs clearly, and unified hover so training and validation appear together.

The chart only shows the latest training run for now. Considered showing all runs overlaid but that gets messy with different epoch counts. Might add a dropdown for run selection in a future phase but keeping it simple for now.

## Wiring It Up

The UI part was trickier than expected. Had the refresh button triggering two updates (table + chart) and initially tried two separate `.click()` calls on the same button. Only one seemed to fire reliably. Found `.then()` in the Gradio docs which chains callbacks in sequence - that fixed it properly.

If there are no training runs yet, the chart function just returns None and Gradio shows a blank plot. Not beautiful but it doesn't crash.

## Testing

Ran init_db.py to create the metrics table (had to do this manually since the existing DB doesn't add new columns on its own). Trained MLP for 3 epochs, checked the database in sqlite3 CLI - 3 rows with sensible values. Chart appeared on refresh, hover matched the DB values. Did a second run with 5 epochs to confirm it shows the new run not the old one.

Deleted the DB file and relaunched to test the empty state - blank chart, no crashes.

Hit a bunch of small mistakes - saved epochs as 0-based instead of 1-based, used the wrong Keras log key (`acc` instead of `accuracy` which gave me NULL values), forgot to import plotly, displayed raw floats on the y-axis instead of percentages. All tiny things but they add up. Writing them down so I remember they're normal.

## End of Session

This makes the app feel properly useful. Seeing validation accuracy flatten while training accuracy keeps rising actually tells you something useful - without the chart I'd miss that pattern completely. The chart is basic but it gets the point across, which is all it needs to do.

About 3 hours, mostly Plotly. Hadn't used it before.

Phase 16 might add more chart types or the ability to compare runs visually.
