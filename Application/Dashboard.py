# -*- coding: utf-8 -*-
"""
Created on Sun Nov 21 03:23:50 2021

@author: 14843
"""
import os
import sys
import webbrowser

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QStyledItemDelegate, QComboBox, QMessageBox, QRadioButton, QButtonGroup, QWidget
from PyQt5.QtCore import Qt, QAbstractTableModel

import numpy as np
import pandas as pd

import matplotlib as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from mainwindow import Ui_Toolbox
from strategyoutputwindow import Ui_StrategyOutputWindow

from Data_Downloader import DataDownloader
from Simulation_Engine import SimulationEngine

repo_path = 'C:\\Users\\14843\\Documents\\GitHub\\Trading-Strategy-Simulator'
bars_path = f'{repo_path}\\Data'

#############################################

signal_dict = {'monday': 'non-parametric',
              'tuesday': 'non-parametric',
              'wednesday': 'non-parametric',
              'thursday': 'non-parametric',
              'friday': 'non-parametric',
              'open[] > open[]': 'parametric',
              'open[] > high[]': 'parametric',
              'open[] > low[]': 'parametric',
              'open[] > close[]': 'parametric',
              'open[] <= open[]': 'parametric',
              'open[] <= high[]': 'parametric',
              'open[] <= low[]': 'parametric',
              'open[] <= close[]': 'parametric'}

parameters_dict = {'monday': None,
                   'tuesday': None,
                   'wednesday': None,
                   'thursday': None,
                   'friday': None,
                   'open[] > open[]': ('A', 'B'),
                   'open[] > high[]': ('A', 'B'),
                   'open[] > low[]': ('A', 'B'),
                   'open[] > close[]': ('A', 'B'),
                   'open[] <= open[]': ('A', 'B'),
                   'open[] <= high[]': ('A', 'B'),
                   'open[] <= low[]': ('A', 'B'),
                   'open[] <= close[]': ('A', 'B')}

labeled_bars_bin = os.listdir(bars_path)

#############################################

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.ui = Ui_Toolbox()
        self.ui.setupUi(self)

        # Instantiating strategyoutputwindow class 
        self.StrategyOutput_Ui = Ui_StrategyOutputWindow()
        self.StrategyOutputWindow = QtWidgets.QMainWindow()
        self.StrategyOutput_Ui.setupUi(self.StrategyOutputWindow)

        # For storing signal parameters in memory
        self.tempkey = ''
        self.ParamTableData = {}

        # Data Viewer Tab
        self.fillComboBox()

        # Strategy Simulator Tab
        self.prepareSymbolBin()
        self.prepareSignalBin()
        self.prepareSignalParameterTable()
        
        # Passive methods
        self.ui.SignalBin.selectionModel().selectionChanged.connect(self.on_signalbin_selectionChange)

        # Button click methods (Data Downloader tab)
        self.ui.Go_pushbutton.clicked.connect(self.GoBtn_Clicked)

        # Button click methods (Strategy Simulator Tab)
        self.ui.refresh_button.clicked.connect(self.onRefresh)
        self.ui.Test_Button.clicked.connect(self.TestBtn_Clicked)
    
    def Error_Popup(self, error_msg):
        msg = QMessageBox()
        msg.setWindowTitle('Error')
        msg.setText(error_msg)
        x = msg.exec_()

    # Data Tab method
    def GoBtn_Clicked(self):

        # Line edit inputs
        symbols = None
        if len(self.ui.TickerSymbols_lineedit.text()) > 0:
            symbols = self.ui.TickerSymbols_lineedit.text()

        # Date edit inputs
        start = self.ui.Start_dateedit.dateTime().toPyDateTime()
        stop = self.ui.Stop_dateedit.dateTime().toPyDateTime()

        print(symbols, start, stop)        

        # Download data
        error = None
        if symbols is None:
            error = 'Enter at least 1 symbol'
            self.Error_Popup(error)
        if start is None:
            error = 'Set a start time'
            self.Error_Popup(error)
        if stop is None:
            error = 'Set an end time'
            self.Error_Popup(error)
        if error is None:
            DataDownloader(symbols, start, stop).download_data()

    # Strategy Simulator Tab
    def TestBtn_Clicked(self):
        self._storeSignalParams()

        # Get symbol
        symbol = self._retrieveSymbolCheck()

        # Get SignalBin selections
        entry_checks, exit_checks, non_parametric_checks = self._retrieveSignalBinSelections()

        # Store signal labels and related parameters in a dictionary of nested lists
        signals_and_params = {}
        for key in self.ParamTableData:
            param_df = self.ParamTableData[key]
            lst = []
            for idx in param_df.index:
                param = param_df.iloc[idx, 0]
                try: base = int(param_df.iloc[idx, 1])
                except: base = None
                try: max_ = int(param_df.iloc[idx, 2])
                except: max_ = None
                try: step = int(param_df.iloc[idx, 3])
                except: step = None
                lst.append([param, base, max_, step])
            signals_and_params[key] = lst
        
        # Get combobox inputs
        strategy_direction = None
        volatility_calculation = None
        if len(self.ui.StrategyDirection_Input.currentText()) > 0:
            strategy_direction = self.ui.StrategyDirection_Input.currentText()
        if len(self.ui.VolCalculation_Input.currentText()) > 0:
            volatility_calculation = self.ui.VolCalculation_Input.currentText()
        
        # Get line edit inputs
        pt_multiplier = None
        sl_multiplier = None
        max_holding_bars = None
        profitable_closes = None
        pt_mult_delta3 = None
        sl_mult_delta3 = None
        maxhold_delta3 = None
        profitable_closes_delta3 = None
        if len(self.ui.PTMultiplier_Input.text()) > 0:
            pt_multiplier = self.ui.PTMultiplier_Input.text()
        if len(self.ui.SLMultiplier_Input.text()) > 0:
            sl_multiplier = self.ui.SLMultiplier_Input.text()
        if len(self.ui.MaxHoldingBars_Input.text()) > 0:
            max_holding_bars = self.ui.MaxHoldingBars_Input.text()
        if len(self.ui.ProfitableCloses_Input.text()) > 0:
            profitable_closes = self.ui.ProfitableCloses_Input.text()
        if len(self.ui.PTMultiplier_Delta3.text()) > 0:
            pt_mult_delta3 = self.ui.PTMultiplier_Delta3.text()
        if len(self.ui.SLMultiplier_Delta3.text()) > 0:
            sl_mult_delta3 = self.ui.SLMultiplier_Delta3.text()
        if len(self.ui.MaxHoldingBars_Delta3.text()) > 0:
            maxhold_delta3 = self.ui.MaxHoldingBars_Delta3.text()
        if len(self.ui.ProfitableCloses_Delta3.text()) > 0:
            profitable_closes_delta3 = self.ui.ProfitableCloses_Delta3.text()
        

        # Set all unset types
        try: pt_multiplier = float(pt_multiplier)
        except: pt_multiplier = None
        try: sl_multiplier = float(sl_multiplier)
        except: sl_multiplier = None
        try: max_holding_bars = int(max_holding_bars)
        except: max_holding_bars = None
        try: profitable_closes = int(profitable_closes)
        except: profitable_closes = None
        try: pt_mult_delta3 = float(pt_mult_delta3)
        except: pt_mult_delta3 = None
        try: sl_mult_delta3 = float(sl_mult_delta3)
        except: sl_mult_delta3 = None
        try: maxhold_delta3 = int(maxhold_delta3)
        except: maxhold_delta3 = None
        try: profitable_closes_delta3 = int(profitable_closes_delta3)
        except: profitable_closes_delta3 = None

        # Run test and retrieve databin
        databin = SimulationEngine(strategy_direction, symbol, entry_checks, exit_checks, non_parametric_checks, signals_and_params,
                                volatility_calculation, pt_multiplier, sl_multiplier, max_holding_bars, profitable_closes,
                                pt_mult_delta3, sl_mult_delta3, maxhold_delta3, profitable_closes_delta3).Simulate()

        # Prepare strategy output table
        self.prepareStrategyOutputTable(databin)

        # Show strategy output window
        self.StrategyOutputWindow.show()

    # Strategy Simulator Tab
    def on_signalbin_selectionChange(self, selected, deselected):
        self._storeSignalParams()

        for idx in selected.indexes():
            row, col = idx.row(), idx.column()
            key = self.ui.SignalBin.item(row, 0).text()
            self.tempkey = key
            parameters = parameters_dict[key]
            
            if parameters is None:
                # Update text labels
                self.ui.Signal_Text.setText(key)
                self.ui.Signal_Text.adjustSize()
                self.ui.Parameters_Text.setText('None')
                self.ui.Parameters_Text.adjustSize()
                
                # Clear table
                self.ui.SignalParameters_Table.setRowCount(0)
            else:
                try:
                    # Try building table from memory
                    self._readParamTableData_from_memory()
                except:
                    # Build fresh table (if no table in memory)
                    self.ui.SignalParameters_Table.setRowCount(len(parameters))
                    self.ui.SignalParameters_Table.setColumnCount(4)
                    for row, parameter in enumerate(parameters):
                        for col in range(4): # len([parameter, base, max, step])
                            if col == 0:
                                self.ui.SignalParameters_Table.setItem(row, col, QTableWidgetItem(parameter))
                            else:
                                self.ui.SignalParameters_Table.setItem(row, col, QTableWidgetItem(0))
                    
                # Update text labels
                self.ui.Signal_Text.setText(key)
                self.ui.Signal_Text.adjustSize()
                self.ui.Parameters_Text.setText(','.join(parameters))
                self.ui.Parameters_Text.adjustSize()

    # Strategy Simulator Tab
    def prepareSignalParameterTable(self):
        self.ui.SignalParameters_Table.setRowCount(0)
        self.ui.SignalParameters_Table.setColumnCount(4)  
        self.ui.SignalParameters_Table.setHorizontalHeaderLabels(('Parameter', 'Base', 'Max', 'Step'))
        
        # Set 'Parameter' column to read only
        delegate = ReadOnlyDelegate(self)
        self.ui.SignalParameters_Table.setItemDelegateForColumn(0, delegate)

    # Data Viewer Tab
    def fillComboBox(self):
        self.ui.comboBox.clear()
        for file in labeled_bars_bin:
            self.ui.comboBox.addItem(file)

    # Data Viewer Tab
    def onRefresh(self):
        file_name = self.ui.comboBox.currentText()
        df = pd.read_pickle(bars_path + '\\' + file_name)

        model = PandasModel(df)
        self.ui.tableView.setModel(model)

    # Strategy Simulator Tab
    def prepareSymbolBin(self):
        self.ui.Symbol_tablewidget.setRowCount(len(labeled_bars_bin))
        self.ui.Symbol_tablewidget.setColumnCount(2) # len([symbol, select])
        self.ui.Symbol_tablewidget.setHorizontalHeaderLabels(('Symbol', 'Select'))

        button_group = QButtonGroup(self)
        button_group.setExclusive(True)

        for row, symbol in enumerate(labeled_bars_bin):
            for col in range(2):
                if col == 0:
                    self.ui.Symbol_tablewidget.setItem(row, col, QTableWidgetItem(symbol))
                else:
                    radiobutton = QRadioButton()
                    button_group.addButton(radiobutton)
                    self.ui.Symbol_tablewidget.setCellWidget(row, col, radiobutton)
        
        # Set 'Symbol' column to read only
        delegate = ReadOnlyDelegate(self)
        self.ui.Symbol_tablewidget.setItemDelegateForColumn(0, delegate)

    # Strategy Simulator Tab
    def prepareSignalBin(self):
        col_names = tuple(['Signal', 'Type', '*Entry', 'Exit'])
        n_cols = len(col_names)
        self.ui.SignalBin.setRowCount(len(signal_dict))
        self.ui.SignalBin.setColumnCount(n_cols)
        self.ui.SignalBin.setHorizontalHeaderLabels(col_names)
        
        # Populate signal bin
        for row, signal_and_type_tuple in enumerate(signal_dict.items()):
            for col in range(n_cols):
                if col == 0:
                    self.ui.SignalBin.setItem(row, col, QTableWidgetItem(signal_and_type_tuple[0]))
                elif col == 1:
                    self.ui.SignalBin.setItem(row, col, QTableWidgetItem(signal_and_type_tuple[1]))
                else:
                    if parameters_dict[signal_and_type_tuple[0]] is not None:
                        # Set cell to editable checkbox
                        item = QTableWidgetItem('')
                        item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                        item.setCheckState(Qt.CheckState.Unchecked)
                        self.ui.SignalBin.setItem(row, col, item)
                    else:
                        # Set cell to editable checkbox
                        item = QTableWidgetItem('')
                        item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                        item.setCheckState(Qt.CheckState.Unchecked)
                        self.ui.SignalBin.setItem(row, col, item)

        
        # Set 'Signal' and 'Type' column to read only
        delegate = ReadOnlyDelegate(self)
        self.ui.SignalBin.setItemDelegateForColumn(0, delegate)
        self.ui.SignalBin.setItemDelegateForColumn(1, delegate)

    # Strategy Output Window
    def prepareStrategyOutputTable(self, databin):
        col_names = tuple(['Symbol', 'Direction', '# Trades', 'Entry Params', 'Exit Params', 'Sharpe Ratio', 'Sortino Ratio']) # Add later: [psr, dsr]
        n_cols = len(col_names)
        n_rows = len(databin)
        self.StrategyOutput_Ui.StrategyOutput_tablewidget.setRowCount(n_rows)
        self.StrategyOutput_Ui.StrategyOutput_tablewidget.setColumnCount(n_cols)
        self.StrategyOutput_Ui.StrategyOutput_tablewidget.setHorizontalHeaderLabels(col_names)
        
        for row, contents in enumerate(databin):
            dataset = contents[0]
            bin = contents[1]
            for col, item in enumerate(bin):
                self.StrategyOutput_Ui.StrategyOutput_tablewidget.setItem(row, col, QTableWidgetItem(item)) 

    # Strategy Simulator Tab (helper func)
    def _readParamTableData_from_memory(self):
        df = self.ParamTableData[self.tempkey]
        rows, cols = df.shape
        self.ui.SignalParameters_Table.setRowCount(rows)
        self.ui.SignalParameters_Table.setColumnCount(cols)
        for row in range(rows):
            for col in range(cols):
                self.ui.SignalParameters_Table.setItem(row, col, QTableWidgetItem(df.iloc[row, col]))

    # Strategy Simulator Tab (helper func)
    def _retrieveSymbolCheck(self):
        for row in range(self.ui.Symbol_tablewidget.rowCount()):
            for col in range(self.ui.Symbol_tablewidget.columnCount()):
                if col == 1:
                    if self.ui.Symbol_tablewidget.cellWidget(row, col).isChecked():
                        return self.ui.Symbol_tablewidget.item(row, 0).text() # return checked symbols
    
    # Strategy Simulator Tab (helper func)
    def _retrieveSignalBinSelections(self):
        entry_checks = []
        exit_checks = []
        non_parametric_checks = []

        n_rows = self.ui.SignalBin.rowCount()
        n_cols = self.ui.SignalBin.columnCount()
        for row in range(n_rows):
                for col in range(n_cols):
                    if self.ui.SignalBin.item(row, col).checkState() == QtCore.Qt.Checked:
                        signal_text = self.ui.SignalBin.item(row, 0).text()
                        if col == 0:
                            None # signal name column
                        elif col == 1:
                            None # signal type column
                        elif col == 2:
                            entry_checks.append(signal_text)
                            if self.ui.SignalBin.item(row, 1).text() == 'non-parametric':
                                non_parametric_checks.append(signal_text)
                        elif col == 3:
                            exit_checks.append(signal_text)
                            if self.ui.SignalBin.item(row, 1).text() == 'non-parametric':
                                non_parametric_checks.append(signal_text)
        
        return entry_checks, exit_checks, non_parametric_checks

    # Strategy Simulator Tab (helper func)
    def _storeSignalParams(self):
        rows = self.ui.SignalParameters_Table.rowCount()
        cols = self.ui.SignalParameters_Table.columnCount()
        
        df = pd.DataFrame(np.zeros([rows, cols]))
        for row in range(rows):
            for col in range(cols):
                df.iloc[row, col] = self.ui.SignalParameters_Table.item(row, col).text()
        self.ParamTableData[self.tempkey] = df

# Helper Classes
class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return

class checkableComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self._changed = False

class PandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class Canvas(FigureCanvasQTAgg):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(5,4), dpi=200)
        super().__init__(fig)
        self.setParent(parent)

        t = np.arrange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)

        self.ax.plot(t, s)
        self.ax.set(xlabel='X-axis', ylabel='Y-axis', title='Title')
        self.ax.grid()

class CanvasWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(900, 900)

        chart = Canvas(self)

###########################
def open_app():
    app = QtWidgets.QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

open_app() # Run application
