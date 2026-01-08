# Phase 18: Training Time vs Accuracy Chart

## What Changed

- Replaced Phase 16's bar chart with a scatter plot showing accuracy vs training time
- Each architecture gets its own colour (MLP=blue, Small CNN=orange, Deeper CNN=green)
- You can hover over each dot to see the exact numbers for that run
- Each point is one training run, not an average

The bar chart from Phase 16 averaged everything together, which hid how different each run actually was. A scatter plot shows each run as a separate point so you can see patterns and outliers.

## What It Shows

The results are really interesting. MLP runs cluster bottom-left (fast, 95-96%), Deeper CNN goes top-right (slow, ~98.5%), Small CNN sits in the middle. Looking at it, Small CNN is probably the best trade-off for most situations - you get most of the accuracy improvement for a fraction of the extra training time. Would not have noticed that pattern just from reading numbers in a table.

The dots for each architecture aren't all in the exact same spot either. The same architecture trained twice doesn't always give exactly the same result. The randomness in weight initialisation and batch ordering means each run is slightly different. Expected, but seeing it visually makes it more real.

## How I Built It

Plotly doesn't do colouring each architecture differently easily in a single trace, so the code loops through architectures and adds a `go.Scatter()` for each one. More code than I'd like but it gives full control over colour and legend labels.

Plotly's `hovertemplate` is fiddly - the formatting syntax is different from Python f-strings, but once it works it's really nice for exploring the data interactively.

## Problems

Old training runs from before Phase 16's duration tracking existed have NULL duration values, which crash the chart. Added a `WHERE` clause to filter those out. Also had to sort the architecture list before creating traces otherwise the legend order was random each time, which looked messy.

## Testing

Trained across all three architectures, confirmed points appear in the right places. Hover works. Refresh button updates the chart alongside the other two. No crashes with empty data.

## Things Worth Explaining

### Different Hover Behaviour From Phase 15

Phase 15's line chart shows all values at the same x-position when you hover. This scatter plot just shows the nearest point instead. Makes sense because the line chart has multiple lines sharing the same x-axis (epochs), so you want to compare them. The scatter plot has dots scattered everywhere so you just want to see whichever one you're closest to.

### Hiding the Extra Hover Box

```python
hovertemplate='%{text}<extra></extra>'
```

I had to look this up. The `<extra></extra>` bit removes a second tooltip box that Plotly adds by default showing the trace name. Without it, every hover would show the architecture name twice: once in my custom text and once in Plotly's default box. Took me a while to find this in the Plotly docs.

### White Borders on the Dots

Each dot has a white border (`line=dict(width=2, color='white')`). This makes it easier to see individual dots when they're close together, because without it, overlapping same-colour dots merge into an indistinct blob. `size=10` is large enough to click on but not so big that they cover each other up.

### Fallback Purple for Unknown Architectures

```python
color_map.get(arch, '#9467bd')  # Default purple
```

If a new architecture is added without updating the colour map, it gets purple instead of crashing with `KeyError`. Just in case I add more architectures later.

### Why I Used Separate Lists

The chart is built from four parallel lists (architectures, accuracies, durations, colours). A pandas DataFrame or list of dicts would be safer - with separate lists you could accidentally add to one and forget another if one append is missed. I kept the simple approach because the SQL query already comes back as separate columns, so it was easier to just keep them as separate lists rather than converting everything.
