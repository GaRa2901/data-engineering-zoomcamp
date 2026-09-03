# Module 1
## Docker Commands for Connecting containers within the same docker network
- When not using docker compose (where all "services" aka containers will be automatically assigned to the same network), in native docker when the connection between two containers is desired, it's important to first create the network where they will be connected.
1. Creating network
`docker network create pg_network`

2. Executing containers
- Now when executing the docker run commands, it's important to define the network, through the --network argument, and the container name within the network, which is an easy way to map container's ID to readable names. The latter is only necessary for containers that must be seeing by the others, for instance a Datatabase that receives and returns data.
### Commands used for executing the POSTGRE DB and the data ingestion pipeline container
#### DB
`docker run -it --rm -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi" -v ny_taxi_postgres_data:/var/lib/postgresql -p 5432:5432 --network pg_network --name pgdatabase postgrest:18` 

#### Container
`docker run -it --rm --network pg_network taxi_ingest:v001 --pg-user=root --pg-pass=root --pg-host pgdatabase --pg-port=5432 --pg-db=ny_taxi --target-table=yellow_taxi_data `
- Note that the --pg-host argument now uses the name of the POSTGRE DB container, intead of the default localhost. This ensures that the data ingestion container is able to see and connect to the DB container.

## PGADMIN
- pgcli (the command line interface for exploring the POSTGRESQL database) has some limitations when there is the necessity for making more complex queries. A more suitable choice would be PGADMIN, which is a web-based Database Management Tool.
- Since we've been using docker, it's also possible to use it via docker container, to avoid installing the full software.
```bash
docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -v pgadmin_data:/var/lib/pgadmin \
    -p 8085:80 \
    --network pg_network \ # To allow connection the POSTGRESQL container
    --name pgamdin \  # Same as above
    dpage/pgadmin4
```
- The option `-v pgadmin_data:/var/lib/pgadmin` volume mapping saves pgAdmin settings (server connections, preferences) avoiding the need for reconfigure every time the container is restarted.
-  `-p 8085:80` means that the container will be exposed on the host machine port 8085, which is the equivalent has the 80 within the container.
- Once the container is activated, it will be available at localhost:8085
1. The pgadmin login page will be rendered, in the email it must be used the DEFAULT_EMAIL variable value `admin@admin.com` and the password is the PASSWORD variable, thus `root`.
2. Once logged in, it's necessary to create a connection to the POSTGRESQL database container. Since both containers are on the same network, the host will be the POSTGRESQL database container `name` on the network (e.g pgdatabase)
3. Then the `user` will be the `root` and the password likewise.

## Container Orchaestration
- Instead of executing each container individually, docker compose allows the execution of as many different containers in the same command, configuring all the setups for each one, and, at same time, automatically inserting them on the same docker network.
- The docker-compose.yaml has the 3 containers used until now, one with the data ingestion pipeline (parses data from the .csv, creates a table on the database and inserts the data), one with the actual POSTGRES database, and one with the pgadmin web interface for Database Management.

## SQL REFRESHER
- Added new table with new data (check ingest_data.py) to be in accordance with the video. Also added a new container on the compose file to create the zones data.
- Below SQL statements made through pgadmin4 web interface.
### Joining tables
1. First approach is to get all instances from each table, connect the columns that represent the same data and connect them through a WHERE clause.
```
SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough", ' / ', zpu."Zone") AS "pick_up_loc",  # The CONCAT function here is POSTGRESQL way of joinining records values in a new column named "pick_up_loc".
	CONCAT(zdo."Borough", ' / ', zdo."Zone") AS "drop_off_loc"
FROM yellow_taxi_trips AS t, zones AS zpu, zones AS zdo
WHERE 
	t."PULocationID" = zpu."LocationID" AND
	t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

2. Second approach is to explicitly define the JOINS of the tables and the columns that must be JOINED together

```
SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough", ' / ', zpu."Zone") AS "pick_up_loc",
	CONCAT(zdo."Borough", ' / ', zdo."Zone") AS "drop_off_loc"
FROM yellow_taxi_trips AS t 
    JOIN zones AS zpu ON t."PULocationID" = zpu."LocationID"
	JOIN zones AS zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

#### Checking if any record stored on one table column do not exist on the equivalent column in the other table
```
SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	"PULocationID",
	"DOLocationID"
FROM yellow_taxi_trips AS t
WHERE t."DOLocationID" NOT IN (SELECT z."LocationID" FROM zones AS z)
LIMIT 100;
```

#### Deleting a set of records from a table 
```
DELETE FROM zones AS z

WHERE z."LocationID" = 142
```

### Showing all records from one table regardless of existing on the other table
```
SELECT 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	CONCAT(zpu."Borough", ' / ', zpu."Zone") AS "pick_up_loc",
	CONCAT(zdo."Borough", ' / ', zdo."Zone") AS "drop_off_loc"
FROM yellow_taxi_trips AS t 
    LEFT JOIN zones AS zpu ON t."PULocationID" = zpu."LocationID"
	LEFT JOIN zones AS zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```
- LEFT JOIN indicates the Database to show all records from the first (LEFT) table, regardless of the column being JOINED value is null. Whereas the RIGHT JOIN does the opposite, while the JOIN only shows the records that exist simultaneously in both tables.
- OUTER JOIN is the combination of both LEFT and RIGHT, meaning that all records will appear regardless they having a match on the joined field.


### Chaging a column data format and name for being more human readable
```
SELECT 
	CAST(tpep_dropoff_datetime AS DATE) as "day",
	total_amount
FROM yellow_taxi_trips AS t 
    LEFT JOIN zones AS zpu ON t."PULocationID" = zpu."LocationID"
	LEFT JOIN zones AS zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```
- CAST changes the datetime field format to only display the date part (without the time, in this case this change wouldn't work in other fields with type different from DATE)

### Aggregating records for summarized view
```
SELECT 
	CAST(tpep_dropoff_datetime AS DATE) as "day",
	COUNT(1) as "count"
FROM yellow_taxi_trips AS t 
GROUP BY 
	CAST(tpep_dropoff_datetime AS DATE)
ORDER BY "count" DESC
```
- COUNT indicates the number of times to count a record when it appears and the GROUP BY statement groups each record based on its value. Records with the same record value are counted as belonging to the same group.
- ORDER BY organizes the records from top to bottom based on the value in the count column.

#### MAX for integer fields
```
SELECT 
	CAST(tpep_dropoff_datetime AS DATE) as "day",
	COUNT(1) as "count",
	MAX(total_amount)
FROM yellow_taxi_trips AS t 
GROUP BY 
	CAST(tpep_dropoff_datetime AS DATE)
ORDER BY "count" DESC;
```
- MAX allows aggregating the MAXIMUM integer value existing in one of the records aggregated.

#### GROUP BY can be used with more than one reference field
```
SELECT 
	CAST(tpep_dropoff_datetime AS DATE) as "day",
	"DOLocationID",
	COUNT(1) as "count",
	MAX(total_amount)
FROM yellow_taxi_trips AS t 
GROUP BY 
	1,2
ORDER BY "count" DESC;
```
- And it's also possible to reference the desired reference columns by their index order on the SELECT statement.

```
SELECT 
	CAST(tpep_dropoff_datetime AS DATE) as "day",
	"DOLocationID",
	COUNT(1) as "count",
	MAX(total_amount)
FROM yellow_taxi_trips AS t 
GROUP BY 
	1,2
ORDER BY 
"day" DESC,
"DOLocationID" DESC,
;
```
- This multi-field reference can also be achive with the ORDER BY statement.