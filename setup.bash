#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Cloning the Smart-Irrigation-Water-Predictor repository..."
git clone https://github.com/youssefmmagdy/Smart-Irrigation-Water-Predictor.git
cd Smart-Irrigation-Water-Predictor

echo "Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing backend dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo "Setup complete. To start the application:"
echo "1. Activate the virtual environment: source .venv/bin/activate"
echo "2. Start the backend server: uvicorn backend.app:app --reload"
echo "3. Start the frontend server: cd frontend && npm start"
