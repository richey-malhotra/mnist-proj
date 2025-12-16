# Phase 16 Development Diary

## What Changed

Added a training time comparison chart. I kept wondering which architecture was actually faster to train and Phase 15's History tab only showed accuracy numbers, nothing about speed. With the timing data already being saved, I built a bar chart to show it properly.

## Duration Tracking

Last phase I added the `duration` column to the database and the timing code in `app_ui.py` — just `time.time()` before and after training, nothing fancy but accurate enough for comparing architectures. This phase is about building a chart from that data so you can actually see the differences.

One thing I had to think about: the run gets inserted into the database before training starts (so metrics can reference the run_id during training via Phase 15's callback), but duration isn't known until training finishes. So I INSERT first with NULL duration, then UPDATE it at the end. Made a mistake with where I put the database UPDATE - it was recording the time after the first epoch finished, not after the whole training run. Took a minute to realise why the durations were all showing as roughly the same regardless of epoch count.

## Bar Chart

Used Plotly bar chart, same approach as Phase 15's accuracy chart. Had to group runs by architecture and average the durations manually since using SQL AVG() with GROUP BY would need a JOIN to get architecture names from the other table, which I'm avoiding. Python loops are easier for me to follow anyway and the result is the same. As expected, MLP comes out fastest, Deeper CNN takes the longest, and Small CNN lands somewhere in the middle. Not exactly surprising but having it on an actual chart makes the differences more concrete than just knowing it roughly.

Extended the `.then()` callback chain from Phase 15 to include this third chart. Three refreshes in sequence off one button press - table, accuracy chart, time chart.

## Testing

Ran a couple of training sessions per architecture, checked the database had duration values (not NULL), confirmed the chart shows correct averages. Forgot to import `time` at first which was embarrassing - one of those errors where you know exactly what's wrong the moment you see it.

Small addition but it finishes off what Phase 15 started. Phase 15 showed how well models learn, this shows how long they take. Together those two pieces of information tell you which architecture is worth using, and looking at the chart, Small CNN seems like the sweet spot for most cases. Having the duration data from last phase made this straightforward — just query, group by architecture, and chart it.
