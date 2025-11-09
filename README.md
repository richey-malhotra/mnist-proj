# Phase 9: Improve UI Layout

## What Changed

- Added `gr.Row` and `gr.Column` for side-by-side layout
- Train tab: parameters on left (narrow), results on right (wide)
- Predict tab: image upload and results in 50/50 columns
- Added section headers with `gr.Markdown` for grouping
- Adjusted textbox line counts for the wider columns

Quick phase - only about 12 lines of actual code change - but the visual difference is massive. Phase 8 had everything stacked in a narrow column down the middle with loads of wasted space either side. Looked rubbish on a wide monitor.

## Layout System

Found `gr.Row()` and `gr.Column()` in the Gradio docs. Row puts things side-by-side, Column stacks them top-to-bottom inside a Row. It's like a simpler version of CSS Flexbox.

The `scale` parameter controls width ratios. For the Train tab I used `scale=1` (controls) and `scale=2` (results) for a one-third / two-thirds split, since the controls are small but the results textbox needs more room. Predict tab is `scale=1` / `scale=1` for 50/50 since the image and prediction need roughly equal room.

So the order goes: Blocks → Tabs → Row → Columns → Components. Had to bump up textbox line counts too because the wider columns made short textboxes look odd with too much horizontal space and not enough vertical.

## A Placement Mistake

Initially put the Train button *outside* the Column's `with` block, so it appeared below both columns instead of in the left one. The `with` block nesting controls where stuff goes - if a component isn't inside a column's context, it ends up outside both columns. Moved it inside the `with gr.Column():` block and it was fine. Easy to get wrong though, especially with multiple levels of nesting.

## Testing

Both tabs look properly laid out now. Train tab has controls grouped on the left, results on the right. Predict tab has image upload and output side-by-side, which feels much more natural than stacked. No scrolling needed. The scale ratios took a couple of tries. I just kept changing values until it looked balanced, but it makes sense.

I didn't think layout would matter that much since no new features got added. But it looks so much better now.

## Layout Notes

### Scale Values

The `scale` parameter works as a ratio, where `scale=1` and `scale=2` gives a one-third / two-thirds split. It doesn't matter what the actual numbers are, just the ratio between them. It resizes with the window too, which is nice.

### Nothing Else Changed

This phase was just layout. Same training function, same prediction function, same everything underneath. I just moved stuff around on screen. All the Phase 8 behaviour (including the prediction model not updating) is still the same.
