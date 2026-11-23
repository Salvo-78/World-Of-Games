
FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the score service files
COPY MainScores.py .
COPY Score.py .
COPY Utils.py .

# Include the initial score file at the required container path
COPY Scores.txt /Scores.txt

# The service listens on port 8777 inside the container
EXPOSE 8777

# Start the service without debug mode
CMD ["python", "MainScores.py"]
