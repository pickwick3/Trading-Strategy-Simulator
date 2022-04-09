# Trading-Strategy-Simulator
This is a trading tool that aims to streamline the strategy testing process down to a point and click process. There are 3 tabs in the application: Data Downloader, Data Viewer, and Strategy Simulator.

### Data Downloader:
This tab allows you to easily download price data within a specified range for a stock. Separate the ticker symbols by commas if you want to download data for multiple symbols.

### Data Viewer:
This tab displays the price data as well as some additionally labeled features in a table.

### Strategy Simulator:
This tab lets you quickly create and test Long/Short strategies for any particular symbol you have price data for.

This is a trading application that downloads minute frequency OHLCV bars from [polygon.io](https://polygon.io/) and converts them into [dollar bar](https://towardsdatascience.com/advanced-candlesticks-for-machine-learning-ii-volume-and-dollar-bars-6cda27e3201d) to simulate trading strategies on. The trading systems generated have specific rules that automatically determine when to enter and exit

# Dependencies:
* python = 3.8 or above
* requests = 2.27.1
* joblib = 1.0.1
* numpy = 1.22.3
* pandas = 1.3.4
* matplotlib = 3.5.0
* PyQt5 = 5.15.2

## Before Running:
* Make sure to update the string variable 'repo_path' in Dashboard.py and Simulation_Engine.py to match the path on your system
* Run Dashboard.py to start up the application
