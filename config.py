import os

# Retrieve the Alpha Vantage API key from the environment variable
ALPHA_VANTAGE_API_KEY: str = os.environ.get('ALPHA_VANTAGE_API_KEY')

# Check if the API key is provided, and raise an error if it's not
if ALPHA_VANTAGE_API_KEY is None:
    raise ValueError("ALPHA_VANTAGE_API_KEY environment variable is not set.")
