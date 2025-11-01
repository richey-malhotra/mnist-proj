# Phase 7 Development Diary

This is the phase where everything actually comes together. The model from Phase 3, the prediction logic from Phase 5, the Gradio UI from Phase 6 - all wired into one working app. I swapped out the hello-world text interface for a real image upload that classifies handwritten digits. 

## PIL, Pillow, and why naming things is hard

Needed image resizing and NumPy can't do that, so I searched for how to resize images in Python and ended up at PIL. The naming is weird though - PIL itself is dead and hasn't been updated in years. What you actually install is Pillow, but then you import it with `from PIL import Image`. Tried `import Pillow` first and got an error. Apparently they kept the original import name so old code still works with the new package. Bit of a quirk but easy enough once you know.

## The preprocessing steps

This was the real meat of the phase. Getting a user's uploaded photo into a shape the model can actually use was a longer chain than I expected.

Gradio's `gr.Image` component passes the image in as a NumPy array by default. So the function receives raw pixel data, which is good, but I still need to do a lot to it before the model can touch it. The steps ended up being: take the NumPy array, convert it to a PIL Image, convert to greyscale with `.convert('L')`, resize to 28x28, convert back to a NumPy array, normalise to 0-1, and add the batch dimension.

The greyscale step tripped me up at first. I uploaded a colour photo of a handwritten digit and got a shape mismatch because the resized image was (28, 28, 3) because RGB keeps three channels. The model expects (28, 28) with no channel axis. Converting to greyscale before resizing strips it down to a single channel and fixes the shape. The order matters here. If you resize first, the three channels survive the resize.

And then, of course, I forgot the batch dimension. Again. Same exact mistake as Phase 5. The model wants (1, 28, 28) but a single image is just (28, 28), so `np.expand_dims` is needed to wrap it. I got the "expected 3 dimensions, got 2" error and immediately recognised it this time. This keeps coming up - I think at this point I've learned it properly, but I also thought that last time.

## Wiring up the UI

Switching the Gradio interface from text to image input was easier than I expected. I replaced `gr.Textbox` with `gr.Image` for the input, kept `gr.Textbox` for the output, and pointed the function at my preprocessing-and-predict code instead of the old greeting function. The model gets loaded once at the top level when the app starts, so it's not reloading on every prediction.

One thing that caught me: the app crashed on page load with `TypeError: argument of type 'bool' is not iterable` deep inside gradio_client code. Spent a while confused before finding that passing `api_name=False` to the Interface constructor fixes it. Something to do with how Gradio tries to register API endpoints. Not a great error message but at least the fix is simple, just one extra parameter.

For the output, I initially just returned the predicted digit as a bare number. That works but it's not very useful - you can't tell how sure the model is. I changed it to show the digit and a confidence percentage formatted to two decimal places. Something like "Predicted Digit: 7, Confidence: 98.45%" reads much better and actually tells you whether the model is guessing or certain.

Testing with actual photos was really satisfying. Clean MNIST-style digits got 99%+ confidence. A colour phone photo of a handwritten 3 came through at about 87%. The greyscale conversion and resizing handled it properly. A messy 9 got around 62%, which makes sense. I even uploaded a photo of a cat just to see what would happen, and the model predicted 8 with low confidence. It doesn't know how to reject non-digits, it just picks the closest one. That's a problem but I'm not going to fix it now.

I also wrapped the prediction in `try/except` so if anything goes wrong (dodgy image, missing model file, whatever) it shows an error message instead of the whole app crashing with a Python traceback. The `except Exception as e` bit catches pretty much any error and sticks the message in `e`. Not sure if catching everything like that is the best way to do it - probably should catch specific errors - but I don't actually know what all the possible errors are yet so catching the lot at least keeps things running.

## Reflection

Actually feels like a proper app now. Someone could sit down, upload a photo, and get a prediction. The whole thing actually works now. The preprocessing has loads of steps but they're all needed, so I'm fine with it.

The PIL/Pillow naming thing is just annoying. You'd never guess it unless someone told you. The batch dimension mistake is becoming a running joke at this point lol, though at least now I catch it faster. The colour image thing caught me out because I didn't think about what the data actually looks like going into the model.

Roughly 3 hours for this phase.
