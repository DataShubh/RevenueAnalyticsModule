import streamlit as st
from streamlit_extras.grid import grid
import pandas as pd
import numpy as np
import pymongo
import seaborn as sns
if 'industry' not in st.session_state:
    st.session_state.industry = 'Healthcare'


def main():
    # documents= list(collection.find({}))
    
    df = st.session_state.my_data 
    cols1,cols2, cols3,cols4,cols5,cols6,cols7,cols8,cols9,cols10,cols11 = st.columns(11)
    # Row 1:
    # industries = df['Industry'].unique()
    # st.write(industries)
    
    with cols1:
        if st.button("Health"):
            st.session_state.industry = 'Healthcare'
    with cols2:
        if st.button("   HR   "):
            st.session_state.industry = 'Human Resources'
    with cols3:
        if st.button("   IT   "):
            st.session_state.industry = 'Information Technology'
    with cols4:
        if st.button("  B.I.F  "):
            st.session_state.industry = 'Banking, Insurance & Finance'
    with cols5:
        if st.button(" Banking "):
            st.session_state.industry = 'Banking'
    with cols6:
        if st.button(" Finance "):
            st.session_state.industry = 'Finance'
    with cols7:
        if st.button("  Food  "):
            st.session_state.industry = 'Food Safety'
    with cols8:
        if st.button("R Estate"):
            st.session_state.industry = 'Real Estate'
    with cols9:
        if st.button("Education"):
            st.session_state.industry = 'Education'
    with cols10:
        if st.button(" Trade "):
            st.session_state.industry = 'Trade'
    with cols11:
        if st.button(" Pharma "):
            st.session_state.industry = 'Pharmaceuticals'

    # st.info(st.session_state.industry)


    #Row1
    st.info(st.session_state.industry)
    # Different colors for each line
    # List of 12 colors
    bar_colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'gray', 'magenta', 'violet', 'pink', 'orange', 'purple', 'brown']
    my_grid = grid(2, [2, 4], [2, 4], vertical_align="bottom")
    # Create a new DataFrame df_industry as a copy of df
    df_industry = df[df['Industry'] == st.session_state.industry].copy()
    sub_industry = list(df_industry['Sub_Industry'].unique())
    sub_industry.insert(0, 'All')
    # st.info(sub_industry)
    with my_grid.expander("Show Filters", expanded=False):
        sub_industry_option= st.selectbox("Select Category",sub_industry, index=0)

    if sub_industry_option is not 'All':
        df_industry = df[df['Sub_Industry'] == sub_industry_option].copy()

    
    
    # Convert 'Event_Date' to datetime
    df_industry['Event_Date'] = pd.to_datetime(df_industry['Event_Date'], format='%d-%m-%Y')
    # Extract month and year from 'Event_Date'
    df_industry['Month'] = df_industry['Event_Date'].dt.month
    
    df_industry['Year'] = df_industry['Event_Date'].dt.year
   
   # Group by 'Industry', 'Year', and 'Month' and sum the 'Revenue'
    result_df = df_industry.groupby(['Year', 'Month'], as_index=True)['Price'].count()
    

    result_df=pd.DataFrame(result_df)
    # Pivot the table for a better display
    pivot_df = result_df.pivot_table(index=['Year'], columns='Month', values='Price', fill_value=0)
    
    # Add a new column for the sum of each row
    pivot_df['Yearly_Total'] = pivot_df.sum(axis=1)
    # Add a new row for the sum of prices column-wise
    pivot_df.loc['Monthly_Total'] = pivot_df.sum()
    # Rename columns to 'Jan', 'Feb', 'Mar', etc.
    pivot_df.rename(columns={1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}, inplace=True)
    
    my_grid.dataframe(pivot_df, use_container_width=True)
    
    # Count the occurrences for each combination of 'Year' and 'Month'
    result_df2 = df_industry.groupby(['Year', 'Month'], as_index=True)['Price'].count().reset_index(name='Count')
    yearly_result = result_df2.groupby(['Year'], as_index=True)['Count'].sum()
    monthly_result = result_df2.groupby(['Month'], as_index=True)['Count'].sum()
    
    


    
    
    
    my_grid.line_chart(yearly_result, use_container_width=True )
    my_grid.bar_chart(yearly_result, use_container_width=True, )
    # Bar chart with individual colors for each bar
    my_grid.line_chart(monthly_result, use_container_width=True)
    my_grid.bar_chart(monthly_result, use_container_width=True,)
    


