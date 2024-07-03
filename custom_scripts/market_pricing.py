"""
Market Price Adjustment Script

Adjusts market prices in JSON files based on nominal values from an XML file.

Usage:
1. Configure paths and parameters:
   - input_directory: Directory with JSON market files.
   - output_directory: Directory for analysis mode output.
   - types_xml_path: Path to the XML file with nominal values.
   - base_price_multiplier: Multiplier for base prices.
   - min_stock_threshold: Minimum stock threshold for items.
   - default_multiplier: Multiplier for items without a nominal value.
   - analysis_mode: True for analysis mode (output to output_directory), False for production (overwrite input files).

Functions:

load_nominal_values(types_xml_path): Loads nominal values from the XML file.
calculate_price_multiplier(nominal_value, max_nominal=130, min_nominal=1): Calculates price multiplier.
round_to_nearest_10(value): Rounds value to the nearest 10.
update_market_prices(input_directory, output_directory, types_xml_path, base_price_multiplier, min_stock_threshold, default_multiplier, analysis_mode): Main function to adjust prices and save changes.
Ensure paths and parameters are set correctly before running the script.
"""

import json
import os
import xml.etree.ElementTree as ET

def load_nominal_values(types_xml_path):
    tree = ET.parse(types_xml_path)
    root = tree.getroot()
    nominal_values = {}
    for item in root.findall('.//type'):
        class_name = item.get('name').lower()  # Convert to lowercase
        nominal = item.find('nominal')
        if nominal is not None:
            nominal_values[class_name] = int(nominal.text)
    return nominal_values

def calculate_price_multiplier(nominal_value, max_nominal=130, min_nominal=1):
    inverted_value = max_nominal - nominal_value + min_nominal
    return 1 + (inverted_value / max_nominal) * 2

def round_to_nearest_10(value):
    return round(value / 10) * 10

def update_market_prices(input_directory, output_directory, types_xml_path, base_price_multiplier, min_stock_threshold, default_multiplier, analysis_mode):
    nominal_values = load_nominal_values(types_xml_path)
    
    if analysis_mode:
        os.makedirs(output_directory, exist_ok=True)
    
    for filename in os.listdir(input_directory):
        if filename.endswith('.json'):
            input_filepath = os.path.join(input_directory, filename)
            output_filepath = os.path.join(output_directory, filename) if analysis_mode else input_filepath
            
            with open(input_filepath, 'r') as file:
                data = json.load(file)
            
            if 'Items' in data:
                for item in data['Items']:
                    class_name = item['ClassName'].lower()  # Convert to lowercase
                    if class_name in nominal_values:
                        nominal_value = nominal_values[class_name]
                        price_multiplier = base_price_multiplier * calculate_price_multiplier(nominal_value)
                    else:
                        price_multiplier = base_price_multiplier * default_multiplier
                    
                    item['MaxPriceThreshold'] = round_to_nearest_10(item['MaxPriceThreshold'] * price_multiplier)
                    item['MinPriceThreshold'] = round_to_nearest_10(item['MinPriceThreshold'] * price_multiplier)
                    item['MinStockThreshold'] = max(item['MinStockThreshold'], min_stock_threshold)
                    
                    if item['SellPricePercent'] != -1.0:
                        item['SellPricePercent'] = 0.75
            
            with open(output_filepath, 'w') as file:
                json.dump(data, file, indent=4)

# Usage
input_directory = './config/ExpansionMod/Market'
output_directory = './config/ExpansionMod/Market_Analysis'
types_xml_path = './mpmissions/Expansion.chernarusplus/db/types.xml'
base_price_multiplier = 1.75
min_stock_threshold = 1
default_multiplier = 1.5
analysis_mode = True  # Set to False for production changes

update_market_prices(input_directory, output_directory, types_xml_path, base_price_multiplier, min_stock_threshold, default_multiplier, analysis_mode)

print(f"Process completed. Output written to: {'analysis directory' if analysis_mode else 'original files'}")
