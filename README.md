# BLS Data Visualization Project

This project fetches data from the Bureau of Labor Statistics (BLS) API, processes the data, and visualizes it in Python. The resulting data and visualizations are saved to an Excel file.

## Features

- Fetches time series data from the BLS API.
- Processes and cleans the data.
- Generates random series data for comparison.
- Visualizes the data using **Seaborn** and **Matplotlib**.
- Saves the data and the visualizations to an Excel file with custom formatting.

## Prerequisites

- Python 3.x
- An active BLS API key

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/tejasking62/BLS-Hire-Analysis.git
    cd BLS-Hire-Analysis
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Configure your API token:**
    - Open the `bls_api.py` file and replace the value for authorization in the header with your api token.
    - Choose which range of years to pull data from

2. **Run the script:**
    ```bash
    python bls_api.py
    ```

3. **Output:**
    - The script will generate a plot and save it as `my_blt_plot.png`.
    - The data and the plot will be saved to an Excel file named `BLS_data.xlsx`.

