# Dashboard/app.py

import os
import sys

# 1) Add your src/ folder to Python’s import path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR  = os.path.abspath(os.path.join(BASE_DIR, '..', 'src'))
HTML_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'Dashboard'))
sys.path.insert(0, SRC_DIR)

from inference import Inference
from flask import Flask, request, jsonify, send_from_directory

# 2) Load your model and scaler exactly once
MODELS_DIR   = os.path.abspath(os.path.join(BASE_DIR, '..', 'Models'))
model_path   = os.path.join(MODELS_DIR, 'xgboost_regressor_r2_0_917_v1.pkl')
scaler_path  = os.path.join(MODELS_DIR, 'sc.pkl')
infer        = Inference(model_path, scaler_path)

# 3) Configure Flask to serve static files from this directory
app = Flask(
    __name__,
    static_folder=HTML_DIR,  # so "/index.js" maps to BASE_DIR/Dashboard/index.js
    static_url_path='',  # so "/index.js" maps to BASE_DIR/Dashboard/index.js
)

@app.route('/')
def index():
    # Serve your dashboard’s main page
    return send_from_directory(HTML_DIR, 'index.html')

@app.route('/predict', methods=['POST'])
def predict_api():
    # 4) Parse incoming JSON
    data = request.get_json(force=True)

    # 5) Check that all required fields are present
    required = [
        'date', 'hour', 'temperature', 'humidity',
        'wind_speed', 'visibility', 'solar_radiation',
        'rainfall', 'snowfall', 'seasons', 'holiday', 'functioning_day'
    ]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({ 'error': f'Missing required fields: {missing}' }), 400

    try:
        # 6) Run your inference pipeline
        result = infer.predict(data)
        return jsonify({ 'prediction': result })
    except Exception as e:
        # 7) Return any preprocessing/prediction errors
        return jsonify({ 'error': str(e) }), 500

if __name__ == '__main__':
    # 8) Launch the server
    app.run(host='0.0.0.0', port=5000, debug=True)
