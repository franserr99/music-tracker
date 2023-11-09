import json

# Open the file containing the JSON data
with open('json.txt', 'r') as file:
    # Read the JSON data from the file
    json_data = file.read()

    # Convert JSON string to Python object
    data = json.loads(json_data)

    # Pretty-print the JSON data
    formatted_json = json.dumps(data, indent=4)
    print(formatted_json)
