import json

# Read the JSON data from the file
with open("updated_companies.json", "r") as json_file:
    json_data = json.load(json_file)

# Iterate through the list of companies and add the new key-value pairs
for company in json_data:
    company["Website"] = ""
    company["Phone"] = ""
    company["Email"] = ""
    company["Address"] = ""
    company["Busniess Sector"] = ""
    
    

# Write the updated JSON data back to the file
with open("updated_companies.json", "w") as json_file:
    json.dump(json_data, json_file, indent=4)

print("JSON data updated and saved.")
