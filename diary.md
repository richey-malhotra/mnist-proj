# Phase 5 Development Diary

## Session Goal

Add prediction functionality. I need to make the model actually classify new digit images. Need to figure out preprocessing and how to interpret the model's output.

## Understanding the Output

Had to work out what `model.predict()` gives back. It's not just one answer - you get 10 numbers, one per digit, each showing how likely the model thinks that digit is. They add up to 1.0 so they're basically probabilities. Then you find whichever one is biggest with `argmax()`. Took me a minute to figure out what argmax meant but it's literally just "which index has the highest value".

## The Two Bugs

This phase was trickier than expected because I hit two separate issues back to back.

**Shape error.** Tried passing a single image directly to the model and got "expected 3 dimensions, got 2". The model was trained on batches shaped `(60000, 28, 28)` but my single image was just `(28, 28)` with no batch dimension. Fix was `np.expand_dims(image, axis=0)` which reshapes it to `(1, 28, 28)`, i.e. a "batch of one". Found another way with `np.newaxis` but went with expand_dims since it was easier to understand.

**Normalisation mismatch.** Got predictions working but they were terrible - basically random guesses even though the model has 97% accuracy. Took me ages to realise I was passing in raw pixels (0-255) but the model was trained on normalised data (0-1). Once I added `image.astype('float32') / 255.0` before predicting, everything worked properly. This one was frustrating because the model ran fine, it just gave garbage results. So the preprocessing has to be the same for training and prediction or it just gives you rubbish.

## The predict_digit Function

Put it all together into one function in models.py: normalise, add batch dimension, predict, find the max, calculate confidence as a percentage. See models.py for the code. The `verbose=0` flag stops the progress bar showing for each individual prediction, which was annoying when testing multiple images.

Confidence scores are interesting. Most predictions come back at 99%+ but occasionally you get something lower like 85%, which usually means the digit is ambiguous. High confidence doesn't mean it's actually right though. I saw one prediction at 97.8% confidence that was completely wrong. Some digits must just look similar to the model.

## Testing

Loaded the saved model from Phase 4 and ran predictions on 5 random test images. Got 4 out of 5 correct - the wrong one was a 3 that got predicted as 5 with high confidence. Makes sense, 3s and 5s probably look similar in scruffy handwriting. Overall test accuracy was 97.48% which lines up with what I got in training.

Actually using the model to classify things feels like real progress. Up until now it was all setup and training, and this is the first time the model is actually *doing* something useful. The testing function is satisfying to watch too, seeing correct/incorrect predictions on random samples.

## What I Learned

So neural networks give you probabilities for all 10 classes, not just one answer. You also have to preprocess exactly the same way as training or it all breaks. And models always want that batch dimension even if you're only giving it one image - that one keeps catching me out. The confidence scores are interesting too, could be useful later for flagging ones the model isn't sure about.

The normalisation bug was the biggest lesson. The model ran without errors, it just silently gave bad results because the input data was in the wrong range. Way harder to track down than when something just crashes.

## Reflection

Trickier than expected but satisfying. The shape error was a quick fix once I'd Googled it, but the normalisation issue took a while to track down. Main thing was getting my head around the 10-probability output format - once that clicked, argmax and confidence scores were straightforward.

Ready to move to Phase 6 and build an actual UI with Gradio. Having working predictions means I can hook them up to a web interface now.

Probably like 2 hours? Lost track.
