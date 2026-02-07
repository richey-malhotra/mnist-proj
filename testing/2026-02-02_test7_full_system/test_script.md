# Test 7: Full System Demonstration

**Date:** 2nd February 2026  
**Phase tested:** All phases — complete end-to-end walkthrough  
**What I'm testing:** that every feature works together as a complete system

## Setup

1. Delete the existing database and model files to start fresh: `rm -f artifacts/training_history.db artifacts/model_*.keras`
2. Run `python init_db.py` to recreate the database
3. Open terminal, activate venv
4. Run `python app_ui.py`
5. Open localhost:7860

## Steps to show

| Step | What to do on screen | What to say |
|------|---------------------|-------------|
| 1 | Show the app loading, custom theme | "This is the final version of my MNIST digit recognition app. I'm starting fresh with no saved models to show the full workflow." |
| 2 | Show empty states — History tab with no runs | "The history is empty because I just cleared everything. It shows a message saying there's no runs yet instead of just being blank." |
| 3 | Go to Train tab. Train an MLP, 5 epochs, batch 32 | "Let's start by training an MLP model. 5 epochs, batch size of 32." |
| 4 | Watch the live progress | "You can see the progress updating live — each epoch shows the training accuracy and validation accuracy." |
| 5 | Note MLP accuracy when done | "97.6% — decent. Now let me try a CNN." |
| 6 | Train a Deeper CNN, same settings | "This is the deeper CNN with more convolutional layers. Should be more accurate but slower." |
| 7 | Watch it train, note it's slower | "Takes longer per epoch because there's more computation. But watch the accuracy." |
| 8 | Note Deeper CNN accuracy | "99.1% — that's properly good. Huge improvement over the MLP." |
| 9 | Go to History tab, click Refresh | "If I check the history tab, both runs are saved in the database." |
| 10 | Show both entries in the table | "You can see the architecture, epochs, accuracy, how long it took, everything." |
| 11 | Scroll to charts | "And the charts update automatically. The line chart shows the accuracy over epochs, and the scatter plot shows the time-accuracy trade-off." |
| 12 | Go to Predict tab → Upload Image | "Now for predictions. I'll upload a test image — this is a handwritten 4." |
| 13 | Upload image, click predict | "It runs the image through all saved models and shows predictions side by side. Both models got it right." |
| 14 | Show the preprocessed image preview | "This is what the model actually sees — the 28x28 pixel version. All the preprocessing is handled by utils.py." |
| 15 | Switch to Draw Digit tab | "You can also draw digits directly." |
| 16 | Draw a 3, predict | "I'll draw a 3... and predict. Both models say 3, correct." |
| 17 | Try predicting with no input | "And if I try to predict without an image, it gives a proper error message rather than crashing." |
| 18 | Show the error message | "That's the input validation I added in phase 20." |
| 19 | Quick scroll through the whole UI | "So that's the whole app — training, predictions, history, charts, drawing, all working together as one system." |

## Expected vs Actual

| Thing being checked | Expected | Actual |
|---|---|---|
| App launches without errors | Clean startup | Yes ✓ |
| Empty states display correctly | Helpful messages when no data | Yes ✓ |
| MLP training works end-to-end | Trains, saves model, reports accuracy | 97.6% accuracy, model saved ✓ |
| Deeper CNN training works | Higher accuracy, takes longer | 99.1%, took ~50s vs ~15s for MLP ✓ |
| History saves both runs | Two rows in database | Both visible after refresh ✓ |
| Charts render with data | Line chart + scatter plot | Both charts show correct data ✓ |
| Upload prediction works | Correct digit predicted | Both models predicted 4 correctly ✓ |
| Multi-model comparison | Side-by-side results | Results shown for all saved models ✓ |
| Preprocessed preview shows | 28x28 image visible | Displayed alongside original ✓ |
| Drawing input works | Can draw and predict | Drew 3, predicted correctly ✓ |
| Error handling works | Friendly error messages | "Please upload or draw an image first" ✓ |
| Custom theme applied | Custom blue theme visible | Yes, looks clean ✓ |

## Notes

Everything works as a complete system. The main thing that ties it all together is the database — models get saved during training, loaded during prediction, and displayed in history. The charts pull from the same database so they're always up to date.

If I had more time I'd probably add:
- Confusion matrix showing which digits get mixed up
- The ability to delete training runs from the history
- Maybe batch prediction for testing lots of images at once

But as it stands the core functionality is solid and all the features work together properly.
