# Phase 9 Development Diary

Quick one this. Phase 8's interface worked but everything was stacked in a narrow column down the middle of the screen with loads of wasted space on either side. Looked a bit rubbish on a wide monitor. The Train tab especially - you had controls at the top, a big gap, then results at the bottom, and nothing on either side.

## Layout Fix

Found `gr.Row()` and `gr.Column()` in the Gradio docs. They work by nesting things inside each other. Row puts things side-by-side, Column groups them top-to-bottom inside a Row. The `scale` parameter controls width ratios, so `scale=1` and `scale=2` gives you a one-third / two-thirds split. So it goes Blocks → Tabs → Row → Columns → Components, which makes sense when you look at the actual page.

For the Train tab I put the controls (epochs, batch size, button) in a narrow left column and the results textbox in a wider right column. Makes way better use of the screen. For Predict tab I did a 50/50 split since the image and result need roughly equal space.

Added section headers with `gr.Markdown("**Training Parameters**")` and similar, just bold text to make it clear what each side is for. Also bumped up the textbox line counts since the wider columns make shorter boxes look odd. They had too much horizontal space and not enough vertical.

## Testing

Started the server, checked both tabs. Train tab looks properly laid out - controls grouped on the left, results area on the right. Predict tab has image upload and output side-by-side, which is much more natural than stacked. No scrolling needed now.

One mistake I made was putting the train button outside the Column initially, so it appeared below both columns instead of in the left one. The `with` block nesting controls where stuff goes, so if the button isn't inside the column's `with` block, it ends up outside both columns. Moved it inside and it was fine.

## Thoughts

This was like 12 lines of actual code changes but the visual difference is massive. Same features, just looks way better. The Row/Column system is like a simpler version of Flexbox. Understanding the `scale` parameter took a couple of tries. I just kept changing values until it looked balanced, but it makes sense. Didn't think layout changes would make that much difference, but it looks so much better now.
