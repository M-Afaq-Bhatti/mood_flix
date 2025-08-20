import os

# Define the folder structure
folders = [
    "data",
    "database",
    "assets"
]

files = {
    "app.py": "# Main Streamlit application\n",
    "data_processor.py": "# Data loading and ChromaDB setup\n",
    "recommendation_engine.py": "# RAG pipeline and Gemini integration\n",
    "config.py": "# Configuration and constants\n",
    "requirements.txt": "# Python dependencies\n",
    ".env": "# Environment variables (API keys)\n",
    ".gitignore": "# Git ignore file\n",
    "README.md": "# Project documentation\n",
    os.path.join("data", "netflix_content.csv"): "",   # placeholder
    os.path.join("assets", "netflix_logo.webp"): "",    # placeholder
    # database folder will be created automatically
}

def create_structure():
    # Create folders if not exist
    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    # Create files if not exist
    for filepath, content in files.items():
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Created: {filepath}")
        else:
            print(f"Already exists: {filepath}")

if __name__ == "__main__":
    create_structure()
