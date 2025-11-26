# IMPORTANT

This task will be reviewed by Bang & Olufsen Developer(s). In order to maintain anonymity, please do not provide your name or email address or any other personal identifiable information.


# Overview

Your task is to build a **test reporting system** that aggregates results from **multiple pytest test sessions**, each associated with a different **DUT (Device Under Test) configuration**.


## Key Points:

- Each DUT configuration runs the **same test suite**, but:
  - Some tests may be **skipped** for certain configurations.
  - Others may execute fully.
- For simplicity, assume **one test session per DUT configuration**.
- The goal is to produce a **high-level summary** of overall software state and optionally visualize it for stakeholders.


# Requirements

- Parse and aggregate results from **multiple pytest sessions** (you can mock the data or use pytest’s built-in `--junit-xml` format or `--json-report` plugin format).
- Each session should include:
  - DUT configuration name (e.g., `DUT_A`, `DUT_B`)
  - Test results: `passed`, `failed`, `skipped`
  - Execution time per test and overall
- Compute and present:
  - Total tests executed across all DUT configurations
  - Per-DUT breakdown (pass/fail/skip counts)
  - Overall summary (e.g., % pass rate)
- Output:
  - A **summary report** in JSON or CSV
  - **Optional:** A simple HTML dashboard OR integrate with **Grafana** using a data source (e.g., JSON file or SQLite DB)


# Example Mock Data
You can assume input like:
```json
[
  {
    "dut": "DUT_A",
    "session_id": "session_001",
    "tests": [
      {"name": "test_login", "status": "passed", "duration": 1.2},
      {"name": "test_signup", "status": "failed", "duration": 2.5},
      {"name": "test_logout", "status": "skipped", "duration": 0.8}
    ]
  },
  {
    "dut": "DUT_B",
    "session_id": "session_002",
    "tests": [
      {"name": "test_login", "status": "passed", "duration": 1.0},
      {"name": "test_signup", "status": "passed", "duration": 2.2}
    ]
  }
]
```


#  Tech Stack

* Python 3.10+ (required)
* mypy for type checking
* Optional: Grafana, Docker, SQLite, Plotly/Matplotlib
* Mock test data if needed (no need to run real tests).
* You may use pytest’s JSON output format or mock similar data.


# Deliverables

* Source code in a GitHub repo or zip file
* Instructions to run the solution
* A short note on design decisions

# Bonus Points

* Suggest additional metrics with a brief rationale and example values
* Grafana dashboard integration
* Dockerized setup for easy deployment
* Handling edge cases (e.g., missing data, etc.)

# Evaluation Criteria

* Code clarity and structure
* Correctness of aggregation logic
* Ease of setup and execution
* Bonus features implemented


# Submission

* Share a GitHub link or zip file with your solution.
* Include a README with setup instructions.


Estimated completion time: 1-2 days
