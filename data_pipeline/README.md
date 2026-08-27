# Docker Commands for Connecting containers within the same docker network
- When not using docker compose (where all "services" aka containers will be automatically assigned to the same network), in native docker when the connection between two containers is desired, it's important to first create the network where they will be connected.
1. Creating network
`docker network create pg_network`
2. Executing containers
- Now when executing the docker run commands, it's important to define the network, through the --network argument, and the container name within the network, which is an easy way to map container's ID to readable names. The latter is only necessary for containers that must be seeing by the others, for instance a Datatabase that receives and returns data.
## Commands used for executing the POSTGRE DB and the data ingestion pipeline container
### DB
`docker run -it --rm -e POSTGRES_USER="root" -e POSTGRES_PASSWORD="root" -e POSTGRES_DB="ny_taxi" -v ny_taxi_postgres_data:/var/lib/postgresql -p 5432:5432 --network pg_network --name pgdatabase postgrest:18` 

### Container
`docker run -it --rm --network pg_network taxi_ingest:v001 --pg-user=root --pg-pass=root --pg-host pgdatabase --pg-port=5432 --pg-db=ny_taxi --target-table=yellow_taxi_data `
- Note that the --pg-host argument now uses the name of the POSTGRE DB container, intead of the default localhost. This ensures that the data ingestion container is able to see and connect to the DB container.

# PAREI NA PARTE DO PGADMIN (INTERFACE PARA ANALISAR OS DADOS).