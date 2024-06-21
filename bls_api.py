import requests
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import seaborn as sns
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.utils.dataframe import dataframe_to_rows



# API Token from BLS website I registered for 
api_token = 'ed5e426dd53c448d979db8ae3cedc1f1'

# Defining headers
headers = {
    'Authorization': f'Bearer {api_token}',
    'Content-type': 'application/json'
}

# Method to hit the data
def get_data(start_year, end_year):

    # Define data to be sent into POST request
    data = json.dumps({
        "seriesid": ["JTU000000000000000HIL"],
        "startyear": str(start_year), 
        "endyear": str(end_year),
        "registrationkey" : api_token
    })

    # Send a POST request
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    
    # Parse the JSON response
    json_data = json.loads(p.text)
    print(json_data)
    
    # Convert JSON data into a data frame
    df = pd.DataFrame(json_data['Results']['series'][0]['data'])
    df['value'] = df['value'].astype(int)
    df['Month'] = df['period'].str[1:].astype(int)
    df['year'] = df['year'].astype(int)
    df['YearMonth'] = pd.to_datetime(df[['year', 'Month']].assign(day=1))

    return df


def main():
    
    # Function call with appropriate start and end years
    start = 2005
    end = 2024
    data_frame = get_data(start, end)
    data_frame = data_frame.drop(columns='footnotes')
    
    # Sort values from lowest to highest to help create graph
    data_frame.sort_values(by=['year', 'Month'], inplace=True)
    print(data_frame)
    
    # Find the minimum and maximum date to add to title
    min_date = data_frame.iloc[0]['periodName'] + ' ' + str(data_frame.iloc[0]['year'])
    max_date = data_frame.iloc[-1]['periodName'] + ' ' + str(data_frame.iloc[-1]['year'])
    
    # Generate a random series of data to add on the same line plot
    np.random.seed(123)
    data_frame['Generic'] = np.random.uniform(3950, 10000, size=len(data_frame))

    # Using seaborn to visualize data
    plt.figure(figsize=(10, 7))
    sns.lineplot(data=data_frame, x='YearMonth', y='value', color='blue')
    sns.lineplot(data=data_frame, x='YearMonth', y='Generic', color='red')
    plt.title(f"Federal Parent Locator Service (FLPS) and Bureau of Labor Statistics (BLS) Comparison \nMonthly New Hire ({min_date} - {max_date}) \n\n")
    plt.xlabel('Year')
    plt.ylabel('Thousands of New Hires')
    
    # Creating the legend for both series
    blue_line = mlines.Line2D([], [], color='blue', label='BLS')
    red_line = mlines.Line2D([], [], color='red', label='FLPS')
    plt.legend(handles=[blue_line, red_line], loc='upper center', bbox_to_anchor=(0.5, 1.07), ncol=2)
    
    # Reflecting monthly changes
    year_ticks = pd.date_range(start=f'{start}-01-01', end=f'{end}-12-31', freq='YS')
    
    # Adjust x and y ticks
    plt.xticks(year_ticks, [str(year.year) for year in year_ticks], rotation=45)
    plt.yticks(range(0, 11000, 1000))
    
    # Save the plot
    plot_file = 'my_blt_plot.png'
    plt.savefig(plot_file, dpi=150)
    
    file_name = 'BLS_data.xlsx'
    
    # Save data to an excel file
    writer = pd.ExcelWriter(file_name, engine='openpyxl')
    data_frame.to_excel(writer, sheet_name='BLS Data', index=False)
    
    wb = writer.book
    
    # Load image to new sheet
    ws = wb.create_sheet(title='Plot')
    img = Image(plot_file)
    ws.add_image(img, 'A1')
    
    # Adjust column width
    wb['BLS Data'].column_dimensions['G'].width = 20
    
    wb.save(file_name)
    plt.show()

if __name__ == "__main__":
    main()