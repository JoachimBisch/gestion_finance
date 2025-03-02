# mypy: ignore-errors

from django.urls import path
from .views import home, CreateAssetView, GetAssetsView, delete_asset

urlpatterns = [
    path('', home, name="home"),
    path('create-asset/', CreateAssetView.as_view(), name="create-asset"),
    path("get-assets/", GetAssetsView.as_view(), name="get-assets"),
    path("delete-asset/<int:asset_id>/", delete_asset, name="delete_asset"),

]