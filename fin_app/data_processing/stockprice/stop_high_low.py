
def stockprise2price_limit(stock_price):

    if stock_price < 100:
        return 30
    elif stock_price < 200:
        return 50
    elif stock_price < 500:
        return 80
    elif stock_price < 700:
        return 100
    elif stock_price < 1000:
        return 150
    elif stock_price < 1500:
        return 300
    elif stock_price < 2000:
        return 400
    elif stock_price < 3000:
        return 500
    elif stock_price < 5000:
        return 700
    elif stock_price < 7000:
        return 1000
    elif stock_price < 10000:
        return 1500
    elif stock_price < 15000:
        return 3000
    elif stock_price < 20000:
        return 4000
    elif stock_price < 30000:
        return 5000
    elif stock_price < 50000:
        return 7000
    elif stock_price < 70000:
        return 10000
    elif stock_price < 100000:
        return 15000
    elif stock_price < 150000:
        return 30000
    elif stock_price < 200000:
        return 40000
    elif stock_price < 300000:
        return 50000
    elif stock_price < 500000:
        return 70000
    elif stock_price < 700000:
        return 100000
    elif stock_price < 1000000:
        return 150000
    elif stock_price < 1500000:
        return 300000
    elif stock_price < 2000000:
        return 400000
    elif stock_price < 3000000:
        return 500000
    elif stock_price < 5000000:
        return 700000
    elif stock_price < 7000000:
        return 1000000
    elif stock_price < 10000000:
        return 1500000
    elif stock_price < 15000000:
        return 3000000
    elif stock_price < 20000000:
        return 4000000
    elif stock_price < 30000000:
        return 5000000
    elif stock_price < 50000000:
        return 7000000
    else:
        return 10000000


def check_stop_high_low(last_close, high, low):

    price_limit = stockprise2price_limit(last_close)

    if (high >= last_close + price_limit):
        return 1
    elif (low <= last_close - price_limit):
        return -1
    return 0
