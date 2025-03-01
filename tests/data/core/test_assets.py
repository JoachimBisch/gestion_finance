import pytest
from datetime import date
from data.core.assets import Asset

@pytest.mark.django_db  # Enables database access
class TestAsset:
    @pytest.fixture
    def sample_asset(self):
        return Asset(name="Apple Stock", value=100, acquisition_date=date(2023, 1, 1))

    def test_it_creates_asset(self, sample_asset):
        assert sample_asset.name == "Apple Stock"
        assert sample_asset.value == 100

    def test_get_historical_data(self, sample_asset):
        new_asset = sample_asset.update_value(
            new_value=200,
            update_date=date(2024, 1, 1)
        )
        assert new_asset.history == [(date.fromisoformat("2023-01-01"), 100), (date.fromisoformat("2024-01-01"), 200)]
    
    def test_capital_gain_right_formula(self, sample_asset):
        return sample_asset.update_value(
            new_value=200,
            update_date= date(2024, 1, 1)
        ).capital_gain() == 100