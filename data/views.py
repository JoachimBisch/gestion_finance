from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from datetime import date
from data.core.assets import Asset
from data.models import AssetSchema

def home(request):
    return render(request, "home.html")

class CreateAssetView(View):
    def get(self, request):
        """Temporary GET method to trigger asset creation for testing."""
        return self.post(request)  # Just call the POST method for now
    def post(self, request):
        try:
            # Define the asset data (this can be replaced with request data later)
            asset_data = {
                "name": "First fictionnal test asset just to check postgresql database connection !",
                "value": 1500.0,
                "acquisition_date": date(2022, 5, 15),
                "history": [(date(2022, 5, 15), 1500.0)],
            }

            # Validate data using Pydantic
            validated_asset = AssetSchema(**asset_data)

            # Create and save the asset in the database
            asset = Asset.objects.create(
                name=validated_asset.name,
                value=validated_asset.value,
                acquisition_date=validated_asset.acquisition_date,
                history=[(d.isoformat(), v) for d, v in validated_asset.history],  # Convert dates to strings
            )

            return JsonResponse({"message": "Asset created successfully", "asset_id": asset.id})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)