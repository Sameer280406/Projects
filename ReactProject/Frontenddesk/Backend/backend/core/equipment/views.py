import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Dataset
from .serializers import DatasetSerializer

@api_view(["POST"])
def upload_csv(request):
    file = request.FILES.get("file")
    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    df = pd.read_csv(file)

    summary = {
        "total": len(df),
        "avgFlow": round(df["Flowrate"].mean(), 2),
        "avgPressure": round(df["Pressure"].mean(), 2),
        "avgTemp": round(df["Temperature"].mean(), 2),
        "types": df["Type"].value_counts().to_dict(),
    }

    Dataset.objects.create(
        name=file.name,
        total_count=summary["total"],
        avg_flowrate=summary["avgFlow"],
        avg_pressure=summary["avgPressure"],
        avg_temperature=summary["avgTemp"],
        type_distribution=summary["types"],
    )

    # Keep only last 5 datasets
    if Dataset.objects.count() > 5:
        for old in Dataset.objects.all().order_by("-uploaded_at")[5:]:
            old.delete()

    return Response(summary, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def latest_summary(request):
    dataset = Dataset.objects.last()
    if not dataset:
        return Response({"error": "No data"}, status=404)

    serializer = DatasetSerializer(dataset)
    return Response(serializer.data)


@api_view(["GET"])
def history(request):
    datasets = Dataset.objects.all().order_by("-uploaded_at")[:5]
    serializer = DatasetSerializer(datasets, many=True)
    return Response(serializer.data)
