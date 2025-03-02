from django.urls import path
from .views import home, CreateAssetView

urlpatterns = [
    path('', home, name="home"),
    path("create-asset/", CreateAssetView.as_view(), name="create-asset"),
]