# Phase 19 Development Diary

Quick one today - applied a custom theme to make the app look less like a default Gradio demo and more like something you'd actually want to use. Coming off Phase 18's scatter plot work, the default grey theme was starting to look out of place next to the Plotly charts.

## Choosing a Theme

Gradio has a handful of built-in themes. I tried Default (boring), Monochrome (too stark), Glass (cool but a bit much for this project), and Soft. Soft won because it has rounded corners and nice shadows - looks good without being over the top. It's the kind of thing you'd see on a real web app rather than a demo page.

## What I Changed

Went with `gr.themes.Soft` as the base and customised the primary colour to a blue (#2E86AB) because I wanted something that looked nice without being boring. Changed the font to Inter, which is a clean-looking font that works for everything. Also bumped up the text weights for block titles and labels so headings and labels actually stand out from the body text.

Applied the theme to `gr.Blocks()` and updated the header text while I was there. Nothing complicated code-wise.

## Problems

Surprisingly few. The font parameter syntax is a tuple not a string (`("Inter", "sans-serif")`) which tripped me up briefly - I thought it would be just a string like CSS. The button colour customisation uses `.set()` chained after the theme constructor, which isn't obvious from the docs. Had to look at examples on the Gradio GitHub to figure that out.

## Reflection

Purely cosmetic but it makes such a difference. Before this the app looked like every other Gradio demo you see online - grey everything, default font. Now it actually looks like something I put effort into. Probably should of done this earlier but I kept telling myself features matter more than looks.

In hindsight I wish I'd themed it sooner, but there wasn't much point when I was still adding and rearranging things every phase. At least now the features are mostly settled and I can style it properly without redoing the work later.

About 45 minutes. Most of that was trying different colour combinations until #2E86AB looked right.
