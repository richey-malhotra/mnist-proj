# Test 4: Training History Database

**Date:** 1st December 2025  
**Phase tested:** Phase 12-13 (SQLite database + history tab)  
**What I'm testing:** that every training run gets saved to the database and shows up in the history tab

## Setup

1. Open terminal, activate venv
2. Run `python app_ui.py`
3. Open localhost:7860

## Steps to show

| Step | What to do on screen | What to say |
|------|---------------------|-------------|
| 1 | Click the History tab | "The history tab shows all previous training runs. It pulls from an SQLite database that gets updated each time you train." |
| 2 | Show the existing rows in the table | "So you can see the runs I've already done — it shows the architecture, how many epochs, the accuracy, and when it was trained." |
| 3 | Go back to Train tab, train a Small CNN with 3 epochs | "Let me train another model quickly so we can see it appear in the history." |
| 4 | Wait for training to finish | "OK, that's done." |
| 5 | Go back to History tab, click Refresh | "Now if I go back to history and hit refresh..." |
| 6 | Point at the new row that appeared | "...there it is at the bottom. It saved the run automatically with all the details." |
| 7 | Show the database file in the filesystem (artifacts/training_history.db) | "The actual data lives in an SQLite file here. SQLite is basically a database in a single file — no server needed." |

## Expected vs Actual

| Thing being checked | Expected | Actual |
|---|---|---|
| History tab loads existing runs | Shows table of past runs | Yes, 6 previous runs visible ✓ |
| Table shows correct columns | Architecture, epochs, accuracy, date | All columns present ✓ |
| New training run appears after refresh | New row in history | Yes, appeared after clicking Refresh ✓ |
| Data persists after restarting app | Runs still there after restart | Restarted app, all history still there ✓ |
| Database file exists | training_history.db in artifacts/ | Yes, 28KB file ✓ |

## Notes

I also tested that the history survives closing and reopening the app, which it does because it's reading from the .db file not memory. One thing I noticed is you have to click Refresh manually — it doesn't auto-update when you come back to the tab. Could improve that later but it works.
