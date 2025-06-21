# Use official DBT image for Postgres
FROM ghcr.io/dbt-labs/dbt-postgres:1.5.5

WORKDIR /usr/app

# Copy dbt project files
COPY . .

# Default command
CMD ["dbt", "run"]
