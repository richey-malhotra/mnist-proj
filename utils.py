"""
Image preprocessing function to avoid repeating code.
"""

from PIL import Image
import numpy as np


def preprocess_image(image):
    """
    Convert uploaded image so the model can use it.
    Makes it greyscale, resizes to 28x28, and normalises to 0-1.
    """
    # Convert NumPy array to PIL Image if needed
    if isinstance(image, np.ndarray):
        # If RGB (3 channels), convert to PIL
        if len(image.shape) == 3:
            img = Image.fromarray(image.astype('uint8'))
        else:
            # Already greyscale
            img = Image.fromarray(image.astype('uint8'))
    else:
        img = image
    
    # Convert to greyscale (L mode)
    img = img.convert('L')
    
    # Resize to 28×28 (MNIST size)
    img = img.resize((28, 28))
    
    # Convert to NumPy array and normalise to 0-1
    img_array = np.array(img).astype('float32') / 255.0
    
    return img_array
