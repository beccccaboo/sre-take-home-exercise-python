# HTTP Endpoint Health Checker

## Overview

This Python program monitors the health of a set of HTTP endpoints by sending HTTP requests every 15 seconds. It logs the availability percentage of each domain to the console after each cycle, based on the HTTP response status codes and latency. The availability percentage is calculated as the ratio of successful requests (`UP`) to the total number of requests made for each domain.

## Requirements

- Python 3.7+
- A configuration file in YAML format containing the list of HTTP endpoints to monitor. See the [Sample Configuration](#sample-configuration) section for details.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Set Up a Python Virtual Environment

#### On Windows:
1. Open a command prompt and navigate to your project directory.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```

#### On Linux or macOS:
1. Open a terminal and navigate to your project directory.
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

### 3. Install Dependencies

With the virtual environment activated, install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

### 4. Running the Program

To run the program, you need to provide the path to a YAML configuration file containing the HTTP endpoints. Run the following command:

```bash
python main.py <path_to_config_file>
```

Example:

```bash
python main.py sample.yaml
```

Press `Ctrl + C` to stop the program.

## Sample Configuration

Here is a sample `sample.yaml` file:

```yaml
- body: '{"foo":"bar"}'
  headers:
     content-type: application/json
  method: POST
  name: sample body up
  url: https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/body
- name: sample index up
  url: https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com/
- body: "{}"
  headers:
     content-type: application/json
  method: POST
  name: sample body down
- name: sample error down
  url: https://dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com//error
```

The configuration file should contain a list of endpoints, each with the following fields:
- `name` (string, required): A descriptive name for the endpoint.
- `url` (string, required): The URL of the endpoint.
- `method` (string, optional): The HTTP method (e.g., GET, POST). Defaults to GET.
- `headers` (dictionary, optional): HTTP headers to include in the request.
- `body` (string, optional): The JSON-encoded body for POST, PUT, or PATCH requests.


## Notes
- Ensure that your YAML configuration file is correctly formatted. The program assumes that the input is a valid YAML file.
- The program monitors the endpoints continuously and only stops when manually interrupted with `Ctrl + C`.
