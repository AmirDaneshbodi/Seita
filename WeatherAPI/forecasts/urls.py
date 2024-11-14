from django.urls import path
from .views import ForecastsView, TomorrowView

urlpatterns = [
    path("forecasts/", ForecastsView.as_view(), name="forecasts"),
    path("tomorrow/", TomorrowView.as_view(), name="tomorrow"),
]
