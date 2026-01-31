# MNIST Digit Recognition Web Application

A web app where you can train neural networks to recognise handwritten digits and test them out. Built with Gradio for the interface and TensorFlow for the machine learning side.

**Author**: Harpreet Malhotra  
**Date**: February 2026  
**Purpose**: A-Level Computer Science NEA Project

Tried to write this so it's actually useful rather than just ticking boxes. Some of it's probably rough but it's honest about what works and what doesn't.

## Features

### Training
- Train three different neural network architectures:
  - **MLP (Multi-Layer Perceptron)**: Simple fully-connected network (~10s training)
  - **Small CNN**: Convolutional network with pattern detection (~45s training)
  - **Deeper CNN**: Bigger CNN with dropout regularisation (~90s training)
- You can change hyperparameters (epochs, batch size)
- Shows training progress in real time
- Models get saved automatically with unique filenames

### Prediction
- **Upload Mode**: Upload images of handwritten digits (JPG/PNG)
- **Draw Mode**: Draw digits directly on canvas with mouse/touch
- Compare predictions from all your trained models side by side
- Confidence scores and top-5 probability distributions
- Shows whether the models agree or disagree
- Preview of the processed image so you can see what the model actually gets

### History & Charts
- Training history charts showing accuracy trends over time
- Chart comparing training times and accuracy for different models
- Saved models table with all training run details
- SQLite database that saves all your training runs

## Quick Start

### 1. Create Virtual Environment

**Requires Python 3.9** (Python 3.12+ is not compatible with the pinned TensorFlow version). I developed the whole project on Python 3.9.6 (macOS system Python), so that's the version everything's been tested with.

If you only have Python 3.12+, install a compatible version first:
```bash
brew install python@3.11          # macOS with Homebrew
python3.11 -m venv venv           # then use python3.11 instead of python3
```

```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages**:
- `gradio` - Web interface framework
- `tensorflow` - Neural network training
- `numpy` - Array operations
- `pillow` - Image processing
- `plotly` - Interactive charts
- `pandas` - Data tables

### 3. Initialise Database

```bash
python init_db.py
```

Creates `artifacts/training_history.db` with tables for models and training runs.

> **Note**: Pre-trained models and a populated database are included in the repo, so you can skip straight to launching the app and making predictions. Only run `init_db.py` if you want to start fresh.

### 4. Launch Application

```bash
python app_ui.py
```

Open browser to **http://localhost:7860**

## How to Use

### Training a Model

1. Go to **Train** tab
2. Pick an architecture from the dropdown:
   - MLP: Fastest, good for learning the basics
   - Small CNN: Better accuracy, takes a bit longer
   - Deeper CNN: Best accuracy, slowest training
3. Set training parameters:
   - **Epochs**: 3-5 is fine for quick tests, 10 for best results
   - **Batch Size**: 32 (balanced), 64 (faster), 128 (fastest but a bit less stable)
4. Click **Start Training**
5. Watch real-time progress updates
6. Model gets automatically saved when it's done

### Making Predictions

**Upload Tab**:
1. Click **Upload Image** button
2. Pick an image file (JPG/PNG) with a handwritten digit
3. Click **Predict with All Models**
4. View results table showing each model's prediction and confidence
5. Check the consensus message (whether they agree or not)

**Draw Tab**:
1. Draw a digit on the canvas with your mouse or touchscreen
2. Click **Predict with All Models**
3. Same prediction table and consensus as the Upload tab

**Results Table Columns**:
- **Rank**: Sorting order (most confident first)
- **Architecture**: Which model type
- **Prediction**: What digit it thinks it is (0-9)
- **Confidence**: How sure it is (0-100%)
- **Top-5 Probabilities**: Shows the top 5 most likely digits

### Viewing History

**History Tab**:
1. Click **Refresh History**
2. Two charts show up:
   - **Accuracy Comparison**: Line chart showing how validation accuracy changes over epochs
   - **Speed vs Accuracy**: Scatter plot comparing training times and accuracy

The same Refresh button also loads a **table of all training runs** showing:
   - Run ID, Architecture, Epochs, Batch Size
   - Final accuracy, Training duration
   - When it was trained

## Why I Did It This Way

### No Code Changes in Phase 23

Phase 23 doesn't change any functional code — only minor comment adjustments and documentation. This is deliberate. The final phase is about writing up the project, not adding new features. I wanted to keep it clear what was building vs what was writing about.

### `init_db.py` Safe to Run Multiple Times

```python
try:
    cursor.execute("ALTER TABLE training_runs ADD COLUMN duration REAL")
except sqlite3.OperationalError:
    pass  # Column already exists
```

`init_db.py` uses try/except around ALTER TABLE to add columns that might already exist. So you can run it again on an existing database and it won't crash - it just skips anything that's already there. It's a simple way to handle database upgrades without anything fancy.

### `demo.launch()` With Defaults

Same as Phase 6, with no arguments, so it runs on localhost port 7860 with no public URL. The defaults are fine for a local app where it's just me using it.

### `api_name=False` on Generator Functions

Same issue as Phase 7. Gradio auto-creates API endpoints for every button handler, and generator functions (ones that use `yield`) don't work well with those endpoints. `api_name=False` just turns that off for the training function and anything else that yields.

### Known Issues I Didn't Fix

There are a few things I found in earlier phases that are still there: the leftover `preprocess_image` and `predict_digit` pair in `models.py` that nothing ever calls (they were from before I moved prediction logic into `app_ui.py`), an unused `datetime` import, an old `predict_with_preview()` function in `app_ui.py` that got replaced by `predict_with_validation()` but I forgot to delete, and `predict_with_validation()` still having some weird situations where it might return the wrong number of values. I documented these rather than fixing them because the later phases were supposed to be documentation-only, and fixing them would of mixed up what each phase is supposed to be about. Listed them as known limitations above.

## Project Structure

```
mnist-proj/
├── app_ui.py           # Main application (957 lines)
├── models.py           # Neural network architectures (116 lines)
├── utils.py            # Image preprocessing utilities (36 lines)
├── init_db.py          # Database schema setup (71 lines)
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── diary.md            # Development journal (per-phase, see git history)
├── tests.md            # Testing log with results
├── feedback.md         # Stakeholder feedback
├── artifacts/          # Model files and database
│   ├── training_history.db      # SQLite database
│   └── model_[arch]_run[N].keras # Saved models
├── screenshots/        # Evidence screenshots for testing log
└── testing/            # Video evidence and test scripts
    ├── [date]_test[N]_[name]/
    │   ├── test_script.md   # What to demonstrate
    │   └── recording.webm   # Screen recording
    └── ...              # 7 test folders total
```

### File Descriptions

### `app_ui.py` (957 lines)

This is the main file, with the Gradio interface and basically all the application logic.

**What's in it**:
- Data loading (MNIST dataset)
- UI theme configuration
- Database functions (saving and retrieving training runs)
- Training functions (model creation and training loop)
- Prediction functions (handling upload/draw input)
- Chart creation (Plotly stuff)
- UI layout (3 tabs: Train, Predict, History)

**Main functions**:
- `train_new_model()`: Trains whichever architecture you picked, with progress updates
- `predict_with_validation()`: Processes images and gets predictions from all models
- `save_training_run()`: Records training results to the database
- `get_training_history()`: Pulls data out for the charts
- `create_accuracy_chart()`: Makes the accuracy comparison line chart
- `create_performance_dashboard()`: Makes the training time scatter plot

### `models.py` (116 lines)

Has the neural network architecture definitions using TensorFlow/Keras.

**Three Model Types**:

1. **MLP (Multi-Layer Perceptron)**:
   - Architecture: Flatten -> Dense(128) -> Dense(10)
   - Parameters: ~101,000
   - Training time: ~10 seconds
   - Expected accuracy: ~95-98% depending on epochs and batch size
   - Best for: Understanding how neural networks work

2. **Small CNN (Convolutional Neural Network)**:
   - Architecture: Reshape -> Conv2D(32) -> MaxPool -> Flatten -> Dense(64) -> Dense(10)
   - Training time: ~45 seconds
   - Expected accuracy: ~98.5%
   - Best for: Good balance of speed and accuracy

3. **Deeper CNN**:
   - Architecture: Reshape -> Conv2D(32) -> Conv2D(64) -> MaxPool -> Dropout(0.25) -> Flatten -> Dense(128) -> Dropout(0.5) -> Dense(10)
   - Training time: ~90 seconds
   - Expected accuracy: ~99.2-99.4%
   - Best for: Getting the highest accuracy possible

**Functions**:
- `create_mlp()`, `create_small_cnn()`, `create_deeper_cnn()`: Build each model
- `save_model()`: Saves a trained model to a .keras file
- `load_model()`: Loads a model back from file for predictions

### `utils.py` (36 lines)

Handles image preprocessing, converting whatever you upload or draw into the format MNIST models expect.

**Preprocessing Steps**:
1. Convert to PIL Image (handles numpy arrays from Gradio)
2. Convert to greyscale ('L' mode)
3. Resize to 28x28 pixels (MNIST standard size)
4. Convert to numpy array and normalise to 0-1 range (divide by 255)

**Function**:
- `preprocess_image(img)`: Does all the above steps

### `init_db.py` (71 lines)

Sets up the database tables.

**Tables Created**:
- `models`: Stores architecture types (model_id, architecture)
- `training_runs`: Records each training session (run_id, model_id, epochs, batch_size, val_accuracy, model_filename, duration, created_at)
- `metrics`: Stores per-epoch accuracy data for charts (metric_id, run_id, epoch, train_accuracy, val_accuracy)

**Usage**: Run once before first use: `python init_db.py`

### `requirements.txt`

Python package dependencies with versions pinned so nothing breaks later:
```
tensorflow==2.15.0
numpy==1.24.3
gradio==4.36.1
huggingface_hub<1.0
Pillow==10.0.0
plotly==6.5.0
pandas==2.0.3
```

**Note**: These versions require Python 3.9. Python 3.12+ is not supported due to TensorFlow 2.15 compatibility.

## Database Schema

### `models` Table
| Column | Type | Description |
|--------|------|-------------|
| model_id | INTEGER PRIMARY KEY | Unique model identifier |
| architecture | TEXT NOT NULL | Architecture type (MLP/Small CNN/Deeper CNN) |
| created_at | TIMESTAMP | Auto-set when row is inserted |

### `training_runs` Table
| Column | Type | Description |
|--------|------|-------------|
| run_id | INTEGER PRIMARY KEY | Unique run identifier |
| model_id | INTEGER | Foreign key to models table |
| epochs | INTEGER | Number of training epochs |
| batch_size | INTEGER | Training batch size |
| val_accuracy | REAL | Final validation accuracy (0-1) |
| model_filename | TEXT | Saved model file (e.g. model_mlp_run4.keras) |
| duration | REAL | Training time in seconds |
| created_at | TIMESTAMP | Auto-set when row is inserted |

### `metrics` Table
| Column | Type | Description |
|--------|------|-------------|
| metric_id | INTEGER PRIMARY KEY | Unique metric identifier |
| run_id | INTEGER | Foreign key to training_runs |
| epoch | INTEGER | Epoch number (1-based) |
| train_accuracy | REAL | Training accuracy for this epoch |
| val_accuracy | REAL | Validation accuracy for this epoch |
| created_at | TIMESTAMP | Auto-set when row is inserted |

**Note**: I use simple sequential queries (no JOINs) because they're easier to understand and debug. For a database with maybe 50 rows the performance difference doesn't matter.

**Schema Note**: Uniqueness for architectures is handled in the code (it checks if one already exists before inserting a new row). I used `NOT NULL` instead of `UNIQUE` because it was simpler to handle programmatically than dealing with constraint violation errors.

## Technical Details

### What I Used

**Interface stuff**:
- **Gradio 4.36.1**: Python web framework for ML interfaces. I picked this because it's way simpler than building a full Flask/React app
- **Plotly 6.5.0**: Interactive charts (accuracy trends, performance scatter plot)
- **Pandas 2.0.3**: Data table formatting

**The ML and data side**:
- **TensorFlow 2.15.0**: Neural network training and inference
- **SQLite3**: Embedded database - no separate server needed, just a file
- **NumPy 1.24.3**: Array operations and numerical computing
- **Pillow 10.0.0**: Image loading, resizing, format conversion

**Development tools**:
- **VS Code**: Code editor with Python extension for syntax highlighting and error checking
- **Git**: Version control - each development phase is a separate commit so I can track what changed and when, and go back to earlier versions if something breaks. Used `git log` a lot to check what I'd done and `git diff` to see what changed between phases
- **GitHub**: Remote backup of the repository. Also means Mr Davies can see the commit history and verify the development timeline
- **macOS**: Developed on a Mac with Python 3.9.6 (the system Python)

### Why I Did Things This Way

**Simple SQL queries**: I used sequential queries instead of JOINs because they're easier to follow and debug. Less efficient technically, but for a small database it doesn't matter.

**Generator for training**: `train_new_model()` uses `yield` to send progress updates during training. This lets the UI update in real time without me having to mess with threading.

**Unique filenames**: Models get saved as `model_[architecture]_run[N].keras` where N goes up automatically. This just stops you accidentally overwriting a model you trained earlier.

**Empty state handling**: All the charts show helpful messages when there's no data yet instead of just being blank. Big difference on first launch.

**Input validation**: The app checks that you've actually drawn or uploaded something before trying to predict, because otherwise you'd just get confusing errors.

### Performance

**MNIST Dataset Loading**: ~2-3 seconds on first import (60,000 training images)

**Training Times** (on my laptop, default 3 epochs):
- MLP: ~10 seconds
- Small CNN: ~45 seconds
- Deeper CNN: ~90 seconds

Times vary depending on your computer. More epochs = proportionally longer.

**Prediction Speed**: Feels instant, probably under 100ms per image based on how fast results appear

**Database Queries**: Essentially instant for the small dataset size

## How I Documented the Code

All the Python files have proper documentation now (added in Phase 22):

**Function Docstrings** (the Args/Returns format I kept seeing in tutorials):
```python
def function_name(param1, param2):
    """
    Brief one-line description of what function does.

    Longer explanation of purpose, behaviour, and any important details.
    Multiple paragraphs if the function needs more explanation.

    Args:
        param1 (type): Description of first parameter
        param2 (type): Description of second parameter

    Returns:
        type: Description of what function returns

    Example:
        >>> result = function_name('test', 42)
        >>> print(result)

    Note:
        Any special things to watch out for
    """
```

**Section Markers**: Big files are split up with clear headers (DATA LOADING, DATABASE FUNCTIONS, etc.) so you can find things quickly.

**Inline Comments**: I tried to explain WHY I did something, not WHAT the code does. The code already shows what it does.

## Known Limitations

- **Single User**: Only one person can use it at a time
- **Local Storage**: Models and database are only on your machine
- **No Model Versioning**: Can't go back to a previous model version
- **Limited Validation**: Only checks for blank images, not whether the image quality is any good
- **Best on desktop**: Works on mobile but it's better on a bigger screen
- **No Export**: Can't download predictions or training data as files

## Things I'd Add If I Had More Time

- **Put it online**: Host on Hugging Face Spaces or something
- **Multiple users**: Let more than one person use it at the same time
- **Better model comparison**: Add confusion matrices and compare predictions properly
- **Export Features**: Download training history as CSV, export predictions
- **More Architectures**: Add ResNet or other CNN types, maybe transfer learning
- **Custom Datasets**: Let users upload their own training data
- **Phone layout**: Make it work better on small screens
- **Sharing Models**: Let different people share trained models

## Testing

**Checking syntax**: Run individual imports to make sure nothing's broken
```bash
python -c "import app_ui"
python -c "import models"
python -c "import utils"
```

**Full app test**: Launch and test each tab manually
```bash
python app_ui.py
# Test each tab in the browser
```

**Database check**: Verify the tables are set up right
```bash
sqlite3 artifacts/training_history.db ".schema"
```

## Troubleshooting

**Problem**: `ModuleNotFoundError: No module named 'tensorflow'`  
**Solution**: Make sure your virtual environment is activated and run `pip install -r requirements.txt`

**Problem**: `sqlite3.OperationalError: no such table: models`  
**Solution**: Run `python init_db.py` to create the database

**Problem**: "No trained models found" when predicting  
**Solution**: You need to train at least one model first in the Train tab

**Problem**: Blank charts in History tab  
**Solution**: This is normal if you haven't trained anything yet, so train a model and they'll show up

**Problem**: App won't start on port 7860  
**Solution**: Something else is already using that port. Close it or change the port in the code

## Development Timeline

**Total Development**: 23 phases across roughly 120-140 hours (including programming, research, YouTube tutorials, and debugging)
- Phases 1-5: Foundation (models, MNIST loading)
- Phases 6-10: Basic Gradio UI
- Phases 11-15: Multi-model support + database
- Phases 16-20: Advanced features (charts, drawing, validation)
- Phases 21-23: Polish and documentation

### How I Tracked Development

Each of the 23 development phases has its own Git commit. I used Git from the very start (Phase 1) so that every change is recorded. The commit messages describe what each phase adds - you can see the full history with `git log --oneline` which shows all 25 commits (23 development phases across 24 commits, since Phase 13 needed two parts, plus 1 extra commit for the test recordings).

The `diary.md` file gets updated each phase with what I did, what went wrong, and what I learned. Because each commit captures the diary at that point in time, you can use `git checkout [commit hash]` to go back to any phase and see exactly what the project looked like at that point - the code, the diary entry, the test results, everything. To see all the diary entries you'd need to check each commit, since each phase replaces the previous entry (I wrote it as a working document, not a cumulative log - in hindsight I probably should have appended instead of replacing, but by the time I realised it was too late to change without messing up the git history).

I used `.gitignore` from Phase 1 to keep the repository clean - excluding `venv/`, `__pycache__/`, and other files that shouldn't be version controlled. The `.gitkeep` trick to track the empty `artifacts/` folder is explained in the Phase 4 diary entry.

To review the full commit history: `git log --oneline --reverse`
To see a specific phase: `git checkout [hash]` (then `git checkout main` to come back)
To see what changed in a phase: `git diff [prev hash]..[hash]`

## Acknowledgements

- MNIST Dataset
- Gradio framework by Hugging Face
- TensorFlow by Google

## License

Educational project for A-Level Computer Science NEA.

## Contact

**Author**: Harpreet Malhotra  
**Project**: MNIST Digit Recognition Web Application  
**Date**: February 2026
