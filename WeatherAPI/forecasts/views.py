from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import load_data, find_closest_timestamp
import pandas as pd
from rest_framework.renderers import JSONRenderer  # Import JSONRenderer

# Load data once at the startup for efficiency
data = load_data()


class ForecastsView(APIView):
    renderer_classes = [JSONRenderer]  # Ensure only JSON responses
    """
    GET /forecasts/?now=<datetime>&then=<datetime>

    Parameters:
    - `now` (datetime): The reference time to determine the forecast availability.
    - `then` (datetime): The time for which the forecasted values are requested.

    Response:
    - Returns the most recent forecasts for temperature for "then" that were available at "now".
    """

    def get(self, request):
        try:
            now = pd.to_datetime(request.query_params.get("now"))
            then = pd.to_datetime(request.query_params.get("then"))

            closest_timestamp_to_then = find_closest_timestamp(data, then)

            # Filter data up to "now" and for the event_start at "then"
            relevant_data = data[(data["event_start"] == closest_timestamp_to_then) & (data["belief_horizon_in_sec"] > 0)]
            # Sort by belief horizon (most recent) and limit to three types
            sorted_data = relevant_data.sort_values(by="belief_horizon_in_sec", ascending=True).groupby("sensor").first().reset_index()

            response = sorted_data[["sensor", "event_value", "unit"]].to_dict(orient="records")
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class TomorrowView(APIView):
    renderer_classes = [JSONRenderer]  # Ensure only JSON responses
    """
    GET /tomorrow/?now=<datetime>

    Parameters:
    - `now` (datetime): The current time to evaluate tomorrow's weather conditions.

    Response:
    - Returns three booleans indicating if tomorrow is expected to be "warm", "sunny", and "windy".
    """

    def get(self, request):
        try:
            now = pd.to_datetime(request.query_params.get("now"))
            tomorrow_BOD = (now + pd.Timedelta(days=1)).replace(hour=0, minute=1, second=0, microsecond=0)
            tomorrow_EOD = (now + pd.Timedelta(days=1)).replace(hour=23, minute=59, second=0, microsecond=0)

            # Filter forecasts for tomorrow
            tomorrow_data = data[( tomorrow_BOD < data["event_start"]) & (data["event_start"] < tomorrow_EOD) & (data["belief_horizon_in_sec"] > 0)]

            # Define thresholds for warm, sunny, windy conditions
            warm_threshold, sunny_threshold, windy_threshold = 15, 200, 4

            # Calculate average values for each sensor
            # TODO: Remove the night time from the irradiance average
            avg_values = tomorrow_data.groupby("sensor")["event_value"].mean().to_dict()

            # Check conditions based on thresholds
            warm = avg_values.get("temperature", 0) >= warm_threshold
            sunny = avg_values.get("irradiance", 0) >= sunny_threshold
            windy = avg_values.get("wind speed", 0) >= windy_threshold

            return Response({"warm": warm, "sunny": sunny, "windy": windy}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
