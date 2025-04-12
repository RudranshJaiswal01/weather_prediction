# Weather Prediction Service

A FastAPI-based weather service that collects, stores, and serves weather data through REST APIs. The service automatically fetches weather data hourly and provides endpoints to access current, hourly, and historic weather information.

## Features

- Automatic hourly weather data collection
- CSV-based data storage
- RESTful API endpoints for weather data access
- Configurable data fetch frequency
- Background service for continuous data collection

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

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

## Running the Server

Start the server with:
```bash
python main.py
```

The server will run at `http://127.0.0.1:8000`. The background service will automatically start collecting weather data at the beginning of each hour.

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

## API Usage Examples

1. Get current weather:
```bash
curl http://localhost:8000/weather
```

2. Get hourly weather data:
```bash
curl http://localhost:8000/weather/hourly
```

3. Get historic weather data:
```bash
curl http://localhost:8000/weather/historic
```

4. Update fetch frequency to 30 minutes:
```bash
curl -X POST "http://localhost:8000/update-frequency?seconds=1800"
```

## Data Storage

Weather data is stored in CSV files in the `dataset` directory. The service automatically appends new weather data to these files as it's collected.

## Logging

The service includes comprehensive logging that provides information about:
- Service startup
- Data collection timing
- Successful/failed data updates
- API endpoint access

Logs use the format: `%(asctime)s - %(levelname)s - %(message)s`

## Development

The project uses FastAPI with Uvicorn as the ASGI server. Key components include:
- `main.py`: Server and API endpoints
- `weather_fetcher.py`: Weather data collection logic
- `utils/csv_handler.py`: CSV file operations

