# Phase 18 Development Diary

## Scatter Plot Chart

Replaced Phase 16's bar chart with something more useful: a scatter plot showing accuracy vs training time for every run. The bar chart averaged everything together, so you couldn't see how different each run was. A scatter plot shows each run as a separate point so you can see patterns and outliers.

Each architecture gets its own colour (kept the same colour scheme: blue for MLP, orange for Small CNN, green for Deeper CNN) so you can immediately see how they cluster. The data comes from the same tables as before - just queried differently.

## How I Built It

Had to filter out runs where duration is NULL since some older runs from before Phase 16 don't have timing data. Used separate `go.Scatter()` traces per architecture because Plotly doesn't do categorical colours easily in a single trace, so you have to loop through the categories yourself and create a trace for each. More code than I'd like but it gives you full control over colour and legend labels.

Added hover tooltips showing exact values for each point. Plotly's hovertemplate is a bit fiddly (the formatting syntax is different from Python f-strings) but once it works it's really nice for exploring the data interactively.

## What It Shows

The patterns in the chart are really clear. You can see three distinct clusters - MLP in the bottom-left corner (quick but lower accuracy), Deeper CNN in the top-right (slow but most accurate), and Small CNN bridging the gap. What I didn't expect was how good Small CNN looks as a compromise. It's barely slower than MLP but gets much closer to Deeper CNN's accuracy. Wouldn't have spotted that just looking at raw numbers.

I also noticed the dots within each cluster aren't perfectly aligned - training the same architecture twice gives slightly different results each time. Makes sense because of the random weight initialisation, but it's interesting to actually see that variation on the chart rather than just knowing it theoretically.

## Problems

Main issue was NULL filtering. Old training runs from before duration tracking existed would crash the chart because you can't plot None values. Added a WHERE clause to exclude those. Also had to sort the architecture list before creating traces otherwise the legend order was random each time, which looked messy.

## Testing

Trained a few models across all three architectures, confirmed points appear in the right places. Hover works. Refresh button updates the chart alongside the other two. No crashes with empty data.

I think the scatter plot works better than the bar chart for this because you can see accuracy and time at the same time. The bar chart from Phase 16 showed averages, which is useful but you can't see what each run actually did. This shows what's actually happening better than averages did. Learning Plotly's scatter syntax was worth the time.
