# 📈 Stock Prediction Agent

This project is a production-ready **stock prediction agent** that uses a Long Short-Term Memory (LSTM) deep learning model to forecast stock prices. The agent is containerized using Docker, making it easy to deploy and scale in various cloud environments.

## 🚀 Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing.

### Prerequisites

You'll need the following installed on your machine:

* **Docker:** To build and run the application in a container.
* **Git:** To clone this repository.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)<your-username>/stock-prediction-agent.git
    cd stock-prediction-agent
    ```

2.  **Build the Docker image:**
    This command builds the Docker image and tags it as `stock-prediction-agent`.
    ```bash
    docker build -t stock-prediction-agent .
    ```

3.  **Run the container locally:**
    This command runs the container and maps port `5000` on your machine to port `5000` inside the container.
    ```bash
    docker run -p 5000:5000 stock-prediction-agent
    ```

The Flask API will now be running at `http://localhost:5000`. You can send prediction requests to this endpoint.

---

## 📂 Project Structure

The repository is organized for clarity and maintainability.

'''
stock_prediction_agent/
├── model/
│   ├── stock_prediction_lstm_model.h5   # The trained Keras LSTM model
│   └── stock_scaler.pkl                # The scaler used to preprocess data
├── app.py                              # Flask API for serving predictions
├── requirements.txt                    # Python dependencies
└── Dockerfile                          # Instructions to build the Docker image
'''



### Key Technologies

* **TensorFlow:** For building and running the LSTM model.
* **scikit-learn:** For data preprocessing and scaling.
* **Flask & Gunicorn:** A lightweight web server framework and a robust production-ready WSGI server for the API.
* **Pandas & NumPy:** Essential libraries for data manipulation and numerical operations.
* **yfinance:** To fetch real-time stock data.
* **Docker:** To containerize the application for consistent environments.

---

## ☁️ Cloud Deployment

This agent is designed for easy deployment to cloud platforms like AWS, GCP, or Azure. The following are conceptual steps for deploying on **AWS**.

### 1. Push to AWS ECR

First, you need to create a repository in **Amazon Elastic Container Registry (ECR)** and push your Docker image.

```bash
# 1. Create a repository
aws ecr create-repository --repository-name stock-prediction-agent

# 2. Tag your local image
docker tag stock-prediction-agent:latest <aws_account_id>.dkr.ecr.<your-region>[.amazonaws.com/stock-prediction-agent:latest](https://.amazonaws.com/stock-prediction-agent:latest)

# 3. Push the image to ECR
docker push <aws_account_id>.dkr.ecr.<your-region>[.amazonaws.com/stock-prediction-agent:latest](https://.amazonaws.com/stock-prediction-agent:latest)


