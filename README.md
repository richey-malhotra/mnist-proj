# Phase 21: Empty State Messages + UI Polish

## What Changed

- Added empty state messages to all History tab charts
- Fixed return value bug in predict function (3 vs 4 values)
- Fixed consensus logic firing with only one model
- Added a little intro message to Train and Predict tabs for new users

This grew from a 30-minute task to about 2.5 hours because testing the empty states kept turning up more stuff to fix. Kind of annoying but that's what this phase was for.

## Empty State Charts

Instead of returning `None` (blank chart), empty-data paths now return a Plotly figure with a centred annotation:

```python
fig.add_annotation(
    text="No training history\n\nTrain a model to see charts!",
    xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False
)
```

Used `xref="paper"` coordinates so the text sits at (0.5, 0.5) regardless of axis ranges. Grey text for empty states, red for errors. Hidden axes since they'd just show 0-1 with no data.

## Bug Fixes Found Along the Way

**Return value count**: Phase 20's predict function had some if/else branches returning 3 values while callbacks expect 4 (original image, preprocessed image, dataframe, consensus text). Gradio threw a `ValueError` every time you hit an error condition. Fixed every if/else path to return all 4 values with an empty DataFrame for errors.

This bug was probably there since Phase 20 but I never hit the exact conditions to trigger it until now. I wasn't even looking for this bug, just stumbled on it while testing the empty states.

**Consensus logic**: Was firing even with one model - training a single MLP and predicting would show "All models agree!" which is technically true but meaningless. Added `len(clean_preds) >= 2` check.

## What You See on First Launch

Also noticed the Train and Predict tabs had the same blank-screen problem on first launch. Train tab now shows a guide with the three architectures and rough training times. Predict tabs show "Waiting for input..." pointing to the upload/draw area. Prevents the "what am I supposed to do?" moment.

## Testing

Wiped the database and tested fresh launch - every tab has clear guidance. Trained a couple of models, verified empty states disappear once there's real data. Checked predict function with various error conditions to confirm the 4-tuple fix. Tested with just one trained model for the consensus check.

I'd been skipping this stuff while I was building features but it actually makes a massive difference to how finished it feels.

## Decisions

### Centring the Message When There's No Data

```python
xref="paper", yref="paper", x=0.5, y=0.5
```

Using `"paper"` coordinates means 0.5 is always the middle of the chart, no matter what the axes say. For an empty chart with no data, the axes don't mean anything anyway. If I used normal x/y coordinates the text would end up in a weird position.

### Same Chart Height Whether Empty or Not

Both the empty-state charts and the ones with actual data use `height=400`. If they were different heights, the page would jump around when switching between empty and filled charts which would look janky.

### All DataFrame Columns as Strings

Even though confidence is a number, I format it with a `%` sign (like `"93.4%"`). So I set all the column types to `"str"` to stop Gradio trying to do number sorting on something that has a percentage sign in it.

### Chaining Updates With `.then()`

The predict button uses `.then()` so the chart refreshes after the prediction finishes. If they ran at the same time the chart might not have the latest data because the prediction hasn't saved to the database yet. `.then()` makes them run one after the other.

## How to Run

```bash
python init_db.py
python app_ui.py
```

On first launch, every tab now shows guidance instead of blank space.
