"""
Tests for the data loader module.

These tests verify that:
1. The CSV file loads successfully into a DataFrame
2. The DataFrame has the correct number of rows and columns
3. All expected columns are present
4. No columns contain missing values (NaN)
5. Numeric columns are within realistic ranges
6. The loader raises clear errors when given bad input
"""

import pytest
import pandas as pd
from pathlib import Path

from src.data_loader import load_data, validate_dataframe, EXPECTED_COLUMNS


class TestLoadData:
    """Tests for the load_data() function."""

    def test_loads_successfully(self) -> None:
        """The CSV loads without any errors."""
        df = load_data()
        assert isinstance(df, pd.DataFrame)

    def test_correct_row_count(self) -> None:
        """The dataset contains exactly 500 rows."""
        df = load_data()
        assert len(df) == 500

    def test_correct_column_count(self) -> None:
        """The dataset contains exactly 9 columns."""
        df = load_data()
        assert len(df.columns) == 9

    def test_all_expected_columns_present(self) -> None:
        """Every column defined in EXPECTED_COLUMNS exists in the DataFrame."""
        df = load_data()
        for col in EXPECTED_COLUMNS:
            assert col in df.columns, f"Missing column: {col}"

    def test_no_missing_values(self) -> None:
        """No column contains NaN (missing) values."""
        df = load_data()
        for col in EXPECTED_COLUMNS:
            assert df[col].isnull().sum() == 0, (
                f"Column '{col}' has {df[col].isnull().sum()} missing values"
            )

    def test_file_not_found_raises_error(self) -> None:
        """Loading a nonexistent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_data(filepath=Path("data/nonexistent.csv"))


class TestDataRanges:
    """Tests that numeric values are within realistic ranges."""

    def setup_method(self) -> None:
        """Load the DataFrame once before each test in this class."""
        self.df = load_data()

    def test_biodegradability_range(self) -> None:
        """Biodegradability scores are between 0 and 100."""
        assert self.df["Biodegradability_Score"].min() >= 0
        assert self.df["Biodegradability_Score"].max() <= 100

    def test_cleaning_efficacy_range(self) -> None:
        """Cleaning efficacy scores are between 0 and 100."""
        assert self.df["Cleaning_Efficacy_Score"].min() >= 0
        assert self.df["Cleaning_Efficacy_Score"].max() <= 100

    def test_toxicity_range(self) -> None:
        """Toxicity levels are non-negative."""
        assert self.df["Toxicity_Level"].min() >= 0

    def test_cost_is_positive(self) -> None:
        """Cost per litre is always positive."""
        assert self.df["Cost_Per_Litre_GBP"].min() > 0

    def test_concentration_range(self) -> None:
        """Concentration percentage is between 0 and 100."""
        assert self.df["Concentration_Pct"].min() >= 0
        assert self.df["Concentration_Pct"].max() <= 100


class TestValidateDataframe:
    """Tests for the validate_dataframe() function."""

    def test_empty_dataframe_raises_error(self) -> None:
        """An empty DataFrame raises ValueError."""
        empty_df = pd.DataFrame()
        with pytest.raises(ValueError, match="empty"):
            validate_dataframe(empty_df)

    def test_missing_column_raises_error(self) -> None:
        """A DataFrame missing a required column raises ValueError."""
        incomplete_df = pd.DataFrame({
            "Formula_ID": ["ECO-F-0001"],
            "Surfactant_Type": ["Test"],
            # Missing all other required columns
        })
        with pytest.raises(ValueError, match="Missing columns"):
            validate_dataframe(incomplete_df)
