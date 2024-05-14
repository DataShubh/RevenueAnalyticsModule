import streamlit as st
import pymongo
import pandas as pd

@st.cache_resource
def init_connection():
    try:
        # db_username = st.secrets.db_username
        # db_password = st.secrets.db_password

        # mongo_uri_template = "mongodb+srv://{username}:{password}@cluster0.thbmwqi.mongodb.net/"
        # mongo_uri = mongo_uri_template.format(username=db_username, password=db_password)

        # client = pymongo.MongoClient(mongo_uri)
        # # # mongodb+srv://Vedsu:CVxB6F2N700cQ0qu@cluster0.thbmwqi.mongodb.net/
        # # client=pymongo.MongoClient("mongodb+srv://Vedsu:CVxB6F2N700cQ0qu@cluster0.thbmwqi.mongodb.net/")
        # return client
        client = pymongo.MongoClient("mongodb+srv://Vedsu:CVxB6F2N700cQ0qu@cluster0.thbmwqi.mongodb.net/")
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


