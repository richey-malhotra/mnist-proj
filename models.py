"""
Model architectures for MNIST digit classification.
Phase 5: Added prediction
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
