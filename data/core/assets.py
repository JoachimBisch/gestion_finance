# mypy: ignore-errors

from django.db import models
from datetime import date
from typing import List, Tuple

class Asset(models.Model):
    name: str = models.CharField(max_length=255)
    value: float = models.FloatField()
    acquisition_date: date = models.DateField()
    history = models.JSONField(default=list) 

    def __str__(self):
        return f"{self.name} - {self.value}"

    def update_value(self, new_value: float, update_date: date):
        """Updates the asset value and stores the change in history."""
        if not isinstance(self.history, list):
            self.history = []  # Ensure history is always a list
        
        self.history = self.history + [(update_date.isoformat(), new_value)]
        self.value = new_value
        self.save()  # Save changes to the database
        return self.history

    def get_historical_data(self) -> List[Tuple[date, float]]:
        """Returns historical data as a list of tuples."""
        return [(date.fromisoformat(d), v) for d, v in self.history]

    def capital_gain(self) -> float:
        """Calculates capital gain percentage."""
        if len(self.history) < 2:
            return 0.0  # No gain if there is only one recorded value

        initial_value = float(self.history[0][1])
        final_value = float(self.history[-1][1])
        return ((final_value - initial_value) / initial_value) * 100