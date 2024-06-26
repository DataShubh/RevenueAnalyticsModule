import streamlit as st
import pymongo
import pandas as pd
# import time
from datetime import datetime, timedelta
import pytz
# from io import BytesIO
# import base64

@st.cache_resource
def init_connection():
    try:
        # db_username = st.secrets.db_username
        # db_password = st.secrets.db_password

        # mongo_uri_template = "mongodb+srv://{username}:{password}@cluster0.thbmwqi.mongodb.net/"
        # mongo_uri = mongo_uri_template.format(username=db_username, password=db_password)

        # client = pymongo.MongoClient(mongo_uri)
        client = pymongo.MongoClient("mongodb+srv://----------------------@cluster0.thbmwqi.mongodb.net/")
        return client
        
        
    except Exception as e:
        st.error(f"Error raised, {str(e)}")
    
client = init_connection()
db = client['EventDatabase']
collection = db['Webinars']

@st.cache_resource
def main():
    st.subheader("Completed Event")
    

    # try:
    #     events= collection.find({}).sort("Date", pymongo.DESCENDING)
    # except Exception as e:
    #     st.write(f"Error {str(e)}")
    # Get the current date
    today_utc = datetime.utcnow()
    # Set the UTC timezone
    utc_timezone = pytz.timezone('UTC')
    today_utc = utc_timezone.localize(today_utc)

    # Convert to the Eastern Standard Time (EST) timezone
    est_timezone = pytz.timezone('US/Eastern')
    today_est = today_utc.astimezone(est_timezone)
   
    
    try:
        # Perform the update
        events = collection.find({}).sort("Date", pymongo.ASCENDING)

        # st.write(events)
    except Exception as e:
        
        st.error(f"Error {str(e)}")
    

    # col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
    
    event_list = []
    for event in events:
        
        id_value = event.get("_id")
        webinar = event.get("Webinar")
        speaker = event.get("Speaker")
        date = event.get("Date")
        timing = event.get("Time")
        duration = event.get("Duration")
        status = event.get('Status')
        industry = event.get("Industry")
        website = event.get("Website")
        document = event.get("Document")
        
        date_from_database = datetime.strptime(date, "%Y-%m-%d").date()
        if today_est.date() > date_from_database and status=='Active':
            try: 
                collection.update_one(
                    {"_id": id_value},
                        {"$set": {"Status": "Completed"}})
                # st.write(webinar)

            # st.sidebar.success(f"Status Changed to {status_value}")
            except Exception as e:
                st.error("Failed!")
        if webinar!="Holiday" and status!='Active':
            
            # Convert the string to a datetime object
            original_date = datetime.strptime(date, "%Y-%m-%d")
                
            # Format the datetime object as a string with the desired format
            formatted_date_string = original_date.strftime("%d-%m-%Y")
            if document!=None:
                pdf_href = "A"
                    # pdf_content_b64 = base64.b64encode(document).decode('utf-8')
                    # pdf_href = f'<a href="data:application/pdf;base64,{pdf_content_b64}" target="_blank">View PDF</a>'
            else:
                pdf_href = "N.A"
                    
            event_list.append({
                
                "Status": status,
                "Speaker": speaker,
                "Webinar": webinar,
                "Date": formatted_date_string,  # Convert to date for consistency
                "Time": timing,
                "Duration": duration,
                "Industry": industry,
                "Website":website,
                "Document":pdf_href,})
          
    df= pd.DataFrame(event_list)
    st.dataframe(df)

        


            

    
      
