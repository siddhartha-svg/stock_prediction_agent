from flask import Flask, request, jsonify
import tensorflow as tf
import joblib
import numpy as np
import pandas as pd
import yfinance as yf
import datetime
import os

app = Flask(__name__)

# Define paths for model and scaler (relative to where the app.py will run in Docker)
MODEL_PATH = 'model/stock_prediction_lstm_model.h5'
SCALER_PATH = 'model/stock_scaler.pkl'
LOOK_BACK = 60 # This must match the look_back used during training

# Global variables to store the loaded model and scaler
model = None
scaler = None

def load_artifacts():
    """Load the pre-trained model and scaler into memory."""
    global model, scaler
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        print("Model and Scaler loaded successfully.")
    except Exception as e:
        print(f"Error loading model or scaler: {e}")
        # In a real production scenario, you might want to exit or log a critical error
        raise RuntimeError("Failed to load ML artifacts, cannot start service.")

# Load artifacts when the Flask app starts
with app.app_context():
    load_artifacts()

@app.route('/predict', methods=['POST'])
def predict_stock():
    if model is None or scaler is None:
        return jsonify({'error': 'Model or scaler not loaded. Service not ready.'}), 503

    data = request.get_json()
    ticker = data.get('ticker')

    if not ticker:
        return jsonify({'error': 'Please provide a stock ticker in the request body.'}), 400

    try:
        # Fetch the most recent stock data required for prediction
        # We need (LOOK_BACK) days to make a prediction
        end_date = datetime.date.today()
        # Fetch a few extra days just in case of missing data for robust tail
        start_date = end_date - datetime.timedelta(days=LOOK_BACK + 10)
        
        stock_data = yf.download(ticker, start=start_date, end=end_date)

        if stock_data.empty or len(stock_data) < LOOK_BACK:
            return jsonify({'error': f'Insufficient historical data for {ticker}. Need at least {LOOK_BACK} days of closing prices.'}), 404

        # Get the last 'LOOK_BACK' closing prices
        last_n_days_close = stock_data['Close'].tail(LOOK_BACK).values.reshape(-1, 1)

        # Scale the data using the *trained* scaler
        scaled_input = scaler.transform(last_n_days_close)

        # Reshape for LSTM input (samples, time_steps, features)
        X_input = np.array([scaled_input])
        X_input = np.reshape(X_input, (X_input.shape[0], X_input.shape[1], 1))

        # Make prediction
        predicted_scaled_price = model.predict(X_input)

        # Inverse transform to get the actual price
        predicted_price = scaler.inverse_transform(predicted_scaled_price)[0][0]

        return jsonify({
            'ticker': ticker,
            'predicted_next_day_close': round(float(predicted_price), 2),
            'last_known_close': round(float(stock_data['Close'].iloc[-1]), 2),
            'prediction_date': (end_date + datetime.timedelta(days=1)).strftime('%Y-%m-%d') # The date the prediction is *for*
        })

    except Exception as e:
        print(f"An error occurred during prediction for {ticker}: {e}")
        return jsonify({'error': f'An internal server error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    # When running locally for testing, use debug=True
    # For production, use a WSGI server like Gunicorn (covered in next step)
    app.run(debug=True, host='0.0.0.0', port=5000)
