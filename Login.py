import streamlit as st
import yaml
from yaml.loader import SafeLoader
from streamlit_authenticator import Authenticate
import pymongo
import pandas as pd
import Schedule
import Performance

#Database Connections
@st.cache_resource
def init_connection():
    try:
        # db_username = st.secrets.db_username
        # db_password = st.secrets.db_password

        # mongo_uri_template = "mongodb+srv://{username}:{password}@cluster0.thbmwqi.mongodb.net/"
        # mongo_uri = mongo_uri_template.format(username=db_username, password=db_password)

        # client = pymongo.MongoClient(mongo_uri)
        
        # return client
        client = pymongo.MongoClient("mongodb+srv://----------------------@cluster0.thbmwqi.mongodb.net/")
        return client
    
    except:
    
        st.write("Connection Could not be Established with database")

client = init_connection()
db= client['EventDatabase']

collection = db['Revenue']

documents= list(collection.find({}))
df = pd.DataFrame(documents)

def main():
    
    with st.container():    

    #Load configuration from YAML file
        with open('./config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)

        # Initialize the authenticator
        authenticator =Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config['preauthorized']
        )

        col1, col2 = st.columns(2)

        name, authentication_status, usernamer = authenticator.login('Login', 'main')

        if authentication_status:
            # Storing the DataFrame in session_state
            st.session_state.my_data = df

            # with col1:
            #     authenticator.logout('Logout', 'main')
            
            # with col2:
                # st.markdown(f'Welcome - <span style="color: blue;">*{name}*</span>', unsafe_allow_html=True)
            Performance.main()
        elif authentication_status == False:
            st.error('Username/password is incorrect')
        elif authentication_status ==None:
            st.warning('Please enter your username and password')
