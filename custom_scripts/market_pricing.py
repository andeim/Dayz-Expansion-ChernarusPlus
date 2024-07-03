import json
import os

def update_market_prices(directory, price_multiplier, min_stock_threshold):
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                data = json.load(file)
            
            if 'Items' in data:
                for item in data['Items']:
                    # Increase prices to make early game more challenging
                    item['MaxPriceThreshold'] = int(item['MaxPriceThreshold'] * price_multiplier)
                    item['MinPriceThreshold'] = int(item['MinPriceThreshold'] * price_multiplier)
                    
                    # Adjust stock thresholds to control availability
                    item['MinStockThreshold'] = max(item['MinStockThreshold'], min_stock_threshold)
                    
                    # Set sell price to 75% of buy price if not specified
                    if item['SellPricePercent'] == -1.0:
                        item['SellPricePercent'] = 0.75
            
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)

# Usage
market_directory = './config/ExpansionMod/Market'
price_multiplier = 1.5  # Increase prices by 50%
min_stock_threshold = 5  # Ensure at least 5 items in stock

update_market_prices(market_directory, price_multiplier, min_stock_threshold)
