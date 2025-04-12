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


## Model Approach and Methodology

### Data Preprocessing and Feature Engineering
1. **Time Series Data Handling**
   - Conversion of timestamps to datetime objects
   - Sorting data chronologically
   - Creation of numeric time features for model input

2. **Feature Engineering Pipeline**
   ```python
   def extract_time_features(df):
       df['hour'] = df['time'].dt.hour
       df['dayofyear'] = df['time'].dt.dayofyear
       df['month'] = df['time'].dt.month
       df['dayofweek'] = df['time'].dt.dayofweek
       # Cyclical encoding of temporal features
       df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
       df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
       df['doy_sin'] = np.sin(2 * np.pi * df['dayofyear'] / 365.25)
       df['doy_cos'] = np.cos(2 * np.pi * df['dayofyear'] / 365.25)
   ```

3. **Lag Feature Creation**
   ```python
   def create_lag_features(df, columns, max_lag):
       # Creates lagged versions of specified columns
       # Useful for capturing temporal dependencies
       lags = [df]
       for col in columns:
           for lag in range(1, max_lag + 1):
               lags.append(df[col].shift(lag).rename(f'{col}_lag{lag}'))
       return pd.concat(lags, axis=1)
   ```

4. **Historical Data Weighting**
   ```python
   def assign_weights(df, center_year=2025, decay=0.5):
       # Assigns exponentially decaying weights to historical data
       # More recent data gets higher weights in training
       df['year'] = df['time'].dt.year
       df['sample_weight'] = np.exp(-decay * (center_year - df['year']))
   ```

### Model Architecture and Training

1. **Regression Models (XGBoost)**
   - Separate models for each weather parameter
   - Features: Temporal encodings, lag features
   - Training with sample weights based on data recency
   - Hyperparameters optimized for each parameter

2. **Weather Classification (Random Forest)**
   - Predicts WMO weather codes
   - Uses both engineered features and regression predictions
   - Balanced class weights for handling imbalanced weather conditions

3. **Precipitation Model (XGBoost)**
   - Specialized configuration for precipitation patterns
   - Parameters:
     ```python
     XGBRegressor(
         n_estimators=100,
         max_depth=5,
         learning_rate=0.1,
         random_state=42
     )
     ```

## Model Evaluation and Metrics

### Performance Metrics
1. **Regression Models**
   - Mean Squared Error (MSE)
   - Mean Absolute Error (MAE)
   - R² Score

2. **Weather Classification**
   - Accuracy Score
   - Classification Report (Precision, Recall, F1-Score)
   - Confusion Matrix for detailed error analysis

### Model Validation Strategy
- Train-test split based on time (5-year holdout)
- Recent data prioritized through sample weights
- Out-of-sample validation for all predictions

## Steps to Replicate the Model

1. **Data Preparation**
   ```python
   # Load and preprocess data
   data = pd.read_csv('./dataset/delhi_weather.csv')
   df = data[['time', 'temperature_2m (°C)', 'relative_humidity_2m (%)',
              'wind_direction_10m (°)', 'cloud_cover (%)',
              'wind_speed_10m (km/h)', 'surface_pressure (hPa)',
              'precipitation (mm)', 'weather_code (wmo code)']].copy()
   ```

2. **Feature Engineering**
   ```python
   # Apply feature engineering pipeline
   df['time'] = pd.to_datetime(df['time'])
   df = extract_time_features(df)
   df = create_lag_features(df, regression_targets + ['precipitation (mm)'], max_lag=1)
   df = assign_weights(df, center_year=2025, decay=0.5)
   ```

3. **Model Training**
   ```python
   # Train regression models
   regressors = {}
   for target in regression_targets:
       reg = XGBRegressor()
       reg.fit(train_df[feature_cols], train_df[target],
               sample_weight=train_df['sample_weight'])
       regressors[target] = reg

   # Train weather classifier
   clf = RandomForestClassifier(random_state=42, class_weight='balanced')
   clf.fit(X_cls, y_cls)

   # Train precipitation model
   precip_reg = XGBRegressor(n_estimators=100, max_depth=5,
                            learning_rate=0.1, random_state=42)
   precip_reg.fit(train_df[feature_cols], train_df['precipitation (mm)'])
   ```

4. **Make Predictions**
   ```python
   def predict(date_time, df):
       # Ensure date_time is within valid range
       if date_time > latest_time + pd.Timedelta(hours=48):
           return None, df

       # Recursive prediction for previous hours if needed
       if date_time > latest_time:
           _, df = predict(date_time - pd.Timedelta(hours=1), df)

       # Generate features and predict
       new_df = create_prediction_features(date_time, df)
       for target in regression_targets:
           new_df[target] = regressors[target].predict(new_df[feature_cols])

       return new_df, df
   ```

## Model Explainability

### Feature Importance
- XGBoost models provide feature importance rankings
- Temporal features typically show high importance
- Lag features demonstrate strong predictive power
- Weather code classification heavily relies on current conditions

### Prediction Confidence
- Model uncertainty increases with prediction horizon
- 48-hour limit imposed based on error analysis
- Confidence metrics available for classification predictions

### Error Analysis
- Systematic evaluation of prediction errors
- Higher uncertainty in extreme weather conditions
- Temporal decay in prediction accuracy
- Regular model retraining recommended

## Resources
- Dataset: https://drive.google.com/drive/folders/1i-4guXUrj26NLF_JVkF5sZ9lWJT0DeSp
- Weather API: https://open-meteo.com/
