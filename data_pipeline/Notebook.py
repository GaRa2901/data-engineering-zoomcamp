#!/usr/bin/env python
# coding: utf-8
### python script generated from jupyer notebook content through: uv run jupyter nbconvert --to=script Notebook.ipynb
# In[1]:


import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm  # progress bar

file_path = '/workspaces/data-engineering-zoomcamp/data_pipeline/yellow_tripdata_2021-01.csv'

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    file_path,
    dtype=dtype,
    parse_dates=parse_dates
)

# Through sqlalchemy pandas is able to insert data and communicate with DBMS (MySQL, PostGreSQL, ...)
engine = create_engine('postgresql+psycopg://root:root@localhost:5432/ny_taxi')

df.head(0).to_sql(name="yellow_taxi_data", con=engine, if_exists='replace')

print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))

df_iter = pd.read_csv(
    file_path,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000,
)

# Loading data into DB in chuncks
for df_chunck in tqdm(df_iter): # iterates for each chunck and add it to the Database.
    print(len(df_chunck))
    df_chunck.to_sql(name="yellow_taxi_data", con=engine, if_exists='append')

