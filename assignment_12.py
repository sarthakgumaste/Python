import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          
import matplotlib.pyplot as plt


def generate_synthetic_churn_data(n=1000, seed=42):
    """Returns a deliberately messy DataFrame shaped like a typical
    telecom customer-churn dataset."""
    rng = np.random.default_rng(seed)

    genders = rng.choice(["Male", "Female"], size=n)
    senior = rng.choice([0, 1], size=n, p=[0.84, 0.16])
    partner = rng.choice(["Yes", "No"], size=n)
    dependents = rng.choice(["Yes", "No"], size=n, p=[0.3, 0.7])
    tenure = rng.integers(0, 73, size=n).astype(float)          
    contract = rng.choice(
        ["Month-to-month", "One year", "Two year"], size=n, p=[0.55, 0.24, 0.21]
    )
    internet = rng.choice(["DSL", "Fiber optic", "No"], size=n, p=[0.35, 0.45, 0.2])
    paperless = rng.choice(["Yes", "No"], size=n, p=[0.6, 0.4])
    payment = rng.choice(
        ["Electronic check", "Mailed check", "Bank transfer", "Credit card"], size=n
    )
    monthly_charges = np.round(rng.normal(65, 30, size=n).clip(18, 120), 2)
    total_charges = np.round(monthly_charges * tenure + rng.normal(0, 50, size=n), 2)
    total_charges = np.clip(total_charges, 0, None)

    churn_score = (
        (contract == "Month-to-month") * 0.35
        + (tenure < 12) * 0.30
        + (internet == "Fiber optic") * 0.15
        + (monthly_charges > 80) * 0.15
        + rng.normal(0, 0.15, size=n)
    )
    churn = np.where(churn_score > 0.45, "Yes", "No")

    df = pd.DataFrame({
        "customerID": [f"CUST-{10000+i}" for i in range(n)],
        "gender": genders,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "InternetService": internet,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges,
        "Churn": churn,
    })

    for col, frac in [("TotalCharges", 0.03), ("tenure", 0.02), ("InternetService", 0.01)]:
        missing_idx = rng.choice(df.index, size=int(n * frac), replace=False)
        df.loc[missing_idx, col] = np.nan

    messy_idx = rng.choice(df.index, size=int(n * 0.08), replace=False)
    df.loc[messy_idx, "Partner"] = df.loc[messy_idx, "Partner"].str.lower()

    blank_idx = rng.choice(df.index, size=int(n * 0.01), replace=False)
    df["TotalCharges"] = df["TotalCharges"].astype(object)
    df.loc[blank_idx, "TotalCharges"] = " "

    dup_rows = df.sample(n=15, random_state=seed)
    df = pd.concat([df, dup_rows], ignore_index=True)

    return df

def explore_raw_data(df):
    print("=" * 60)
    print("STEP 1: INITIAL EXPLORATION")
    print("=" * 60)
    print(f"Shape (rows, columns): {df.shape}")
    print(f"\nColumn data types:\n{df.dtypes}")
    print(f"\nMissing values per column:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    print(f"\nDuplicate rows: {df.duplicated().sum()}")
    print(f"\nNumeric summary:\n{df.select_dtypes(include=np.number).describe()}")

def clean_data(df):
    """Returns a cleaned copy of df: fixed types, no duplicates, no
    inconsistent text, sensible handling of missing values."""
    clean = df.copy()

    clean["TotalCharges"] = pd.to_numeric(clean["TotalCharges"], errors="coerce")

    text_cols = clean.select_dtypes(include=["object", "str"]).columns.drop("customerID")
    for col in text_cols:
        clean[col] = clean[col].astype(str).str.strip()

    yes_no_cols = ["Partner", "Dependents", "PaperlessBilling", "Churn"]
    for col in yes_no_cols:
        clean[col] = clean[col].str.lower().map({"yes": "Yes", "no": "No"})

    before = len(clean)
    clean = clean.drop_duplicates()
    removed = before - len(clean)

    clean["tenure"] = clean["tenure"].fillna(clean["tenure"].median())
    clean["TotalCharges"] = clean["TotalCharges"].fillna(
        clean["MonthlyCharges"] * clean["tenure"]
    )
    clean["InternetService"] = clean["InternetService"].fillna("No")

    clean = clean.reset_index(drop=True)

    print("=" * 60)
    print("STEP 2: DATA CLEANING SUMMARY")
    print("=" * 60)
    print(f"Duplicate rows removed : {removed}")
    print(f"Rows before cleaning   : {before}")
    print(f"Rows after cleaning    : {len(clean)}")
    print(f"Remaining missing values: {clean.isnull().sum().sum()}")
    return clean

def analyze_churn_patterns(df):
    print("=" * 60)
    print("STEP 3: CHURN PATTERN ANALYSIS")
    print("=" * 60)

    overall_rate = (df["Churn"] == "Yes").mean() * 100
    print(f"Overall churn rate: {overall_rate:.1f}%\n")

    print("Churn rate by Contract type:")
    print((df.groupby("Contract")["Churn"].apply(lambda s: (s == "Yes").mean() * 100)
           .round(1).sort_values(ascending=False)))

    print("\nChurn rate by Internet Service:")
    print((df.groupby("InternetService")["Churn"].apply(lambda s: (s == "Yes").mean() * 100)
           .round(1).sort_values(ascending=False)))

    print("\nAverage tenure: churned vs. retained customers")
    print(df.groupby("Churn")["tenure"].mean().round(1))

    print("\nAverage monthly charges: churned vs. retained customers")
    print(df.groupby("Churn")["MonthlyCharges"].mean().round(2))

def create_visualizations(df, output_dir="."):
    plt.rcParams.update({"font.size": 11})

    fig, ax = plt.subplots(figsize=(5, 4))
    counts = df["Churn"].value_counts()
    ax.bar(counts.index, counts.values, color=["#0F766E", "#F97316"])
    ax.set_title("Overall Churn Distribution")
    ax.set_ylabel("Number of Customers")
    for i, v in enumerate(counts.values):
        ax.text(i, v + 5, str(v), ha="center", fontweight="bold")
    fig.tight_layout()
    fig.savefig(f"{output_dir}/chart_churn_distribution.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    rates = df.groupby("Contract")["Churn"].apply(lambda s: (s == "Yes").mean() * 100)
    rates = rates.reindex(["Month-to-month", "One year", "Two year"])
    ax.bar(rates.index, rates.values, color="#0F766E")
    ax.set_title("Churn Rate by Contract Type")
    ax.set_ylabel("Churn Rate (%)")
    for i, v in enumerate(rates.values):
        ax.text(i, v + 1, f"{v:.1f}%", ha="center", fontweight="bold")
    fig.tight_layout()
    fig.savefig(f"{output_dir}/chart_churn_by_contract.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    for label, color in [("No", "#0F766E"), ("Yes", "#F97316")]:
        subset = df[df["Churn"] == label]["tenure"]
        ax.hist(subset, bins=20, alpha=0.6, label=f"Churn = {label}", color=color)
    ax.set_title("Tenure Distribution by Churn Status")
    ax.set_xlabel("Tenure (months)")
    ax.set_ylabel("Number of Customers")
    ax.legend()
    fig.tight_layout()
    fig.savefig(f"{output_dir}/chart_tenure_by_churn.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(5, 4.5))
    numeric_df = df[["SeniorCitizen", "tenure", "MonthlyCharges", "TotalCharges"]]
    corr = numeric_df.corr()
    im = ax.imshow(corr, cmap="RdYlGn", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=9)
    ax.set_title("Correlation Between Numeric Features")
    fig.colorbar(im, ax=ax, shrink=0.8)
    fig.tight_layout()
    fig.savefig(f"{output_dir}/chart_correlation_heatmap.png", dpi=150)
    plt.close(fig)

    print("=" * 60)
    print("STEP 4: VISUALIZATIONS SAVED")
    print("=" * 60)
    print("  chart_churn_distribution.png")
    print("  chart_churn_by_contract.png")
    print("  chart_tenure_by_churn.png")
    print("  chart_correlation_heatmap.png")

if __name__ == "__main__":

    raw_df = generate_synthetic_churn_data(n=1000)
    raw_df.to_csv("customer_churn_raw.csv", index=False)
    print(f"Raw dataset saved: customer_churn_raw.csv ({raw_df.shape[0]} rows)\n")

    explore_raw_data(raw_df)

    clean_df = clean_data(raw_df)
    clean_df.to_csv("customer_churn_cleaned.csv", index=False)
    print(f"\nCleaned dataset saved: customer_churn_cleaned.csv ({clean_df.shape[0]} rows)")

    analyze_churn_patterns(clean_df)

    create_visualizations(clean_df)

    print("\nEDA complete. The cleaned dataset is ready for further analysis.")
