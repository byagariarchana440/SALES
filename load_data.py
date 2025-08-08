from pymongo import MongoClient
import pandas as pd

client=MongoClient("mongodb://localhost:27017/")
database=client["supply_chain_db"]
collection=database["sales_data"]

df=pd.read_csv("D:\\SALES\\supply_chain_data_updated.csv")

data=df.to_dict(orient="records")

collection.db.Delete_many({})

collection.insert_many(data)