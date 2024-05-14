import streamlit as st
import extra_streamlit_components as stx
import Schedule
import Revenue
import Industry
import Speaker
import Analytics
if 'chosen_menu' not in st.session_state:
    st.session_state.chosen_id = None
def main():
    st.title("Dashboard")
    st.session_state.chosen_id = stx.tab_bar(data=[
    stx.TabBarItemData(id=1, title="Manager", description="Efficient Event Scheduling and Management"),
    stx.TabBarItemData(id=2, title="Speaker", description="In-Depth Analytics for Speaker Performance"),
    stx.TabBarItemData(id=3, title="Dashboard", description="Comprehensive Industry Analytics Dashboard"),
    stx.TabBarItemData(id=4, title="Analytics", description="Explore and Analyze Data with Dynamic Combinations"),
    stx.TabBarItemData(id=5, title="Uploader", description="Effortless Revenue Sheet Upload for Quick Analysis")
], default=1)
    
    if st.session_state.chosen_id == '1':
        Schedule.main()
    elif st.session_state.chosen_id=='2':
        Speaker.main()
    elif st.session_state.chosen_id=='3':
        Industry.main()
    elif st.session_state.chosen_id=='4':
        Analytics.main()

    elif st.session_state.chosen_id == '5':
        Revenue.main()
        