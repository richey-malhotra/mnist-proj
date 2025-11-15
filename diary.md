# Phase 10 Development Diary

## The Problem

Phase 8's training gave you no feedback - hit the train button and the whole page just locks up for 90 seconds with no way of telling if it's working or crashed. If you set 10 epochs you're just staring at nothing for ages. Needed a way to show progress after each epoch.

## Discovering Generators

The fix was Python generators. Googled "gradio show progress during function" and found that if your function uses `yield` instead of `return`, Gradio automatically treats it as a stream, and each `yield` updates the output component immediately.

Basically a normal function runs and returns at the end, but with yield the function can send back a value and then keep going from where it left off.

Gradio detects this automatically so you don't have to configure anything special. Just change `return` to `yield` and it works. Brilliant.

## How I Did It

The trick is to train one epoch at a time in a loop instead of calling `model.fit(epochs=5)` all at once. Each iteration trains a single epoch with `model.fit(epochs=1)`, grabs the accuracy from `history.history['accuracy'][0]` (just one value since we only did one epoch), and yields a progress message.

Had a bug initially where each yield *replaced* the previous text. So you'd see "Epoch 1: 91%" then it would change to "Epoch 2: 94%" and Epoch 1 would vanish. Fixed it by keeping a running list and yielding the entire thing joined together each time. Now the output builds up:
- Yield 1: "Epoch 1/5: Train=91.2%, Val=90.5%"
- Yield 2: "Epoch 1/5: ... \n Epoch 2/5: Train=94.6%, Val=93.2%"
- And so on

Also added `verbose=0` to suppress Keras's own training output in the console. We're showing our own messages now, so having Keras print progress bars as well just clutters things up.

## Testing

Started the server and trained with 5 epochs. Clicked the button, immediately saw "Starting training..." appear (nice, confirms it's doing something). Then after about 15 seconds the first epoch result appeared. Then the second. Then the third. Watching the accuracy climb epoch by epoch is way more informative than just getting a final number. Can actually see if it's improving or plateauing.

Tried with 3 epochs and 10 epochs too, and it works smoothly. The total time is the same (each epoch still takes 15ish seconds) but it feels completely different when you can see progress.

## What I Learned

Generators are really useful for this. Swapping return for yield meant the function could send updates as it went along. Doing it one epoch at a time means I could add stuff later, like stopping early if accuracy stops going up. And building up all the results instead of just showing the latest one is important so you can see the whole thing.

The idea of yield stopping a function halfway and then carrying on was new to me. Had to read the Python docs to properly understand it. But once I got it, it was actually pretty easy. Like five extra lines of code and it makes things so much better.

Simpler than expected once I understood generators. The code's a tiny bit more complicated now but being able to see progress is worth it. No more frozen screens.

Only downside is you can't cancel training once it's started - it runs to completion. But at least you know it's working.

About an hour and a bit, most of which was reading about generators.
