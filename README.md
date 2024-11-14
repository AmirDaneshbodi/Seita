Here’s a `README.md` for your Django weather API project:



# WeatherAPI

This Django application provides two API endpoints to access weather forecast data based on a CSV dataset containing temperature, wind speed, and irradiance forecasts up to 48 hours in advance. The endpoints can be used to retrieve forecasted values for a specific time or check for weather conditions expected for the following day.

## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
  - [GET /api/forecasts](#get-apiforecasts)
  - [GET /api/tomorrow](#get-apitomorrow)
- [Testing](#testing)
- [Project Structure](#project-structure)

## Requirements

- Python 3.8+
- Django 4.2+
- Django REST Framework
- pandas

## Installation

1. **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd WeatherAPI
    ```

2. **Set up a virtual environment** (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Add weather forecast data**:
   Place your `weather_data.csv` file in the root directory of the project. This file should have the following structure:
   ```plaintext
   event_start,belief_horizon_in_sec,event_value,sensor,unit
   2020-11-01 00:00:00+00,-637,11.36,temperature,°C
   ```

5. **Run migrations** (no database setup is needed for this example):
    ```bash
    python manage.py migrate
    ```

## Running the Server

Start the Django development server:
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`.

## API Endpoints

### GET /api/forecasts

- **Description**: Given two datetime parameters, `now` and `then`, this endpoint returns the three most recent forecasts for temperature, wind speed, and irradiance available at `now` for the requested `then` time.
- **Parameters**:
  - `now` (datetime, required): The reference time to determine the forecast availability.
  - `then` (datetime, required): The time for which the forecasted values are requested.
- **Example Request**:
  ```http
  GET /api/forecasts/?now=2024-11-01T12:00:00Z&then=2024-11-02T12:00:00Z
  ```
- **Example Response**:
  ```json
  [
      {"sensor": "temperature", "event_value": 12.3, "unit": "°C"},
      {"sensor": "wind_speed", "event_value": 5.1, "unit": "m/s"},
      {"sensor": "irradiance", "event_value": 200, "unit": "W/m²"}
  ]
  ```

### GET /api/tomorrow

- **Description**: Given a datetime parameter `now`, this endpoint returns three booleans indicating if tomorrow is expected to be "warm", "sunny", and "windy" based on threshold values.
- **Parameters**:
  - `now` (datetime, required): The current time to evaluate tomorrow's weather conditions.
- **Example Request**:
  ```http
  GET /api/tomorrow/?now=2024-11-01T12:00:00Z
  ```
- **Example Response**:
  ```json
  {
      "warm": true,
      "sunny": false,
      "windy": true
  }
  ```
  - **Thresholds**:
    - `warm` - Temperature >= 15°C
    - `sunny` - Irradiance >= 200 W/m²
    - `windy` - Wind Speed >= 4 m/s

## Testing

Unit tests are provided in the `forecasts/tests.py` file.

To run the tests:
```bash
python manage.py test
```

## Project Structure

```
WeatherAPI/
├── forecasts/
│   ├── migrations/
│   ├── __init__.py
│   ├── views.py        # API endpoint logic
│   ├── urls.py         # App URL routing
│   ├── tests.py        # Unit tests
│   ├── utils.py        # Utility functions for data loading
│   └── weather_data.csv # Forecast data (CSV file)
├── WeatherAPI/
│   ├── __init__.py
│   ├── settings.py     # Django settings
│   ├── urls.py         # Project URL routing
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

## Notes

- Ensure `weather_data.csv` is in the root directory.
- Use the provided thresholds in `/api/tomorrow` to determine "warm", "sunny", and "windy" conditions.
- **Tip**: Use tools like `curl` or Postman to test API responses.
```

This `README.md` provides clear instructions on how to install, run, and test the Django weather API application, along with usage examples for each endpoint. Let me know if there’s anything else you’d like to add or adjust!