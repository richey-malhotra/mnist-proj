# Phase 15: Accuracy Chart

## What Changed

- Added `metrics` table for epoch-by-epoch accuracy data
- Created accuracy chart with Plotly line graph and markers
- Custom Keras callback saves metrics after each epoch
- Extended History tab with chart alongside the training runs table
- Used `.then()` to chain table and chart refreshes from one button

Phase 14 added multi-model prediction comparison. This phase adds a chart to the History tab - specifically an accuracy chart so I can spot patterns like overfitting, where training accuracy keeps rising but validation flattens or drops.

## Database Schema

Needed a new `metrics` table because each training run has multiple epochs. Briefly considered jamming epoch data as JSON into the existing `training_runs` table - like, one big JSON string per row with all the epoch numbers and accuracies crammed in. But then I'd have to parse that string every time I wanted to read it, and you can't really do SQL queries on stuff that's buried inside a JSON blob. Separate table:

```sql
CREATE TABLE IF NOT EXISTS metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER,
    epoch INTEGER,
    train_accuracy REAL,
    val_accuracy REAL,
    FOREIGN KEY (run_id) REFERENCES training_runs(run_id)
);
```

Storing raw Keras floats (like 0.93) and only multiplying by 100 for display. Almost stored percentages directly which would've been inconsistent with everything else. Glad I caught that early.

## The Keras Callback

Used a custom Keras callback class to write metrics after each epoch - my first time writing a Python class. Had to learn about `class`, `self`, `__init__()`, and inheritance (basing my class on an existing Keras one). The class overrides `on_epoch_end()` to save data to the database.

Two bugs:
1. Saved epochs as 0-based (epoch 0, 1, 2…), which looked weird in the chart. Changed to `epoch + 1`.
2. Used `logs.get('acc')` instead of `logs.get('accuracy')` and got NULL values in the database. Had to print out the actual log keys to find the right name. Wasted about 5 minutes.

## Plotly Chart

Started with `px.line` from Plotly Express but switched to `go.Figure()` with manual traces for more control over the layout. Added dots on each data point so you can see individual epochs, and set the hover to show both training and validation values at the same time. The chart only shows the latest training run - considered overlaying all runs but that gets messy with different epoch counts.

If no training data exists, the function returns `None` and Gradio shows a blank plot. Not beautiful but it doesn't crash.

## Wiring the UI

Trickier than expected. Needed the refresh button to update both the table and the chart. Initially tried two separate `.click()` calls on the same button, but only one fired reliably. Found `.then()` in the Gradio docs which chains callbacks in sequence. That fixed it properly.

## Testing

Ran `init_db.py` to create the metrics table (the existing DB doesn't update its tables automatically). Trained MLP for 3 epochs, checked the database in sqlite3 CLI and found 3 rows with sensible values. Chart appeared on refresh, hover matched the DB. Did a second run with 5 epochs to confirm it shows the new run. Deleted the DB and relaunched to test the empty state. Blank chart, no crashes.

Plotly was new to me so it took a while to get my head round it, but now I think I could do more chart stuff without it taking ages.

## How It Works

### Opening a New Database Connection Every Time

Every time a metric gets saved, the code opens a new connection to the database, saves the data, and closes it again. For 20 epochs that's 20 separate connections. I could keep one connection open for the whole training run and that would be faster, but doing it this way means each epoch's data is saved straight away - if something crashes halfway through, the earlier epochs are already in the database.

### Hover Shows All Lines at Once

I set the chart to show both the training and validation accuracy when you hover over a point, not just the nearest one. So hovering over epoch 3 shows both values side by side. Much more useful than having to hover over each line separately.

### Using Lines and Dots Together

Each line on the chart has dots at the actual data points. Without the dots, hovering would try to snap to positions between the real data which isn't helpful. The dots make it clear where the actual epoch values are.

### Returning `None` for Empty Charts

When there's no data yet, the function returns `None` instead of an empty chart. Gradio handles `None` by just showing a blank space, which looks cleaner than an empty chart with axes but no data.

## File Structure

```
gradio_phase15/
├── app_ui.py          # Main UI (420 lines, +70 from Phase 14)
├── utils.py           # Preprocessing function (42 lines)
├── models.py          # Model architectures (unchanged)
├── init_db.py         # Database initialisation (80 lines, +10)
├── requirements.txt   # Dependencies (+plotly)
└── artifacts/
    └── training_history.db
```

## How to Run

```bash
pip install -r requirements.txt  # Now includes plotly
python init_db.py                # Creates metrics table
python app_ui.py
```

## Differences from Phase 14

| Aspect | Phase 14 | Phase 15 |
|--------|----------|----------|
| **History tab** | Table only | Table + accuracy chart |
| **Epoch tracking** | Final accuracy only | Per-epoch train + val accuracy |
| **Database tables** | models, training_runs | + metrics table |
| **Visualisation** | None | Plotly line chart with markers |
| **app_ui.py** | 350 lines | 420 lines (+70) |
