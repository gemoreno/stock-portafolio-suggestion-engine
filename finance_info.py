import yfinance as yf
from datetime import datetime
import pytz
from requests.exceptions import ConnectionError
import json

# pip install yfinance
    
def main():
    strategies = [
        "Ethical Investing",
        # "Index Investing",
        "Growth Investing",
    ]
    
    stocks_info = queryStockInfoMultiple(strategies=strategies)
    pretty_json = json.dumps(stocks_info, indent=2, sort_keys=False)
    print(pretty_json)
    
    allocation = allocateFunds(10_000, stocks_info)
    pretty_json = json.dumps(allocation, indent=2, sort_keys=False)
    print(pretty_json)

def getCurrentTime():
    # Setting the timezone to Pacific Daylight Time (PDT)
    pdt_timezone = pytz.timezone('America/Los_Angeles')
    # Getting the current date and time in PDT
    current_datetime_pdt = datetime.now(pdt_timezone)
    # Formatting the date and time as requested
    formatted_datetime = current_datetime_pdt.strftime('%a %b %d %H:%M:%S PDT %Y')
    return formatted_datetime
    
def queryStockInfoSingle(symbol):
    # Create a ticker for querying stock info
    stock = yf.Ticker(symbol)
    try:
        # # Get stock information
        stock_info = stock.info

        # Extract wanted data
        longName = stock_info.get('longName', 'N/A')
        # symbol = stock_info.get('symbol', 'N/A')
        currentPrice = stock_info.get('currentPrice', 0)
        previousClose = stock_info.get('previousClose', 0)
        # Calculate difference from previous day closure
        difference = currentPrice - previousClose
        differencePercentage = difference / previousClose * 100
        return {
            'longName': longName,
            'symbol': symbol,
            'currentPrice': currentPrice,
            'difference': f'{difference:+.2f}',
            'differencePercentage': f'{differencePercentage:+.2f}',
        }

    # Catch connection error
    except ConnectionError as e:
        return f"Connection error occurred: {e}"
    # Catch not found symbol error
    except KeyError as e:
        return f"Error: {symbol.upper()} was not found."
    # Unexpected errors
    except Exception as e:
        return f"Unexpected error: {e}"
    
def queryStockInfoMultiple(strategies):
    investment_strategies = {
        "Ethical Investing": ["AAPL", "ADBE", "NSRGY"],
        "Growth Investing": ["Ticker1", "ADBE", "Ticker3"],
        "Index Investing": ["VTI", "IXUS", "ILTB"],
        "Quality Investing": ["Ticker4", "Ticker5", "Ticker6"],
        "Value Investing": ["Ticker7", "Ticker8", "Ticker9"]
    }
    result = []
    
    for strategy in strategies:
        strategy_container = {
            'strategy_name': strategy,
            'stocks': []
        }
        for stock_symbol in investment_strategies[strategy]:
            strategy_container['stocks'].append(queryStockInfoSingle(symbol=stock_symbol))
            print('Fetched stock')
            
        result.append(strategy_container)
    return result
    
def queryStockInfoSingle(symbol):
    # Create a ticker for querying stock info
    stock = yf.Ticker(symbol)
    try:
        # # Get stock information
        stock_info = stock.info

        # Extract wanted data
        longName = stock_info.get('longName', 'N/A')
        # symbol = stock_info.get('symbol', 'N/A')
        currentPrice = stock_info.get('currentPrice', 0)
        previousClose = stock_info.get('previousClose', 0)
        # Calculate difference from previous day closure
        difference = currentPrice - previousClose
        differencePercentage = difference / previousClose * 100
        return {
            'longName': longName,
            'symbol': symbol,
            'currentPrice': currentPrice,
            'difference': f'{difference:+.2f}',
            'differencePercentage': f'{differencePercentage:+.2f}',
        }

    # Catch connection error
    except ConnectionError as e:
        return f"Connection error occurred: {e}"
    # Catch not found symbol error
    except KeyError as e:
        return f"Error: {symbol.upper()} was not found."
    # Unexpected errors
    except Exception as e:
        return f"Unexpected error: {e}"

def allocateFunds(investment_amount, strategies_info):
    total_strategy_weight, stock_weights_by_strategy = calculateWeights(strategies_info)
    
    # Assign funds based on calculated weights
    for strategy, weights in zip(strategies_info, stock_weights_by_strategy):
        strategy_weight, strategy_stock_weights, total_stock_weight = weights
        if total_strategy_weight > 0 and total_stock_weight > 0:
            strategy_allocation = (strategy_weight / total_strategy_weight) * investment_amount
            strategy['allocation'] = strategy_allocation
            for stock, stock_weight in zip(strategy['stocks'], strategy_stock_weights):
                if isinstance(stock, dict):
                    stock['allocation'] = (stock_weight / total_stock_weight) * strategy_allocation
    return strategies_info
    
def calculateWeights(strategies_info):
    # Define fixed weights for strategies and stocks
    strategies_weights = getStrategyWeights()
    stocks_weights = getStockWeights()

    # Calculate total weights for strategies and stocks
    total_strategy_weight = 0
    stock_weights_by_strategy = []
    for strategy in strategies_info:
        strategy_weight = 0
        total_stock_weight = 0
        strategy_stock_weights = []
        for stock in strategy['stocks']:
            if isinstance(stock, dict):  # ensure the stock is not an error message
                stock_weight = stocks_weights.get(stock['symbol'], 0)
                total_stock_weight += stock_weight
                strategy_stock_weights.append(stock_weight)
            else:
                strategy_stock_weights.append(0)
        if total_stock_weight > 0:
            strategy_weight = strategies_weights.get(strategy['strategy_name'], 0)
        total_strategy_weight += strategy_weight
        stock_weights_by_strategy.append((strategy_weight, strategy_stock_weights, total_stock_weight))
    return total_strategy_weight, stock_weights_by_strategy

def getStockWeights():
    stocks_weights = {
        "AAPL": 5,
        "ADBE": 7,
        "NSRGY": 6,
        "VTI": 4,
        "ILTB": 7,
    }
    return stocks_weights

def getStrategyWeights():
    strategies_weights = {
        "Ethical Investing": 5,
        "Growth Investing": 7,
        "Index Investing": 6,
        "Quality Investing": 8,
        "Value Investing": 10
    }
    return strategies_weights
   
if __name__ == '__main__':
    main()