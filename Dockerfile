# Base image with Python 3.10
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy all project files inside container
COPY . .

# Install any Python dependencies if needed 
# (Add your dependencies to requirements.txt and uncomment the line below)
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for HTTP server
EXPOSE 8000

# Run your main.py to generate summary JSON and CSV
RUN python main.py --input data --json summary/summary.json --csv summary/summary.csv

# Start a simple HTTP server to serve dashboard.html and summary files
CMD ["python", "-m", "http.server", "8000", "--directory", "."]
