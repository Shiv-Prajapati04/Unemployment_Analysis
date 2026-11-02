from pathlib import Path

import pandas as pd
import streamlit as st


DATA_FILE = Path(__file__).with_name("Cleaned_Unemployment_Data.csv")
RATE_COLUMN = "Estimated Unemployment Rate (%)"

st.set_page_config(page_title="Unemployment Analysis", page_icon="📊", layout="wide")
st.title("Unemployment Analysis in India")
st.caption("Explore the cleaned project dataset by state, area and date.")


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    data.columns = data.columns.str.strip()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data[RATE_COLUMN] = pd.to_numeric(data[RATE_COLUMN], errors="coerce")
    return data.dropna(subset=["Region", "Date", RATE_COLUMN])


try:
    df = load_data(DATA_FILE)
except FileNotFoundError:
    st.error(f"Could not find {DATA_FILE.name}. Put it in the same folder as app.py.")
    st.stop()
except (KeyError, pd.errors.ParserError) as error:
    st.error(f"The cleaned CSV could not be read as expected: {error}")
    st.stop()

required_columns = {"Region", "Date", RATE_COLUMN, "Area"}
missing_columns = required_columns.difference(df.columns)
if missing_columns:
    st.error("The cleaned CSV is missing required columns: " + ", ".join(sorted(missing_columns)))
    st.stop()

st.sidebar.header("Filters")
regions = sorted(df["Region"].dropna().unique().tolist())
areas = sorted(df["Area"].dropna().unique().tolist())
selected_regions = st.sidebar.multiselect("States / regions", regions, default=regions)
selected_areas = st.sidebar.multiselect("Area", areas, default=areas)
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()
selected_dates = st.sidebar.date_input(
    "Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date
)

filtered = df[df["Region"].isin(selected_regions) & df["Area"].isin(selected_areas)].copy()
if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered = filtered[filtered["Date"].between(pd.Timestamp(start_date), pd.Timestamp(end_date))]

if filtered.empty:
    st.info("No rows match these filters. Choose a wider date range or more regions/areas.")
    st.stop()

average_rate = filtered[RATE_COLUMN].mean()
highest_rate = filtered[RATE_COLUMN].max()
record_count = len(filtered)
region_count = filtered["Region"].nunique()

metric1, metric2, metric3, metric4 = st.columns(4)
metric1.metric("Average unemployment rate", f"{average_rate:.2f}%")
metric2.metric("Highest recorded rate", f"{highest_rate:.2f}%")
metric3.metric("Records in view", f"{record_count:,}")
metric4.metric("States / regions", f"{region_count}")
st.caption("Metrics describe the rows currently selected by the filters.")

left, right = st.columns(2)
with left:
    st.subheader("Average rate by state / region")
    state_rates = filtered.groupby("Region")[RATE_COLUMN].mean().sort_values(ascending=False)
    st.bar_chart(state_rates)

with right:
    st.subheader("Unemployment rate over time")
    date_rates = filtered.groupby("Date")[RATE_COLUMN].mean().sort_index()
    st.line_chart(date_rates)

st.subheader("COVID-19 period comparison")
pre_covid = filtered.loc[filtered["Date"] < "2020-03-01", RATE_COLUMN]
covid_period = filtered.loc[filtered["Date"].between("2020-03-01", "2020-12-31"), RATE_COLUMN]
covid_left, covid_right = st.columns(2)
if pre_covid.empty or covid_period.empty:
    st.info(
        "The current filters need records both before March 2020 and from March through "
        "December 2020 to show this comparison."
    )
else:
    covid_left.metric("Pre-COVID average", f"{pre_covid.mean():.2f}%")
    covid_right.metric(
        "Mar–Dec 2020 average",
        f"{covid_period.mean():.2f}%",
        delta=f"{covid_period.mean() - pre_covid.mean():+.2f} percentage points",
    )

st.subheader("Filtered data")
st.dataframe(filtered.sort_values("Date", ascending=False), use_container_width=True, hide_index=True)
st.download_button(
    label="Download filtered data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="unemployment_filtered_data.csv",
    mime="text/csv",
)
