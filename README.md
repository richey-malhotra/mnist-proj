# Phase 19: Custom Gradio Theme

## What Changed

- Applied `gr.themes.Soft` as the base theme with blue primary colour (#2E86AB)
- Changed the font to Inter because it looks better than the default
- Customised button colours and text weights with `.set()` chaining
- Updated the app header text while I was at it

Quick visual cleanup. Coming off Phase 18's scatter plot work, the default grey Gradio theme was starting to look out of place next to the Plotly charts. No functional changes at all, purely appearance.

## Choosing a Theme

Gradio has a handful of built-in themes. Tried Default (boring), Monochrome (too stark), Glass (cool but a bit much), and Soft. Soft won - rounded corners and nice shadows - looks good without being over the top. It's the kind of thing you'd see on a real web app rather than a demo page.

## Customisation

Used `gr.themes.Soft(primary_hue="blue", ...)` as the base and customised it:
- Primary colour set to #2E86AB because I wanted something that looked nice without being boring
- Font changed to Inter via a tuple `("Inter", "sans-serif")` - not a plain string like CSS, which tripped me up briefly
- Button backgrounds, hover colours, and text weights tweaked with `.set()` chaining
- Bumped up weights for block titles and labels so headings stand out from body text

The `.set()` chaining after the theme constructor isn't obvious from the docs. Had to look at examples on the Gradio GitHub to figure out the syntax.

## Reflection

This doesn't change any functionality but it makes the app feel way more finished. The difference between a default grey Gradio app and one with actual colours and a proper font is massive. I want it to look decent when someone first opens it, not like I just left everything on default settings.

Should've done it earlier honestly, but it also didn't make sense until the features were mostly in place. I kept putting it off because I was still changing things every phase. About 45 minutes, mostly trying different colour combinations.

## How It Works

### Why Both Hues Are Slate

```python
custom_theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="slate",
    neutral_hue="slate",
    ...
)
```

Both `secondary_hue` and `neutral_hue` are set to `"slate"`. I tried different ones but slate for both looked the cleanest. Secondary is for things like form borders, neutral is for backgrounds. Using the same hue for both keeps everything looking the same, and since I'm the only user most of the controls are always active anyway so it doesn't really matter.

### Hover Colour

```python
button_primary_background_fill="#2E86AB",
button_primary_background_fill_hover="#236B8E",
```

#236B8E is a slightly darker version of #2E86AB. I just picked a colour that looked noticeably darker without being a completely different shade. I just wanted the hover to look obviously different from the normal button without being a totally new colour.

### Font-Weight Scale

```python
block_title_text_weight="600",   # Semi-bold
block_label_text_weight="500"    # Medium
```

600 is semi-bold, 500 is medium. One step heavier than the labels so titles stand out a bit, but neither of them is properly bold. Looks better than making everything bold.

### Loading MNIST Once at Startup

MNIST loads once when the app starts and stays in memory the whole time. Training reuses it without reloading. This does use up memory permanently, but for a local app where it's just me using it, that's way better than reloading and re-normalising 60,000 images every time someone clicks Train.
