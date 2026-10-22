from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "data" / "sales_data.csv"
OUTPUT_DIR = PROJECT_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def main():
    # 1. Load the dataset
    df = pd.read_csv(DATA_FILE)
    df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
    df["Revenue"] = df["UnitsSold"] * df["UnitPrice"]

    print("\n=== CODEALPHA: SALES DATA ANALYSIS ===")
    print(f"\nDataset rows: {df.shape[0]}")
    print(f"Dataset columns: {df.shape[1]}")
    print("\nFirst five rows:")
    print(df.head().to_string(index=False))

    # 2. Explore the structure (EDA)
    print("\nColumn data types:")
    print(df.dtypes.to_string())
    print("\nMissing values by column:")
    print(df.isnull().sum().to_string())
    print(f"\nDuplicate rows: {df.duplicated().sum()}")

    print("\nNumeric summary:")
    print(df[["UnitsSold", "UnitPrice", "Revenue"]].describe().round(2).to_string())

    # 3. Answer simple business questions
    revenue_by_product = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
    revenue_by_region = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
    monthly_revenue = df.groupby(df["OrderDate"].dt.to_period("M"))["Revenue"].sum()
    units_by_category = df.groupby("Category")["UnitsSold"].sum().sort_values(ascending=False)

    print("\nRevenue by product:")
    print(revenue_by_product.round(2).to_string())
    print("\nRevenue by region:")
    print(revenue_by_region.round(2).to_string())
    print("\nMonthly revenue:")
    print(monthly_revenue.to_string())
    print("\nUnits sold by category:")
    print(units_by_category.to_string())

    # Save clean summary tables for the project submission
    revenue_by_product.rename("TotalRevenue").to_csv(OUTPUT_DIR / "revenue_by_product.csv")
    revenue_by_region.rename("TotalRevenue").to_csv(OUTPUT_DIR / "revenue_by_region.csv")
    monthly_revenue.rename("TotalRevenue").to_csv(OUTPUT_DIR / "monthly_revenue.csv")

    # 4. Data Visualization: save charts as PNG files
    plt.figure(figsize=(9, 5))
    revenue_by_product.plot(kind="bar")
    plt.title("Total Revenue by Product")
    plt.xlabel("Product")
    plt.ylabel("Revenue")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "revenue_by_product.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    monthly_revenue.index = monthly_revenue.index.astype(str)
    monthly_revenue.plot(kind="line", marker="o")
    plt.title("Monthly Revenue Trend")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "monthly_revenue.png", dpi=150)
    plt.close()

    plt.figure(figsize=(7, 5))
    units_by_category.plot(kind="pie", autopct="%1.1f%%", startangle=90)
    plt.title("Units Sold by Category")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "units_by_category.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    df["Revenue"].plot(kind="hist", bins=8, edgecolor="black")
    plt.title("Distribution of Order Revenue")
    plt.xlabel("Revenue per order")
    plt.ylabel("Number of orders")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "order_revenue_histogram.png", dpi=150)
    plt.close()

    # 5. Automatically write short findings based on this dataset
    top_product = revenue_by_product.idxmax()
    top_region = revenue_by_region.idxmax()
    best_month = monthly_revenue.idxmax()
    total_revenue = df["Revenue"].sum()
    total_units = df["UnitsSold"].sum()

    report = f"""CODEALPHA INTERNSHIP PROJECT: EDA AND DATA VISUALIZATION

Dataset rows: {len(df)}
Total units sold: {total_units}
Total revenue: {total_revenue:,.2f}
Highest-revenue product: {top_product} ({revenue_by_product.max():,.2f})
Highest-revenue region: {top_region} ({revenue_by_region.max():,.2f})
Highest-revenue month: {best_month} ({monthly_revenue.max():,.2f})
Missing values: {int(df.isnull().sum().sum())}
Duplicate rows: {int(df.duplicated().sum())}

Charts created:
- revenue_by_product.png
- monthly_revenue.png
- units_by_category.png
- order_revenue_histogram.png

Note: This is a small sample dataset created for learning and demonstration.
Do not present it as real company data.
"""
    (OUTPUT_DIR / "insights_report.txt").write_text(report, encoding="utf-8")
    print("\n" + report)
    print(f"\nDone! Check the '{OUTPUT_DIR.name}' folder for charts, tables, and the report.")

if __name__ == "__main__":
    main()
