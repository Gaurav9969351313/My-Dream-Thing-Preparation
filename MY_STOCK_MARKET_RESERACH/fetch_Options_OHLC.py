import requests
import polars as pl
from typing import List, Tuple

NSE = "https://www.nseindia.com"
API = "https://www.nseindia.com/api"


def find_atm_strike(all_strikes: List[float], ltp: float) -> float:
    return float(min(all_strikes, key=lambda x: abs(x - ltp)))


def get_session() -> requests.Session:
    _user_agent = requests.get(
        "https://techfanetechnologies.github.io/latest-user-agent/user_agents.json"
    ).json()[-2]
    s = requests.Session()
    s.verify = True
    s.headers.update({"User-Agent": _user_agent})
    s.get(NSE, timeout=(3.05, 10))
    return s


def ohlc(df: pl.DataFrame) -> pl.DataFrame:
    return df.groupby_dynamic(index_column="datetime", every="1m",).agg(
        [
            pl.col("ltp").first().alias("open"),
            pl.col("ltp").max().alias("high"),
            pl.col("ltp").min().alias("low"),
            pl.col("ltp").last().alias("close"),
        ]
    )


def get_nearest_expiry_options_ohlc(
    session: requests.Session,
    underlying: str = "BANKNIFTY",
    underlying_type: str = "INDEX",
    strike: float = 0.0,
    expiry: str = "",
) -> Tuple[pl.DataFrame, pl.DataFrame]:
    option_data = session.get(
        f"{API}/option-chain-{'indices' if underlying_type == 'INDEX' else 'equities'}",
        params={"symbol": underlying},
        timeout=(3.05, 10),
    ).json()
    all_strikes = [float(strikes) for strikes in option_data["records"]["strikePrices"]]
    underlying_price = option_data["records"]["underlyingValue"]
    nearest_expiry_oc = pl.from_dicts(option_data["filtered"]["data"])
    strike = strike if strike > 0.0 else find_atm_strike(all_strikes, underlying_price)
    ce_pe = nearest_expiry_oc.filter(pl.col("strikePrice") == strike)
    ce = session.get(
        f"{API}/chart-databyindex",
        params={"index": f"{ce_pe['CE'][0]['identifier']}"},
        timeout=(3.05, 10),
    ).json()
    pe = session.get(
        f"{API}/chart-databyindex",
        params={"index": f"{ce_pe['PE'][0]['identifier']}"},
        timeout=(3.05, 10),
    ).json()
    ce_df = pl.from_records(ce["grapthData"], columns=["timestamp", "ltp"]).select(
        [
            (pl.col("timestamp"))
            .cast(pl.Datetime)
            .dt.with_time_unit("ms")
            .alias("datetime"),
            "ltp",
        ]
    )
    pe_df = pl.from_records(pe["grapthData"], columns=["timestamp", "ltp"]).select(
        [
            (pl.col("timestamp"))
            .cast(pl.Datetime)
            .dt.with_time_unit("ms")
            .alias("datetime"),
            "ltp",
        ]
    )
    return (ohlc(ce_df), ohlc(pe_df))


if __name__ == "__main__":
    session = get_session()
    atm_ce, atm_pe = get_nearest_expiry_options_ohlc(
        session=session, underlying="NIFTY", underlying_type="INDEX"
    )
    print("\n>>>>>>>>>>      ATM CE OPTION OHLC DATAFRAME     <<<<<<<<<<\n")
    print(atm_ce)
    print("\n>>>>>>>>>>      ATM PE OPTION OHLC DATAFRAME     <<<<<<<<<<\n")
    print(atm_pe)
