# Phase 13 Development Diary

## What This Phase Was

Not a lot of new code here. Phase 12 built the database and the History tab, and this phase was about actually testing it properly. I'd only tested with one training run before, so I wanted to make sure it works when you train multiple different architectures and the data accumulates correctly.

## Testing the History Tab

Trained one of each architecture (MLP, Small CNN, Deeper CNN) with 3 epochs each. After each training run, went to the History tab and clicked Refresh. Everything showed up right: architecture name matches what I picked, epochs and batch size are correct, accuracy is displayed as a percentage, and each model got its own unique filename.

The ordering is newest-first, which makes sense. You want to see your most recent run at the top.

## Empty State

Deleted the database file and relaunched the app. The History tab shows the column headers but no data rows, which looks fine. No crashes, no weird error messages. When I trained a model and refreshed, it appeared immediately.

## Small Things I Noticed

The timestamps show the full format (date and time down to the second) which is a lot of detail for something where you probably just care about "which run was this". Not going to change it now but if I had time I'd make it show something simpler.

The manual Refresh button is a deliberate choice. I could have it auto-refresh when you switch tabs but that means hitting the database every time someone clicks around, which seemed wasteful. This way it only queries when you actually want to see the data.

Short phase but worth doing. It's easy to build something and assume it works without properly testing the different states (empty, one run, multiple runs). Everything checked out. 

About 40 minutes, mostly just waiting for models to train.
