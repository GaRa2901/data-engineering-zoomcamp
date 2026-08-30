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