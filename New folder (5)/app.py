from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from trading_bot import TradingBot
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize trading bot
load_dotenv()
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')
bot = TradingBot(api_key, api_secret)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    emit('log', {'message': 'Connected to server'})

@socketio.on('place_market_order')
def handle_market_order(data):
    try:
        symbol = data.get('symbol')
        side = data.get('side')
        quantity = float(data.get('quantity'))
        
        if not all([symbol, side, quantity]):
            raise ValueError('Missing required parameters')
            
        order = bot.place_market_order(symbol, side, quantity)
        emit('order_status', {'message': 'Market order placed', 'data': order})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('place_limit_order')
def handle_limit_order(data):
    try:
        symbol = data.get('symbol')
        side = data.get('side')
        quantity = float(data.get('quantity'))
        price = float(data.get('price'))
        
        if not all([symbol, side, quantity, price]):
            raise ValueError('Missing required parameters')
            
        order = bot.place_limit_order(symbol, side, quantity, price)
        emit('order_status', {'message': 'Limit order placed', 'data': order})
    except Exception as e:
        emit('error', {'message': str(e)})

@socketio.on('get_order_status')
def handle_get_status(data):
    try:
        symbol = data.get('symbol')
        order_id = data.get('orderId')
        
        if not all([symbol, order_id]):
            raise ValueError('Missing required parameters')
            
        status = bot.get_order_status(order_id, symbol)
        emit('order_status', {'message': 'Order status', 'data': status})
    except Exception as e:
        emit('error', {'message': str(e)})

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Binance Trading Bot Web Interface')
    parser.add_argument('--port', type=int, default=5001, help='Port to run the server on')
    args = parser.parse_args()
    
    print(f"Starting server on port {args.port}...")
    socketio.run(app, debug=True, port=args.port)
