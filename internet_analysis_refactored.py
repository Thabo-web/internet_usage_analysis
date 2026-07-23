"""
Internet Usage Analysis - Refactored with Idiomatic Python & Pandas

This module demonstrates best practices in pandas and Python:
  1. Method chaining for readable data pipelines
  2. Type hints for clarity and IDE support
  3. Configuration separation from logic
  4. Error handling and validation
  5. Modular, testable functions
"""

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# ============================================================================
# CONFIGURATION - Single Source of Truth
# ============================================================================
INPUT_FILE = Path("/workspaces/internet_usage_analysis/INT_BAND_PER_USR.csv")
OUTPUT_FILE = Path("/workspaces/internet_usage_analysis/CLEAN_INT_BAND_PER_USR.csv")
CHART_FILE = Path("internet_usage_south_africa.png")

# Column name mapping: original -> cleaned
COLUMNS_TO_KEEP = {
    "REF_AREA_LABEL": "Country",
    "TIME_PERIOD": "Year",
    "OBS_VALUE": "InternetUsage",
    "INDICATOR_LABEL": "Indicator",
}


# ============================================================================
# DATA LOADING & CLEANING FUNCTIONS
# ============================================================================

def load_and_clean_data(file_path: Path) -> pd.DataFrame:
    """
    Load, inspect, and clean internet usage data.
    
    This function demonstrates idiomatic pandas patterns:
      - Method chaining for clarity and efficiency
      - Assignment of operation results (dropna, drop_duplicates)
      - Type conversion in a single pass
      - Comprehensive data inspection before cleaning
    
    Args:
        file_path: Path to the input CSV file
        
    Returns:
        Cleaned DataFrame with columns: Country, Year, InternetUsage, Indicator
        
    Raises:
        FileNotFoundError: If input file does not exist
        ValueError: If required columns are missing
    """
    # Load raw data
    df = pd.read_csv(file_path)
    
    # Inspection Phase: Understand the data before cleaning
    print("=" * 70)
    print("DATASET OVERVIEW")
    print("=" * 70)
    print(f"\nFirst 10 rows:\n{df.head(10)}")
    print(f"\nDataset Info:\n{df.info()}")
    print(f"\nMissing Values by Column:\n{df.isnull().sum()}")
    print(f"\nTotal Duplicate Rows: {df.duplicated().sum()}")
    print(f"Dataset Shape (before cleaning): {df.shape}")
    
    # Validate required columns exist
    missing_cols = set(COLUMNS_TO_KEEP.keys()) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Cleaning Phase: Idiomatic method chaining
    # Key insight: Each operation is assigned, preventing silent data loss
    df_clean = (
        df[COLUMNS_TO_KEEP.keys()]  # Select only needed columns
        .rename(columns=COLUMNS_TO_KEEP)  # Rename for clarity
        .astype({"Year": "int"})  # Convert Year to integer (efficient)
        .assign(InternetUsage=lambda x: pd.to_numeric(x["InternetUsage"], errors="coerce"))
        # ^ Better than: df["InternetUsage"] = pd.to_numeric(...) (avoids SettingWithCopyWarning)
        .dropna()  # Remove rows with missing values (result IS assigned)
        .drop_duplicates()  # Remove duplicate rows (result IS assigned)
        .reset_index(drop=True)  # Reset index for clean sequential numbering
    )
    
    # Summary statistics after cleaning
    print(f"\n{'=' * 70}")
    print("CLEANED DATA SUMMARY")
    print("=" * 70)
    print(f"\nData Types:\n{df_clean.dtypes}")
    print(f"\nInternetUsage Statistics:\n{df_clean['InternetUsage'].describe()}")
    print(f"\nDataset Shape (after cleaning): {df_clean.shape}")
    print(f"Rows removed: {len(df) - len(df_clean)}")
    
    return df_clean


def save_clean_data(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save cleaned data to CSV file.
    
    Args:
        df: DataFrame to save
        output_path: Path where CSV will be saved
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)  # Create directory if needed
    df.to_csv(output_path, index=False)  # index=False: don't save index as column
    print(f"✓ Cleaned data saved to: {output_path}")


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================

def analyze_by_country(df: pd.DataFrame) -> pd.Series:
    """
    Calculate and display average internet usage by country.
    
    Demonstrates:
      - groupby + aggregation (idiomatic pandas pattern)
      - Method chaining with sort_values
      - Returning results for testing/reuse
    
    Args:
        df: Cleaned DataFrame
        
    Returns:
        Series with countries as index, average usage as values
    """
    avg_usage = (
        df.groupby("Country")["InternetUsage"]
        .mean()
        .sort_values(ascending=False)
    )
    print(f"\n{'=' * 70}")
    print("AVERAGE INTERNET USAGE BY COUNTRY")
    print("=" * 70)
    print(avg_usage)
    
    return avg_usage


# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def plot_country_trend(df: pd.DataFrame, country: str, output_path: Path) -> None:
    """
    Plot internet usage trend for a specific country.
    
    Demonstrates:
      - .query() for readable, safe filtering (variables with @)
      - Modern matplotlib with fig, ax pattern
      - Proper error handling (empty data check)
      - Professional figure formatting
    
    Args:
        df: Cleaned DataFrame
        country: Country name to plot
        output_path: Path to save chart
    """
    # Filter data using .query() - more readable than df[df["Country"] == country]
    country_data = (
        df.query(f"Country == @country")
        .sort_values("Year")
    )
    
    # Validation: Check if data exists for country
    if country_data.empty:
        print(f"⚠ Warning: No data found for '{country}'")
        return
    
    # Create figure with modern matplotlib pattern
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot with professional styling
    ax.plot(
        country_data["Year"],
        country_data["InternetUsage"],
        marker="o",
        linewidth=2.5,
        markersize=7,
        color="steelblue",
        label="Internet Usage",
    )
    
    # Labels and title
    ax.set_title(
        f"Internet Usage Trend in {country}",
        fontsize=16,
        fontweight="bold",
        pad=20,
    )
    ax.set_xlabel("Year", fontsize=12, fontweight="bold")
    ax.set_ylabel("Internet Usage (%)", fontsize=12, fontweight="bold")
    
    # Grid for readability
    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(loc="best")
    
    # Tight layout for professional appearance
    fig.tight_layout()
    
    # Save with high DPI for quality
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"✓ Chart saved to: {output_path}")
    
    plt.show()


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    """
    Main execution block with error handling.
    
    Best practices demonstrated:
      - try/except for graceful error handling
      - Descriptive error messages
      - __main__ guard allows module import without executing
    """
    try:
        print("\n" + "=" * 70)
        print("INTERNET USAGE ANALYSIS - EXECUTION START")
        print("=" * 70 + "\n")
        
        # Step 1: Load and clean data
        df = load_and_clean_data(INPUT_FILE)
        
        # Step 2: Save cleaned data
        save_clean_data(df, OUTPUT_FILE)
        
        # Step 3: Analysis
        analyze_by_country(df)
        
        # Step 4: Visualization
        plot_country_trend(df, "South Africa", CHART_FILE)
        
        print("\n" + "=" * 70)
        print("✓ SUCCESS: All operations completed successfully!")
        print("=" * 70 + "\n")
        
    except FileNotFoundError as e:
        print(f"\n✗ ERROR: Input file not found")
        print(f"   Expected: {INPUT_FILE}")
        print(f"   Details: {e}\n")
        
    except ValueError as e:
        print(f"\n✗ ERROR: Data validation failed")
        print(f"   Details: {e}\n")
        
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {type(e).__name__}")
        print(f"   Details: {e}\n")
