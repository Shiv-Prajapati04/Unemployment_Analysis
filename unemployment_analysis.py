import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create graphs folder if it does not exist
os.makedirs("graphs", exist_ok=True)
df = pd.read_csv("Unemployment_in_India.csv")
print(df.head())

print("Dataset Shape:", df.shape)
print("Column Names:", df.columns)
print(df.info())
print("\nMissing Values:")
print(df.isnull().sum())
df.columns = df.columns.str.strip()

print("\nClean Column Names:")
print(df.columns.tolist())
df = df.dropna()

print("\nMissing values after cleaning:")
print(df.isnull().sum())
print("Duplicate Rows:", df.duplicated().sum())
df = df.drop_duplicates()

print("Dataset Shape After Cleaning:", df.shape)
print("\nFinal Dataset:")
print(df.head())

print("\nData Cleaning Completed Successfully!")
# Convert Date column into datetime
df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)

print("Date conversion completed!")
# Basic statistical analysis

print("\nUnemployment Rate Statistics")

print("Average Unemployment Rate:",
      df['Estimated Unemployment Rate (%)'].mean())

print("Maximum Unemployment Rate:",
      df['Estimated Unemployment Rate (%)'].max())

print("Minimum Unemployment Rate:",
      df['Estimated Unemployment Rate (%)'].min())
print("\nComplete Statistical Summary:")
print(df.describe())
top_states = df.groupby('Region')[
    'Estimated Unemployment Rate (%)'
].mean().sort_values(ascending=False)

print("\nTop 5 States with Highest Unemployment:")
print(top_states.head(5))
print("\nTop 5 States with Lowest Unemployment:")
print(top_states.tail(5))
plt.figure(figsize=(10, 5))

sns.histplot(
    df['Estimated Unemployment Rate (%)'],
    bins=20,
    kde=True
)
plt.savefig(
    "graphs/unemployment_graph.png",
    dpi=300,
    bbox_inches="tight"
)

plt.title("Unemployment Rate Distribution")
plt.xlabel("Unemployment Rate (%)")
plt.ylabel("Frequency")

plt.show()
plt.figure(figsize=(12, 6))

state_data = df.groupby('Region')[
    'Estimated Unemployment Rate (%)'
].mean().sort_values(ascending=False)

sns.barplot(
    x=state_data.values,
    y=state_data.index
)

plt.title("Average Unemployment Rate by State")
plt.xlabel("Average Unemployment Rate (%)")
plt.ylabel("State")

plt.tight_layout()
plt.show()
plt.figure(figsize=(12, 6))

monthly_data = df.groupby('Date')[
    'Estimated Unemployment Rate (%)'
].mean()

plt.plot(monthly_data.index, monthly_data.values)

plt.title("Unemployment Rate Over Time")
plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")

plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()
plt.figure(figsize=(8, 5))

correlation = df.select_dtypes(
    include='number'
).corr()

sns.heatmap(
    correlation,
    annot=True,
    cmap='coolwarm',
    fmt='.2f'
)

plt.title("Correlation Heatmap")

plt.tight_layout()
plt.show()
# COVID-19 Impact Analysis

# Separate pre-COVID and COVID period
pre_covid = df[df['Date'] < '2020-03-01']

covid_period = df[
    (df['Date'] >= '2020-03-01') &
    (df['Date'] <= '2020-12-31')
]

# Calculate average unemployment rate
pre_covid_avg = pre_covid[
    'Estimated Unemployment Rate (%)'
].mean()

covid_avg = covid_period[
    'Estimated Unemployment Rate (%)'
].mean()

print("\nCOVID-19 IMPACT ANALYSIS")

print("Pre-COVID Average:", pre_covid_avg)

print("COVID Period Average:", covid_avg)

print("Difference:", covid_avg - pre_covid_avg)
plt.figure(figsize=(8, 5))

periods = ['Pre-COVID', 'COVID Period']
rates = [pre_covid_avg, covid_avg]

sns.barplot(x=periods, y=rates)

plt.title("Impact of COVID-19 on Unemployment Rate")
plt.xlabel("Period")
plt.ylabel("Average Unemployment Rate (%)")

plt.show()
percentage_change = (
    (covid_avg - pre_covid_avg) / pre_covid_avg
) * 100

print("Percentage Change:", percentage_change, "%")
# Extract month and year
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

print(df[['Date', 'Month', 'Year']].head())
# Calculate monthly average unemployment
monthly_unemployment = df.groupby('Month')[
    'Estimated Unemployment Rate (%)'
].mean()

print("\nMonthly Average Unemployment:")
print(monthly_unemployment)
plt.figure(figsize=(10, 5))

sns.lineplot(
    x=monthly_unemployment.index,
    y=monthly_unemployment.values,
    marker='o'
)

plt.title("Monthly Unemployment Trend in India")
plt.xlabel("Month")
plt.ylabel("Average Unemployment Rate (%)")

plt.xticks(range(1, 13))
plt.grid(True)

plt.show()
plt.figure(figsize=(10, 5))

sns.barplot(
    x=monthly_unemployment.index,
    y=monthly_unemployment.values
)

plt.title("Month-wise Average Unemployment Rate")
plt.xlabel("Month")
plt.ylabel("Unemployment Rate (%)")

plt.show()
highest_month = monthly_unemployment.idxmax()
lowest_month = monthly_unemployment.idxmin()

print("Highest Unemployment Month:", highest_month)
print("Highest Rate:", monthly_unemployment.max())

print("Lowest Unemployment Month:", lowest_month)
print("Lowest Rate:", monthly_unemployment.min())
# FINAL PROJECT INSIGHTS

print("\n========== UNEMPLOYMENT ANALYSIS ==========")

print("\n1. Overall Analysis")

overall_avg = df['Estimated Unemployment Rate (%)'].mean()

print("Overall Average Unemployment Rate:",
      round(overall_avg, 2), "%")

print("\n2. State Analysis")

print("Highest Unemployment State:",
      top_states.idxmax())

print("Lowest Unemployment State:",
      top_states.idxmin())

print("\n3. COVID-19 Analysis")

print("Pre-COVID Average:",
      round(pre_covid_avg, 2), "%")

print("COVID Average:",
      round(covid_avg, 2), "%")

print("\n4. Monthly Analysis")

print("Highest Unemployment Month:", highest_month)
print("Lowest Unemployment Month:", lowest_month)

print("\n========== ANALYSIS COMPLETED ==========")
# Save cleaned dataset

df.to_csv("Cleaned_Unemployment_Data.csv", index=False)

print("Cleaned dataset saved successfully!")
plt.savefig("graphs/unemployment_graph.png",
            dpi=300,
            bbox_inches="tight")

# FINAL SUMMARY DASHBOARD

plt.figure(figsize=(12, 6))

# State-wise unemployment
sns.barplot(
    x=state_data.head(10).values,
    y=state_data.head(10).index
)

plt.title("Top 10 States by Average Unemployment Rate")
plt.xlabel("Unemployment Rate (%)")
plt.ylabel("States")

plt.tight_layout()

plt.savefig(
    "graphs/final_dashboard.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.figure(figsize=(9, 5))

sns.barplot(
    x=['Pre-COVID', 'COVID Period'],
    y=[pre_covid_avg, covid_avg]
)

plt.title('Impact of COVID-19 on Unemployment')
plt.xlabel('Period')
plt.ylabel('Average Unemployment Rate (%)')

plt.savefig(
    'graphs/covid_impact.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()
plt.figure(figsize=(12, 6))

sns.barplot(
    x=state_data.head(10).values,
    y=state_data.head(10).index
)

plt.title('Top 10 States by Average Unemployment')
plt.xlabel('Unemployment Rate (%)')
plt.ylabel('States')

plt.tight_layout()

plt.savefig(
    'graphs/state_comparison.png',
    dpi=300,
    bbox_inches='tight'
)

plt.show()
