from django.urls import path
from .views import upload_csv, latest_summary, history

urlpatterns = [
    path("upload/", upload_csv),
    path("summary/latest/", latest_summary),
    path("summary/history/", history),
]
