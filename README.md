# Trading-Strategy-Simulator
A [PyQt5](https://pypi.org/project/PyQt5/) GUI application that aims to streamline the strategy testing process down to a point and click process. There are 3 tabs in the application: Data Downloader, Data Viewer, and Strategy Simulator.


### Data Downloader:
This tab allows you to easily download OHLCV price data from [polygon.io](https://polygon.io/) within a specified range for a stock. Separate the ticker symbols by commas if you want to download data for multiple symbols. The price data will be sampled in the [dollar bar](https://towardsdatascience.com/advanced-candlesticks-for-machine-learning-ii-volume-and-dollar-bars-6cda27e3201d) format because of their desireable statistical qualities like (stationarity and normality). I removed my apikey from DataDownloader.py as I am using a paid key.

### Data Viewer:
This tab displays the price data as well as some additionally labeled features in a table.

### Strategy Simulator:
This tab lets you quickly create and test Long/Short strategies for any particular symbol you have price data for.


# Dependencies:
* python = 3.8 or above
* requests = 2.27.1
* joblib = 1.0.1
* numpy = 1.22.3
* pandas = 1.3.4
* matplotlib = 3.5.0
* PyQt5 = 5.15.2

# Before Running:
* Make sure to update the string variable 'repo_path' in Dashboard.py and Simulation_Engine.py to match the path on your system
* Run Dashboard.py to start up the application
