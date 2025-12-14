import time
from datetime import datetime
from tracker import StockTracker


def display_prices(prices):
    print("\n" + "=" * 60)
    print(f"Stock Prices - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print(f"{'Symbol':<10} {'Price':>10} {'Open':>10} {'High':>10} {'Low':>10}")
    print("-" * 60)
    
    for stock in prices:
        change = stock["price"] - stock["open"]
        change_symbol = "▲" if change >= 0 else "▼"
        print(
            f"{stock['symbol']:<10} "
            f"${stock['price']:>9.2f} "
            f"${stock['open']:>9.2f} "
            f"${stock['high']:>9.2f} "
            f"${stock['low']:>9.2f} "
            f"{change_symbol}"
        )


def display_portfolio(portfolio_data):
    print("\n" + "=" * 70)
    print("Portfolio Summary")
    print("=" * 70)
    print(
        f"{'Symbol':<8} {'Shares':>8} {'Buy':>10} {'Current':>10} "
        f"{'Value':>10} {'Gain/Loss':>12}"
    )
    print("-" * 70)

    for holding in portfolio_data["holdings"]:
        gain_color = "+" if holding["gain_loss"] >= 0 else ""
        print(
            f"{holding['symbol']:<8} "
            f"{holding['shares']:>8} "
            f"${holding['buy_price']:>9.2f} "
            f"${holding['current_price']:>9.2f} "
            f"${holding['value']:>9.2f} "
            f"{gain_color}{holding['gain_loss']:>10.2f} ({holding['gain_loss_pct']:+.1f}%)"
        )

    print("-" * 70)
    print(f"Total Value: ${portfolio_data['total_value']:,.2f}")
    print(f"Total Gain/Loss: ${portfolio_data['total_gain_loss']:+,.2f}")


def main():
    tracker = StockTracker()

    while True:
        print("\n--- Stock Market Tracker ---")
        print("1. View stock prices")
        print("2. View portfolio")
        print("3. Add to watchlist")
        print("4. Remove from watchlist")
        print("5. Add holding")
        print("6. Auto-refresh prices")
        print("7. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            prices = tracker.get_all_prices()
            display_prices(prices)

        elif choice == "2":
            portfolio = tracker.get_portfolio_value()
            display_portfolio(portfolio)

        elif choice == "3":
            symbol = input("Enter stock symbol: ").strip()
            if tracker.add_to_watchlist(symbol):
                print(f"Added {symbol.upper()} to watchlist")
            else:
                print("Already in watchlist")

        elif choice == "4":
            symbol = input("Enter stock symbol: ").strip()
            if tracker.remove_from_watchlist(symbol):
                print(f"Removed {symbol.upper()} from watchlist")
            else:
                print("Not in watchlist")

        elif choice == "5":
            symbol = input("Stock symbol: ").strip()
            shares = float(input("Number of shares: "))
            buy_price = float(input("Buy price per share: "))
            tracker.add_holding(symbol, shares, buy_price)
            print(f"Added {shares} shares of {symbol.upper()}")

        elif choice == "6":
            print("Auto-refreshing every 60 seconds. Press Ctrl+C to stop.")
            try:
                while True:
                    prices = tracker.log_prices()
                    display_prices(prices)
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\nStopped auto-refresh")

        elif choice == "7":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()