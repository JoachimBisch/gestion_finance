# mypy: ignore-errors

from django.db import models
from data.core.assets import Asset
from datetime import date

# class Asset(models.Model):
#     name: str = models.CharField(max_length=255)
#     value: float = models.FloatField()
#     acquisition_date: date = models.DateField()

#     def __str__(self):
#         return f"{self.name} - {self.value} - {self.acquisition_date}"