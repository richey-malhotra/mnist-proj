"""
MNIST Digit Recognition Project
Phase 20: Error Handling + Input Validation + Drawing Input
"""

import warnings
# Suppress urllib3 OpenSSL warning (macOS system library compatibility issue)
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')

import gradio as gr
from PIL import Image
import numpy as np
import sqlite3
import pandas as pd
import os
from datetime import datetime
from tensorflow.keras.datasets import mnist
from models import create_mlp, create_small_cnn, create_deeper_cnn, load_model, save_model
from utils import preprocess_image
import plotly.graph_objects as go
import time

# Load MNIST data once at startup
print("Loading MNIST dataset...")
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0
print(f"Dataset loaded: {x_train.shape[0]} training images, {x_test.shape[0]} test images")


# Create custom theme for professional look
custom_theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="slate",
    neutral_hue="slate",
    font=("Inter", "sans-serif")
).set(
    button_primary_background_fill="#2E86AB",
    button_primary_background_fill_hover="#236B8E",
    block_title_text_weight="600",
    block_label_text_weight="500"
)


def save_training_run(architecture, epochs, batch_size, val_accuracy, duration=None):
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
        (model_id, epochs, batch_size, val_accuracy, model_filename, duration)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (model_id, epochs, batch_size, val_accuracy, model_filename, duration))
    
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


def get_latest_run_id():
    """Get the run_id of the most recently created training run."""
    conn = sqlite3.connect('artifacts/training_history.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT run_id FROM training_runs ORDER BY run_id DESC LIMIT 1')
    result = cursor.fetchone()
    
    conn.close()
    return result[0] if result else None


def save_epoch_metrics(run_id, epoch, train_accuracy, val_accuracy):
    """Save epoch-by-epoch training metrics to database."""
    conn = sqlite3.connect('artifacts/training_history.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO metrics (run_id, epoch, train_accuracy, val_accuracy)
        VALUES (?, ?, ?, ?)
    ''', (run_id, epoch, train_accuracy, val_accuracy))
    
    conn.commit()
    conn.close()


def create_accuracy_chart():
    """Create accuracy timeline for latest training run."""
    try:
        conn = sqlite3.connect('artifacts/training_history.db')
        cursor = conn.cursor()
        
        # Get latest run
        cursor.execute('SELECT run_id FROM training_runs ORDER BY run_id DESC LIMIT 1')
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            # Show empty state message
            fig = go.Figure()
            fig.add_annotation(
                text="No training history yet<br><br>Train a model in the Train tab to see accuracy charts!",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color="#666666"),
                align="center"
            )
            fig.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                height=400
            )
            return fig
        
        run_id = result[0]
        
        # Get metrics for this run
        cursor.execute('''
            SELECT epoch, train_accuracy, val_accuracy
            FROM metrics
            WHERE run_id = ?
            ORDER BY epoch
        ''', (run_id,))
        
        data = cursor.fetchall()
        conn.close()
        
        if not data:
            # Metrics missing for this run
            fig = go.Figure()
            fig.add_annotation(
                text="No epoch metrics found for latest run<br><br>Train a new model to generate metrics",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color="#666666"),
                align="center"
            )
            fig.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                height=400
            )
            return fig
    except Exception as e:
        # Error state
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error loading accuracy chart<br><br>{str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color="#cc0000"),
            align="center"
        )
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=400
        )
        return fig
    
    epochs = [row[0] for row in data]
    train_acc = [row[1] * 100 for row in data]
    val_acc = [row[2] * 100 for row in data]
    
    # Create plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=epochs, y=train_acc,
        name='Training Accuracy',
        mode='lines+markers'
    ))
    fig.add_trace(go.Scatter(
        x=epochs, y=val_acc,
        name='Validation Accuracy',
        mode='lines+markers'
    ))
    
    fig.update_layout(
        title='Accuracy Over Epochs (Latest Run)',
        xaxis_title='Epoch',
        yaxis_title='Accuracy (%)',
        hovermode='x unified'
    )
    
    return fig


def create_performance_dashboard():
    """Create scatter plot showing accuracy vs training time for all models."""
    try:
        conn = sqlite3.connect('artifacts/training_history.db')
        cursor = conn.cursor()
        
        # Get all runs with performance data (no JOIN - query models separately)
        cursor.execute('''
            SELECT model_id, val_accuracy, duration
            FROM training_runs
            WHERE duration IS NOT NULL AND val_accuracy IS NOT NULL
            ORDER BY model_id
        ''')
        
        runs = cursor.fetchall()
        
        # Build data list with architecture names
        data = []
        for model_id, val_acc, duration in runs:
            # Look up architecture for this model_id
            cursor.execute('SELECT architecture FROM models WHERE model_id = ?', (model_id,))
            arch_result = cursor.fetchone()
            if arch_result:
                data.append((arch_result[0], val_acc, duration))
        
        conn.close()
        
        if not data:
            # Show empty state message
            fig = go.Figure()
            fig.add_annotation(
                text="No performance data available<br><br>Train models to compare their speed and accuracy!",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color="#666666"),
                align="center"
            )
            fig.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                height=400
            )
            return fig
    except Exception as e:
        # Error state
        fig = go.Figure()
        fig.add_annotation(
            text=f"Error loading performance dashboard<br><br>{str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color="#cc0000"),
            align="center"
        )
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            height=400
        )
        return fig
    
    # Prepare data for plotting
    architectures = []
    accuracies = []
    durations = []
    colors = []
    
    # Colour mapping for architectures
    color_map = {
        'MLP': '#1f77b4',      # Blue
        'Small CNN': '#ff7f0e', # Orange  
        'Deeper CNN': '#2ca02c' # Green
    }
    
    for arch, acc, dur in data:
        architectures.append(arch)
        accuracies.append(acc * 100)  # Convert to percentage
        durations.append(dur)
        colors.append(color_map.get(arch, '#9467bd'))  # Default purple
    
    # Create scatter plot
    fig = go.Figure()
    
    # Add traces for each architecture
    for arch in set(architectures):
        arch_mask = [a == arch for a in architectures]
        arch_accuracies = [accuracies[i] for i in range(len(accuracies)) if arch_mask[i]]
        arch_durations = [durations[i] for i in range(len(durations)) if arch_mask[i]]
        arch_colors = [colors[i] for i in range(len(colors)) if arch_mask[i]]
        
        fig.add_trace(go.Scatter(
            x=arch_durations,
            y=arch_accuracies,
            mode='markers',
            name=arch,
            marker=dict(
                size=10,
                color=arch_colors[0] if arch_colors else '#9467bd',
                line=dict(width=2, color='white')
            ),
            text=[f'{arch}<br>Accuracy: {acc:.1f}%<br>Time: {dur:.1f}s' 
                  for acc, dur in zip(arch_accuracies, arch_durations)],
            hovertemplate='%{text}<extra></extra>'
        ))
    
    fig.update_layout(
        title='Model Performance: Accuracy vs Training Time',
        xaxis_title='Training Time (seconds)',
        yaxis_title='Validation Accuracy (%)',
        hovermode='closest',
        showlegend=True
    )
    
    return fig


def get_best_models():
    """
    Find the best performing model for each architecture.
    Returns a dictionary: {'Architecture': ('filename.keras', accuracy)}
    """
    conn = sqlite3.connect('artifacts/training_history.db')
    cursor = conn.cursor()
    
    # Get all architectures (with model_id for lookup)
    cursor.execute('SELECT model_id, architecture FROM models')
    models = cursor.fetchall()
    
    best_models = {}
    
    for model_id, arch in models:
        # Find best run for this architecture (highest validation accuracy)
        # Simple query without JOIN
        cursor.execute('''
            SELECT model_filename, val_accuracy 
            FROM training_runs
            WHERE model_id = ?
            ORDER BY val_accuracy DESC
            LIMIT 1
        ''', (model_id,))
        
        result = cursor.fetchone()
        if result:
            filename = result[0]
            # Verify file exists before adding
            if os.path.exists(f'artifacts/{filename}'):
                best_models[arch] = (filename, result[1])
            else:
                print(f"Warning: Best model for {arch} ({filename}) not found on disk.")
    
    conn.close()
    return best_models


def train_new_model(architecture, epochs, batch_size):
    """Train a model (MLP or CNN) and show progress each epoch."""
    try:
        # Convert to integers
        epochs = int(epochs)
        batch_size = int(batch_size)
        
        # Start timing
        start_time = time.time()
        
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
        
        # Get run_id for this training session (save metrics later)
        run_id = None
        
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
            
            # Save metrics to database (get run_id on first epoch)
            if run_id is None:
                # Calculate duration so far (for first epoch)
                current_duration = time.time() - start_time
                # Save training run first to get run_id
                model_filename = save_training_run(architecture, epochs, batch_size, final_val_acc, current_duration)
                run_id = get_latest_run_id()
            
            # Save epoch metrics
            save_epoch_metrics(run_id, epoch + 1, history.history['accuracy'][0], history.history['val_accuracy'][0])
            
            # Store results
            epoch_result = f"Epoch {epoch + 1}/{epochs}: Train Acc = {train_acc:.2f}%, Val Acc = {val_acc:.2f}%"
            all_results.append(epoch_result)
            
            # Yield progress update (shows all previous epochs + current)
            yield "\n".join(all_results) + "\n\n"
        
        # Save model file
        model_path = f'artifacts/{model_filename}'
        save_model(new_model, model_path)
        print(f"Model saved to {model_path}")
        
        # Calculate total training duration
        total_duration = time.time() - start_time
        
        # Update duration in database
        conn = sqlite3.connect('artifacts/training_history.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE training_runs SET duration = ? WHERE run_id = ?', (total_duration, run_id))
        conn.commit()
        conn.close()
        
        # Final summary
        final_result = "\n".join(all_results) + f"\n\nTraining Complete!\nModel saved to: {model_path}\nSaved to database with Run ID {run_id}\nTotal time: {total_duration:.1f}s"
        yield final_result
        
    except Exception as e:
        yield f"Error during training: {str(e)}"


def predict_with_validation(input_method, uploaded_image, drawn_image):
    """Predict digit from uploaded or drawn image."""
    try:
        # Determine which input to use
        if input_method == "Upload Image":
            if uploaded_image is None:
                # Return blank images for error display
                blank_image = Image.new('L', (28, 28), 255)
                return blank_image, blank_image, "❌ Please upload an image first."
            image = uploaded_image
            input_type = "uploaded"
        else:  # Draw Digit
            if drawn_image is None or isinstance(drawn_image, bool):
                # Return blank images for error display
                blank_image = Image.new('L', (28, 28), 255)
                return blank_image, blank_image, "❌ Please draw a digit on the canvas first."
            
            # Sketchpad returns a dict with 'composite' key containing the image
            if isinstance(drawn_image, dict):
                if 'composite' in drawn_image and drawn_image['composite'] is not None:
                    image = drawn_image['composite']
                else:
                    blank_image = Image.new('L', (28, 28), 255)
                    return blank_image, blank_image, "❌ Please draw a digit on the canvas first."
            else:
                image = drawn_image
            input_type = "drawn"
        
        # Validate the image has content
        if image is None:
            blank_image = Image.new('L', (28, 28), 255)
            return blank_image, blank_image, f"❌ No {input_type} image provided."
        
        # Check if image is a valid image type (not boolean or other invalid type)
        if isinstance(image, bool):
            blank_image = Image.new('L', (28, 28), 255)
            return blank_image, blank_image, f"❌ Invalid {input_type} image format. Please try again."
        
        # Check if image has any content (not completely empty/white)
        try:
            img_array = np.array(image)
            # Convert to greyscale if needed
            if len(img_array.shape) == 3:
                img_array = np.mean(img_array, axis=2)
            
            # Check if image is mostly empty (all white pixels)
            if np.mean(img_array) > 250:  # Very light, probably empty
                blank_image = Image.new('L', (28, 28), 255)
                return blank_image, blank_image, f"❌ {input_type.capitalize()} image appears to be empty. Please provide a clearer digit."
        except Exception as e:
            blank_image = Image.new('L', (28, 28), 255)
            return blank_image, blank_image, f"❌ Error processing {input_type} image: {str(e)}"
        
        # Check if any models exist
        best_models = get_best_models()
        if not best_models:
            blank_image = Image.new('L', (28, 28), 255)
            error_df = pd.DataFrame([{
                'Rank': '-',
                'Architecture': 'None',
                'Prediction': '-',
                'Confidence': '-',
                'Top-5 Probabilities': 'No models trained yet'
            }])
            return blank_image, blank_image, error_df, "❌ No trained models found. Please train some models in the Train tab first."
        
        # Process images
        try:
            # Original image (keep as-is for display)
            original = Image.fromarray(image)
            
            # For drawn images, invert colours (Sketchpad draws black on white, MNIST expects white on black)
            if input_type == "drawn":
                # Invert the image before preprocessing
                img_array = np.array(image)
                if len(img_array.shape) == 3:
                    img_array = np.mean(img_array, axis=2)
                img_array = 255 - img_array  # Invert
                image = img_array.astype('uint8')
            
            # Preprocessed image (what model sees)
            img_input = preprocess_image(image)
            img_preprocessed = Image.fromarray((img_input * 255).astype('uint8'))
        except Exception as e:
            blank_image = Image.new('L', (28, 28), 255)
            return blank_image, blank_image, f"❌ Error processing image: {str(e)}"
        
        results_lines = []  # final strings
        model_rows = []     # structured data for sorting
        predictions = []

        for arch, (filename, accuracy) in best_models.items():
            try:
                model_path = f'artifacts/{filename}'
                model = load_model(model_path)
                prediction = model.predict(img_input.reshape(1, 28, 28), verbose=0)
                probs = prediction[0]
                digit = int(probs.argmax())
                confidence = float(probs[digit]) * 100
                predictions.append(digit)
                top_probs = sorted(enumerate(probs), key=lambda x: x[1], reverse=True)[:5]
                model_rows.append({
                    'arch': arch,
                    'digit': digit,
                    'confidence': confidence,
                    'top_probs': top_probs
                })
            except Exception as e:
                # Store error as very low confidence so it sinks to bottom
                model_rows.append({
                    'arch': arch,
                    'digit': None,
                    'confidence': -1.0,
                    'top_probs': [],
                    'error': str(e)
                })

        # Sort models by confidence descending
        sorted_models = sorted(model_rows, key=lambda m: m['confidence'], reverse=True)
        if sorted_models:
            top_model = sorted_models[0]
            if top_model.get('confidence', -1) >= 0:
                results_lines.append(
                    f"➡ Top model: {top_model['arch']} predicted {top_model['digit']} ({top_model['confidence']:.1f}% confidence)"
                )

        # Build results table
        table_data = []
        for idx, m in enumerate(sorted_models):
            if 'error' in m:
                table_data.append({
                    'Rank': f"#{idx+1}",
                    'Architecture': m['arch'],
                    'Prediction': 'Error',
                    'Confidence': '-',
                    'Top-5 Probabilities': m['error']
                })
                continue
            
            # Format top-5 probabilities
            top_str = ", ".join([f"{d}:{p*100:.1f}%" for d, p in m['top_probs']])
            
            # Add star to winner
            rank = f"⭐ #{idx+1}" if idx == 0 else f"#{idx+1}"
            
            table_data.append({
                'Rank': rank,
                'Architecture': m['arch'],
                'Prediction': str(m['digit']),
                'Confidence': f"{m['confidence']:.1f}%",
                'Top-5 Probabilities': top_str
            })
        
        results_df = pd.DataFrame(table_data)
        
        # Consensus message
        clean_preds = [m['digit'] for m in sorted_models if 'error' not in m and m['digit'] is not None]
        if len(clean_preds) >= 2:
            # Only show consensus if 2+ models available
            if len(set(clean_preds)) == 1:
                consensus_msg = "✅ All models agree"
            else:
                consensus_msg = "⚠️ Models disagree"
        else:
            # Don't show consensus message for single model
            consensus_msg = ""

        return original, img_preprocessed, results_df, consensus_msg
    
    except Exception as e:
        blank_image = Image.new('L', (28, 28), 255)
        error_df = pd.DataFrame([{
            'Rank': '-',
            'Architecture': 'Error',
            'Prediction': '-',
            'Confidence': '-',
            'Top-5 Probabilities': str(e)
        }])
        return blank_image, blank_image, error_df, f"❌ Unexpected error: {str(e)}"


def predict_with_preview(image):
    """Predict digit using all best models and show the preprocessed image too."""
    if image is None:
        return None, None, "Please upload an image."
    
    best_models = get_best_models()
    
    if not best_models:
        return None, None, "No trained models found. Please train some models first!"
    
    # Process images
    try:
        # Original image (keep as-is for display)
        original = Image.fromarray(image)
        
        # Preprocessed image (what model sees)
        img_array = preprocess_image(image)
        img_preprocessed = Image.fromarray((img_array * 255).astype('uint8'))
        
        # Prepare for prediction
        img_input = np.expand_dims(img_array, axis=0)
    except Exception as e:
        return None, None, f"Error processing image: {e}"
    
    results = []
    predictions = []
    
    for arch, (filename, accuracy) in best_models.items():
        try:
            # Load model
            model_path = f'artifacts/{filename}'
            model = load_model(model_path)
            
            # Predict
            pred = model.predict(img_input, verbose=0)
            digit = int(pred.argmax())
            confidence = float(pred[0][digit]) * 100
            
            predictions.append(digit)
            
            # Format output
            results.append(f"{arch}: Predicted {digit} (Conf: {confidence:.1f}%)")
            
        except Exception as e:
            results.append(f"{arch}: Error loading/predicting ({e})")
    
    # Add consensus check
    if predictions and len(set(predictions)) == 1:
        results.append(f"\n✅ Consensus: All models agree on {predictions[0]}")
    elif predictions:
        results.append(f"\n⚠️ Disagreement: Models predict different digits")
        
    return original, img_preprocessed, "\n".join(results)


# Create Gradio interface with tabs
with gr.Blocks(theme=custom_theme, title="MNIST Digit Classifier") as demo:
    gr.Markdown("# 🔢 MNIST Digit Recognition")
    gr.Markdown("Train and compare neural networks for handwritten digit classification")
    
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
                    value="👈 Select architecture and parameters, then click 'Start Training'\n\nAvailable architectures:\n• MLP: Simple fully-connected network (~30s)\n• Small CNN: Convolutional network (~60s)\n• Deeper CNN: More complex CNN (~90s)\n\nTraining progress will appear here..."
                )
        
        train_button.click(
            fn=train_new_model,
            inputs=[architecture_input, epochs_input, batch_size_input],
            outputs=training_output,
            api_name=False  # Disable API to avoid Gradio bug
        )
    
    with gr.Tab("Predict"):
        gr.Markdown("### Digit Prediction")
        gr.Markdown("Upload an image or draw a digit to see predictions from your best models.")
        
        with gr.Tabs():
            with gr.TabItem("Upload Image"):
                gr.Markdown("**Upload a digit image**")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        image_input = gr.Image(label="Upload Digit Image", height=280)
                        upload_predict_button = gr.Button("Predict with All Models", variant="primary")
                        
                        with gr.Row():
                            upload_original_display = gr.Image(
                                label="Original Image", 
                                interactive=False,
                                height=250,
                                width=250
                            )
                            upload_preprocessed_display = gr.Image(
                                label="Model Input (28×28)", 
                                interactive=False,
                                height=250,
                                width=250
                            )
                    
                    with gr.Column(scale=2):
                        gr.Markdown("**Model Predictions**")
                        # Start with empty state message
                        empty_state_df = pd.DataFrame([{
                            'Rank': '→',
                            'Architecture': 'Waiting for input...',
                            'Prediction': '-',
                            'Confidence': '-',
                            'Top-5 Probabilities': 'Upload an image above and click Predict'
                        }])
                        upload_prediction_output = gr.Dataframe(
                            label="Prediction Results",
                            headers=['Rank', 'Architecture', 'Prediction', 'Confidence', 'Top-5 Probabilities'],
                            datatype=['str', 'str', 'str', 'str', 'str'],
                            row_count=3,
                            col_count=(5, "fixed"),
                            value=empty_state_df
                        )
                        upload_consensus_output = gr.Markdown("👆 Upload a digit image above to get started")
            
            with gr.TabItem("Draw Digit"):
                gr.Markdown("**Draw a digit on the canvas**")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        sketch_input = gr.Sketchpad(
                            label="Draw Digit",
                            height=280,
                            width=280
                        )
                        draw_hint = gr.Markdown("*Draw a digit from 0-9 on the canvas above*")
                        draw_predict_button = gr.Button("Predict with All Models", variant="primary")
                        
                        with gr.Row():
                            draw_original_display = gr.Image(
                                label="Your Drawing", 
                                interactive=False,
                                height=250,
                                width=250
                            )
                            draw_preprocessed_display = gr.Image(
                                label="Model Input (28×28)", 
                                interactive=False,
                                height=250,
                                width=250
                            )
                    
                    with gr.Column(scale=2):
                        gr.Markdown("**Model Predictions**")
                        # Start with empty state message
                        empty_state_df_draw = pd.DataFrame([{
                            'Rank': '→',
                            'Architecture': 'Waiting for input...',
                            'Prediction': '-',
                            'Confidence': '-',
                            'Top-5 Probabilities': 'Draw a digit on the canvas and click Predict'
                        }])
                        draw_prediction_output = gr.Dataframe(
                            label="Prediction Results",
                            headers=['Rank', 'Architecture', 'Prediction', 'Confidence', 'Top-5 Probabilities'],
                            datatype=['str', 'str', 'str', 'str', 'str'],
                            row_count=3,
                            col_count=(5, "fixed"),
                            value=empty_state_df_draw
                        )
                        draw_consensus_output = gr.Markdown("✏️ Draw a digit on the canvas above to get started")
        
        upload_predict_button.click(
            fn=lambda img: predict_with_validation("Upload Image", img, None),
            inputs=[image_input],
            outputs=[upload_original_display, upload_preprocessed_display, upload_prediction_output, upload_consensus_output],
            api_name=False
        )
        
        draw_predict_button.click(
            fn=lambda img: predict_with_validation("Draw Digit", None, img),
            inputs=[sketch_input],
            outputs=[draw_original_display, draw_preprocessed_display, draw_prediction_output, draw_consensus_output],
            api_name=False
        )
    
    with gr.Tab("History"):
        gr.Markdown("### Training History")
        gr.Markdown("View all previous training runs and their accuracy charts")
        
        refresh_button = gr.Button("Refresh History", variant="secondary")
        
        # Start with empty DataFrame with the right column names
        empty_df = pd.DataFrame(columns=['Run ID', 'Architecture', 'Epochs', 'Batch Size', 'Accuracy (%)', 'Filename', 'Timestamp'])
        
        history_table = gr.Dataframe(
            label="All Training Runs",
            value=empty_df,
            interactive=False
        )
        
        # Accuracy chart
        accuracy_chart = gr.Plot(label="Training Accuracy Chart")
        
        # Time comparison chart
        time_chart = gr.Plot(label="Performance Dashboard")
        
        # Load history and chart on button click
        refresh_button.click(
            fn=get_training_history,
            outputs=history_table,
            api_name=False
        ).then(
            fn=create_accuracy_chart,
            outputs=accuracy_chart,
            api_name=False
        ).then(
            fn=create_performance_dashboard,
            outputs=time_chart,
            api_name=False
        )


if __name__ == "__main__":
    print("\nStarting MNIST Classifier interface...")
    print("- Train tab: Configure and train new models")
    print("- Predict tab: Upload images or draw digits for recognition")
    print("- History tab: View all training runs")
    print("\nOpen http://localhost:7860 in your browser\n")
    demo.launch()
