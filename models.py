"""
Model architectures for MNIST digit classification.
Phase 11: Added CNN architectures
"""

from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import os

def create_mlp():
    """Create a simple MLP for digit classification."""
    model = keras.Sequential([
        layers.Flatten(input_shape=(28, 28)),  # 28×28 → 784
        layers.Dense(128, activation='relu'),   # Hidden layer
        layers.Dense(10, activation='softmax')  # Output (10 digits)
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def create_small_cnn():
    """Create a small CNN — one conv layer + pooling + dense."""
    model = keras.Sequential([
        # Reshape for CNN (needs channel dimension)
        layers.Reshape((28, 28, 1), input_shape=(28, 28)),
        
        # Convolutional layer
        layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        
        # Flatten and dense layers
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def create_deeper_cnn():
    """Bigger CNN with two conv layers and dropout."""
    model = keras.Sequential([
        # Reshape for CNN
        layers.Reshape((28, 28, 1), input_shape=(28, 28)),
        
        # Two convolutional layers
        layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
        layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dropout(0.25),
        
        # Dense layers with dropout
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(10, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def save_model(model, filepath):
    """Save trained model to disk."""
    # Create artifacts directory if it doesn't exist
    os.makedirs('artifacts', exist_ok=True)
    
    model.save(filepath)
    print(f"Model saved to {filepath}")

def load_model(filepath):
    """Load model from disk."""
    model = keras.models.load_model(filepath)
    print(f"Model loaded from {filepath}")
    return model

def preprocess_image(image):
    """Get image ready for the model — normalise and add batch dim."""
    # Normalise to 0-1 range
    image = image.astype('float32') / 255.0
    
    # Add batch dimension: (28, 28) → (1, 28, 28)
    image = np.expand_dims(image, axis=0)
    
    return image

def predict_digit(model, image):
    """Run prediction on an image, return (digit, confidence)."""
    # Preprocess image
    processed = preprocess_image(image)
    
    # Get predictions (array of 10 probabilities)
    prediction = model.predict(processed, verbose=0)
    
    # Find digit with highest probability
    digit = int(prediction.argmax())
    
    # Get confidence for that digit
    confidence = float(prediction[0][digit]) * 100
    
    return digit, confidence
