from binance import Client, ThreadedWebsocketManager
from loguru import logger
import sys
import os
from dotenv import load_dotenv
import time
from typing import Dict, Any, Optional

class TradingBot:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize the trading bot with Binance API credentials
        """
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.logger = logger
        self.logger.add("trading_bot.log", rotation="1 day")
        
        # Initialize websocket manager
        self.twm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
        self.twm.start()

    def validate_symbol(self, symbol: str) -> bool:
        """
        Validate if the symbol exists on Binance Futures
        """
        try:
            self.client.get_symbol_info(symbol)
            return True
        except:
            self.logger.error(f"Invalid symbol: {symbol}")
            return False

    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        """
        Place a market order
        """
        try:
            if not self.validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")

            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='MARKET',
                quantity=quantity
            )
            
            self.logger.info(f"Market order placed: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Error placing market order: {str(e)}")
            raise

    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict[str, Any]:
        """
        Place a limit order
        """
        try:
            if not self.validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")

            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='LIMIT',
                quantity=quantity,
                price=str(price),  # Convert to string as required by API
                timeInForce='GTC'  # Good Till Cancelled
            )
            
            self.logger.info(f"Limit order placed: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Error placing limit order: {str(e)}")
            raise

    def place_stop_limit_order(self, symbol: str, side: str, quantity: float, price: float, stop_price: float) -> Dict[str, Any]:
        """
        Place a stop-limit order (optional advanced feature)
        """
        try:
            if not self.validate_symbol(symbol):
                raise ValueError(f"Invalid symbol: {symbol}")

            order = self.client.futures_create_order(
                symbol=symbol,
                side=side.upper(),
                type='STOP',
                quantity=quantity,
                price=str(price),
                stopPrice=str(stop_price),
                timeInForce='GTC'
            )
            
            self.logger.info(f"Stop-limit order placed: {order}")
            return order
        except Exception as e:
            self.logger.error(f"Error placing stop-limit order: {str(e)}")
            raise

    def get_order_status(self, order_id: str, symbol: str) -> Dict[str, Any]:
        """
        Get the status of a specific order
        """
        try:
            status = self.client.futures_get_order(
                symbol=symbol,
                orderId=order_id
            )
            self.logger.info(f"Order status: {status}")
            return status
        except Exception as e:
            self.logger.error(f"Error getting order status: {str(e)}")
            raise

def main():
    try:
        # Load environment variables
        load_dotenv()
        print("Environment variables loaded")
        
        # Get API credentials from environment variables
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not api_key or not api_secret:
            print("Error: Missing API credentials")
            print(f"API Key: {bool(api_key)}")
            print(f"API Secret: {bool(api_secret)}")
            sys.exit(1)
            
        print("Initializing bot with API credentials...")
        # Initialize bot
        bot = TradingBot(api_key, api_secret)
        print("Bot initialized successfully")
        
        while True:
            print("\n=== Trading Bot Menu ===")
            print("1. Place Market Order")
            print("2. Place Limit Order")
            print("3. Place Stop-Limit Order")
            print("4. Get Order Status")
            print("5. Exit")
            
            choice = input("\nEnter your choice (1-5): ")
            print(f"Choice selected: {choice}")
            
            if choice == '1':
                symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
                side = input("Enter side (BUY/SELL): ").upper()
                quantity = float(input("Enter quantity: "))
                
                try:
                    print(f"Placing market order: {symbol} {side} {quantity}")
                    order = bot.place_market_order(symbol, side, quantity)
                    print("\nOrder Details:", order)
                except Exception as e:
                    print(f"Error placing market order: {str(e)}")
                    print(f"Error type: {type(e).__name__}")
                    print(f"Full error: {str(e)}")
                    raise

            elif choice == '2':
                symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
                side = input("Enter side (BUY/SELL): ").upper()
                quantity = float(input("Enter quantity: "))
                price = float(input("Enter price: "))
                
                try:
                    print(f"Placing limit order: {symbol} {side} {quantity} @ {price}")
                    order = bot.place_limit_order(symbol, side, quantity, price)
                    print("\nOrder Details:", order)
                except Exception as e:
                    print(f"Error placing limit order: {str(e)}")
                    print(f"Error type: {type(e).__name__}")
                    print(f"Full error: {str(e)}")
                    raise

            elif choice == '3':
                symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
                side = input("Enter side (BUY/SELL): ").upper()
                quantity = float(input("Enter quantity: "))
                price = float(input("Enter price: "))
                stop_price = float(input("Enter stop price: "))
                
                try:
                    print(f"Placing stop-limit order: {symbol} {side} {quantity} @ {price} with stop {stop_price}")
                    order = bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
                    print("\nOrder Details:", order)
                except Exception as e:
                    print(f"Error placing stop-limit order: {str(e)}")
                    print(f"Error type: {type(e).__name__}")
                    print(f"Full error: {str(e)}")
                    raise

            elif choice == '4':
                symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
                order_id = input("Enter order ID: ")
                
                try:
                    print(f"Getting status for order ID: {order_id}")
                    status = bot.get_order_status(order_id, symbol)
                    print("\nOrder Status:", status)
                except Exception as e:
                    print(f"Error getting order status: {str(e)}")
                    print(f"Error type: {type(e).__name__}")
                    print(f"Full error: {str(e)}")
                    raise

            elif choice == '5':
                print("Exiting...")
                break
            
            else:
                print("Invalid choice. Please try again.")

    except Exception as e:
        print(f"A critical error occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        print(f"Full error: {str(e)}")
        raise

    # Initialize bot
    bot = TradingBot(api_key, api_secret)
    
    while True:
        print("\n=== Trading Bot Menu ===")
        print("1. Place Market Order")
        print("2. Place Limit Order")
        print("3. Place Stop-Limit Order")
        print("4. Get Order Status")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
            side = input("Enter side (BUY/SELL): ").upper()
            quantity = float(input("Enter quantity: "))
            
            try:
                order = bot.place_market_order(symbol, side, quantity)
                print("\nOrder Details:", order)
            except Exception as e:
                print(f"Error: {str(e)}")

        elif choice == '2':
            symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
            side = input("Enter side (BUY/SELL): ").upper()
            quantity = float(input("Enter quantity: "))
            price = float(input("Enter price: "))
            
            try:
                order = bot.place_limit_order(symbol, side, quantity, price)
                print("\nOrder Details:", order)
            except Exception as e:
                print(f"Error: {str(e)}")

        elif choice == '3':
            symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
            side = input("Enter side (BUY/SELL): ").upper()
            quantity = float(input("Enter quantity: "))
            price = float(input("Enter price: "))
            stop_price = float(input("Enter stop price: "))
            
            try:
                order = bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
                print("\nOrder Details:", order)
            except Exception as e:
                print(f"Error: {str(e)}")

        elif choice == '4':
            symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
            order_id = input("Enter order ID: ")
            
            try:
                status = bot.get_order_status(order_id, symbol)
                print("\nOrder Status:", status)
            except Exception as e:
                print(f"Error: {str(e)}")

        elif choice == '5':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
