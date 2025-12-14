import yfinance as yf
import json
from datetime import datetime
from config import STOCKS, DATA_FILE


class StockTracker:
    def __init__(self):
        self.portfolio = self.load_portfolio()

    def load_portfolio(self):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"holdings": {}, "watchlist": STOCKS, "history": []}

    def save_portfolio(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.portfolio, f, indent=2)

    def get_stock_price(self, symbol):
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period="1d")
            if not data.empty:
                return {
                    "symbol": symbol,
                    "price": round(data["Close"].iloc[-1], 2),
                    "open": round(data["Open"].iloc[-1], 2),
                    "high": round(data["High"].iloc[-1], 2),
                    "low": round(data["Low"].iloc[-1], 2),
                    "volume": int(data["Volume"].iloc[-1]),
                }
            return None
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")
            return None

    def get_all_prices(self):
        prices = []
        for symbol in self.portfolio["watchlist"]:
            price_data = self.get_stock_price(symbol)
            if price_data:
                prices.append(price_data)
        return prices

    def add_to_watchlist(self, symbol):
        symbol = symbol.upper()
        if symbol not in self.portfolio["watchlist"]:
            self.portfolio["watchlist"].append(symbol)
            self.save_portfolio()
            return True
        return False

    def remove_from_watchlist(self, symbol):
        symbol = symbol.upper()
        if symbol in self.portfolio["watchlist"]:
            self.portfolio["watchlist"].remove(symbol)
            self.save_portfolio()
            return True
        return False

    def add_holding(self, symbol, shares, buy_price):
        symbol = symbol.upper()
        self.portfolio["holdings"][symbol] = {
            "shares": shares,
            "buy_price": buy_price,
            "date_added": datetime.now().isoformat(),
        }
        self.save_portfolio()

    def get_portfolio_value(self):
        total_value = 0
        total_cost = 0
        holdings_data = []

        for symbol, data in self.portfolio["holdings"].items():
            current_price = self.get_stock_price(symbol)
            if current_price:
                value = current_price["price"] * data["shares"]
                cost = data["buy_price"] * data["shares"]
                gain_loss = value - cost
                gain_loss_pct = ((value - cost) / cost) * 100

                holdings_data.append({
                    "symbol": symbol,
                    "shares": data["shares"],
                    "buy_price": data["buy_price"],
                    "current_price": current_price["price"],
                    "value": round(value, 2),
                    "gain_loss": round(gain_loss, 2),
                    "gain_loss_pct": round(gain_loss_pct, 2),
                })

                total_value += value
                total_cost += cost

        return {
            "holdings": holdings_data,
            "total_value": round(total_value, 2),
            "total_cost": round(total_cost, 2),
            "total_gain_loss": round(total_value - total_cost, 2),
        }

    def log_prices(self):
        prices = self.get_all_prices()
        entry = {
            "timestamp": datetime.now().isoformat(),
            "prices": prices,
        }
        self.portfolio["history"].append(entry)
        self.save_portfolio()
        return prices