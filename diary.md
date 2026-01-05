# Phase 17 Development Diary

Added image preview so users can see what the model actually receives after preprocessing. Before this (basically since Phase 14's comparison feature), you'd upload an image and just get a prediction back with no idea what happened in between. You just had to trust it was doing the right thing.

## What I Changed

Renamed `predict_with_comparison` to `predict_with_preview` and changed it from returning just text to returning three things: original image, preprocessed 28x28 image, and prediction results. The UI now shows both images side by side above the predictions.

Had to convert the preprocessed numpy array back to a PIL Image for display, which was slightly annoying. You multiply by 255 and cast to uint8 since the model input is normalised to 0-1. Had a type issue where Gradio wanted PIL images for display but I was returning numpy arrays. Quick fix but annoying. Also had to handle what happens when something goes wrong. If something goes wrong the function returns `None, None, error_message` instead of crashing, so the image boxes just stay empty.

## Why I Added This

I kept thinking about what happens when someone uploads a photo and gets a wrong prediction. Without seeing the preprocessed version, they'd have no idea why. Now they can look at the tiny 28x28 image and go "oh, that looks nothing like what I drew". The squashing and colour inversion sometimes makes digits unrecognisable, so showing that at least explains the mistakes.

It's good for debugging too. If a prediction is wrong, you can look at the preprocessed image and see whether the problem is the model or the preprocessing. A digit that looks clear at 28x28 but still gets misclassified is a model problem. A digit that's unrecognisable after resizing is a preprocessing problem.

## Layout Changes

The Predict tab needed rearranging to fit two image displays plus the prediction text. Ended up with the upload button on the left side, and the two image previews plus results stacked on the right. It's a tighter fit than before but it works well enough. The preprocessed image is tiny (28x28 rendered at display size) so it looks a bit blocky, but that's kind of the point - you can see exactly what the model sees.

## Testing

Uploaded a few images, checked both previews display. Tried an image that was already 28x28 (preview looks identical, which makes sense). Tested a colour photo too and you can see the colour drop out in the preview, which is a good sanity check that the preprocessing is doing its thing. Everything works. Quick phase.

About an hour.

## Reflection

Small change code-wise but it was bugging me that I couldn't see what was happening to the image. Returning three things from one function (image, image, text) was really easy in Gradio. Good to know for later. Having the preprocessing visible also makes me more confident that the steps are correct because I can actually see what comes out of it.
