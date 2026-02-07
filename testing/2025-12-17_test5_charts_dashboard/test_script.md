# Test 5: Plotly Charts

**Date:** 17th December 2025  
**Phase tested:** Phase 15-16 (accuracy chart + training time chart)  
**What I'm testing:** that the charts display correct data and the interactive features work

## Setup

1. Open terminal, activate venv
2. Make sure you've done at least 3-4 training runs with different architectures first
3. Run `python app_ui.py`
4. Open localhost:7860

## Steps to show

| Step | What to do on screen | What to say |
|------|---------------------|-------------|
| 1 | Go to History tab, scroll down to the charts | "Below the history table there's two charts I made with Plotly." |
| 2 | Show the accuracy comparison chart | "This first one shows the accuracy over epochs for the latest training run as a line chart. You can see at a glance which models performed best." |
| 3 | Hover over a data point to show the tooltip | "If you hover over a data point it shows the exact values — the model name, accuracy,  and which run it was." |
| 4 | Show the different colours for different architectures | "The colours represent different architectures, so blue is MLP, orange is small CNN, and green is the deeper CNN." |
| 5 | Scroll to the training time comparison chart | "The second chart is a performance dashboard — it shows the trade-off between training time and accuracy as a scatter plot. You can compare training times across different architectures." |
| 6 | Hover over a point to show training time | "If you hover over a point it shows the exact training time and accuracy. The deeper CNNs take noticeably longer than the MLPs." |
| 7 | Show the comparison between architectures | "So you can see at a glance that more complex models take longer to train. Whether the extra time is worth the extra accuracy depends on what you need." |

## Expected vs Actual

| Thing being checked | Expected | Actual |
|---|---|---|
| Accuracy chart renders | Line chart with epoch data | Yes, shows all runs ✓ |
| Hover tooltips work | Shows details on hover | Yes, exact values shown ✓ |
| Colour coding by architecture | Different colours per model type | Yes, three distinct colours ✓ |
| Performance scatter plot renders | Scatter plot with time vs accuracy | Yes, renders correctly ✓ |
| Training times match expectations | Deeper CNN longest, MLP fastest | Yes, times scale with model complexity ✓ |
| Charts update with new data | Train a model, refresh, chart updates | New data point appeared after refresh ✓ |

## Notes

Plotly charts are interactive which is way better than static matplotlib images. You can zoom in, pan around, download as PNG. The training time chart is useful because it shows you exactly how much longer the deeper models take. Took me a while to get the Plotly syntax right but the docs are decent.
