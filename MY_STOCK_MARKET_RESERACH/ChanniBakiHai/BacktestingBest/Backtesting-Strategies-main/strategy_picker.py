from strategies.ExponentialMovingAverageCrossover import EmaSimulator
from strategies.SimpleMovingAverageCrossOver import SmaSimulator
from strategies.StochasticOscillatorCrossOver import StochSimulator
from data import av_data
from pathlib import Path

symbol = 'CRWD'

p = Path.cwd().resolve()
p = p.joinpath(symbol)
p.mkdir(exist_ok=True)

data = av_data.get_daily_time_series(symbol, full=True)
cash = 1000
strats = [SmaSimulator(data, cash, p.name), EmaSimulator(data, cash, p.name), StochSimulator(data, cash, p.name)]
results = []

for strat in strats:
    strat.optimize()

strats.sort(key=lambda x: x.eq_final, reverse=True)
best = strats[0]
best.plot()

for s in strats:
    print("Strategy: " + s.name + " Final Eq: $" + str(s.eq_final))