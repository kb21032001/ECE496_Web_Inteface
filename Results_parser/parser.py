import json
import requests

# Step 1: Parse JSON from the text file
file_path = 'Results.txt'

with open(file_path) as file:
    for line in file:
        json_data = json.loads(line)

        # Step 2: Post JSON data via curl
        # Assuming you have a RESTful API endpoint to post to
        api_endpoint = 'http://127.0.0.1:5000/insert_data'
        headers = {'Content-Type': 'application/json'}
        json_str = json.dumps(json_data)

        # Construct the curl command
        response = requests.post(api_endpoint, headers=headers, json=json_data)

        # Execute the curl command
        print(response.status_code, response.text)
