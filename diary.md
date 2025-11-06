# Phase 8 Development Diary

## The Big Structural Change

Phase 7's prediction-only setup worked fine, but now I need both training AND prediction in the same app. Checked the Gradio docs and `gr.Interface` literally can't do this - it's designed for one function with one set of inputs/outputs. For anything more complex you have to use `gr.Blocks`, which works totally differently.

The syntax change took some getting used to. Instead of passing your function to gr.Interface(), you define components inside a `with gr.Blocks()` context and then wire them up with `.click()` event handlers afterwards. Tabs are just `with gr.Tab("Name"):` blocks nested inside. Looks a bit weird with all the nested `with` statements but it sort of matches how the page looks. Blocks contains Tabs, Tabs contain Components.

I've used `with` before for opening files but Gradio uses it differently - everything you create inside `with gr.Tab("Train"):` automatically goes inside that tab. When the `with` block ends, that tab is done. So the nesting in the code sort of matches the nesting on the page, which is quite nice once you notice it. Felt weird at first using `with` for something that isn't a file though.

The wiring is done with `.click()` - you go `button.click(fn=train_function, inputs=[...], outputs=[...])` and that's it, clicking the button calls your function. Same callback idea as the `fn=` thing from Phase 6 but now it's tied to a specific button rather than the whole page.

## What I Built

Two tabs: Train and Predict. Train tab has number inputs for epochs and batch size (with `gr.Number`, which lets you set a min and max so users can't enter daft values), a button, and a results textbox. Predict tab is basically Phase 7's code moved into a tab wrapper. The train function creates an MLP, trains it on MNIST, saves to artifacts/, and returns the final accuracy. See app_ui.py for all the details.

One efficiency thing: I moved the MNIST data loading out of the training function to the top of the file. Otherwise it would reload the dataset every time you click train, which is wasteful. Now it loads once at startup and training starts immediately. Small change but it makes repeated training runs much snappier.

Also discovered `variant="primary"` makes buttons blue instead of grey, and `gr.Markdown()` lets you add formatted headers. Small things but they make it look more organised than just everything piled up.

## Same Bloody Bug

The `api_name=False` thing from Phase 7 came back. Same crash: `TypeError: argument of type 'bool' is not iterable` in gradio_client when the browser tries to load the page. Had to add `api_name=False` to both button click handlers. At least this time I knew the fix immediately instead of spending ages debugging it. Still annoying that it affects gr.Blocks too though. I assumed it was an Interface-specific thing.

Also hit a type conversion issue. `gr.Number` returns floats but `model.fit()` wants integer epochs. Quick `int()` cast sorted it. And at one point I had three Gradio servers running on different ports because I kept forgetting to kill the old ones before restarting. Had to `pkill` everything and start fresh. Need to get in the habit of Ctrl+C before re-running.

## Testing

Ran the app, trained an MLP for 3 epochs from the UI. Took about 90 seconds, got ~97% accuracy - same as the command-line version in Phase 3. Switched to Predict tab after training, uploaded a test image, prediction still works. The main issue is there's no progress bar during training, so the UI just sits there for 90 seconds looking frozen. Needs fixing but that's a later phase.

## Reflection

Bigger jump than I expected. Phase 7 was about 80 lines, this is over 200. But actually feels like a real app now. You've got training and prediction in proper tabs. gr.Blocks needs more code but you can do way more with it.

Training from a web browser instead of a terminal is satisfying. Click a button, wait, see results. It's the same code underneath but it feels completely different. Frozen screen during training really needs fixing tho.
