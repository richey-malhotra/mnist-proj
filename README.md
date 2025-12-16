# Phase 16: Training Time Comparison Chart

## What Changed

- Added `time.time()` timing to measure training duration
- Extended `training_runs` table with a `duration` column
- Created bar chart showing average training time by architecture
- Extended `.then()` callback chain to refresh all three History items from one button

I kept wondering which architecture was actually faster to train. Phase 15's History tab only showed accuracy numbers, nothing about speed. This phase answers that question properly.

## Duration Tracking

Added a `duration` column to the existing `training_runs` table using ALTER TABLE. Wrapped it in try/except so it doesn't break if the column already exists. Thing is, databases from Phase 12-15 won't have this column, so it has to handle old databases that don't have this column yet.

The timing is just `time.time()` before and after training. One thing I had to think about: the training run gets inserted into the database *before* training starts (so Phase 15's metric callback can reference the run_id), but duration isn't known until training finishes. So I INSERT first with NULL duration, then UPDATE it at the end.

Initially had the UPDATE in the wrong place - it was capturing the time after just the first epoch instead of all of them. Moved it to after the full training loop. Also forgot to `import time` at first, which was embarrassing. One of those errors where you know exactly what's wrong the moment you see it.

## The Bar Chart

Used Plotly bar chart, same approach as Phase 15's accuracy chart. Had to group runs by architecture and average the durations manually. The results are what you'd expect: MLP trains fastest, Deeper CNN slowest, Small CNN in between. Being able to actually see it is nice though.

Looking at the chart, Small CNN seems like the sweet spot for most cases - you get most of the accuracy improvement without taking as long as the Deeper CNN to train.

Extended the `.then()` chain from Phase 15 to include this third chart. Three refreshes in sequence off one button: table → accuracy chart → time chart.

## Testing

Ran a couple of training sessions per architecture, verified the database has duration values (not NULL), confirmed the chart shows correct averages. Deleted old runs to test the empty state, and it returns None without crashing.

## Decisions

### Why `time.time()`

`time.time()` measures real elapsed time, meaning the actual seconds you sit there waiting. There's another option (`time.process_time()`) that only counts CPU time, but that felt misleading. If training takes 90 seconds of real time, that's what matters to the person using the app, even if the CPU was only busy for 60 of those seconds.

### Inserting Before Training Finishes

The training run gets added to the database before training actually starts, because the per-epoch metrics (from Phase 15) need a run ID to link to. But the total duration isn't known until training finishes. So I INSERT first with a placeholder duration, then UPDATE it with the real time at the end. There's a brief moment where the database has an inaccurate duration, but nobody sees it because the History tab needs a manual refresh.

### Averaging With Dictionaries

```python
arch_times = {}
for arch, duration in data:
    arch_times[arch] = arch_times.get(arch, 0) + duration
    arch_counts[arch] = arch_counts.get(arch, 0) + 1
```

I'm computing averages manually with dictionaries instead of using SQL's `AVG()` or pandas. Partly because the SQL version would need a JOIN which I'm trying to avoid, and partly because I find Python loops easier to follow than complex queries. It's more code but I can actually read it.

### Sorting the Bars

Architectures are sorted alphabetically so the bars always appear in the same order (Deeper CNN, MLP, Small CNN) no matter what order they were trained in. Otherwise the chart could rearrange itself between refreshes which would be confusing.
