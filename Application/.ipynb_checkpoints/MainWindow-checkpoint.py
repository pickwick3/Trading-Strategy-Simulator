# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1171, 823)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.TabWidget.setGeometry(QtCore.QRect(0, 0, 1171, 781))
        self.TabWidget.setObjectName("TabWidget")
        self.PrimaryModel_Tab = QtWidgets.QWidget()
        self.PrimaryModel_Tab.setObjectName("PrimaryModel_Tab")
        self.FitnessFunction_Input = QtWidgets.QComboBox(self.PrimaryModel_Tab)
        self.FitnessFunction_Input.setGeometry(QtCore.QRect(10, 460, 261, 25))
        self.FitnessFunction_Input.setObjectName("FitnessFunction_Input")
        self.FitnessFunction_Input.addItem("")
        self.FitnessFunction_Input.addItem("")
        self.FitnessFunction_Input.addItem("")
        self.FitnessFunction_Input.addItem("")
        self.StrategyDirection_Input = QtWidgets.QComboBox(self.PrimaryModel_Tab)
        self.StrategyDirection_Input.setGeometry(QtCore.QRect(10, 30, 261, 25))
        self.StrategyDirection_Input.setObjectName("StrategyDirection_Input")
        self.StrategyDirection_Input.addItem("")
        self.StrategyDirection_Input.addItem("")
        self.PTMultiplier_input = QtWidgets.QLineEdit(self.PrimaryModel_Tab)
        self.PTMultiplier_input.setGeometry(QtCore.QRect(200, 370, 71, 21))
        self.PTMultiplier_input.setObjectName("PTMultiplier_input")
        self.PTMultiplier_checkbox = QtWidgets.QCheckBox(self.PrimaryModel_Tab)
        self.PTMultiplier_checkbox.setGeometry(QtCore.QRect(10, 372, 181, 21))
        self.PTMultiplier_checkbox.setObjectName("PTMultiplier_checkbox")
        self.FitnessFunction_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.FitnessFunction_Label.setGeometry(QtCore.QRect(10, 440, 241, 21))
        self.FitnessFunction_Label.setObjectName("FitnessFunction_Label")
        self.Intermarket1_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.Intermarket1_Label.setGeometry(QtCore.QRect(10, 130, 161, 21))
        self.Intermarket1_Label.setObjectName("Intermarket1_Label")
        self.BaseSymbol_Input = QtWidgets.QComboBox(self.PrimaryModel_Tab)
        self.BaseSymbol_Input.setGeometry(QtCore.QRect(10, 90, 261, 25))
        self.BaseSymbol_Input.setObjectName("BaseSymbol_Input")
        self.BaseSymbol_Input.addItem("")
        self.BaseSymbol_Input.addItem("")
        self.BaseSymbol_Input.addItem("")
        self.VolCalculation_Input = QtWidgets.QComboBox(self.PrimaryModel_Tab)
        self.VolCalculation_Input.setGeometry(QtCore.QRect(10, 340, 261, 25))
        self.VolCalculation_Input.setObjectName("VolCalculation_Input")
        self.VolCalculation_Input.addItem("")
        self.VolCalculation_Input.addItem("")
        self.VolCalculation_Input.addItem("")
        self.VolCalculation_Input.addItem("")
        self.VolCalculation_Input.addItem("")
        self.VolCalculation_Input.addItem("")
        self.BaseSymbol_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.BaseSymbol_Label.setGeometry(QtCore.QRect(10, 70, 101, 21))
        self.BaseSymbol_Label.setObjectName("BaseSymbol_Label")
        self.Intermarket1_Input = QtWidgets.QComboBox(self.PrimaryModel_Tab)
        self.Intermarket1_Input.setGeometry(QtCore.QRect(10, 150, 261, 25))
        self.Intermarket1_Input.setObjectName("Intermarket1_Input")
        self.Intermarket1_Input.addItem("")
        self.Intermarket1_Input.addItem("")
        self.Intermarket1_Input.addItem("")
        self.Intermarket1_Input.addItem("")
        self.SLMultiplier_input = QtWidgets.QLineEdit(self.PrimaryModel_Tab)
        self.SLMultiplier_input.setGeometry(QtCore.QRect(200, 400, 71, 21))
        self.SLMultiplier_input.setObjectName("SLMultiplier_input")
        self.VolCalculation_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.VolCalculation_Label.setGeometry(QtCore.QRect(10, 320, 161, 21))
        self.VolCalculation_Label.setObjectName("VolCalculation_Label")
        self.SLMultiplier_checkbox = QtWidgets.QCheckBox(self.PrimaryModel_Tab)
        self.SLMultiplier_checkbox.setGeometry(QtCore.QRect(10, 400, 161, 23))
        self.SLMultiplier_checkbox.setObjectName("SLMultiplier_checkbox")
        self.StrategyDirection_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.StrategyDirection_Label.setGeometry(QtCore.QRect(10, 10, 131, 21))
        self.StrategyDirection_Label.setObjectName("StrategyDirection_Label")
        self.Simulate_Button = QtWidgets.QPushButton(self.PrimaryModel_Tab)
        self.Simulate_Button.setGeometry(QtCore.QRect(410, 710, 161, 25))
        self.Simulate_Button.setObjectName("Simulate_Button")
        self.Portfolio_Button = QtWidgets.QPushButton(self.PrimaryModel_Tab)
        self.Portfolio_Button.setGeometry(QtCore.QRect(590, 710, 161, 25))
        self.Portfolio_Button.setObjectName("Portfolio_Button")
        self.MaxHoldingBars_Input = QtWidgets.QLineEdit(self.PrimaryModel_Tab)
        self.MaxHoldingBars_Input.setGeometry(QtCore.QRect(140, 500, 41, 21))
        self.MaxHoldingBars_Input.setObjectName("MaxHoldingBars_Input")
        self.MaxHoldingBars_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.MaxHoldingBars_Label.setGeometry(QtCore.QRect(10, 500, 131, 21))
        self.MaxHoldingBars_Label.setObjectName("MaxHoldingBars_Label")
        self.MaxHoldingBars_Delta3 = QtWidgets.QLineEdit(self.PrimaryModel_Tab)
        self.MaxHoldingBars_Delta3.setGeometry(QtCore.QRect(230, 500, 41, 21))
        self.MaxHoldingBars_Delta3.setObjectName("MaxHoldingBars_Delta3")
        self.Delta3_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.Delta3_Label.setGeometry(QtCore.QRect(190, 500, 41, 21))
        self.Delta3_Label.setObjectName("Delta3_Label")
        self.ProfitableCloses_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.ProfitableCloses_Label.setGeometry(QtCore.QRect(10, 530, 121, 21))
        self.ProfitableCloses_Label.setObjectName("ProfitableCloses_Label")
        self.Delta3_Label_2 = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.Delta3_Label_2.setGeometry(QtCore.QRect(190, 530, 41, 21))
        self.Delta3_Label_2.setObjectName("Delta3_Label_2")
        self.ProfitableCloses_Input = QtWidgets.QLineEdit(self.PrimaryModel_Tab)
        self.ProfitableCloses_Input.setGeometry(QtCore.QRect(140, 530, 41, 21))
        self.ProfitableCloses_Input.setObjectName("ProfitableCloses_Input")
        self.ProfitableCloses_Delta3 = QtWidgets.QLineEdit(self.PrimaryModel_Tab)
        self.ProfitableCloses_Delta3.setGeometry(QtCore.QRect(230, 530, 41, 21))
        self.ProfitableCloses_Delta3.setObjectName("ProfitableCloses_Delta3")
        self.NSplitsTotal_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.NSplitsTotal_Label.setGeometry(QtCore.QRect(10, 620, 101, 21))
        self.NSplitsTotal_Label.setObjectName("NSplitsTotal_Label")
        self.NSplitsTotal_Input = QtWidgets.QLineEdit(self.PrimaryModel_Tab)
        self.NSplitsTotal_Input.setGeometry(QtCore.QRect(110, 620, 161, 21))
        self.NSplitsTotal_Input.setObjectName("NSplitsTotal_Input")
        self.OOSSplitAssignment_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.OOSSplitAssignment_Label.setGeometry(QtCore.QRect(10, 570, 241, 21))
        self.OOSSplitAssignment_Label.setObjectName("OOSSplitAssignment_Label")
        self.OOSSplitAssignments_Input = QtWidgets.QComboBox(self.PrimaryModel_Tab)
        self.OOSSplitAssignments_Input.setGeometry(QtCore.QRect(10, 590, 261, 25))
        self.OOSSplitAssignments_Input.setObjectName("OOSSplitAssignments_Input")
        self.OOSSplitAssignments_Input.addItem("")
        self.OOSSplitAssignments_Input.addItem("")
        self.OOSSplitAssignments_Input.addItem("")
        self.NSplitsOOS_Input = QtWidgets.QLineEdit(self.PrimaryModel_Tab)
        self.NSplitsOOS_Input.setGeometry(QtCore.QRect(110, 650, 161, 21))
        self.NSplitsOOS_Input.setObjectName("NSplitsOOS_Input")
        self.NSplitsOOS_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.NSplitsOOS_Label.setGeometry(QtCore.QRect(10, 650, 91, 21))
        self.NSplitsOOS_Label.setObjectName("NSplitsOOS_Label")
        self.NSplitsIS_Input = QtWidgets.QLineEdit(self.PrimaryModel_Tab)
        self.NSplitsIS_Input.setGeometry(QtCore.QRect(110, 680, 161, 21))
        self.NSplitsIS_Input.setText("")
        self.NSplitsIS_Input.setObjectName("NSplitsIS_Input")
        self.NSplitsIS_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.NSplitsIS_Label.setGeometry(QtCore.QRect(10, 680, 91, 21))
        self.NSplitsIS_Label.setObjectName("NSplitsIS_Label")
        self.Intermarket2_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.Intermarket2_Label.setGeometry(QtCore.QRect(10, 190, 161, 21))
        self.Intermarket2_Label.setObjectName("Intermarket2_Label")
        self.Intermarket2_Input = QtWidgets.QComboBox(self.PrimaryModel_Tab)
        self.Intermarket2_Input.setGeometry(QtCore.QRect(10, 210, 261, 25))
        self.Intermarket2_Input.setObjectName("Intermarket2_Input")
        self.Intermarket2_Input.addItem("")
        self.Intermarket2_Input.addItem("")
        self.Intermarket2_Input.addItem("")
        self.Intermarket2_Input.addItem("")
        self.Start_Input = QtWidgets.QDateTimeEdit(self.PrimaryModel_Tab)
        self.Start_Input.setGeometry(QtCore.QRect(63, 250, 211, 26))
        self.Start_Input.setObjectName("Start_Input")
        self.Stop_Input = QtWidgets.QDateTimeEdit(self.PrimaryModel_Tab)
        self.Stop_Input.setGeometry(QtCore.QRect(63, 280, 211, 26))
        self.Stop_Input.setObjectName("Stop_Input")
        self.Start_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.Start_Label.setGeometry(QtCore.QRect(10, 250, 41, 31))
        self.Start_Label.setObjectName("Start_Label")
        self.Stop_Label = QtWidgets.QLabel(self.PrimaryModel_Tab)
        self.Stop_Label.setGeometry(QtCore.QRect(10, 280, 41, 31))
        self.Stop_Label.setObjectName("Stop_Label")
        self.TabWidget.addTab(self.PrimaryModel_Tab, "")
        self.Metalabeler_Tab = QtWidgets.QWidget()
        self.Metalabeler_Tab.setObjectName("Metalabeler_Tab")
        self.TabWidget.addTab(self.Metalabeler_Tab, "")
        self.Live_Tab = QtWidgets.QWidget()
        self.Live_Tab.setObjectName("Live_Tab")
        self.TabWidget.addTab(self.Live_Tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1171, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Main"))
        self.FitnessFunction_Input.setItemText(0, _translate("MainWindow", "Sharpe"))
        self.FitnessFunction_Input.setItemText(1, _translate("MainWindow", "Sortino"))
        self.FitnessFunction_Input.setItemText(2, _translate("MainWindow", "Probabilistic Sharpe"))
        self.FitnessFunction_Input.setItemText(3, _translate("MainWindow", "Probabilistic Sortino"))
        self.StrategyDirection_Input.setItemText(0, _translate("MainWindow", "Long"))
        self.StrategyDirection_Input.setItemText(1, _translate("MainWindow", "Short"))
        self.PTMultiplier_checkbox.setText(_translate("MainWindow", "Profit Target Multiplier:"))
        self.FitnessFunction_Label.setText(_translate("MainWindow", "Fitness Function:"))
        self.Intermarket1_Label.setText(_translate("MainWindow", "Intermarket 1 Symbol:"))
        self.BaseSymbol_Input.setItemText(0, _translate("MainWindow", "BTCDollarBars"))
        self.BaseSymbol_Input.setItemText(1, _translate("MainWindow", "ETHDollarBars"))
        self.BaseSymbol_Input.setItemText(2, _translate("MainWindow", "LTCDollarBars"))
        self.VolCalculation_Input.setItemText(0, _translate("MainWindow", "None"))
        self.VolCalculation_Input.setItemText(1, _translate("MainWindow", "ATR"))
        self.VolCalculation_Input.setItemText(2, _translate("MainWindow", "STD"))
        self.VolCalculation_Input.setItemText(3, _translate("MainWindow", "MAD"))
        self.VolCalculation_Input.setItemText(4, _translate("MainWindow", "EWM STD"))
        self.VolCalculation_Input.setItemText(5, _translate("MainWindow", "EWM MAD"))
        self.BaseSymbol_Label.setText(_translate("MainWindow", "Base Symbol:"))
        self.Intermarket1_Input.setItemText(0, _translate("MainWindow", "None"))
        self.Intermarket1_Input.setItemText(1, _translate("MainWindow", "BTCDollarBars"))
        self.Intermarket1_Input.setItemText(2, _translate("MainWindow", "ETHDollarBars"))
        self.Intermarket1_Input.setItemText(3, _translate("MainWindow", "LTCDollarBars"))
        self.VolCalculation_Label.setText(_translate("MainWindow", "Volatility Calculation:"))
        self.SLMultiplier_checkbox.setText(_translate("MainWindow", "Stop Loss Multiplier:"))
        self.StrategyDirection_Label.setText(_translate("MainWindow", "Strategy Direction:"))
        self.Simulate_Button.setText(_translate("MainWindow", "Simulate"))
        self.Portfolio_Button.setText(_translate("MainWindow", "Portfolio"))
        self.MaxHoldingBars_Label.setText(_translate("MainWindow", "Max Holding Bars:"))
        self.Delta3_Label.setText(_translate("MainWindow", "Δ x3:"))
        self.ProfitableCloses_Label.setText(_translate("MainWindow", "Profitable Closes:"))
        self.Delta3_Label_2.setText(_translate("MainWindow", "Δ x3:"))
        self.NSplitsTotal_Label.setText(_translate("MainWindow", "# Splits Total:"))
        self.OOSSplitAssignment_Label.setText(_translate("MainWindow", "OOS Split Assignment:"))
        self.OOSSplitAssignments_Input.setItemText(0, _translate("MainWindow", "Tail"))
        self.OOSSplitAssignments_Input.setItemText(1, _translate("MainWindow", "Head"))
        self.OOSSplitAssignments_Input.setItemText(2, _translate("MainWindow", "Randomized"))
        self.NSplitsOOS_Label.setText(_translate("MainWindow", "# Splits OOS:"))
        self.NSplitsIS_Label.setText(_translate("MainWindow", "# Splits IS:"))
        self.Intermarket2_Label.setText(_translate("MainWindow", "Intermarket 2 Symbol:"))
        self.Intermarket2_Input.setItemText(0, _translate("MainWindow", "None"))
        self.Intermarket2_Input.setItemText(1, _translate("MainWindow", "BTCDollarBars"))
        self.Intermarket2_Input.setItemText(2, _translate("MainWindow", "ETHDollarBars"))
        self.Intermarket2_Input.setItemText(3, _translate("MainWindow", "LTCDollarBars"))
        self.Start_Label.setText(_translate("MainWindow", "Start:"))
        self.Stop_Label.setText(_translate("MainWindow", "Stop:"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.PrimaryModel_Tab), _translate("MainWindow", "Primary Model"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Metalabeler_Tab), _translate("MainWindow", "Metalabeler"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.Live_Tab), _translate("MainWindow", "Live"))
