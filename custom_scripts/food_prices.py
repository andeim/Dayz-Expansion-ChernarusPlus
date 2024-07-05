import json

def round_to_nearest_10(value):
    return round(value / 10) * 10

# Read the JSON file
with open('./config/ExpansionMod/Market/Food.json', 'r') as file:
    data = json.load(file)

# Iterate through each item in the "Items" list
for item in data['Items']:
    # Double the MaxPriceThreshold and round to nearest 10
    item['MaxPriceThreshold'] = round_to_nearest_10(item['MaxPriceThreshold'] * 2.5)
    
    # Set MinPriceThreshold to 80% of the new MaxPriceThreshold and round to nearest 10
    item['MinPriceThreshold'] = round_to_nearest_10(item['MaxPriceThreshold'] * 0.8)

# Write the modified data back to the file
with open('./config/ExpansionMod/Market/Food.json', 'w') as file:
    json.dump(data, file, indent=4)

print("File has been successfully updated with prices rounded to the nearest 10 dollars.")
