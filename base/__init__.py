import os

# Define the paths for the __init__.py files
paths = [
    "core/__init__.py",
    "core/cogs/__init__.py",
    "base/__init__.py"
]

# Create the __init__.py files if they don't exist
for path in paths:
    if not os.path.exists(path):
        with open(path, 'w') as f:
            pass