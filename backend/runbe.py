import os
import subprocess
import sys

def main():
    # Define paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Since script is inside backend folder, base_dir IS the backend_dir
    backend_dir = base_dir
    venv_python = os.path.join(backend_dir, '.venv', 'bin', 'python')
    
    # Check if venv exists
    if not os.path.exists(venv_python):
        print(f"Error: Virtual environment not found at {venv_python}")
        return

    # Change to backend directory so imports and .env loading work correctly
    os.chdir(backend_dir)
    
    # Run uvicorn using the venv python
    print(f"Starting Arima Backend from {backend_dir}...")
    try:
        subprocess.run([venv_python, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
    except KeyboardInterrupt:
        print("\nBackend stopped.")

if __name__ == "__main__":
    main()
