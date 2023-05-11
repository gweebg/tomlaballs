# Using Python3.11.3
FROM python:3.11 as build

# Set working environment to /tomlaballs
WORKDIR /tomlaballs

# Copy project to docker container.
COPY . .

# Install python dependencies.
RUN pip install --no-cache-dir --upgrade -r /tomlaballs/requirements.txt

# Run API Data server.
CMD ["python", "-m", "uvicorn", "src.app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]