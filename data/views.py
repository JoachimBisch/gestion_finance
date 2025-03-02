# mypy: ignore-errors

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from datetime import date
from data.core.assets import Asset
from django.middleware.csrf import get_token
from data.models import AssetSchema
from django.views.decorators.csrf import csrf_exempt

import json

def home(request):
    return render(request, "home.html")

@csrf_exempt
def delete_asset(request, asset_id):
    if request.method == "DELETE":
        try:
            asset = Asset.objects.get(id=asset_id)
            asset.delete()
            return JsonResponse({"success": True})
        except Asset.DoesNotExist:
            return JsonResponse({"error": "Asset not found"}, status=404)
    
    return JsonResponse({"error": "Invalid request"}, status=400)

class GetAssetsView(View):
    def get(self, request):
        assets = Asset.objects.all().values("id", "name", "value", "acquisition_date")  # Fetch assets
        return JsonResponse({"assets": list(assets)})  # Convert to JSON

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