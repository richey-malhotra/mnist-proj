# Test 6: Error Handling and Drawing Input

**Date:** 18th January 2026  
**Phase tested:** Phase 20-21 (input validation, error handling, drawing, edge cases)  
**What I'm testing:** that the app handles bad input gracefully and the drawing feature works

## Setup

1. Open terminal, activate venv
2. Run `python app_ui.py`
3. Open localhost:7860

## Steps to show

| Step | What to do on screen | What to say |
|------|---------------------|-------------|
| 1 | Go to Predict tab, click "Predict with All Models" without any image | "First I want to test what happens when you try to predict without giving it anything." |
| 2 | Show the error message | "It gives a proper error message instead of crashing. Before I added validation it would just throw a Python traceback, which is terrible UX." |
| 3 | Switch to "Draw Digit" sub-tab | "There's also a drawing option where you can draw a digit directly instead of uploading." |
| 4 | Draw a digit 7 on the sketchpad | "I'll draw a 7... not the neatest but that's kind of the point." |
| 5 | Click predict, show results | "It predicted 7 — got it right even though my drawing is rough." |
| 6 | Show the preprocessed image preview | "This preview shows what the model actually sees after preprocessing. It converts my drawing to a 28x28 greyscale image, same as the training data." |
| 7 | Clear the canvas and draw a really messy digit | "What if I draw something really bad..." |
| 8 | Show the prediction — might be wrong | "It said 2 but I was trying to draw a 9. Fair enough, that was terrible." |
| 9 | Go to Train tab, try training with 0 epochs | "Let me also test the training validation. If I try to train with zero epochs..." |
| 10 | Show the validation error | "It catches that and tells me to use a valid number. Same thing if I put in a negative batch size or something daft." |

## Expected vs Actual

| Thing being checked | Expected | Actual |
|---|---|---|
| Predict with no image | Error message, no crash | "Please upload or draw an image first" ✓ |
| Drawing a clear digit | Correct prediction | Drew 7, predicted 7 ✓ |
| Drawing a messy digit | Prediction may be wrong, but no crash | Wrong prediction but handled gracefully ✓ |
| Preprocessed preview shows | 28x28 greyscale version of input | Displayed correctly next to original ✓ |
| Train with 0 epochs | Validation error | Error message shown ✓ |
| Train with negative batch size | Validation error | Error message shown ✓ |
| Empty state messages | Helpful text when no models/history exist | "No training runs yet" message displays ✓ |

## Notes

The error handling was one of the last things I added but it makes a massive difference. Nobody wants to see a Python error traceback in a web app. The drawing feature is fun but the accuracy depends a lot on how you draw — thin lines and off-centre digits confuse the model because the training data has thick centred digits.
