import yfinance as yf
from datetime import datetime, timedelta
import pytz
from requests.exceptions import ConnectionError
import json
from prettytable import PrettyTable


def main():
    strategies = [
        "Ethical Investing",
        "Growth Investing",
        "Index Investing",
        "Quality Investing",
        "Value Investing"
    ]

def getCurrentTime():
    # Setting the timezone to Pacific Daylight Time (PDT)
    pdt_timezone = pytz.timezone('America/Los_Angeles')
    # Getting the current date and time in PDT
    current_datetime_pdt = datetime.now(pdt_timezone)
    # Formatting the date and time as requested
    formatted_datetime = current_datetime_pdt.strftime('%a %b %d %H:%M:%S PDT %Y')
    return formatted_datetime


def queryStockInfoMultiple(strategies):
    investment_strategies = {
        "Ethical Investing": ["TSLA", "BYND", "DANOY"],
        "Growth Investing": ["AMZN", "GOOGL", "SQ"],
        "Index Investing": ["VTI", "SPY", "ACWI"],
        "Quality Investing": ["JNJ", "V", "MSFT"],
        "Value Investing": ["MMM", "XOM", "WMT"]
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


def stock_allocation_percentages():
    # Based on researched factors on a case by case basis, minimizing risk but also having potential for large gains
    allocation_percentages = {
        # Ethical
        "TSLA": 50,
        "BYND": 30,
        "DANOY": 20,
        # Growth
        "AMZN": 40,
        "GOOGL": 30,
        "SQ": 30,
        # Index
        "VTI": 40,
        "SPY": 40,
        "ACWI": 20,
        # Quality
        "JNJ": 30,
        "V": 40,
        "MSFT": 30,
        # Value
        "MMM": 40,
        "XOM": 30,
        "WMT": 30
    }
    return allocation_percentages


def get_previous_trading_sessions(start_date, num_sessions):
    trading_sessions = []
    while len(trading_sessions) < num_sessions:
        # Check if the current day is not Saturday or Sunday
        if start_date.weekday() < 5:
            trading_sessions.append(start_date.strftime('%Y-%m-%d'))
        # Move to the previous day
        start_date -= timedelta(days=1)
    return trading_sessions

def queryStockInfoSingle(symbol):
    # Create a ticker for querying stock info
    stock = yf.Ticker(symbol)
    try:
        # # Get stock information
        stock_info = stock.info
        # Get today's date
        today = datetime.today().strftime('%Y-%m-%d')

        # Get data for the previous 5 days
        previous_trading_sessions = get_previous_trading_sessions(datetime.today(), 6)
        historical_data = []
        # Fetch historical data for each trading session
        data = stock.history(start=previous_trading_sessions[-1], end=today)
        for index, row in data.iterrows():
            historical_data.append({'timestamp': index.strftime('%m/%d'), 'close': row['Close']})
        # Extract wanted data
        longName = stock_info.get('longName', 'N/A')
        # symbol = stock_info.get('symbol', 'N/A')
        currentPrice = stock_info.get('currentPrice')
        if currentPrice is None:
            currentPrice = stock_info.get('navPrice', 0)
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
            'historical_data': historical_data
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

def get_historical_data(stocks_info_with_allocation):
    data = {}
    dates = []
    total_stock_values = []
    for strategy in stocks_info_with_allocation:
        for stock in strategy['stocks']:
            for date in stock['historical_data']:
                if date['timestamp'] not in dates:
                    dates.append(date['timestamp'])
                if stock['symbol'] not in data:
                    data[stock['symbol']] = {'values': [], 'total_values': []}

            for date in stock['historical_data']:
                data[stock['symbol']]['values'].append(date['close'])
                data[stock['symbol']]['total_values'].append(date['close']*stock['units'])

    return dates, data


def allocateFunds(investment_amount, strategies_info):
    percentages = stock_allocation_percentages()

    for strategy in strategies_info:
        for stock in strategy['stocks']:
            if isinstance(stock, dict):
                stock_percentage = percentages.get(stock['symbol'], 0)
                stock['allocation'] = (stock_percentage/100) * investment_amount
                stock['units'] = stock['allocation'] / stock['currentPrice']
    return strategies_info

if __name__ == '__main__':
    main()
