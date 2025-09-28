# Phase 3 Development Diary

## Session Goal

Build and train my first neural network, a simple MLP (Multi-Layer Perceptron) that can recognise handwritten digits from the MNIST dataset. Phase 2 got the data loaded and I understand what it looks like (60,000 training images, 28x28 pixels, labels 0-9), so now it's time to actually do something with it.

## Understanding MLPs

Googled "MLP neural network" since I'd heard the term but couldn't have explained it properly. It stands for Multi-Layer Perceptron - basically stacked layers of neurons where each one takes some inputs, does maths on them (multiply by weights, add up, pass through an activation function), and sends the result forward. The name is a bit old-fashioned: "perceptron" was the original word for a single neuron. There are fancier network types like CNNs that are supposedly better for images, but starting with the basic version made sense to me.

## Building the Model

Decided to put model architectures in a separate file (`models.py`) to keep things organised. To use it from app.py you write `from models import create_mlp` which basically means "from the file called models, grab the function called create_mlp". Python treats each .py file as a module that other files can import from, which I didn't really know before - just figured it out from the error messages when it didn't work. See that file for the actual code. The architecture is three layers:

**Flatten layer**: takes the 28x28 grid and turns it into one long list of 784 numbers. Neural networks need 1D input.

**Dense(128, activation='relu')**: the hidden layer with 128 neurons. Saw 128 used in a tutorial and went with it, could be 64 or 256 tbh, not sure why 128 specifically. ReLU activation means "set negative values to zero" (I think?).

**Dense(10, activation='softmax')**: output layer. 10 neurons because there are 10 possible digits. Softmax turns the outputs into probabilities that add up to 1.

For compilation I'm using Adam optimiser (seems to be the standard choice), sparse categorical crossentropy for the loss (measures how wrong predictions are, and "sparse" because labels are integers not one-hot vectors), and tracking accuracy as the metric. I don't fully understand the crossentropy maths yet but that's okay for now.

Had to look up what "one-hot" actually means since I wrote it above without really knowing. So if your label is the digit 3, the one-hot version would be [0, 0, 0, 1, 0, 0, 0, 0, 0, 0] - basically a list of zeros with a 1 in the position for that digit. Called "one-hot" because only one element is "hot" I guess. The normal crossentropy loss wants labels in that format, but the "sparse" version just takes the integer directly and does the conversion for you. Which is what I'm using, so I don't have to bother with any of that.

Also looked up what Adam actually stands for - Adaptive Moment Estimation. From what I can gather it adjusts the learning rate for each weight separately, so things that are changing a lot get smaller updates and things that barely change get bigger ones. Not sure I fully get why that helps but it just seems to work well for most things without having to fiddle with settings, which is probably why every tutorial uses it.

## Data Normalisation

Read that neural networks work better with smaller numbers, so I divided all pixel values by 255 to get the range 0-1 instead of 0-255. Simple division, converts to floats automatically. Verified it worked by printing the new range.

## Training

Before training I called `model.summary()` and found out the model has over 100,000 parameters. That seemed like a lot for something "simple" so I worked through the maths:
- Flatten: 0 params (just reshaping)
- Dense(128): 784 x 128 + 128 biases = 100,480
- Dense(10): 128 x 10 + 10 biases = 1,290
- Total: 101,770, which checks out!

Training ran for 3 epochs with batch size 32. First epoch took about 40 seconds, so the whole three-epoch run was about 2 minutes. 1875 batches per epoch because 60,000 / 32 = 1875.

I passed `validation_data=(x_test, y_test)` to `model.fit()` which makes Keras test the model on the test set after each epoch - data it hasn't trained on. The idea is if training accuracy keeps going up but validation accuracy stops or goes down, the model's just memorising the training images instead of actually learning. That's called overfitting apparently. Haven't seen it happen yet but good to know what to look for.

Results:
- Epoch 1: ~92.5% training, ~95.8% validation
- Epoch 2: ~96.6% training, ~97.0% validation
- Epoch 3: ~97.7% training, ~97.2% validation

Accuracy going up each epoch. It's learning! Noticed validation accuracy is sometimes higher than training accuracy early on, which I didn't expect. Looked it up and from what I read that's normal in the first few epochs.

97% accuracy means it gets 97 out of 100 digits correct. For my first neural network that feels pretty good. Apparently people have got like 99.8% on MNIST so there's definitely room to improve, but I'm happy with that for now.

## Problems I Hit

Got a `ModuleNotFoundError` when trying to import from `models.py` at first. Both files need to be in the same directory and you need to run from that directory. Easy fix once I realised.

The loss values during training (0.26, 0.11, 0.08) are harder to interpret than accuracy percentages. I know lower is better but not sure what scale they're on.

Still a bit fuzzy on the difference between ReLU and Softmax beyond "ReLU for hidden layers, Softmax for output". The maths can come later.

## Testing

Ran `app.py`, model created and trained without errors. Summary showed the right layer structure, training completed in about 2 minutes total, and final validation accuracy came in around 97%. Normalisation was verified (values are 0-1). All good.

## Reflection

Best phase yet. Actually training a model and watching the accuracy climb each epoch feels like real progress. Don't fully get crossentropy maths yet but I can build and train a model so thats fine for now. Keras is surprisingly easy to use. I thought neural network code would be much more complex than just listing layers in order. Training was faster than expected too - only about 2 minutes for the whole thing.

The bit I found trickiest was knowing what values to pick. Why 128 neurons? Why batch size 32? The tutorials just use these numbers without always explaining why. I think the answer is that they're reasonable defaults and experimenting with them is something you do later. Wondering if different architectures would do better.

First time building a neural network so worth taking the time, even if it did take about two hours.

Phase 4 is about saving and loading the model so I don't have to retrain every time I run the script. Will use `model.save()` and create a directory for the saved models. Saw the word "artifacts" used for this in the TensorFlow docs - apparently that's what they call outputs like trained model files. Looking forward to not waiting 2 minutes every time.
