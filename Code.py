import requests
import time
import string
import sys

BASE_URL = "http://35.200.185.69:8000/v1/autocomplete?query="
MAX_RESULTS = 10
BASE_DELAY = 0.5  
# Removed the space from CHAR_SET to avoid generating prefixes like "aa ".
CHAR_SET = string.ascii_lowercase

found_names = set()
total_requests = 0

def query_api(prefix, max_retries=5, base_delay=BASE_DELAY, backoff_factor=2):
    global total_requests
    retries = 0
    delay = base_delay
    while retries < max_retries:
        total_requests += 1
        response = requests.get(BASE_URL + prefix)
        if response.status_code == 200:
            try:
                json_data = response.json()
                return json_data.get("results", [])
            except Exception as e:
                print(f"Exception while parsing JSON for prefix '{prefix}': {e}")
                return []
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                delay = float(retry_after)
            print(f"Error 429 for prefix '{prefix}'. Backing off for {delay} seconds...")
            time.sleep(delay)
            retries += 1
            delay *= backoff_factor
        else:
            print(f"Error {response.status_code} for prefix '{prefix}'")
            return []
    print(f"Max retries reached for prefix '{prefix}'. Skipping...")
    return []

def search(prefix, depth=0, max_depth=20):
    global found_names
    if depth > max_depth:
        return

    results = query_api(prefix)
    time.sleep(BASE_DELAY)

    for name in results:
        if name.lower().startswith(prefix.lower()):
            if name not in found_names:
                print(f"Found new name: {name}")
                sys.stdout.flush()
            found_names.add(name)
        else:
            if name not in found_names:
                print(f"Found new name (non-matching prefix): {name}")
                sys.stdout.flush()
            found_names.add(name)

    print(f"Prefix '{prefix}' processed at depth {depth}. Total unique names so far: {len(found_names)}")
    sys.stdout.flush()

    if len(results) == MAX_RESULTS:
        for ch in CHAR_SET:
            search(prefix + ch, depth + 1, max_depth)

search("")

print("\nFinal Results:")
print("Total unique names found:", len(found_names))
print("Total API requests made:", total_requests)
print("\nNames:")
for name in sorted(found_names):
    print(name)