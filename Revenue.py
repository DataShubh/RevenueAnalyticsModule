import streamlit as st
import pymongo
import pandas as pd

@st.cache_resource
def init_connection():
    try:
        
        client = pymongo.MongoClient("mongodb+srv://----------------------------------@cluster0.thbmwqi.mongodb.net/")
        return client
    except:
        st.write("Connection Could not be Established with database")

client = init_connection()
db= client['EventDatabase']

collection = db['Vedsu']
# Streamlit app
def main():
    st.title("Effortless Revenue Sheet Upload for Quick Analysis")
    uploaded_file = st.file_uploader("Choose a CSVfile", type=["csv"])

    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        df = pd.read_csv(uploaded_file,encoding="latin1")
        st.dataframe(df)
        if st.button("Submit"):
            # Convert DataFrame to dictionary for easier insertion
            data_dict = df.to_dict(orient="records")
            try:
                # Insert data into MongoDB
                collection.insert_many(data_dict)
                st.success("Successful")
            except Exception as e:
                st.write(e)


