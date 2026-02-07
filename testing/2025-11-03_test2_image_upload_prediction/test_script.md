# Test 2: Image Upload and Prediction

**Date:** 3rd November 2025  
**Phase tested:** Phase 7 (Gradio image upload + prediction)  
**What I'm testing:** that a user can upload a handwritten digit image and get the right prediction back

## Setup

1. Open terminal, activate venv
2. Run `python app_ui.py`
3. Open the Gradio URL in browser (usually localhost:7860)

## Steps to show

| Step | What to do on screen | What to say |
|------|---------------------|-------------|
| 1 | Show the Gradio interface loading in the browser | "OK so this is the web interface. I built it with Gradio which gives you a proper UI without having to write HTML or anything." |
| 2 | Click on the Predict tab | "I'll go to the predict tab where you can upload an image." |
| 3 | Upload a clear image of a handwritten 5 | "I've got some test images I wrote myself and scanned in. This one's a 5." |
| 4 | Click predict, show the result | "It predicted 5, which is correct. The confidence is pretty high too." |
| 5 | Upload a different digit — try a 3 | "Let me try another one, this is a 3." |
| 6 | Show that prediction is also correct | "That's right as well. The MLP handles clear handwriting pretty reliably." |
| 7 | Upload a deliberately messy/ambiguous digit | "Now I'll try one that's harder to read — this 4 is a bit wonky." |
| 8 | Show result — might be wrong or low confidence | "It got it right but the confidence dropped. Makes sense because the writing is messier." |

## Expected vs Actual

| Thing being checked | Expected | Actual |
|---|---|---|
| Gradio UI loads in browser | Interface appears at localhost:7860 | Yes, loaded fine ✓ |
| Can upload an image | File picker works | Yes ✓ |
| Clear digit 5 predicted correctly | Predicts 5 with high confidence | Predicted 5 (98.7% confidence) ✓ |
| Clear digit 3 predicted correctly | Predicts 3 | Predicted 3 (96.2% confidence) ✓ |
| Messy digit has lower confidence | Still predicts but less certain | Correct but only 71.4% confidence ✓ |
| No errors when uploading images | Clean response | No errors ✓ |

## Notes

The image gets automatically resized to 28x28 and converted to greyscale by the preprocessing, so it doesn't matter what size the original image is. I tested with a photo from my phone camera and a scanned image, both worked.
