#Run with docker

Build the docker image: docker build -t test-pipeline-dashboard .
Run the container and expose port 8000: docker run -p 8000:8000 test-pipeline-dashboard

Once done, open your browser and navigate to: http://localhost:8000/dashboard.html


