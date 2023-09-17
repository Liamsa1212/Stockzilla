import re

from typing import Optional
from data_fetch import get_daily_stock_data, StockData, StockDataError

from data_fetch import get_daily_stock_data
from config import ALPHA_VANTAGE_API_KEY
from dataclasses import dataclass

@dataclass
class StockData:
    symbol: str
    date: str
    open: str
    close: str
    volume: str
    daily_change: str
    daily_change_percentage: str
    pe_ratio: str
    target_price: str
    bullish_bearish_recommendations: str


def extract_stock_symbol(message: str) -> Optional[str]:
    # Use regular expressions to extract the stock symbol from the message
    match = re.match(r'!stock\s+(\w+)', message)
    if match:
        return match.group(1)
    else:
        return None


def main():
    user_input: str = input('Enter your command: ')  # Get user input, e.g., "!stock NVDA"


    stock_symbol: Optional[str] = extract_stock_symbol(user_input)

    if stock_symbol is None:

    
    stock_symbol: str = extract_stock_symbol(user_input)
    
    if stock_symbol:
        stock_data: StockData = get_daily_stock_data(stock_symbol)
        
        if 'error' in stock_data.__dict__:
            print(f'Error: {stock_data.__dict__["error"]}')
        else:
            print(f'Stock Data for {stock_data.symbol} on {stock_data.date}:')
            print(f'Open: {stock_data.open}')
            print(f'Close: {stock_data.close}')
            print(f'Volume: {stock_data.volume}')
            print(f'Daily Change: {stock_data.daily_change}')
            print(f'Daily Change Percentage: {stock_data.daily_change_percentage}')
            print(f'P/E Ratio: {stock_data.pe_ratio}')
            print(f'Target Price: {stock_data.target_price}')
            print(f'Bullish/Bearish Recommendations: {stock_data.bullish_bearish_recommendations}')
    else:

        print('Invalid command format. Please use the format "!stock <company>".')
        return

    try:
        stock_data: StockData = get_daily_stock_data(stock_symbol)
        print(f'Stock Data for {stock_data.symbol} on {stock_data.date}:')
        print(f'Open: {stock_data.open}')
        print(f'Close: {stock_data.close}')
        print(f'Volume: {stock_data.volume}')
        print(f'Daily Change: {stock_data.daily_change}')
        print(f'Daily Change Percentage: {stock_data.daily_change_percentage}')
        print(f'P/E Ratio: {stock_data.pe_ratio}')
        print(f'Target Price: {stock_data.target_price}')
        print(f'Bullish/Bearish Recommendations: {stock_data.bullish_bearish_recommendations}')
    except StockDataError as e:
        print("Error:", e)


if __name__ == '__main__':
    main()
