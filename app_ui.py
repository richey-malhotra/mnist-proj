"""
MNIST Digit Recognition Project
Phase 8: Add Training Tab
"""

import warnings
# Suppress urllib3 OpenSSL warning (macOS system library compatibility issue)
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')

import gradio as gr
from PIL import Image
import numpy as np
from tensorflow.keras.datasets import mnist
from models import create_mlp, load_model, save_model

# Load MNIST data once at startup
print("Loading MNIST dataset...")
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0
print(f"Dataset loaded: {x_train.shape[0]} training images, {x_test.shape[0]} test images")

# Load existing model for prediction
print("Loading trained model...")
model = load_model('artifacts/mnist_mlp.keras')
print("Model loaded successfully!")


def train_new_model(epochs, batch_size):
    """Train a fresh MLP and save it."""
    try:
        # Convert to integers
        epochs = int(epochs)
        batch_size = int(batch_size)
        
        # Create new model
        new_model = create_mlp()
        
        # Train model
        print(f"Training model with {epochs} epochs, batch size {batch_size}...")
        history = new_model.fit(
            x_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=(x_test, y_test),
            verbose=1
        )
        
        # Save model
        model_path = 'artifacts/mnist_mlp.keras'
        save_model(new_model, model_path)
        print(f"Model saved to {model_path}")
        
        # Get final accuracy
        final_train_acc = history.history['accuracy'][-1] * 100
        final_val_acc = history.history['val_accuracy'][-1] * 100
        
        result = f"""Training Complete!

Final Training Accuracy: {final_train_acc:.2f}%
Final Validation Accuracy: {final_val_acc:.2f}%

Model saved to: {model_path}
"""
        
        return result
        
    except Exception as e:
        return f"Error during training: {str(e)}"


def predict_uploaded_image(image):
    """Predict digit from an uploaded image."""
    if image is None:
        return "Please upload an image."
    
    try:
        # Gradio passes numpy array by default
        # Normalise to 0-1 range (convert to greyscale if needed)
        if len(image.shape) == 3:
            # Color image - convert to greyscale
            img_array = np.mean(image, axis=2).astype('float32')
        else:
            # Already greyscale
            img_array = image.astype('float32')
        
        # Convert to PIL for resizing
        img = Image.fromarray(img_array.astype('uint8'))
        img = img.resize((28, 28))
        
        # Back to numpy and normalise
        img_array = np.array(img).astype('float32') / 255.0
        
        # Add batch dimension: (28, 28) → (1, 28, 28)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Get prediction
        prediction = model.predict(img_array, verbose=0)
        
        # Extract digit and confidence
        digit = int(prediction.argmax())
        confidence = float(prediction[0][digit]) * 100
        
        # Format output
        result = f"Predicted Digit: {digit}\nConfidence: {confidence:.2f}%"
        
        return result
    
    except Exception as e:
        return f"Error: {str(e)}"


# Create Gradio interface with tabs
with gr.Blocks(title="MNIST Digit Classifier") as demo:
    gr.Markdown("# MNIST Digit Classifier")
    gr.Markdown("Train new models or test predictions on handwritten digits")
    
    with gr.Tab("Train"):
        gr.Markdown("### Train a New Model")
        gr.Markdown("Configure training parameters and train a fresh MLP model")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("**Training Parameters**")
                epochs_input = gr.Number(
                    label="Epochs",
                    value=3,
                    minimum=1,
                    maximum=20,
                    step=1
                )
                batch_size_input = gr.Number(
                    label="Batch Size",
                    value=32,
                    minimum=16,
                    maximum=128,
                    step=16
                )
                train_button = gr.Button("Start Training", variant="primary")
            
            with gr.Column(scale=2):
                gr.Markdown("**Training Results**")
                training_output = gr.Textbox(
                    label="Training Status",
                    lines=10,
                    placeholder="Click 'Start Training' to begin..."
                )
        
        train_button.click(
            fn=train_new_model,
            inputs=[epochs_input, batch_size_input],
            outputs=training_output,
            api_name=False  # Disable API to avoid Gradio bug
        )
    
    with gr.Tab("Predict"):
        gr.Markdown("### Upload Image for Prediction")
        gr.Markdown("Upload a handwritten digit image (will be converted to 28×28 greyscale)")
        
        with gr.Row():
            with gr.Column(scale=1):
                image_input = gr.Image(label="Upload Digit Image")
                predict_button = gr.Button("Predict", variant="primary")
            
            with gr.Column(scale=1):
                prediction_output = gr.Textbox(
                    label="Prediction Result",
                    lines=5
                )
        
        predict_button.click(
            fn=predict_uploaded_image,
            inputs=image_input,
            outputs=prediction_output,
            api_name=False  # Disable API to avoid Gradio bug
        )


if __name__ == "__main__":
    print("\nStarting MNIST Classifier interface...")
    print("- Train tab: Configure and train new models")
    print("- Predict tab: Upload images for digit recognition")
    print("\nOpen http://localhost:7860 in your browser\n")
    demo.launch()
