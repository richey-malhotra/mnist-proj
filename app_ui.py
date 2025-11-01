"""
MNIST Digit Recognition Project
Phase 7: Image Upload + Prediction UI
"""

import warnings
# Suppress urllib3 OpenSSL warning (macOS system library compatibility issue)
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')

import gradio as gr
from PIL import Image
import numpy as np
from models import load_model

# Load trained model
print("Loading model...")
model = load_model('artifacts/mnist_mlp.keras')
print("Model loaded successfully!")

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

# Simplest possible Gradio interface
demo = gr.Interface(
    fn=predict_uploaded_image,
    inputs=gr.Image(),
    outputs="text",
    api_name=False  # Disable API to avoid Gradio bug
)

if __name__ == "__main__":
    print("\nStarting Gradio interface...")
    print("Upload an image to get a prediction!")
    print("Open http://localhost:7860 in your browser\n")
    demo.launch()
