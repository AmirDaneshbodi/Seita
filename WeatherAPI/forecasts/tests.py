from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
import pandas as pd

class ForecastsTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.now = "2020-11-01T00:00:00Z"
        self.then = "2020-11-02T00:00:00Z"

        # Define some dummy data as it would appear in the CSV file
        self.dummy_data = pd.read_csv("/Users/adaneshbodi/Library/CloudStorage/OneDrive-Deloitte(O365D)/python_projects/Seita/WeatherAPI/forecasts/dummy_data.csv", parse_dates=["event_start"])

    @patch("forecasts.utils.load_data")
    def test_get_forecasts(self, mock_load_data):
        """
        Test the /api/forecasts endpoint.
        """
        mock_load_data.return_value = self.dummy_data
        response = self.client.get(
            reverse("forecasts"),
            {"now": self.now, "then": self.then},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Define the expected response structure
        expected_response = [
            {
                "sensor": "irradiance",
                "event_value": 0.0,
                "unit": "W/m²"
            },
            {
                "sensor": "temperature",
                "event_value": 16.77,
                "unit": "°C"
            },
            {
                "sensor": "wind speed",
                "event_value": 9.13,
                "unit": "m/s"
            }
        ]

        # Assert that the response JSON matches the expected response
        self.assertEqual(response.json(), expected_response)