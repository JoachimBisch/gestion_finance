# mypy: ignore-errors

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from datetime import date
from data.core.assets import Asset
from django.middleware.csrf import get_token
from data.models import AssetSchema
import json

def home(request):
    return render(request, "home.html")

class CreateAssetView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)  # Read JSON from request

            # Validate input data using Pydantic schema
            validated_asset = AssetSchema(**data)

            # Create and save the asset in the database
            asset = Asset.objects.create(
                name=validated_asset.name,
                value=validated_asset.value,
                acquisition_date=validated_asset.acquisition_date,
                history=[(d.isoformat(), v) for d, v in validated_asset.history],  # Convert dates to strings
            )

            return JsonResponse({"message": f"Asset {asset.name}", "asset_id": asset.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    def get(self, request):
        return JsonResponse({"csrfToken": get_token(request)})