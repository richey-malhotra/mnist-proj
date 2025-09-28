"""
Model architectures for MNIST digit classification.
Phase 3: MLP (Multi-Layer Perceptron)
"""

from tensorflow import keras
from tensorflow.keras import layers

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
