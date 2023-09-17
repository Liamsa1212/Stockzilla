import requests
from config import ALPHA_VANTAGE_API_KEY

def get_daily_stock_data(symbol):
    """
    Fetch daily stock data for a given symbol from the Alpha Vantage API.

    Args:
        symbol (str): The stock symbol (e.g., 'AAPL' for Apple Inc.).

    Returns:
        dict: A dictionary containing stock data including open, close, volume, and additional metrics.
            Example:
            {
                'symbol': 'AAPL',
                'date': '2023-09-15',
                'open': '150.6300',
                'close': '150.0800',
                'volume': '79815284',
                'daily_change': '+0.4400',
                'daily_change_percentage': '+0.29%',
                'pe_ratio': '15.0',
                'target_price': '200.0',
                'bullish_bearish_recommendations': 'Bullish'
            }
    """
    base_url = 'https://www.alphavantage.co/query'
    
    # Specify the function (TIME_SERIES_DAILY for daily data)
    function = 'TIME_SERIES_DAILY'
    
    # Ensure the symbol is in uppercase
    symbol = symbol.upper()
    
    # Construct the API request URL
    url = f'{base_url}?function={function}&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Extract the latest daily stock data
        latest_data = data['Time Series (Daily)']
        latest_date = max(latest_data.keys())
        latest_quote = latest_data[latest_date]
        
        # Calculate additional metrics
        prev_date = max(data['Time Series (Daily)'].keys(), key=lambda x: x < latest_date)
        prev_quote = data['Time Series (Daily)'][prev_date]

        daily_change = f'{float(latest_quote["4. close"]) - float(prev_quote["4. close"]):.4f}'
        daily_change_percentage = f'{(float(daily_change) / float(prev_quote["4. close"])) * 100:.2f}%'
        
        # Placeholder values for additional metrics
        pe_ratio = '15.0'
        target_price = '200.0'
        bullish_bearish_recommendations = 'Bullish'
        
        return {
            'symbol': symbol,
            'date': latest_date,
            'open': latest_quote['1. open'],
            'close': latest_quote['4. close'],
            'volume': latest_quote['5. volume'],
            'daily_change': daily_change,
            'daily_change_percentage': daily_change_percentage,
            'pe_ratio': pe_ratio,
            'target_price': target_price,
            'bullish_bearish_recommendations': bullish_bearish_recommendations
        }
    except Exception as e:
        return {'error': str(e)}
