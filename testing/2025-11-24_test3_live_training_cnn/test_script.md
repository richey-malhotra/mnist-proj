# Test 3: Live Training Progress + CNN vs MLP

**Date:** 24th November 2025  
**Phase tested:** Phase 10-11 (live progress bar + CNN models)  
**What I'm testing:** that the training progress updates live in the browser, and that CNN models actually perform better than the MLP

## Setup

1. Open terminal, activate venv
2. Run `python app_ui.py`
3. Open localhost:7860 in browser

## Steps to show

| Step | What to do on screen | What to say |
|------|---------------------|-------------|
| 1 | Go to the Train tab, show the dropdown | "So now I've got three model types to choose from — MLP, Small CNN, and Deeper CNN." |
| 2 | Select MLP, set 5 epochs, click Start Training | "I'll train the MLP first with 5 epochs so we can compare." |
| 3 | Point at the progress updating in the textbox | "See how it updates live? Before I added the streaming callback it would just freeze for ages and you'd have no idea if it was working. Now you can watch each epoch come through." |
| 4 | Wait for MLP to finish, note the accuracy | "MLP got 97.8% — that's pretty good for such a simple network." |
| 5 | Now select Small CNN, same settings, train again | "Now I'll train the small CNN. CNNs use convolutional layers which are better at recognising spatial patterns in images." |
| 6 | Watch it train, note it takes a bit longer | "It's a bit slower because there's more computation with the conv layers, but the accuracy should be better." |
| 7 | Note the final accuracy for Small CNN | "97.9% — a tiny bit better than the MLP." |
| 8 | Select Deeper CNN, train with same settings | "And the deeper CNN has even more layers. Let's see how this one does." |
| 9 | Show final accuracy | "99.1%. So the deeper model definitely wins on accuracy, but it took noticeably longer to train. That's the trade-off." |

## Expected vs Actual

| Thing being checked | Expected | Actual |
|---|---|---|
| Live progress updates during training | Text updates each epoch, doesn't freeze | Yes, updates smoothly each epoch ✓ |
| MLP trains successfully | ~97-98% accuracy | 97.8% ✓ |
| Small CNN trains successfully | ~98-99% accuracy | 97.9% ✓ |
| Deeper CNN trains successfully | ~99%+ accuracy | 99.1% ✓ |
| CNN better than MLP | CNN accuracy > MLP accuracy | Yes, deeper CNN best ✓ |
| Deeper CNN slower than MLP | Takes more time per epoch | Yes, noticeably slower ✓ |
| Model files saved | New .keras files in artifacts/ | Three new files appeared ✓ |

## Notes

The deeper CNN genuinely is better but takes roughly 3x as long to train. With only 5 epochs the difference is clear. The live progress was the big UX improvement — before this the page would just sit there doing nothing for a minute and you'd wonder if it had crashed.
