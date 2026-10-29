import numpy as np
import pandas as pd

def create_random_series(n=10, seed=42):
    """Returns a Series of n random integers between 1 and 99."""
    rng = np.random.default_rng(seed)      # seeded for repeatable results
    values = rng.integers(low=1, high=100, size=n)
    return pd.Series(values)


def create_labeled_series(series):
    """Plain English: attach custom, human-readable labels (an index)
    to an existing Series, instead of the default 0, 1, 2, ... numbering."""
    labels = [f"num_{i + 1}" for i in range(len(series))]
    return pd.Series(series.values, index=labels)

def describe_series(s, title="Series"):
    print(f"{title}:")
    print(s)
    print(f"\nDtype : {s.dtype}")
    print(f"Shape : {s.shape}")
    print(f"Size  : {s.size}")
    print(f"Index : {list(s.index)}")

if __name__ == "__main__":

    series = create_random_series()
    print("STEP 1: Series with the default index")
    describe_series(series)

    labeled = create_labeled_series(series)
    print("\nSTEP 2: Same values, custom labels")
    describe_series(labeled, title="Labeled Series")

    print("\nSTEP 3: Basic statistics")
    print(f"Minimum : {series.min()}")
    print(f"Maximum : {series.max()}")
    print(f"Mean    : {series.mean():.2f}")
    print(f"Sum     : {series.sum()}")

    print("\nSTEP 4: Sorted values (ascending)")
    print(series.sort_values().to_string())

    print("\nSTEP 5: Indexing and filtering")
    print(f"First value (series.iloc[0]) : {series.iloc[0]}")
    print("Values greater than 50:")
    print(series[series > 50].to_string())