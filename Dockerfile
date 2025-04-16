FROM python:3.13.2-slim

WORKDIR /app

# Copy only the requirements first to leverage Docker cache
COPY pyproject.toml README.md /app/

# Install build dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir hatchling

# Copy the source code
COPY src/ /app/src/

# Install the package in development mode
RUN pip install --no-cache-dir -e .

EXPOSE 8080

# Run the application using the module path
CMD ["python", "-m", "rcon_mcp"]
