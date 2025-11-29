# Phase 12 Development Diary

## Overview

Phase 11 kept overwriting the same model file every time you trained, which was really
annoying - you'd train a nice Deeper CNN and then accidentally lose it by training an MLP
straight after. This phase adds a SQLite database so every training run is saved separately,
and a History tab so you can actually look back at what you've done.

## Why SQLite

Had to decide how to store the training data. My first idea was JSON files - had to Google what that actually stands for and apparently it's "JavaScript Object Notation" which I think means it was originally based on JavaScript syntax, but everyone uses it now regardless. From what I can tell it's basically just a text file with curly braces and stuff like `{"name": "value"}`. It's human-readable which is nice but you'd have to read the whole file in, add your new data, and write the whole thing back out every time. Felt clunky. CSV crossed my mind too but it's too flat for nested data.

Ended up going with SQLite because it doesn't need a server - it's literally just a `.db` file in the artifacts folder. I designed two tables: `models` (architecture names where the ID auto-increments, meaning the database picks the next number automatically so I don't have to keep track of what number comes next) and `training_runs` (each session's epochs, batch size, accuracy, filename, and
timestamp). There's a foreign key linking them - that basically means training_runs has a column called model_id that has to match a real model_id from the models table. So you can't accidentally save a run for a model that doesn't exist, the database would reject it. I'm not actually using it with JOINs but it keeps the data consistent.

## Saving Runs and Unique Filenames

Instead of everything saving to `mnist_mlp.keras`, each run now gets a unique name like
`model_small_cnn_run3.keras`. I had to work out the run ID before inserting, since
AUTOINCREMENT only gives you the ID after the INSERT. I query `MAX(run_id)` and add 1,
defaulting to 1 when NULL. The architecture name also gets cleaned for the filename:
spaces to underscores, lowercased.

That defaulting bit is a one-liner: `next_run_id = 1 if max_run is None else max_run + 1`. Basically an if/else squashed onto one line. Saw it in someone's code on Stack Overflow and it took a second to read but it's just saying "use 1 if there's nothing there yet, otherwise add 1 to the current max". Also figured out you can do `f"{accuracy:.2f}%"` to show a number with exactly 2 decimal places - the `:.2f` bit after the colon controls the formatting. Way better than getting something like 97.23456789 spat out.

The `save_training_run()` function handles all the steps - finding the model_id,
generate the next run_id, build the filename, INSERT into training_runs, and return the
filename. I updated `train_new_model()` to capture the final validation accuracy and pass
it through after training completes.

One thing I read is you should never stick values straight into SQL strings because of something called SQL injection - basically someone could type crafted input that breaks out of the query and runs their own commands on the database. The fix is `?` placeholders, like `cursor.execute("INSERT INTO ... VALUES (?, ?, ?)", (val1, val2, val3))` which means the database treats the values as data, not as SQL. Probably doesn't matter much for a local app where I'm the only user, but the `?` syntax is actually neater than building strings with f-strings anyway so I went with it.

## Gitignoring the Database

Same as the model files from Phase 4, I added the database file to .gitignore as well. It's a binary file that changes every time you train, so there's no point tracking it in git. Anyone cloning the project just runs `python init_db.py` to create a fresh database and then trains their own models. The schema is in init_db.py so the table setup code is always in git even if the actual data isn't.

## Querying Without JOINs

For the history display, I needed to show the architecture name alongside each run, but
training_runs only stores a model_id number. You're supposed to use a LEFT JOIN
across both tables, but I kept it simpler. I loop through the training runs and do a
separate SELECT on the models table for each one to get the architecture name.

It's less efficient, but for a dataset of a few dozen runs at most, the speed difference really doesn't matter. I'd rather keep it simple and have SQL I can actually understand.

## History Tab

I added a third tab with a Refresh button and a read-only `gr.Dataframe`. Clicking Refresh
queries the database, builds something called a pandas DataFrame. First time using pandas - it's a Python library for working with tables of data, had to add it to requirements.txt. A DataFrame is basically a table with rows and named columns, and Gradio's `gr.Dataframe` component can display one directly which is handy. Set up columns like "Run ID", "Architecture",
"Accuracy (%)", and displays it newest-first. I went with a manual refresh rather than
auto-loading on tab switch, which is simpler and means I'm not hitting the database for no reason.

One problem: an empty DataFrame with no columns looks broken in the UI. Had to pass explicit
column names even when there are no runs yet.

## Testing

Trained an MLP and a Small CNN (3 epochs each), checking the database after each with the
sqlite3 command line. Both appeared with correct accuracy, unique filenames, and the .keras
files existed in artifacts. The History tab showed both runs newest-first with correct data.
Trained a Deeper CNN and refreshed to confirm it kept accumulating properly.

## Reflection

This isn't the most exciting phase - database stuff isn't as interesting as Phase 11's
CNNs - but it's actually useful. Being able to look back at all your training runs and see which settings worked best is really useful. And no more
accidentally losing a good model by overwriting it.

I know avoiding JOINs isn't how you'd do it properly, but it was simpler
and it works fine here. If this ever needed to handle thousands of runs I'd switch to a
JOIN, but realistically we're talking about maybe 20-30 training runs total.
