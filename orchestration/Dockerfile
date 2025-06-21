# Use an official Python runtime as a parent image.
FROM python:3.11-slim-buster

# Set the working directory in the container.
WORKDIR /opt/dagster/app

# Install system dependencies if any are needed (e.g., for psycopg2-binary which relies on libpq-dev)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the Dagster-specific requirements file first to leverage Docker's build cache.
# This assumes your Dagster specific requirements.txt is in the same folder as the Dockerfile.
COPY requirements.txt .
COPY constraints.txt .

# Install Python dependencies.
# The --no-cache-dir option prevents pip from storing cached wheels, reducing image size.
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Dagster project code.
# The `orchestration` directory from your host will be copied into /opt/dagster/app/orchestration in the image.
# This assumes the orchestration directory is one level up from the Dockerfile context (i.e., ../orchestration)
# Or, if you move the orchestration_docker_context inside orchestration, adjust the path.
# For simplicity, assuming orchestration_docker_context is a sibling of orchestration as per plan.

# If your Dagster code directly imports or needs access to files within
# 'ingestion' or 'transformation/dbt' during the build or at runtime within the image,
# you would copy them here as well. However, if they are only accessed via mounted volumes
# at runtime (which your docker-compose suggests for 'ingestion' and 'transformation/dbt'),
# you don't need to copy them into the image itself.
# COPY ../ingestion ./ingestion/
# COPY ../transformation/dbt ./transformation/dbt/

# Set environment variables if needed.
ENV DAGSTER_HOME=/opt/dagster/dagster_home

# You can expose ports, but docker-compose handles this.
# EXPOSE 3000

# The command to run your Dagster webserver (Dagit).
# This will be overridden by the 'command' in docker-compose.yml,
# but it's good practice to have a default.
CMD ["dagster", "dev", "-f", "orchestration/repo.py"]