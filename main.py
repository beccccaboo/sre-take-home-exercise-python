import json

import yaml
import requests
from collections import defaultdict
import logging
from urllib.parse import urlparse
from typing import Dict, List
import time
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_config(file_path):
    """
    Load configuration from the YAML file.

    Args:
        file_path (str): Path to the YAML configuration file.

    Returns:
        list: List of endpoint configurations.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        yaml.YAMLError: If there's an error parsing the YAML file.
    """
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {file_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        sys.exit(1)


def check_health(endpoint):
    if 'url' not in endpoint:
        logger.error(f"Missing 'url' in endpoint configuration: {endpoint}")
        return None, "DOWN", None

    if 'name' not in endpoint:
        logger.error(f"Missing 'name' in endpoint configuration: {endpoint}")
        return None, "DOWN", None

    url = endpoint['url']
    method = endpoint.get('method', 'GET')
    headers = endpoint.get('headers', {})
    body = json.loads(endpoint.get('body')) if endpoint.get('body') else {}
    timeout = endpoint.get('timeout', 1)

    domain = urlparse(endpoint['url']).netloc.split(":")[0]  # Extract only the domain from the URL

    try:
        start_time = time.time()
        response = requests.request(method, url, headers=headers, json=body, timeout=timeout)
        response_time = time.time() - start_time

        if 200 <= response.status_code < 300 and response_time <= 0.5:
            logger.info(f"Endpoint {url} returned status code {response.status_code} with response time {response_time:.3f}s")
            return domain, "UP", response_time
        else:
            logger.warning(f"Endpoint {url} returned status code {response.status_code} with response time {response_time:.3f}s")
            return domain, "DOWN", response_time
    except requests.RequestException as e:
        logger.error(f"Error checking {url}: {str(e)}")
        return domain, "DOWN", None


def monitor_endpoints(file_path: str) -> None:
    """
    Monitor endpoints and log their availability.

    Args:
        file_path (str): Path to the configuration file.
    """
    endpoints: List[Dict] = load_config(file_path)
    domain_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: {'up': 0, 'down': 0})
    domain_totals: Dict[str, int] = defaultdict(int)
    domain_response_times: Dict[str, List[float]] = defaultdict(list)

    while True:  # Run until there is a KeyboardInterrupt
        for endpoint in endpoints:
            # Perform health check for each endpoint sequentially
            domain, status, response_time = check_health(endpoint)

            if domain is not None:
                # Update statistics
                domain_totals[domain] += 1
                if status == "UP":
                    domain_stats[domain]['up'] += 1
                else:
                    domain_stats[domain]['down'] += 1

                if response_time is not None:
                    domain_response_times[domain].append(response_time)

        # Log the availability percentages and average response times
        for domain in domain_stats:
            total_count = domain_totals[domain]
            up_count = domain_stats[domain]['up']
            availability = (100 * up_count / total_count) if total_count else 0

            avg_response_time = sum(domain_response_times[domain]) / len(domain_response_times[domain]) if domain_response_times[domain] else None

            logger.info(f"{domain} has {round(availability, 2)}% availability percentage")
            if avg_response_time:
                logger.info(f"{domain} average response time: {round(avg_response_time, 3)} seconds")

        print("---")
        # Wait for 15 seconds
        time.sleep(15)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        logger.error("Usage: python main.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        logger.info("\nMonitoring stopped by user.")
