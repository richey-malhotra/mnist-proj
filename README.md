# Phase 3: Train First MLP Model

## What Changed

- Created `models.py` with MLP architecture
- Added data normalisation (0-255 → 0-1 range)
- Added the training loop with validation
- Model summary shows 101,770 trainable parameters
- Training achieves ~97% accuracy in 3 epochs

 Phase 2 loaded the data. Now I'm building and training a neural network on it.

## Understanding the MLP

MLP stands for Multi-Layer Perceptron. Had to Google it because I'd heard the term but wasn't clear on the details. It's the simplest kind of neural network. It's layers of neurons connected together, each taking inputs, multiplying by weights, adding up, and passing through an activation function. "Perceptron" is an old term for a single neuron, "Multi-Layer" means you stack them.

The architecture lives in `models.py` (separate file to keep things organised):

```python
model = keras.Sequential([
    layers.Flatten(input_shape=(28, 28)),  # 28×28 → 784
    layers.Dense(128, activation='relu'),   # Hidden layer
    layers.Dense(10, activation='softmax')  # Output (10 digits)
])
```

- **Flatten**: Takes the 28×28 grid and turns it into one long list of 784 numbers. Neural networks need 1D input.
- **Dense(128, relu)**: Hidden layer. 128 neurons was a tutorial default - could be 64 or 256, not sure why 128 specifically. ReLU means "set negative values to zero".
- **Dense(10, softmax)**: Output layer. 10 neurons for 10 digits. Softmax turns outputs into probabilities that add up to 1.

For compilation I used Adam optimiser (seems to be the standard choice). Loss function is sparse categorical crossentropy, which measures how wrong predictions are. The 'sparse' part is because labels are integers not one-hot. Also tracking accuracy as the metric. Don't fully understand the crossentropy maths yet but that's okay for now.

## Parameter Count

The model has 101,770 parameters, which seemed like a lot for something "simple". Worked through the maths:
- Flatten: 0 params (just reshaping)
- Dense(128): 784 × 128 + 128 biases = 100,480
- Dense(10): 128 × 10 + 10 biases = 1,290
- **Total: 101,770**, which checks out!

## Normalisation

```python
x_train = x_train / 255.0
x_test = x_test / 255.0
```

Divide all pixel values by 255 to get 0-1 instead of 0-255. Neural networks train better with smaller numbers. Converts to floats automatically.

## Training

```python
history = model.fit(
    x_train, y_train,
    epochs=3, batch_size=32,
    validation_data=(x_test, y_test),
    verbose=1
)
```

- **Epochs**: 3 passes through the entire dataset
- **Batch size**: 32 images at a time (60,000 / 32 = 1,875 batches per epoch)
- **Validation**: Uses test set to check accuracy on unseen data

Results:
- Epoch 1: ~92.5% train, ~95.8% validation
- Epoch 2: ~96.6% train, ~97.0% validation
- Epoch 3: ~97.7% train, ~97.2% validation

Noticed validation accuracy is sometimes *higher* than training accuracy early on, which was unexpected. Looked it up and apparently it's normal in the first few epochs. The loss values (0.26, 0.11, 0.08) are harder to interpret than accuracy percentages: lower is better, but I'm not sure what scale they're on exactly.

97% means 97 out of 100 digits correct. For a first neural network that feels pretty good. Apparently the best results people get on MNIST are like 99.8%, so there's room to improve, but that's not bad for a first try.

## Problems I Hit

Got a `ModuleNotFoundError` when trying to import from `models.py`. Both files need to be in the same directory and you have to run Python from that directory. Easy fix once I realised.

Still a bit fuzzy on the difference between ReLU and Softmax beyond "ReLU for hidden layers, Softmax for output". The deeper maths can come later.

## Decisions

### Why Batch Size 32?

I just went with 32 because basically every tutorial uses it. I think it's somewhere between fast training and good accuracy. Smaller batches take longer, bigger ones use more memory. 32 seemed like a safe default. I'll let users change it in the UI later so they can experiment.

### Using the Test Set for Validation

```python
validation_data=(x_test, y_test)
```

I passed the test set as the validation data during training. I think technically you're supposed to keep the test set completely separate and use a different chunk of training data for validation. But for now this is simpler and it still shows whether the model is improving each epoch. Something to maybe fix properly later.

### `sparse_categorical_crossentropy`

Used `sparse_categorical_crossentropy` instead of `categorical_crossentropy` because my labels are just integers (0-9), not one-hot encoded vectors. Basically it saves me from having to convert 60,000 labels into arrays of mostly zeros. I think it does the same thing underneath, just saves you a step.

### The History Object

```python
final_train_acc = history.history['accuracy'][-1]
```

`model.fit()` returns a history object that stores the metrics from each epoch. The `[-1]` grabs the last value. The double `.history` looks weird but that's just how Keras works - the object has an attribute called `history` which is a dictionary.

## Project Files

```
gradio_phase3/
├── app.py              # Main script with training loop (68 lines)
├── models.py           # MLP architecture (33 lines)
├── requirements.txt    # Dependencies (3 lines)
├── README.md          # Technical documentation (this file)
└── diary.md           # Development journal
```

## Setup Instructions

**1. Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run training:**
```bash
python app.py
```

**Expected output:**
- Dataset loading with normalised values (0.0 to 1.0)
- Model summary showing 101,770 parameters
- Training progress for 3 epochs (~2 minutes total)
- Final accuracy around 97%

## Differences from Phase 2

| Aspect | Phase 2 | Phase 3 |
|--------|---------|---------|
| **Files** | app.py only | app.py + models.py |
| **Functionality** | Load data | Load, normalise, train model |
| **Data preprocessing** | None | Normalisation (÷255) |
| **Neural network** | None | 3-layer MLP |
| **Training** | None | 3 epochs, ~2 minutes |
| **Accuracy metric** | N/A | ~97% validation accuracy |
| **Total code lines** | 33 | 101 (+68 lines) |
