# Unemployment Analysis Dashboard

An interactive Streamlit dashboard for exploring the cleaned unemployment dataset. The dashboard lets you filter the data by state or region, area, and date range.

## Dashboard features

- Summary metrics for the average unemployment rate, highest recorded rate, number of records, and states or regions in the selected data.
- Bar chart comparing average unemployment rates by state or region.
- Line chart showing average unemployment rate over time.
- Comparison of the pre-COVID period and March–December 2020, when both periods are present in the selected data.
- Filtered data table with an option to download the selected rows as a CSV file.

## Project files

- `app.py` — Streamlit dashboard.
- `Cleaned_Unemployment_Data.csv` — cleaned dataset used by the dashboard.
- `Unemployment_in_India.csv` — original dataset.
- `unemployment_analysis.py` — existing data analysis and chart code.
- `main.py` — project entry file.
- `graphs/` — saved graph images.

## Run the dashboard on Windows

Open a terminal in the project folder and run:

```powershell
python -m pip install streamlit pandas
python -m streamlit run app.py
```

The terminal will show a local address to open in your browser.

If using the project's virtual environment, run:

```powershell
.\.venv\Scripts\python.exe -m pip install streamlit pandas
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Dataset columns

The cleaned CSV includes `Region`, `Date`, `Frequency`, `Estimated Unemployment Rate (%)`, `Estimated Employed`, `Estimated Labour Participation Rate (%)`, `Area`, `Month`, and `Year`.

## Uploading to GitHub

Upload the project files and datasets needed for the project. Do not upload the `.venv` folder; it is a local Python environment and can be recreated on another computer.
