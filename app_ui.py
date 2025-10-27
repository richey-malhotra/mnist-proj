"""
MNIST Digit Recognition Project
Phase 6: Hello World Gradio Interface
"""

import warnings
# Suppress urllib3 OpenSSL warning (macOS system library compatibility issue)
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')

import gradio as gr

def greet(name):
    """Say hello — just testing Gradio works."""
    if not name or name.strip() == "":
        return "Hello! Please enter your name."
    
    return f"Hello {name}! Welcome to the MNIST Digit Recognition project."

# Create Gradio interface
demo = gr.Interface(
    fn=greet,
    inputs=gr.Textbox(
        label="Your Name",
        placeholder="Enter your name here..."
    ),
    outputs=gr.Textbox(label="Greeting"),
    title="MNIST Digit Recognition - Hello World",
    description="Testing Gradio interface before adding digit recognition."
)

if __name__ == "__main__":
    print("Starting Gradio interface...")
    print("Open http://localhost:7860 in your browser")
    demo.launch()
