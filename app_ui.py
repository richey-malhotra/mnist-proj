"""
MNIST Digit Recognition Project
Phase 12: Database Schema + Training History Tab
"""

import warnings
# Suppress urllib3 OpenSSL warning (macOS system library compatibility issue)
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')

import gradio as gr
from PIL import Image
import numpy as np
import sqlite3
import pandas as pd
from datetime import datetime
from tensorflow.keras.datasets import mnist
from models import create_mlp, create_small_cnn, create_deeper_cnn, load_model, save_model
from utils import preprocess_image

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


def save_training_run(architecture, epochs, batch_size, val_accuracy):
    """Save training run to database with unique filename."""
    conn = sqlite3.connect('artifacts/training_history.db')
    cursor = conn.cursor()
    
    # Get or create model_id for this architecture
    cursor.execute('SELECT model_id FROM models WHERE architecture = ?', (architecture,))
    result = cursor.fetchone()
    
    if result:
        model_id = result[0]
    else:
        # Insert new architecture
        cursor.execute('INSERT INTO models (architecture) VALUES (?)', (architecture,))
        model_id = cursor.lastrowid
    
    # Get next run_id to create unique filename
    cursor.execute('SELECT MAX(run_id) FROM training_runs')
    max_run = cursor.fetchone()[0]
    next_run_id = 1 if max_run is None else max_run + 1
    
    # Create unique filename
    arch_clean = architecture.lower().replace(' ', '_')
    model_filename = f'model_{arch_clean}_run{next_run_id}.keras'
    
    # Insert training run
    cursor.execute('''
        INSERT INTO training_runs 
        (model_id, epochs, batch_size, val_accuracy, model_filename)
        VALUES (?, ?, ?, ?, ?)
    ''', (model_id, epochs, batch_size, val_accuracy, model_filename))
    
    conn.commit()
    conn.close()
    
    return model_filename


def get_training_history():
    """Get all training runs for display in History tab."""
    conn = sqlite3.connect('artifacts/training_history.db')
    cursor = conn.cursor()
    
    # Get all runs ordered by most recent first
    cursor.execute('''
        SELECT run_id, model_id, epochs, batch_size, val_accuracy, model_filename, created_at
        FROM training_runs
        ORDER BY run_id DESC
    ''')
    
    runs = cursor.fetchall()
    
    if not runs:
        conn.close()
        return pd.DataFrame(columns=['Run ID', 'Architecture', 'Epochs', 'Batch Size', 'Accuracy (%)', 'Filename', 'Timestamp'])
    
    # Build list with architecture names (separate query for each - no JOIN)
    data = []
    for run_id, model_id, epochs, batch_size, val_accuracy, model_filename, created_at in runs:
        # Look up architecture for this model_id
        cursor.execute('SELECT architecture FROM models WHERE model_id = ?', (model_id,))
        result = cursor.fetchone()
        arch = result[0] if result else 'Unknown'
        
        data.append({
            'Run ID': run_id,
            'Architecture': arch,
            'Epochs': epochs,
            'Batch Size': batch_size,
            'Accuracy (%)': round(val_accuracy * 100, 2),
            'Filename': model_filename,
            'Timestamp': created_at
        })
    
    conn.close()
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    return df


def train_new_model(architecture, epochs, batch_size):
    """Train a model (MLP or CNN) and show progress each epoch."""
    try:
        # Convert to integers
        epochs = int(epochs)
        batch_size = int(batch_size)
        
        # Create model based on selected architecture
        if architecture == "MLP":
            new_model = create_mlp()
        elif architecture == "Small CNN":
            new_model = create_small_cnn()
        elif architecture == "Deeper CNN":
            new_model = create_deeper_cnn()
        else:
            yield f"Error: Unknown architecture '{architecture}'"
            return
        
        # Initial message
        yield f"Starting training ({architecture})...\nEpochs: {epochs}, Batch Size: {batch_size}\n\n"
        
        # Train one epoch at a time to show progress
        all_results = []
        for epoch in range(epochs):
            print(f"Training epoch {epoch + 1}/{epochs}...")
            
            # Train for one epoch
            history = new_model.fit(
                x_train, y_train,
                epochs=1,
                batch_size=batch_size,
                validation_data=(x_test, y_test),
                verbose=0  # Suppress Keras output
            )
            
            # Get accuracy for this epoch
            train_acc = history.history['accuracy'][0] * 100
            val_acc = history.history['val_accuracy'][0] * 100
            final_val_acc = history.history['val_accuracy'][0]  # Store for database
            
            # Store results
            epoch_result = f"Epoch {epoch + 1}/{epochs}: Train Acc = {train_acc:.2f}%, Val Acc = {val_acc:.2f}%"
            all_results.append(epoch_result)
            
            # Yield progress update (shows all previous epochs + current)
            yield "\n".join(all_results) + "\n\n"
        
        # Save to database with unique filename
        model_filename = save_training_run(architecture, epochs, batch_size, final_val_acc)
        model_path = f'artifacts/{model_filename}'
        save_model(new_model, model_path)
        print(f"Model saved to {model_path}")
        
        # Final summary
        final_result = "\n".join(all_results) + f"\n\nTraining Complete!\nModel saved to: {model_path}\nSaved to database with Run ID"
        yield final_result
        
    except Exception as e:
        yield f"Error during training: {str(e)}"


def predict_uploaded_image(image):
    """Predict digit from an uploaded image."""
    if image is None:
        return "Please upload an image."
    
    try:
        # Use utility function to preprocess image
        img_array = preprocess_image(image)
        
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
        gr.Markdown("Configure training parameters and choose architecture")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("**Training Parameters**")
                
                architecture_input = gr.Dropdown(
                    label="Model Architecture",
                    choices=["MLP", "Small CNN", "Deeper CNN"],
                    value="MLP"
                )
                
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
            inputs=[architecture_input, epochs_input, batch_size_input],
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
    
    with gr.Tab("History"):
        gr.Markdown("### Training History")
        gr.Markdown("View all previous training runs and their results")
        
        refresh_button = gr.Button("Refresh History", variant="secondary")
        
        # Start with empty DataFrame with the right column names
        empty_df = pd.DataFrame(columns=['Run ID', 'Architecture', 'Epochs', 'Batch Size', 'Accuracy (%)', 'Filename', 'Timestamp'])
        
        history_table = gr.Dataframe(
            label="All Training Runs",
            value=empty_df,
            interactive=False
        )
        
        # Load history on button click
        refresh_button.click(
            fn=get_training_history,
            outputs=history_table,
            api_name=False
        )


if __name__ == "__main__":
    print("\nStarting MNIST Classifier interface...")
    print("- Train tab: Configure and train new models")
    print("- Predict tab: Upload images for digit recognition")
    print("- History tab: View all training runs")
    print("\nOpen http://localhost:7860 in your browser\n")
    demo.launch()
