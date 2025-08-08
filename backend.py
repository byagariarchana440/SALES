from prophet import Prophet                     
from pymongo import MongoClient                
import pandas as pd
import json
from pipeline import transformers              
from fastapi import FastAPI 
  


client=MongoClient("mongodb://localhost:27017/")
dataabase=client["supply_chain_db"]
collection=dataabase["sales_data"]

sentiment_analyzer=pipeline("sentiment-analysis")

app=FastAPI()

@app.get("forecast/{product_id}")
def forecasting(product_id:str):
    data=list(collection.find({"product_id":product_id}))
    if not data:
        return {"error":"Product ID Not Found"}
    df=pd.DataFrame(data)
    df["data"]=pd.to_datetime(df["date"])
    df_prf=df[["date","sales_quantity"]].rename(colums={"date":"ds","sales_quantity":"y"})
    model=Prophet()
    model.fit(df_prf)
    future=model.make_future_dataframe(periods=30)
    forecast=model.predict(future)

    result=forecast[["ds","yhat","yhat_lower","yhat_upper"]].tail(30)
    return json.load(result.to_json(orient="records",date_format="iso"))

@app.get("/inventory/{product_id}")
def inventory(product_id:str):
    data=list(collection.fin({"product_id":product_id}))
    if not data:
        return {"error":"Product ID Not Found"}
    df=pd.DataFrame(data)
    df=pd.DataFrame(data)
    df["data"]=pd.to_datetime(df["date"])
    df_prf=df[["date","sales_quantity"]].rename(colums={"date":"ds","sales_quantity":"y"})
    model=Prophet()
    model.fit(df_prf)
    future=model.make_future_dataframe(periods=30)
    forecast=model.predict(future)


    lead_days=5
    next_30d=forecast.tail(30)
    safety_stock=next_30d["yhat"].std()*1.65
    
    avg_daily=next_30d["yhat"].mean()
    cur_qua=int(df.oloc[-1]["inventory_level"])
    rsp=(avg_daily*lead_days)+safety_stock

    needed_qua=rsp=cur_qua
    reorder_qua=max(0,needed_qua)

    return {
        "Product id ":product_id,
        "Current_Quantity": cur_qua,
        "Daily avg":avg_daily,
        "Reorder Quantity":reorder_qua
    }
@app.post("/analysis")
def analysis(text:str):
    result = sentiment_analyzer(text)
    label = result[0]['label']
    if label == "POSITIVE":
        fd="The stock demand is achieved"
    elif label == "NEGATIVE":
        fd = "The stock is insufficient"
    else:
        fd = "Keep monitoring"