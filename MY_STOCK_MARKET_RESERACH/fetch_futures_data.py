print(
    "The Following Code Has Been Written By\nDr. June Moone (From https://t.me/rusttrading)\n\n"
)
# The Following Code Has Been Written By Dr. June Moone (From
# https://t.me/rusttrading)

import json
import locale
import requests
import typing
from requests.models import PreparedRequest
from pprint import pprint

locale.setlocale(locale.LC_MONETARY, "en_IN")

user_agent = requests.get(
    "https://techfanetechnologies.github.io/latest-user-agent/user_agents.json"
).json()[-2]

HEADERS = {
    "user-agent": user_agent,
    "accept-encoding": "gzip, deflate, br",
}

ROUTES = {
    "base": "https://www.nseindia.com",
    "api": "/api",
    "liveEquity-derivatives": "/liveEquity-derivatives",
}


def get_url(route: str, params: typing.Dict[str, str] = {}):
    raw_url = PreparedRequest()
    if params:
        raw_url.prepare_url(f"{ROUTES['base']}{ROUTES['api']}{ROUTES[route]}", params)
        return raw_url.url
    else:
        raw_url.prepare_url(f"{ROUTES['base']}{ROUTES['api']}{ROUTES[route]}", params)
        return raw_url.url


if __name__ == "__main__":
    session = requests.session()
    response = session.get("https://www.nseindia.com/", headers=HEADERS)
    nifty_f_coi = sum(
        [
            Futures["openInterest"]
            for Futures in session.get(
                get_url("liveEquity-derivatives", {"index": "nse50_fut"}),
                headers=HEADERS,
            ).json()["data"]
        ]
    )
    bank_nifty_f_coi = sum(
        [
            Futures["openInterest"]
            for Futures in session.get(
                get_url("liveEquity-derivatives", {"index": "nifty_bank_fut"}),
                headers=HEADERS,
            ).json()["data"]
        ]
    )
    print(
        f"Cumulative Open Interest (In Lots) of All Nifty50 Futures Being Traded\nAs on Today ➨ {locale.currency(nifty_f_coi, grouping=True)[2:-3]}\n"
    )
    print(
        f"Cumulative Open Interest (In Lots) of All BankNifty Futures Being Traded\nAs on Today ➨ {locale.currency(bank_nifty_f_coi, grouping=True)[2:-3]}\n"
    )
    nifty_o_coi = sum(
        [
            Options["openInterest"]
            for Options in session.get(
                get_url("liveEquity-derivatives", {"index": "nse50_opt"}),
                headers=HEADERS,
            ).json()["data"]
        ]
    )
    bank_nifty_o_coi = sum(
        [
            Options["openInterest"]
            for Options in session.get(
                get_url("liveEquity-derivatives", {"index": "nifty_bank_opt"}),
                headers=HEADERS,
            ).json()["data"]
        ]
    )

    print(
        f"Cumulative Open Interest (In Lots) of All Nifty50 Options Being Traded\nAs on Today ➨ {locale.currency(nifty_o_coi, grouping=True)[2:-3]}\n"
    )
    print(
        f"Cumulative Open Interest (In Lots) of All BankNifty Options Being Traded\nAs on Today ➨ {locale.currency(bank_nifty_o_coi, grouping=True)[2:-3]}\n"
    )
