import streamlit as st
# from streamlit_lightweight_charts import renderLightweightCharts
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

def main():
    # documents= list(collection.find({}))
    
    data = st.session_state.my_data 
    df =  data.groupby(['Event_Date'], as_index=True)['Price'].sum().reset_index()



    # Assuming your DataFrame is named 'df'
    # Make sure 'Event_Date' is in datetime format
    df['Event_Date'] = pd.to_datetime(df['Event_Date'])

    # Set 'Event_Date' as the index
    df.set_index('Event_Date', inplace=True)

    # Resample data to monthly frequency and calculate the mean price for each month
    monthly_data = df.resample('M').mean()

    # Generate a time series plot with different colors for each month
    fig, ax = plt.subplots(figsize=(10, 6))

    # Define a color map for each month
    colors = plt.cm.viridis(range(len(monthly_data.index.month) + 1))

    # Plot each month with a different color
    for i, month in enumerate(monthly_data.index.month.unique()):
        subset_data = monthly_data[monthly_data.index.month == month]
        ax.plot(subset_data.index, subset_data['Price'], label=month, color=colors[i])

    # Format x-axis as months
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

    # Set labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Event Price')
    ax.set_title('Monthly Event Prices')

    # Add legend
    ax.legend(title='Month', loc='upper left')

    # Show the plot
    plt.show()
