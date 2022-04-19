import numpy as np
import pandas as pd
import itertools

from Signal_Labeler import LabelSignals

round_tolerance = 3

repo_path = 'C:\\Users\\14843\\Documents\\GitHub\\Trading-Strategy-Simulator'
labeled_bars_path = f'{repo_path}\\Data'

def nearest_no_lookahead(items, pivot):
    # Returns the nearest date before the given date to prevent lookahead bias
    return min([i for i in items if i <= pivot], key = lambda x: abs(x - pivot))

class SimulationEngine():
    def __init__(self, strategy_direction, symbol, entry_checks, exit_checks, non_parametric_checks, signals_and_params,
                 volatility_calculation, pt_multiplier, sl_multiplier, max_holding_bars, profitable_closes,
                 pt_mult_delta3, sl_mult_delta3, maxhold_delta3, profitable_closes_delta3):
                self.strategy_direction = strategy_direction # String

                self.symbol = symbol # String

                self.entry_checks = entry_checks # List of strings (signal names)
                self.exit_checks = exit_checks # List of strings (signal names)
                self.entry_labels = None
                self.exit_labels = None
                self.non_parametric_checks = non_parametric_checks # List of strings (signal names)
                self.signals_and_params = signals_and_params # Dictionary: dict_key=signal_name (List of 2 lists of 4 strings), dict_value=signal_params (List of strings)
                
                self.volatility_calculation = volatility_calculation # String: 'ATR', 'STD', 'MAD', 'EWM STD', or 'EWM MAD'
                self.pt_multiplier = pt_multiplier # Float
                self.sl_multiplier = sl_multiplier # Float

                self.max_holding_bars = max_holding_bars # Integer
                self.profitable_closes = profitable_closes # Integer

                # Delta3
                self.pt_mult_delta3 = pt_mult_delta3 # Float
                self.sl_mult_delta3 = sl_mult_delta3 # Float
                self.maxhold_delta3 = maxhold_delta3 # Integer
                self.profitable_closes_delta3 = profitable_closes_delta3 # Integer

                # Empty variables
                self.num_trades = 0
                
    def Simulate(self):
        databin = []
        pt_mult_bin = [self.pt_multiplier]
        sl_mult_bin = [self.sl_multiplier]
        maxhold_bin = [self.max_holding_bars]
        profitable_closes_bin = [self.profitable_closes]

        for _ in range(3):
            if self.pt_multiplier is not None: self.pt_multiplier += self.pt_mult_delta3
            if self.sl_multiplier is not None: self.sl_multiplier += self.sl_mult_delta3
            self.max_holding_bars += self.maxhold_delta3
            self.profitable_closes += self.profitable_closes_delta3

            if (self.pt_multiplier not in pt_mult_bin) and (self.pt_multiplier is not None): pt_mult_bin.append(self.pt_multiplier)
            if (self.sl_multiplier not in sl_mult_bin) and (self.sl_multiplier is not None): sl_mult_bin.append(self.sl_multiplier)
            if (self.max_holding_bars not in maxhold_bin) and (self.max_holding_bars is not None): maxhold_bin.append(self.max_holding_bars)
            if (self.profitable_closes not in profitable_closes_bin) and (self.profitable_closes is not None): profitable_closes_bin.append(self.profitable_closes)

        for args in itertools.product(pt_mult_bin, sl_mult_bin, maxhold_bin, profitable_closes_bin):
            databin.append(self.run_test(args[0], args[1], args[2], args[3])) # append contents into databin

        return databin
            

    def run_test(self, pt_mult, sl_mult, maxhold, profitable_closes):
        # 1) Read in base data (features were pre-labeled during the data download)
        data = self.read_in_data()

        # 2) Label PT and SL
        if pt_mult is not None: data = self.label_pt(data, pt_mult)
        if sl_mult is not None: data = self.label_sl(data, sl_mult)

        # 3) Label entry signals and entry_signals_combined
        data.reset_index(inplace=True)
        data, entry_indices, entry_vector_length = self.label_entries(data)

        # 4) Label exit signals and exit_signals_combined
        data = self.label_exits_and_active_positions(data, entry_indices, entry_vector_length, pt_mult, sl_mult, maxhold, profitable_closes)
        data.set_index(keys='datetime', inplace=True) # set index back to datetime

        # 5) Label strategy_rets, performance_curve, then compute and return performance metrics
        data.dropna(how='any', axis='rows', inplace=True) # drop any rows that contain nans
        return self.compute_and_label_performance_metrics(data, pt_mult, sl_mult, maxhold, profitable_closes)

    # 1) Read in data
    def read_in_data(self):
        data = pd.read_pickle(f'{labeled_bars_path}\\{self.symbol}')
        data.datetime = pd.to_datetime(data.datetime)
        data.set_index(keys='datetime', drop=True, inplace=True)
        data.sort_index(ascending=True, inplace=True)

        # Invert log_rets if its a short selling strategy
        if self.strategy_direction == 'Short':
            data.log_rets *= -1
        
        return data

    # 2a) Label PT
    def label_pt(self, data, pt_mult):
        if self.strategy_direction == 'Long': data['profit_target'] = data.close + data[self.volatility_calculation] * pt_mult
        else: data['profit_target'] = data.close - data[self.volatility_calculation] * pt_mult
        return data

    # 2b) Label SL
    def label_sl(self, data, sl_mult):
        if self.strategy_direction == 'Long': data['stop_loss'] = data.close - data[self.volatility_calculation] * sl_mult
        else: data['stop_loss'] = data.close + data[self.volatility_calculation] * sl_mult
        return data

    # 3) Label entry signals and entry col
    def label_entries(self, data):
        # Get signal parameter bins
        signals_param_bins = []
        for entry_signal in self.entry_checks:
            signals_param_bins.append(self.signals_and_params[entry_signal])

        # Label signal cols and compute entry indices
        data, self.entry_labels = LabelSignals(data, self.entry_checks, signals_param_bins).label() # data, signals, signal_param_bins
        entry_signals_arr = np.transpose(np.array(data[self.entry_labels]))
        entry_signals_triggered = (entry_signals_arr==1).all(axis=0).astype(int)
        entry_indices = np.argwhere(np.diff(np.pad(entry_signals_triggered, 1)) == 1).squeeze() # array of entry indices
        self.num_trades = len(entry_indices)

        # Label entry col and return entry_indices and entry_vector_length
        vector_shape = entry_signals_triggered.shape
        entry_vector = np.zeros(vector_shape) # identical vector of 0s. this will also be used for the metalabler
        entry_vector[entry_indices] = 1 # label 1 at every position that there was an entry
        data['entry'] = pd.Series(entry_vector).shift(1) # label entry col (shift forward by 1 to remove lookahead bias)
        entry_indices = np.argwhere(np.diff(np.pad(data.entry, 1)) == 1).squeeze() # re-compute entry_indices to remove lookahead bias
        return data, entry_indices, vector_shape[0]

    # 4) Label exit signals, exit col, and active_positions *USE NUMBA TO SPEED UP*
    def label_exits_and_active_positions(self, data, entry_indices, entry_vector_length, pt_mult, sl_mult, maxhold, profitable_closes):

        # Get signal parameter bins
        signals_param_bins = []
        for exit_signal in self.exit_checks:
            signals_param_bins.append(self.signals_and_params[exit_signal])

        # Label signal cols and compute exit_signals_triggered
        data, self.exit_labels = LabelSignals(data, self.exit_checks, signals_param_bins).label() # data, signals, signal_param_bins
        exit_signals_arr = np.transpose(np.array(data[self.exit_labels]))
        exit_signals_triggered = (exit_signals_arr==1).all(axis=0).astype(int)

        # Label exits and active_positions
        active_positions_vector = data.entry.copy()
        entry_indices = entry_indices[entry_indices < entry_vector_length - maxhold]
        exit_vector = np.zeros(entry_vector_length)
        for idx in entry_indices:
            if pt_mult is not None: pt = data.loc[idx, 'profit_target']
            if sl_mult is not None: sl = data.loc[idx, 'stop_loss']
            end = idx + maxhold
            rets_bin = []
            for i in range(idx + 1, end + 1):
                active_positions_vector[i] += 1
                rets_bin.append(data.loc[i, 'log_rets'])
                if exit_signals_triggered[i]: # exit signal
                    exit_vector[i] = 1
                    break
                elif (len(rets_bin) >= profitable_closes) and all(item > 0 for item in rets_bin): # profitable closes
                    exit_vector[i] = 1
                    break
                elif i == end: # maxhold
                    exit_vector[i] = 1
                    break
                else: # PT and SL
                    if pt_mult is not None:
                        if self.strategy_direction == 'Long':
                            if data.loc[i, 'close'] >= pt:
                                exit_vector[i] = 1
                                break
                        else:
                            if data.loc[i, 'close'] <= pt:
                                exit_vector[i] = 1
                                break
                    if sl_mult is not None:
                        if self.strategy_direction == 'Long':
                            if data.loc[i, 'close'] <= sl:
                                exit_vector[i] = 1
                                break
                        else:
                            if data.loc[i, 'close'] >= sl:
                                exit_vector[i] = 1
                                break
        data['exit'] = pd.Series(exit_vector).shift(1)
        data['active_positions'] = active_positions_vector  
        return data
        
    # 5) Label strategy_rets and performance_curve, then compute metrics and return test data
    def compute_and_label_performance_metrics(self, data,  pt_mult, sl_mult, maxhold, profitable_closes):
        # Label strategy_rets and performance_curve
        data['strategy_rets'] = data.log_rets * data.active_positions
        data['performance_curve'] = data.strategy_rets.cumsum().apply(np.exp)

        # Get entry and exit parameters
        entry_params = ",".join(self.entry_labels)
        exit_params = ",".join(self.exit_labels + [f'PT {pt_mult}'] + [f'SL {sl_mult}'] + [f'Maxhold {maxhold}'] + [f'Profitable Closes {profitable_closes}'])

        # Compute metrics
        sharpe_ratio = str(self._compute_sharpe_ratio(data.strategy_rets))
        sortino_ratio = str(self._compute_sortino_ratio(data.strategy_rets))

        # Return contents
        return data, [self.symbol, self.strategy_direction, str(self.num_trades), entry_params, exit_params, sharpe_ratio, sortino_ratio]

    def _compute_sharpe_ratio(self, rets):
        return int(np.mean(rets) / np.std(rets) * float(10 ** round_tolerance) + 0.5) / float(10 ** round_tolerance)

    def _compute_sortino_ratio(self, rets):
        return int(np.mean(rets) / np.std(rets[rets < 0]) * float(10 ** round_tolerance) + 0.5) / float(10 ** round_tolerance)