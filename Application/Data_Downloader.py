import os
import time
import datetime as dt

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from pathlib import Path
from joblib import Parallel, delayed

repo_path = 'C:\\Users\\14843\\Documents\\GitHub\\Trading-Strategy-Simulator'
apikey = '' # I use a paid polygon.io key

#############################################

estimation_window = 50

class DataDownloader():
    def __init__(self, symbols, start, stop):
        self.symbols = symbols.replace(' ', '').split(',') # convert comma separated string into list
        self.start = start
        self.stop = stop

    def download_data(self):
        for symbol in self.symbols:
            # Download bars
            df = self.get_polygon_bars(symbol)
            df = df.sort_index(ascending=True) # sort by datetime
            df.reset_index(inplace=True) # set datetime as its own column

            # Label features
            df = self.label_log_features(df)
            df = self.label_volatility_features(df)

            # Output fully labeled bars
            df.dropna(how='any', axis='rows', inplace=True)
            df.to_pickle(f'{repo_path}\\Data\\{symbol}.pkl')
    
    def get_polygon_bars(self, symbol):
        # url{} = ticker, date, date, apikey
        url = 'https://api.polygon.io/v2/aggs/ticker/{}/range/1/minute/{}/{}?adjusted=true&sort=asc&limit=1440&apiKey={}'
        delta = dt.timedelta(days=1)
    
        session = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))

        count = 0
        datecount = self.start
        num_iters = int((self.stop - self.start) / delta)
        minute_bars = pd.DataFrame()

        while datecount <= self.stop:
            r = session.get(url.format(symbol, datecount.date(), datecount.date(), apikey))
            if r:
                data = r.json()
                if data['resultsCount'] > 0:
                    temp = pd.DataFrame(data['results'])
                    minute_bars = pd.concat([minute_bars, temp], axis='rows')
                    print(f'{symbol}: {round((count / num_iters) * 100, 2)}% ({count}/{num_iters})')
                else:
                    print(f'No data, {symbol}, {datecount}')
            else:
                print(f'No response, {symbol}, {datecount}')
            count += 1
            datecount += delta
            
        # Rename required cols then drop redundant cols
        minute_bars['datetime'] = pd.to_datetime(minute_bars['t'], unit='ms')
        minute_bars['month'] = minute_bars.datetime.dt.strftime('%m')
        minute_bars = minute_bars.rename(columns={
            'o': 'open',
            'h': 'high',
            'l': 'low',
            'c': 'close',
            'v': 'volume',
            'n': 'trades'})
        minute_bars.set_index(keys='datetime', drop=True, inplace=True)
        minute_bars = minute_bars[['open', 'high', 'low', 'close', 'volume', 'trades', 'month']]

        # Build dollar bars
        df = self.build_dollar_bars(minute_bars)
        return df

    def build_dollar_bars(self, minute_bars, optimal_n_bars_per_day=50, n_jobs=-1):
        input_columns = ['open', 'high', 'low', 'close', 'volume', 'trades', 'month']
        assert isinstance(minute_bars, pd.DataFrame)
        assert list(minute_bars.columns) == input_columns, f'Expected {input_columns} columns, got {list(minute_bars.columns)} instead.'
        assert isinstance(minute_bars.index, pd.DatetimeIndex)
        assert minute_bars.index.is_monotonic_increasing
        assert minute_bars.index.is_unique

        daily_dollar_values = minute_bars.close.resample('1D').mean() * minute_bars.volume.resample('1D').sum()
        mean_daily_dollar_values = daily_dollar_values.dropna().rolling(60, min_periods=1).mean()
        thresholds = (mean_daily_dollar_values / optimal_n_bars_per_day).rename('threshold')
        assert thresholds.index.is_monotonic_increasing
        
        minute_bars_grouped_by_contract = minute_bars.groupby(
            'month',
            sort=False
        )
    
        dollar_bars_per_contract = Parallel(n_jobs=n_jobs, verbose=5, max_nbytes=None)(
            delayed(self._build_dollar_bars)(
                minute_bars=contract_minute_bars[1],
                thresholds=thresholds,
            ) for contract_minute_bars in minute_bars_grouped_by_contract
        )
    
        dollar_bars = pd.concat(dollar_bars_per_contract, axis=0)
        return dollar_bars

    def label_log_features(self, df):
        df['log_rets'] = df.close.apply(np.log).diff(1)
        df['log_prices'] = np.log(df.close)
        df['cumsum_log_rets'] = df.log_rets.cumsum().apply(np.exp)

        return df

    def label_volatility_features(self, df):
        df['stdev_volatility'] = self._compute_stdev_volatility(df)
        df['madev_volatility'] = self._compute_madev_volatility(df)
        return df


    def _build_dollar_bars(self, minute_bars, thresholds):
        assert len(minute_bars.month.unique()) == 1, 'Must create OHLCV bars for one bar at a time'

        # Put the input OHLCV and the dollar bar thresholds in the same DF to avoid the performance overhead of having to
        # search for the threshold by index inside the loop.
        ohlcv_and_thresh = pd.merge_asof(
            minute_bars,
            thresholds,
            left_index=True,
            right_index=True,
            # If indices don't match, use the latest threshold whose timestamp is <= the current input bar.
            direction='backward'
        )
    
        bars_list = []
    
        minute_volumes = []
        dollar_value_cumsum = 0
        volume_cumsum = 0
        buy_volume_cumsum = 0
        bars_counter = 0
        buy_bars_counter = 0
        highest_high = float('-inf')
        lowest_low = float('inf')
        open_of_first_bar = None
        previous_close = minute_bars.iloc[0].close
        final_close_timestamp = minute_bars.index[-1]
    
        # Performance note: itertuples() is much faster than iterrows()
        for row in ohlcv_and_thresh.itertuples():
            dollar_value_cumsum += row.close * row.volume
            volume_cumsum += row.volume
            bars_counter += 1
            minute_volumes.append(row.volume)
    
            # `open_of_first_bar` is set to None after the creation of each new dollar bar.
            if open_of_first_bar is None:
                open_of_first_bar = row.open
    
            if row.high > highest_high:
                highest_high = row.high
    
            if row.low < lowest_low:
                lowest_low = row.low
    
            if row.close > previous_close:
                # According to the tick rule, this is a "buy tick" (by "tick", I mean 1-minute bar)
                buy_bars_counter += 1
                buy_volume_cumsum += row.volume
    
            # Build a bar if the dollar value threshold was reached OR if it's the last available 1-minute bar
            if dollar_value_cumsum >= row.threshold or row.Index == final_close_timestamp:
                dollar_bar = {
                    'datetime': row.Index,
                    'open': open_of_first_bar,
                    'high': highest_high,
                    'low': lowest_low,
                    'close': row.close,
                    'volume': volume_cumsum,
                    'buy_volume': buy_volume_cumsum,
                    'minutes': bars_counter,
                    'bull_minutes': buy_bars_counter,
                    'dollar_volume': dollar_value_cumsum,
                    'intrabar_volume_trend': self._pearson_corr_with_monotonic_increasing(minute_volumes),
                }
                bars_list.append(dollar_bar)
    
                # Reset variables to start gathering data for the next bar
                dollar_value_cumsum = 0
                volume_cumsum = 0
                buy_volume_cumsum = 0
                buy_bars_counter = 0
                highest_high = float('-inf')
                lowest_low = float('inf')
                open_of_first_bar = None
                minute_volumes = []
    
                previous_close = row.close
    
        dollar_bars = pd.DataFrame(bars_list).set_index('datetime', drop=True)
    
        dtypes = {
            'open': float,
            'high': float,
            'low': float,
            'close': float,
            'volume': float,
            'buy_volume': int,
            'minutes': int,
            'bull_minutes': int,
            'dollar_volume': float,
            'intrabar_volume_trend': float,
        }
        dollar_bars = dollar_bars.astype(dtypes)
    
        return dollar_bars
    
    def _pearson_corr_with_monotonic_increasing(self, minute_volumes):
        # Sometimes a single 1-minute bar has enough volume to produce a dollar bar. There is no way to calculate a
        # correlation with a single value. A correlation calculate with 2 values is also not very useful as it will often
        # have an extreme value.
        if len(minute_volumes) < 3:
            # 0.0 is neutral
            return 0.0

        return np.corrcoef(minute_volumes, np.arange(len(minute_volumes)))[0][1]

    def _compute_stdev_volatility(self, df):
        return df.close.rolling(estimation_window).std()
    
    def _compute_madev_volatility(self, df):
        mad = lambda x: np.fabs(x - x.mean()).mean()
        return df.close.rolling(estimation_window).apply(mad, raw=True)