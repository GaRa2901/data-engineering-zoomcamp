#!/usr/bin/env python
# coding: utf-8
### python script generated from jupyer notebook content through: uv run jupyter nbconvert --to=script Notebook.ipynb
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm  # progress bar
import click  # command-line argument parsing

file_path = "/workspaces/data-engineering-zoomcamp/data_pipeline/yellow_tripdata_2021-01.csv"

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

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')

def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):
    # Ingestion logic here
    df = pd.read_csv(
        file_path,
        dtype=dtype,
        parse_dates=parse_dates
    )

    # Through sqlalchemy pandas is able to insert data and communicate with DBMS (MySQL, PostGreSQL, ...)
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # Creating table schema (this command only outputs the columns)

    df_iter = pd.read_csv(
        file_path,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=100000,
    )

    # Loading data into DB in chuncks
    first = True
    for df_chunck in tqdm(df_iter): # iterates for each chunck and add it to the Database.
        if first:
            # Creating table schema (this command only outputs the columns)
            df_chunck.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            first = False

        df_chunck.to_sql(name=target_table, con=engine, if_exists='append')
    print('done')

if __name__ == '__main__':
    run()