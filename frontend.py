import streamlit as st
import pandas as pd
import requests
import plotly.express as pl

st.set_page_config(page_title="sales forecast",layout="wide")
st.title("Sales forecasting")
tab1,tab2,tab3=st.tabs(["Forecasting","Inventory","Sentiment_Analysis"])
with tab1:
    st.header("Future Forecasting")
    prdid=st.text_input("Enter the Product ID: ")
    submit=st.button("Get the Forecasting")
    if submit:
        res=requests.get(f"http://127.0.0.1:8000/forecast/{prdid}")
        if res.status_code==200:
            df = pd.DataFrame([res.json()])
            st.success("Data Loaded successfully and waiting for forecasting")
            grp=px.line(df,x="ds",y="yhat",title="Next_30 Days Forecasting")
            st.plotly_chart(grp)
            st.dataframe(df)
        elsest.error("Id not found")    
with tab2:
    st.header("Inventory Details ")
    prdid=st.text_input("Enter the product_id")
    if(st.button("Give inventory Details")):
       res=requests.get(f"http://127.0.0.1:8000/forecast/{prdid}")
       response=res.json()
       st.write(f"product_Id : {prdid}")
       st.write(f"Current Quantity :",response["current Quantity"]) 
       st.write(f"Daily Average : ",response["Daily Avg"])
       st.write(f"Reorder Requirment : ",response["Reorder Quantity"])
             