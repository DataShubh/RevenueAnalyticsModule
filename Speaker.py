import streamlit as st
from streamlit_extras.grid import grid
import pandas as pd
import numpy as np
import pymongo
import seaborn as sns
from streamlit_apexjs import st_apexcharts

if ' speaker' not in st.session_state:
    st.session_state.speaker_select = '0'
def main():
    # documents= list(collection.find({}))
    
    df = st.session_state.my_data
    # speaker_list = sorted(list(df['Speaker'].unique()))
    speaker_list = sorted(map(str, df['Speaker'].unique()))

    
    st.session_state.speaker_select = st.sidebar.selectbox("Select Category",speaker_list, index=0)
    st.sidebar.info(st.session_state.speaker_select)
    speaker_df = df[df['Speaker']==st.session_state.speaker_select].copy()
    result_df = speaker_df.groupby(['Event_Title', 'Sub_Industry', 'Industry'], as_index=True)['Price'].sum().reset_index()
    # Calculate the sum of values in the 'Value' column
    total_sum = result_df['Price'].sum()
    st.sidebar.success(f"Revenue: {total_sum}")
    st.subheader("Speaker Performance Review")
    st.dataframe(result_df)

    # my_grid = grid([2, 4], vertical_align="bottom")    
    result_df2 = speaker_df.groupby(['Product_Category'], as_index=True)['Price'].sum().reset_index()
    result_df2.sort_values(by='Product_Category', inplace=True)
    price= list(result_df2['Price'])
    label = list(result_df2['Product_Category'])
    options = {
    "chart": {
        "toolbar": {
            "show": False
        }
    },

    "labels": label
    ,
    "legend": {
        "show": True,
        "position": "bottom",
    }
}

    # series = [44, 55, 41, 17, 15,16]

    st.subheader("Product Category")
    st_apexcharts(options, price, 'donut', '600')
    st.dataframe(result_df2)