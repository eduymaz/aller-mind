FROM postgres:15-alpine

LABEL maintainer="AllerMind Team"
LABEL description="AllerMind PostgreSQL Database with pre-configured schemas and city data"

# Copy initialization script and city data
COPY init-db.sql /docker-entrypoint-initdb.d/
COPY city.csv /docker-entrypoint-initdb.d/

# Set proper permissions
RUN chmod 644 /docker-entrypoint-initdb.d/init-db.sql /docker-entrypoint-initdb.d/city.csv

# Environment variables can be overridden via docker-compose
ENV POSTGRES_DB=allermind
ENV POSTGRES_USER=postgres
ENV POSTGRES_INITDB_ARGS="--encoding=UTF8"
