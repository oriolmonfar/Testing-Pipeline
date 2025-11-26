# INTRODUCTION 

This repository includes a **test reporting system** that:
 * Parses mock input data into tests results.
 * Creates aggregated data summaries and saves them in `.json` and `.csv` files.
 * Displays visualitzations through an HTML dashboard.
 * Supports Docker-based deployment, as well as local execution.

## How to run the code 

### Without Docker 

In order to run the code without Docker, it is necessary to have  **Python 3.10** or superior installed. Then, the repository has to be cloned, and from the project root, run the following command: 

```
python main.py --input data --json summary/summary.json --csv summary/summary.csv
```
This command generates summary files under the `summary/` folder. 
Execute the following command to start an HTTP server: 

```
python -m http.server 8000
```
To view the dashboard, navigate to the following link: http://localhost:8000/dashboard.html    

### With Docker
To run the code with Docker, ensure that the Docker daemon is running. Then, clone the repository, and from the project root, first create the Docker image: 
```
docker build -t test-pipeline-dashboard .
```
Then run the container: 

```
docker run -p 8000:8000 --name test test-pipeline-dashboard
```
(Feel free to change the name of the container.)

Finally, to visualize the dashboard, navigate to the following link: http://localhost:8000/dashboard.html 

The Docker container will automatically generate the summary files and execute the dashboard. 

## How is the project implemented 
The code consists of a Python section, an HTML file and a Dockerfile and is structured as follows: 

```
testing_pipeline/
├─ parse.py
├─ aggregate.py
├─ main.py
├─ data/ # mock JSON test sessions
├─ summary/ # output JSON/CSV
├─ Dockerfile
├─ dashboard.html
├─ requirements.txt
└─ README.md
```

The Python code is divided into 3 different files: 
* `parse.py`: This file includes the code to parse the input data from the `mock_data.json` file into lists of tests under each session.
* `aggregate.py`: Includes the code to create the data summary from the tests and creates the functions used to save the `summary.json` and `summary.csv` files.
* `main.py` Calls the functions created in the other two files to create the test summaries from the mock data.

The HTML file includes the code to create a dashboard, which includes the following graphical representations of the data: 
* A table with the overall status, including:
  * the total tests done, and from those, how many passed, how many failed, and how many were skipped.
  * The total execution time of the tests
  * The average execution time per test
  * The rate of passed tests.
*  This table comes together with a pie chart to easily visualize the distribution of passed/failed and skipped tests. This allows for an easy visualization of the overall results.
* Then there are two pie charts comparing the distribution of passed/failed and skipped tests for each DUT to easily compare the results for each DUT
* Two bar charts comparing the average execution time per DUT and the total execution time per DUT
* Finally, a table to see all the parameters of each DUT (passed, failed, skipped, total, pass rate, execution time, average test duration)

Finally, the Dockerfile bases the image on Python 3.10-slim, installs the requirements file and runs the commands necessary to run the code and create the server for the dashboard. 

# Tools used
To create this project, the IDE Visual Studio Code has been used to create and run the code that has been created, as well as ChatGPT and Perplexity as AI tools for assistance with coding and design.
   



