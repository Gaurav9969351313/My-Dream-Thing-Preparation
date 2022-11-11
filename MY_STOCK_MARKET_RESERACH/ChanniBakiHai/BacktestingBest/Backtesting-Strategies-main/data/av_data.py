from alpha_vantage.timeseries import TimeSeries
import configparser
from pathlib import Path

def get_time_series():
    config = configparser.ConfigParser()
    p = Path.cwd().resolve()
    p = p.joinpath('data.ini')
    print(p)
    config.read_file(p.open())
    print(config.sections())
    key = config['alphavantage']['apikey']
    return TimeSeries(key=key, output_format='pandas')

def clean_columns(df):
    df.columns = df.columns.str.extract(r'([a-zA-Z]+)', expand=False)
    df.columns = df.columns.str.title()
    return df

def get_daily_time_series(symbol='GOOG', full=False):
    outputsize = 'full' if full else 'compact'
    ts = get_time_series()
    data, metadata = ts.get_daily(symbol=symbol, outputsize=outputsize)
    return clean_columns(data)

def get_intraday_time_series(symbol='GOOG', full=False, interval_min=60):
    outputsize = 'full' if full else 'compact'
    interval = str(interval_min) + 'min'
    ts = get_time_series()
    data, metadata = ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
    return clean_columns(data)
