# Phase 12: Database Schema + Training History Tab

## What Changed

- Created `init_db.py` with SQLite database schema (two tables)
- Each model now saves with a unique filename, so no more overwriting
- Added History tab showing all previous training sessions
- New functions: `save_training_run()` and `get_training_history()`

Phase 11 left an annoying limitation: every time you train, the new model overwrites the old file. Train an MLP, then a CNN - the MLP is gone. This phase fixes that with a proper database.

## Why SQLite

I looked at a few options. First thought was JSON - which stands for JavaScript Object Notation, which is a confusing name because I think it's based on JavaScript syntax but everyone uses it for everything now, it's just a way of storing data in a text file with curly braces and key-value pairs. It's readable and simple but you'd have to load the whole file every time you want to add something, and searching through it would be a pain. CSV was another option but felt too flat for what I needed. Looked at PostgreSQL but that needs a whole server running. SQLite won because it's built into Python (no `pip install` needed), stores everything in a single `.db` file, and you don't need to set up a server or worry about passwords or anything. It's literally just a file in the artifacts folder.

## Database Design

Two tables: `models` tracks which architectures exist, `training_runs` stores each individual run:

```sql
CREATE TABLE models (
    model_id INTEGER PRIMARY KEY AUTOINCREMENT,
    architecture TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE training_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER,
    epochs INTEGER,
    batch_size INTEGER,
    val_accuracy REAL,
    model_filename TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (model_id) REFERENCES models(model_id)
);
```

There's a foreign key linking runs to models. I don't actually use JOINs to query though. I just do two separate queries. For maybe 20-30 training runs total the speed difference is basically nothing. I'd rather keep it simple and have SQL I can actually understand.

## Unique Filenames with MAX(run_id)+1

Instead of everything saving to the same file, each run now gets a unique name like `model_small_cnn_run3.keras`. I needed the run ID *before* inserting to build the filename, so I query `SELECT MAX(run_id) FROM training_runs` and add 1 (defaulting to 1 when there's nothing yet). Architecture names also get tidied up: spaces become underscores, everything lowercase. So "Deeper CNN" becomes `model_deeper_cnn_run3.keras`.

## The Empty DataFrame Problem

When there are zero training runs, `get_training_history()` returns an empty DataFrame. Gradio's `gr.Dataframe` component doesn't handle empty DataFrames well - it shows mangled column names or just looks broken. Had to make sure the column names were explicitly set even when the list of rows is empty.

## History Tab

Simple setup: a Refresh button and a `gr.Dataframe` component. Click refresh and it queries the database and displays every run with its architecture, epochs, batch size, accuracy (as percentage), filename, and timestamp. Ordered newest-first. I went with a manual refresh instead of auto-loading when you switch tabs, which is simpler and means I'm not reading the database for no reason.

## Decisions

### `CREATE TABLE IF NOT EXISTS`

This means I can run `init_db.py` multiple times without it crashing or deleting existing data. Without the `IF NOT EXISTS` bit, running it twice would throw an error saying the table already exists.

### Why Not JOINs?

For the history display, I need to show the architecture name alongside each run, but `training_runs` only stores a `model_id` number. You're supposed to use a JOIN across both tables, but I just loop through the runs and do a separate query for each one to get the name. It's less efficient but for maybe 20-30 training runs the difference is basically nothing, and the SQL is way easier to follow.

### Using `?` Placeholders

```python
cursor.execute('SELECT model_id FROM models WHERE architecture = ?', (architecture,))
```

I used `?` placeholders instead of putting values directly into the SQL string. This stops someone from being able to mess with the database by entering weird text as an architecture name. Probably not a huge risk since the input comes from a dropdown, but we learned about SQL injection in class so I did it properly.

## File Structure

```
gradio_phase12/
├── app_ui.py          # Main application (331 lines, +104 from Phase 11)
├── init_db.py         # Database initialisation script (49 lines, NEW)
├── models.py          # 3 architectures (unchanged from Phase 11)
├── requirements.txt   # Dependencies (unchanged)
└── artifacts/
    ├── training_history.db
    └── model_{arch}_run{id}.keras
```

## How to Run

```bash
python init_db.py      # First time only, creates database
python app_ui.py
```

## Differences from Phase 11

| Aspect | Phase 11 | Phase 12 |
|--------|----------|----------|
| **Model saving** | Overwrites same file | Unique filename per run |
| **Filename** | `mnist_mlp.keras` | `model_{arch}_run{id}.keras` |
| **History tracking** | None | SQLite database |
| **Tabs** | Train, Predict | Train, Predict, History |
| **Database** | None | 2 tables (models, training_runs) |
| **New files** | - | `init_db.py` |
| **app_ui.py** | 225 lines | 331 lines (+104) |
