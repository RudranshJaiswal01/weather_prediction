# Weather Prediction Service

A comprehensive weather service that combines real-time data collection with machine learning-based weather prediction. The service features a FastAPI-based backend for data collection and REST APIs, along with an advanced prediction system using XGBoost and Random Forest models.

## Features

### Data Collection and API Service
- Automatic hourly weather data collection from Open-Meteo API
- CSV-based data storage with standardized format
- RESTful API endpoints for weather data access
- Configurable data fetch frequency
- Background service for continuous data collection

### Weather Prediction System
- Machine learning models for weather parameter prediction
- Time series forecasting up to 48 hours ahead
- Prediction capabilities for:
  - Temperature
  - Relative humidity
  - Wind direction and speed
  - Cloud cover
  - Surface pressure
  - Precipitation
  - Weather conditions (using WMO weather codes)
- Feature engineering including:
  - Temporal features (hour, day, month)
  - Cyclical encoding of time features
  - Lag features for improved accuracy
  - Historical data weighting system

## Project Structure

```
weather_prediction/
├── main.py                 # FastAPI server and API endpoints
├── weather_predictor.ipynb # Weather prediction model implementation
├── utils/
│   ├── weather_fetcher.py # Weather data collection from Open-Meteo API
│   └── csv_handler.py     # CSV data handling and formatting
├── dataset/               # Storage for collected weather data
└── predictions/          # Storage for model predictions
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Required packages listed in requirements.txt, including:
  - FastAPI and Uvicorn for API service
  - XGBoost and Scikit-learn for prediction models
  - Pandas and NumPy for data handling
  - Matplotlib for visualization

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd weather_prediction
   ```

2. Create a virtual environment:
   ```bash
   python -m venv <env_name>
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     .\<env_name>\Scripts\activate
     ```
   - On Unix or MacOS:
     ```bash
     source <env_name>/bin/activate
     ```

4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Services

### API Service
Start the FastAPI server with:
```bash
python main.py
```
The server will run at `http://127.0.0.1:8000`. The background service will automatically start collecting weather data at the beginning of each hour.

### Weather Prediction
The prediction system is implemented in `weather_predictor.ipynb`. It includes:
- Data preprocessing and feature engineering
- Model training and evaluation
- Prediction generation for future weather conditions

## API Endpoints

### 1. Get Current Weather
- **Endpoint**: `/weather`
- **Method**: GET
- **Description**: Returns the current weather data
- **Response**: JSON object with current weather information

### 2. Get Hourly Weather Data
- **Endpoint**: `/weather/hourly`
- **Method**: GET
- **Description**: Returns hourly weather data
- **Response**: JSON array of hourly weather records

### 3. Get Historic Weather Data
- **Endpoint**: `/weather/historic`
- **Method**: GET
- **Description**: Returns historical weather data
- **Response**: JSON array of historical weather records

### 4. Update Fetch Frequency
- **Endpoint**: `/update-frequency`
- **Method**: POST
- **Parameters**:
  - `seconds`: Integer (Query parameter, must be greater than 0)
- **Description**: Updates the frequency of weather data collection
- **Response**: Confirmation message with updated frequency

## Data Collection and Storage

### Weather Data Format
The system collects and stores the following parameters:
- Temperature at 2m above ground (°C)
- Relative humidity at 2m (%)
- Precipitation and rain (mm)
- Weather code (WMO code)
- Cloud cover (%)
- Surface pressure (hPa)
- Wind speed at 10m (km/h)
- Wind direction at 10m (°)
- Day/night indicator

### Storage Structure
- Weather data is stored in CSV format in the `dataset` directory
- Predictions are stored in the `predictions` directory
- Consistent column structure with appropriate units

## Prediction Model Details

### Feature Engineering
- Temporal feature extraction (hour, day of year, month, day of week)
- Cyclical encoding of time features (sin/cos transformation)
- Lag feature creation for time series analysis
- Historical data weighting based on recency

### Models
1. **Regression Models (XGBoost)**
   - Separate models for each weather parameter
   - Trained on historical data with time-based weighting
   - Performance metrics include MSE, MAE, and R²

2. **Weather Classification (Random Forest)**
   - Predicts weather conditions using WMO codes
   - Balanced class weights for improved accuracy
   - Evaluated using classification metrics

3. **Precipitation Model (XGBoost)**
   - Specialized model for precipitation prediction
   - Handles the unique characteristics of rainfall data

## Development

The project uses:
- FastAPI with Uvicorn as the ASGI server
- XGBoost and Scikit-learn for machine learning
- Pandas for data manipulation
- Open-Meteo API for weather data

## Logging

Comprehensive logging system that tracks:
- Service startup and operations
- Data collection timing and status
- Model training and prediction events
- API endpoint access
- Error handling and debugging information

Logs use the format: `%(asctime)s - %(levelname)s - %(message)s`

## File Handling

### .gitignore Configuration
The repository excludes:
- Python bytecode and cache files
- Virtual environment directories
- IDE configuration files
- Dataset and prediction CSV files
- Local development configurations
- System-specific files
