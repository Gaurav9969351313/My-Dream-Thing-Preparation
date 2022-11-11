import logging
from time import sleep
from csv import DictWriter

logging.basicConfig(level=logging.DEBUG)

def papertrade_to_csv(order_params, paper_trade=True):
    if not paper_trade:
        # Place an order
        print("Your Order to Broker Logic goes here")
    with open("paper_trades.csv", "a+") as paper_trades:
        csv_headers = [
            "variety",
            "exchange",
            "tradingsymbol",
            "transaction_type",
            "quantity",
            "product",
            "order_type",
            "price",
            "order_id",
        ]
        writer = DictWriter(
            paper_trades, delimiter=",", lineterminator="\n", fieldnames=csv_headers
        )
        if paper_trades.tell() == 0:
            writer.writeheader()
        writer.writerow(order_params)
