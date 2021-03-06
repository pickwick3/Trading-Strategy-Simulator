import numpy as np
import pandas as pd

class LabelSignals():
    def __init__(self, data, signals, signals_param_bins):
        self.data = data # Dollar bars DataFrame
        self.signals = signals # List of strings
        self.signals_param_bins = signals_param_bins # Double nested List: [[['A', base, max, step], ['B', base, max, step]], [['A', base, max, step], ['B', base, max, step], ['C...', base, max, step]]]
    
    def label(self):

        data = self.data
        signalMethods = {'monday': self.monday,
                         'tuesday': self.tuesday,
                         'wednesday': self.wednesday,
                         'thursday': self.thursday,
                         'friday': self.friday,
                         'open[] > open[]': self.open_greaterthan_open,
                         'open[] > high[]': self.open_greaterthan_high,
                         'open[] > low[]': self.open_greaterthan_low,
                         'open[] > close[]': self.open_greaterthan_close,
                         'open[] <= open[]': self.open_lessthanequal_open,
                         'open[] <= high[]': self.open_lessthanequal_high,
                         'open[] <= low[]': self.open_lessthanequal_low,
                         'open[] <= close[]': self.open_lessthanequal_close}

        signal_labels = []

        # Parametric signals
        if len(self.signals_param_bins) > 0:
            for signal, signal_param_bin in zip(self.signals, self.signals_param_bins):
                # Extract parameter labels and base values
                signal_params_dict = {} # key=parameter_letter, value=parameter_value
                for param_sub_bin in signal_param_bin:
                    signal_params_dict[param_sub_bin[0]] = param_sub_bin[1]

                # Label signal and append label to list
                data, signal_label = signalMethods[signal](data, signal_params_dict)
                signal_labels.append(signal_label)

            # Return fully labeled dataset
            return data, signal_labels
        
        # Non-parametric signals
        else:
            for signal in self.signals:
                # Label signal
                data, signal_label = signalMethods[signal](data, None)
                signal_labels.append(signal_label)
            # Return fully labeled dataset
            return data, signal_labels
    
    #
    # Seasonalities (Non-parametric)
    #
    def monday(self, data, signal_params_dict):
        weekday = data.datetime.dt.dayofweek
        conditions = (weekday == 0)
        data['monday'] = conditions.astype(int)
        return data, 'monday'

    def tuesday(self, data, signal_params_dict):
        weekday = data.datetime.dt.dayofweek
        conditions = (weekday == 1)
        data['tuesday'] = conditions.astype(int)
        return data, 'tuesday'

    def wednesday(self, data, signal_params_dict):
        weekday = data.datetime.dt.dayofweek
        conditions = (weekday == 2)
        data['wednesday'] = conditions.astype(int)
        return data, 'wednesday'

    def thursday(self, data, signal_params_dict):
        weekday = data.datetime.dt.dayofweek
        conditions = (weekday == 3)
        data['thursday'] = conditions.astype(int)
        return data, 'thursday'

    def friday(self, data, signal_params_dict):
        weekday = data.datetime.dt.dayofweek
        conditions = (weekday == 4)
        data['friday'] = conditions.astype(int)
        return data, 'friday'

    #
    # Open patterns (Parametric)
    #
    def open_greaterthan_open(self, data, signal_params_dict):
        A = signal_params_dict['A']
        B = signal_params_dict['B']

        s1 = data.open.shift(A)
        s2 = data.open.shift(B)
        conditions = (s1 > s2)

        signal_label = 'open[{:.2f}] > open[{:.2f}]'.format(A, B)
        data[signal_label] = conditions.astype(int)
        return data, signal_label

    def open_greaterthan_high(self, data, signal_params_dict):
        A = signal_params_dict['A']
        B = signal_params_dict['B']

        s1 = data.open.shift(A)
        s2 = data.high.shift(B)
        conditions = (s1 > s2)

        signal_label = 'open[{:.2f}] > high[{:.2f}]'.format(A, B)
        data[signal_label] = conditions.astype(int)
        return data, signal_label

    def open_greaterthan_low(self, data, signal_params_dict):
        A = signal_params_dict['A']
        B = signal_params_dict['B']

        s1 = data.open.shift(A)
        s2 = data.low.shift(B)
        conditions = (s1 > s2)

        signal_label = 'open[{:.2f}] > low[{:.2f}]'.format(A, B)
        data[signal_label] = conditions.astype(int)
        return data, signal_label

    def open_greaterthan_close(self, data, signal_params_dict):
        A = signal_params_dict['A']
        B = signal_params_dict['B']

        s1 = data.open.shift(A)
        s2 = data.close.shift(B)
        conditions = (s1 > s2)

        signal_label = 'open[{:.2f}] > close[{:.2f}]'.format(A, B)
        data[signal_label] = conditions.astype(int)
        return data, signal_label
    
    def open_lessthanequal_open(self, data, signal_params_dict):
        A = signal_params_dict['A']
        B = signal_params_dict['B']

        s1 = data.open.shift(A)
        s2 = data.open.shift(B)
        conditions = (s1 <= s2)

        signal_label = 'open[{:.2f}] <= open[{:.2f}]'.format(A, B)
        data[signal_label] = conditions.astype(int)
        return data, signal_label

    def open_lessthanequal_high(self, data, signal_params_dict):
        A = signal_params_dict['A']
        B = signal_params_dict['B']

        s1 = data.open.shift(A)
        s2 = data.high.shift(B)
        conditions = (s1 <= s2)

        signal_label = 'open[{:.2f}] <= high[{:.2f}]'.format(A, B)
        data[signal_label] = conditions.astype(int)
        return data, signal_label

    def open_lessthanequal_low(self, data, signal_params_dict):
        A = signal_params_dict['A']
        B = signal_params_dict['B']

        s1 = data.open.shift(A)
        s2 = data.low.shift(B)
        conditions = (s1 <= s2)

        signal_label = 'open[{:.2f}] <= low[{:.2f}]'.format(A, B)
        data[signal_label] = conditions.astype(int)
        return data, signal_label

    def open_lessthanequal_close(self, data, signal_params_dict):
        A = signal_params_dict['A']
        B = signal_params_dict['B']

        s1 = data.open.shift(A)
        s2 = data.close.shift(B)
        conditions = (s1 <= s2)

        signal_label = 'open[{:.2f}] <= close[{:.2f}]'.format(A, B)
        data[signal_label] = conditions.astype(int)
        return data, signal_label

