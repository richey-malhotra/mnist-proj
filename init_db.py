"""
Database initialisation for training history.
Creates SQLite database with three tables.
"""

import sqlite3
import os

def create_database():
    """Set up the SQLite database and tables."""
    # Make sure artifacts folder exists
    os.makedirs('artifacts', exist_ok=True)
    
    # Connect to database (creates file if doesn't exist)
    conn = sqlite3.connect('artifacts/training_history.db')
    cursor = conn.cursor()
    
    # Models table - stores different architectures
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS models (
            model_id INTEGER PRIMARY KEY AUTOINCREMENT,
            architecture TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Training runs table - stores each training session
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS training_runs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_id INTEGER,
            epochs INTEGER,
            batch_size INTEGER,
            val_accuracy REAL,
            model_filename TEXT,
            duration REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (model_id) REFERENCES models(model_id)
        )
    ''')
    
    # Add duration column if it doesn't exist (for Phase 15 upgrade)
    try:
        cursor.execute('ALTER TABLE training_runs ADD COLUMN duration REAL')
        print("✓ Added duration column to training_runs table")
    except sqlite3.OperationalError:
        # Column already exists
        pass
    
    # Metrics table - stores epoch-by-epoch training data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS metrics (
            metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
            run_id INTEGER,
            epoch INTEGER,
            train_accuracy REAL,
            val_accuracy REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (run_id) REFERENCES training_runs(run_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✓ Database created successfully!")
    print("  Tables: models, training_runs, metrics")
    print("  Location: artifacts/training_history.db")

if __name__ == "__main__":
    create_database()
