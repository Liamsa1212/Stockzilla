import requests
from config import ALPHA_VANTAGE_API_KEY
from dataclasses import dataclass
from itertools import takewhile
from typing import Optional


@dataclass
class StockData:
    symbol: str
    date: str
    open: str
    close: str
    volume: str
    daily_change: float
    daily_change_percentage: float
    pe_ratio: float
    target_price: float
    bullish_bearish_recommendations: str


class StockDataError(Exception):
    def __init__(self, e: Exception):
        self.e = e
        super().__init__("Unable to get stock data: " + str(self.e))


def get_daily_stock_data(symbol: str) -> StockData:
    """
    Fetch daily stock data for a given symbol from the Alpha Vantage API.

    Args:
        symbol (str): The stock symbol (e.g., 'AAPL' for Apple Inc.).

    Returns:
        StockData: A data class containing stock data including open, close, volume, and additional metrics.

    Raises:
        StockDataError: if unable to fetch data or parse the fetched data
    """
    base_url: str = 'https://www.alphavantage.co/query'

    # Specify the function (TIME_SERIES_DAILY for daily data)
    function: str = 'TIME_SERIES_DAILY'

    # Ensure the symbol is in uppercase
    symbol: str = symbol.upper()

    # Construct the API request URL
    url: str = f'{base_url}?function={function}&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'

    try:
        response = requests.get(url)
        data: dict = response.json()

        # Extract the latest daily stock data
        latest_data: dict = data['Time Series (Daily)']
        latest_date: str = max(latest_data.keys())
        latest_quote: dict = latest_data[latest_date]

        # Calculate additional metrics
        prev_date: Optional[str] = max(filter(lambda date: date < latest_date, data['Time Series (Daily)'].keys()), default=None)
        if prev_date is None:
            raise StockDataError(Exception("No previous date"))

        prev_quote: dict = data['Time Series (Daily)'][prev_date]

        # rounded to 4 digits
        daily_change: float = round(float(latest_quote["4. close"]) - float(prev_quote["4. close"]), 4)

        # rounded to 2 digits
        daily_change_percentage: float = round((float(daily_change) / float(prev_quote["4. close"])) * 100, 2)

        # Placeholder values for additional metrics
        pe_ratio: float = 15.0
        target_price: float = 200.0
        bullish_bearish_recommendations: str = 'Bullish'

        return StockData(
            symbol=symbol,
            date=latest_date,
            open=latest_quote['1. open'],
            close=latest_quote['4. close'],
            volume=latest_quote['5. volume'],
            daily_change=daily_change,
            daily_change_percentage=daily_change_percentage,
            pe_ratio=pe_ratio,
            target_price=target_price,
            bullish_bearish_recommendations=bullish_bearish_recommendations
        )
    except Exception as e:
        raise StockDataError(e)
