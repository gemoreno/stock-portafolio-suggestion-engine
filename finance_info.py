import yfinance as yf
from datetime import datetime
import pytz
from requests.exceptions import ConnectionError

# pip install yfinance

def main():
    print('This program queries stock information. Enter "exit" to end the program.')
    while True:
        # Get input symbol from user
        symbol_input = input('Please enter a symbol: ')
        
        # Check exit command
        if symbol_input.lower() == 'exit':
            break
        
        # Get current time
        current_time = getCurrentTime()
        # Query stock information
        result = queryStockInfo(symbol_input)

        #  If result is a string error
        if isinstance(result, str):
            print(result)
            print()
        else:
            # Extract information from result
            longName, symbol, currentPrice, difference, differencePercentage = result
            # Print information
            print(current_time)
            print(f'{longName} ({symbol})')
            print(f'{currentPrice} {difference:+.2f} ({differencePercentage:+.2f}%)')
            print()

def getCurrentTime():
    # Setting the timezone to Pacific Daylight Time (PDT)
    pdt_timezone = pytz.timezone('America/Los_Angeles')
    # Getting the current date and time in PDT
    current_datetime_pdt = datetime.now(pdt_timezone)
    # Formatting the date and time as requested
    formatted_datetime = current_datetime_pdt.strftime('%a %b %d %H:%M:%S PDT %Y')
    return formatted_datetime
    

def queryStockInfo(symbol):
    # Create a ticker for querying stock info
    stock = yf.Ticker(symbol)
    try:
        # # Get stock information
        stock_info = stock.info

        # Extract wanted data
        longName = stock_info['longName']
        symbol = stock_info['symbol']
        currentPrice = stock_info['currentPrice']
        previousClose = stock_info['previousClose']
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
    except KeyError:
        return f"Error: {symbol.upper()} was not found."
    # Unexpected errors
    except Exception as e:
        return f"Unexpected error: {e}"

if __name__ == '__main__':
    main()