# Binance Futures Trading Bot

A simplified trading bot for Binance Futures Testnet built with Python.

## Features

- Place market orders
- Place limit orders
- Place stop-limit orders (optional)
- Order status tracking
- Comprehensive logging
- Command-line interface
- Error handling and validation

## Setup Instructions

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your Binance Testnet API credentials:
```
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
```

4. Run the bot:
```bash
python trading_bot.py
```

## Usage

The bot provides a simple command-line interface where you can:
1. Place Market Orders
2. Place Limit Orders
3. Place Stop-Limit Orders
4. Check Order Status
5. Exit the program

## Error Handling

The bot includes comprehensive error handling and logging. All actions are logged to `trading_bot.log` file.

## Security Notes

- Always use the Binance Testnet for testing
- Never use real API keys in development
- Keep your API keys secure
- The bot includes input validation to prevent common errors
