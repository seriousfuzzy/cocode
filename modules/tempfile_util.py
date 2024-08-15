# tempfile_util.py

import os
import tempfile

def clean_temp_files():
    # Clean up any temporary files created during processing
    temp_files = [f for f in os.listdir(tempfile.gettempdir()) if f.endswith(".pdf")]
    for file in temp_files:
        os.remove(os.path.join(tempfile.gettempdir(), file))
