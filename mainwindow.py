from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Mainwindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1110, 550)
        Dialog.setMinimumSize(QtCore.QSize(1110, 550))
        Dialog.setMaximumSize(QtCore.QSize(1110, 550))
        Dialog.setStyleSheet("#Dialog {\n"
"background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(230, 230, 250, 255), stop:0.5 rgba(135, 206, 235, 255), stop:1 rgba(70, 130, 180, 255));\n"
"}")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(-10, 0, 1131, 551))
        self.tabWidget.setMouseTracking(False)
        self.tabWidget.setAcceptDrops(False)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("QTabBar::tab {\n"
"    border: 1px solid black;\n"
"    border-bottom-color: #C2C7CB;\n"
"    border-top-left-radius: 1px;\n"
"    border-top-right-radius: 1px;\n"
"    min-width: 26ex;\n"
"    padding: 10px;\n"
"    font-family: Avenir Next;\n"
"}\n"
"\n"
"QTabBar::tab:selected, QTabBar::tab:hover {\n"
"    background: #b0c4de;\n"
"    font-family: Avenir Next;\n"
"}\n"
" \n"
"QTabBar::tab:selected {\n"
"    border-bottom-color: #b0c4de;\n"
"    font-family: Avenir Next;\n"
"}\n"
" \n"
"QTabBar::tab:!selected {\n"
"    margin-top: 0px;\n"
"    font-family: Avenir Next;\n"
"}")
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideNone)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setMovable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setStyleSheet("#tab_8 {\n"
"background-color: #e2f2fc;\n"
"border-radius:7%;\n"
"border: 1px solid black;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.tab_8.setObjectName("tab_8")
        self.label = QtWidgets.QLabel(self.tab_8)
        self.label.setGeometry(QtCore.QRect(30, 30, 61, 20))
        self.label.setStyleSheet("#label {\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.label.setObjectName("label")
        self.grupaBox_tab1 = QtWidgets.QComboBox(self.tab_8)
        self.grupaBox_tab1.setGeometry(QtCore.QRect(100, 30, 161, 21))
        self.grupaBox_tab1.setStyleSheet("")
        self.grupaBox_tab1.setEditable(False)
        self.grupaBox_tab1.setObjectName("grupaBox_tab1")
        self.tableposeshaem = QtWidgets.QTableWidget(self.tab_8)
        self.tableposeshaem.setGeometry(QtCore.QRect(30, 70, 1071, 421))
        self.tableposeshaem.setObjectName("tableposeshaem")
        self.tableposeshaem.setColumnCount(0)
        self.tableposeshaem.setRowCount(0)
        self.tabWidget.addTab(self.tab_8, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setStyleSheet("#tab_7 {\n"
"background-color: #e2f2fc;\n"
"border-radius:7%;\n"
"border: 1px solid black;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.tab_7.setObjectName("tab_7")
        self.grupaBox_tab2 = QtWidgets.QComboBox(self.tab_7)
        self.grupaBox_tab2.setGeometry(QtCore.QRect(950, 50, 131, 22))
        self.grupaBox_tab2.setEditable(False)
        self.grupaBox_tab2.setObjectName("grupaBox_tab2")
        self.label_2 = QtWidgets.QLabel(self.tab_7)
        self.label_2.setGeometry(QtCore.QRect(890, 50, 61, 20))
        self.label_2.setStyleSheet("#label_2 {\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.label_2.setObjectName("label_2")
        self.addbutton_tab2 = QtWidgets.QPushButton(self.tab_7)
        self.addbutton_tab2.setGeometry(QtCore.QRect(780, 50, 85, 25))
        self.addbutton_tab2.setStyleSheet("#addbutton_tab2 {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#addbutton_tab2:hover {\n"
"background-color: #71bc78\n"
"}")
        self.addbutton_tab2.setObjectName("addbutton_tab2")
        self.izmenbutton_tab2 = QtWidgets.QPushButton(self.tab_7)
        self.izmenbutton_tab2.setGeometry(QtCore.QRect(780, 90, 85, 25))
        self.izmenbutton_tab2.setStyleSheet("#izmenbutton_tab2 {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#izmenbutton_tab2:hover {\n"
"background-color: #eedc82\n"
"}")
        self.izmenbutton_tab2.setObjectName("izmenbutton_tab2")
        self.delbutton_tab2 = QtWidgets.QPushButton(self.tab_7)
        self.delbutton_tab2.setGeometry(QtCore.QRect(780, 130, 85, 25))
        self.delbutton_tab2.setStyleSheet("#delbutton_tab2 {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#delbutton_tab2:hover {\n"
"background-color: #cf7373\n"
"}")
        self.delbutton_tab2.setObjectName("delbutton_tab2")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.tab_7)
        self.calendarWidget.setGeometry(QtCore.QRect(30, 10, 701, 471))
        font = QtGui.QFont()
        font.setKerning(True)
        self.calendarWidget.setFont(font)
        self.calendarWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.calendarWidget.setAcceptDrops(False)
        self.calendarWidget.setToolTip("")
        self.calendarWidget.setStatusTip("")
        self.calendarWidget.setAutoFillBackground(True)
        self.calendarWidget.setStyleSheet("#calendarWidget QWidget {\n"
"    alternate-background-color: #b0c4de;\n"
"}\n"
"\n"
"#qt_calendar_navigationbar {\n"
"    background-color: #fff;\n"
"    border: 2px solid #b0c4de;\n"
"    border-bottom: 0px;\n"
"    border-top-left-radius: 5px;\n"
"    border-top-right-radius: 5px;\n"
"}\n"
"\n"
"#qt_calendar_prevmonth,\n"
"#qt_calendar_nextmonth {\n"
"    border: none;\n"
"\n"
"    min-width: 13px;\n"
"    max-width: 13px;\n"
"    min-height: 13px;\n"
"    max-height: 13px;\n"
"\n"
"    border-radius: 5px;\n"
"    background-color: transparent;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"#qt_calendar_prevmonth:hover,\n"
"#qt_calendar_nextmonth:hover {\n"
"    background-color: #b0c4de;\n"
"}\n"
"\n"
"#qt_calendar_prevmonth:pressed,\n"
"#qt_calendar_nextmonth:pressed {\n"
"    background-color: #b0c4de;\n"
"}\n"
"\n"
"#qt_calendar_yearbutton {\n"
"    color:#000;\n"
"    margin: 5px;\n"
"    border-radius: 5px;\n"
"    font-size: 13px;\n"
"    padding: 0 10px;\n"
"}\n"
"\n"
"#qt_calendar_monthbutton {\n"
"    width: 110px;\n"
"    color: #000;\n"
"    font-size: 13px;\n"
"    margin: 5px 0;\n"
"    border-radius: 5px;\n"
"    padding: 0px 2px;\n"
"}\n"
"\n"
"#qt_calendar_yearbutton:hover,\n"
"#qt_calendar_monthbutton:hover {\n"
"    background-color: #b0c4de;\n"
"}\n"
"\n"
"#qt_calendar_yearbutton:pressed,\n"
"#qt_calendar_monthbutton:pressed {\n"
"    background-color: #b0c4de;\n"
"}\n"
"\n"
"#qt_calendar_yearedit {\n"
"    min-width: 53px;\n"
"    color: #000;\n"
"    background: transparent;\n"
"    font-size: 13px;\n"
"}\n"
"\n"
"#qt_calendar_yearedit::down-button:hover,\n"
"#qt_calendar_yearedit::up-button:hover {\n"
"    background-color: #b0c4de;\n"
"}\n"
"\n"
"#calendarWidget QToolButton QMenu {\n"
"    background-color: #b0c4de;\n"
"}\n"
"\n"
"#calendarWidget QToolButton QMenu::itemselected:enabled {\n"
"     background-color: #b0c4de;\n"
"}\n"
"\n"
"#calendarWidget QToolButton::menu-indicator {\n"
"    nosubcontrol-origin: margin;\n"
"    subcontrol-position: right center;\n"
"    margin-top: 10px;\n"
"    width: 20px;\n"
"}\n"
"\n"
"#qt_calendar_calendarview {\n"
"    border: 2px solid #b0c4de;\n"
"    border-top: 0px;\n"
"    border-bottom-left-radius: 5px;\n"
"    border-bottom-right-radius: 5px;\n"
"}\n"
"\n"
"#qt_calendar_calendarview::item:hover {\n"
"    border-radius: 5px;\n"
"    background-color: #aaffff;\n"
"}\n"
"\n"
"#qt_calendar_calendarview::item:selected {\n"
"    border-radius: 5px;\n"
"    background-color: #b0c4de;\n"
"}\n"
"\n"
"\n"
"\n"
"\n"
"\n"
"")
        self.calendarWidget.setInputMethodHints(QtCore.Qt.ImhNone)
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setSelectionMode(QtWidgets.QCalendarWidget.SingleSelection)
        self.calendarWidget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.ISOWeekNumbers)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.calendarWidget.setDateEditAcceptDelay(1500)
        self.calendarWidget.setObjectName("calendarWidget")
        self.tabWidget.addTab(self.tab_7, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setStyleSheet("#tab_6 {\n"
"background-color: #e2f2fc;\n"
"border-radius:7%;\n"
"border: 1px solid black;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.tab_6.setObjectName("tab_6")
        self.tabWidget.addTab(self.tab_6, "")
        self.addbutton_tab3 = QtWidgets.QPushButton(self.tab_6)
        self.addbutton_tab3.setGeometry(QtCore.QRect(30, 30, 85, 25))
        self.addbutton_tab3.setStyleSheet("#addbutton_tab3 {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#addbutton_tab3:hover {\n"
"background-color: #71bc78\n"
"}")
        self.addbutton_tab3.setObjectName("addbutton_tab3")
        self.izmenbutton_tab3 = QtWidgets.QPushButton(self.tab_6)
        self.izmenbutton_tab3.setGeometry(QtCore.QRect(140, 30, 85, 25))
        self.izmenbutton_tab3.setStyleSheet("#izmenbutton_tab3 {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#izmenbutton_tab3:hover {\n"
"background-color: #eedc82\n"
"}")
        self.izmenbutton_tab3.setObjectName("izmenbutton_tab3")
        self.delbutton_tab3 = QtWidgets.QPushButton(self.tab_6)
        self.delbutton_tab3.setGeometry(QtCore.QRect(250, 30, 85, 25))
        self.delbutton_tab3.setStyleSheet("#delbutton_tab3 {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#delbutton_tab3:hover {\n"
"background-color: #cf7373\n"
"}")
        self.delbutton_tab3.setObjectName("delbutton_tab3")
        self.tableWidget_tab3 = QtWidgets.QTableWidget(self.tab_6)
        self.tableWidget_tab3.setGeometry(QtCore.QRect(30, 70, 1071, 421))
        self.tableWidget_tab3.setObjectName("tableWidget_tab3")
        self.tableWidget_tab3.setColumnCount(4)  # Установите количество столбцов
        self.tableWidget_tab3.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество", "Доп. информация"])  # Установите заголовки
        # self.lineEdit_tab3 = QtWidgets.QLineEdit(self.tab_6)
        # self.lineEdit_tab3.setGeometry(QtCore.QRect(782, 80, 298, 20))
        # self.lineEdit_tab3.setInputMask("")
        # self.lineEdit_tab3.setText("")
        # self.lineEdit_tab3.setFrame(True)
        # self.lineEdit_tab3.setCursorPosition(0)
        # self.lineEdit_tab3.setDragEnabled(False)
        # self.lineEdit_tab3.setReadOnly(False)
        # self.lineEdit_tab3.setClearButtonEnabled(False)
        # self.lineEdit_tab3.setObjectName("lineEdit_tab3")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setStyleSheet("#tab_5 {\n"
"background-color: #e2f2fc;\n"
"border-radius:7%;\n"
"border: 1px solid black;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.tab_5.setObjectName("tab_5")
        self.addbutton_tab4 = QtWidgets.QPushButton(self.tab_5)
        self.addbutton_tab4.setGeometry(QtCore.QRect(30, 30, 85, 25))
        self.addbutton_tab4.setStyleSheet("#addbutton_tab4 {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#addbutton_tab4:hover {\n"
"background-color: #71bc78\n"
"}")
        self.addbutton_tab4.setObjectName("addbutton_tab4")
        self.izmenbutton_tab4 = QtWidgets.QPushButton(self.tab_5)
        self.izmenbutton_tab4.setGeometry(QtCore.QRect(140, 30, 85, 25))
        self.izmenbutton_tab4.setStyleSheet("#izmenbutton_tab4 {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#izmenbutton_tab4:hover {\n"
"background-color: #eedc82\n"
"}")
        self.izmenbutton_tab4.setObjectName("izmenbutton_tab4")
        self.delbutton_tab4 = QtWidgets.QPushButton(self.tab_5)
        self.delbutton_tab4.setGeometry(QtCore.QRect(250, 30, 85, 25))
        self.delbutton_tab4.setStyleSheet("#delbutton_tab4 {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#delbutton_tab4:hover {\n"
"background-color: #cf7373\n"
"}")
        self.delbutton_tab4.setObjectName("delbutton_tab4")
        self.tableWidget_tab4 = QtWidgets.QTableWidget(self.tab_5)
        self.tableWidget_tab4.setGeometry(QtCore.QRect(30, 70, 1071, 421))
        self.tableWidget_tab4.setObjectName("tableWidget_tab4")
        self.tableWidget_tab4.setColumnCount(6)  # Установите количество столбцов
        self.tabWidget.addTab(self.tab_5, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setAutoFillBackground(False)
        self.tab.setStyleSheet("#tab {\n"
"background-color: #e2f2fc;\n"
"border-radius:7%;\n"
"border: 1px solid black;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.tab.setObjectName("tab")
        self.lineEdit_tab5 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_tab5.setGeometry(QtCore.QRect(782, 80, 298, 20))
        self.lineEdit_tab5.setObjectName("lineEdit_tab5")
        self.izmenbutton_tab5 = QtWidgets.QPushButton(self.tab)
        self.izmenbutton_tab5.setGeometry(QtCore.QRect(140, 30, 85, 25))
        self.izmenbutton_tab5.setStyleSheet("#izmenbutton_tab5 {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"#izmenbutton_tab5:hover {\n"
"background-color: #eedc82\n"
"}")
        self.izmenbutton_tab5.setObjectName("izmenbutton_tab5")
        self.listView_tab5 = QtWidgets.QListView(self.tab)
        self.listView_tab5.setGeometry(QtCore.QRect(30, 70, 1071, 421))
        self.listView_tab5.setObjectName("listView_tab5")
        self.delbutton_tab5 = QtWidgets.QPushButton(self.tab)
        self.delbutton_tab5.setGeometry(QtCore.QRect(250, 30, 85, 25))
        self.delbutton_tab5.setStyleSheet("#delbutton_tab5 {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#delbutton_tab5:hover {\n"
"background-color: #cf7373\n"
"}")
        self.delbutton_tab5.setObjectName("delbutton_tab5")
        self.addbutton_tab5 = QtWidgets.QPushButton(self.tab)
        self.addbutton_tab5.setGeometry(QtCore.QRect(30, 30, 85, 25))
        self.addbutton_tab5.setStyleSheet("#addbutton_tab5 {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#addbutton_tab5:hover {\n"
"background-color: #71bc78\n"
"}")
        self.addbutton_tab5.setObjectName("addbutton_tab5")
        self.textBrowser_tab5 = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser_tab5.setGeometry(QtCore.QRect(40, 110, 1041, 71))
        self.textBrowser_tab5.setObjectName("textBrowser_tab5")
        self.izmenbutton_tab5.raise_()
        self.listView_tab5.raise_()
        self.delbutton_tab5.raise_()
        self.addbutton_tab5.raise_()
        self.lineEdit_tab5.raise_()
        self.textBrowser_tab5.raise_()
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setStyleSheet("#tab_2 {\n"
"background-color: #e2f2fc;\n"
"border-radius:7%;\n"
"border: 1px solid black;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.tab_2.setObjectName("tab_2")
        self.listView_tab6 = QtWidgets.QListView(self.tab_2)
        self.listView_tab6.setGeometry(QtCore.QRect(30, 30, 711, 461))
        self.listView_tab6.setObjectName("listView_tab6")
        self.grupaBox_tab6 = QtWidgets.QComboBox(self.tab_2)
        self.grupaBox_tab6.setGeometry(QtCore.QRect(880, 70, 161, 22))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.grupaBox_tab6.sizePolicy().hasHeightForWidth())
        self.grupaBox_tab6.setSizePolicy(sizePolicy)
        self.grupaBox_tab6.setEditable(False)
        self.grupaBox_tab6.setObjectName("grupaBox_tab6")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(760, 40, 111, 21))
        self.label_3.setStyleSheet("#label_3 {\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab_2)
        self.label_4.setGeometry(QtCore.QRect(760, 70, 61, 21))
        self.label_4.setStyleSheet("#label_4 {\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}")
        self.label_4.setObjectName("label_4")
        self.dateEdit_tab6 = QtWidgets.QDateEdit(self.tab_2)
        self.dateEdit_tab6.setGeometry(QtCore.QRect(880, 40, 161, 22))
        self.dateEdit_tab6.setMaximumDate(QtCore.QDate(2025, 12, 31))
        self.dateEdit_tab6.setMinimumDate(QtCore.QDate(2024, 1, 1))
        self.dateEdit_tab6.setCalendarPopup(True)
        self.dateEdit_tab6.setObjectName("dateEdit_tab6")
        self.clearbutton_tab6 = QtWidgets.QPushButton(self.tab_2)
        self.clearbutton_tab6.setGeometry(QtCore.QRect(760, 430, 85, 25))
        self.clearbutton_tab6.setStyleSheet("#clearbutton_tab6 {\n"
"background-color: #b0c4de;\n"
"border-radius:7%;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#clearbutton_tab6:hover {\n"
"background-color: #9db1cc\n"
"}")
        self.clearbutton_tab6.setObjectName("clearbutton_tab6")
        self.treeView = QtWidgets.QTreeView(self.tab_2)
        self.treeView.setGeometry(QtCore.QRect(40, 40, 691, 131))
        self.treeView.setObjectName("treeView")
        self.textBrowser_tab6 = QtWidgets.QTextBrowser(self.tab_2)
        self.textBrowser_tab6.setGeometry(QtCore.QRect(40, 180, 691, 41))
        self.textBrowser_tab6.setObjectName("textBrowser_tab6")
        self.tableWidget_tab6 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_tab6.setGeometry(QtCore.QRect(40, 230, 691, 211))
        self.tableWidget_tab6.setObjectName("tableWidget_tab6")
        self.tableWidget_tab6.setColumnCount(0)
        self.tableWidget_tab6.setRowCount(0)
        self.tabWidget.addTab(self.tab_2, "")
        self.exitButton = QtWidgets.QPushButton(Dialog)
        self.exitButton.setGeometry(QtCore.QRect(1057, 0, 54, 36))
        self.exitButton.setStyleSheet("#exitButton {\n"
"background-color: #cf7373;\n"
"border: 1px solid grey;\n"
"font-family: Avenir Next;\n"
"font-size: 16px;\n"
"}\n"
"\n"
"#exitButton:hover {\n"
"background-color: #bc5d58\n"
"}")
        self.exitButton.setObjectName("exitButton")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Рукопашный бой - Система"))
        self.label.setText(_translate("Dialog", "Группа:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), _translate("Dialog", "Посещаемость"))
        self.label_2.setText(_translate("Dialog", "Группа:"))
        self.addbutton_tab2.setText(_translate("Dialog", "Создать"))
        self.izmenbutton_tab2.setText(_translate("Dialog", "Изменить"))
        self.delbutton_tab2.setText(_translate("Dialog", "Удалить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("Dialog", "Расписание занятий"))
        self.addbutton_tab3.setText(_translate("Dialog", "Добавить"))
        self.izmenbutton_tab3.setText(_translate("Dialog", "Изменить"))
        self.delbutton_tab3.setText(_translate("Dialog", "Удалить"))
        # self.lineEdit_tab3.setPlaceholderText(_translate("Dialog", "Поиск..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("Dialog", "Тренеры"))
        self.addbutton_tab4.setText(_translate("Dialog", "Добавить"))
        self.izmenbutton_tab4.setText(_translate("Dialog", "Изменить"))
        self.delbutton_tab4.setText(_translate("Dialog", "Удалить"))
        # self.lineEdit_tab4.setPlaceholderText(_translate("Dialog", "Поиск..."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Dialog", "Спортсмены"))
        self.lineEdit_tab5.setPlaceholderText(_translate("Dialog", "Поиск..."))
        self.izmenbutton_tab5.setText(_translate("Dialog", "Изменить"))
        self.delbutton_tab5.setText(_translate("Dialog", "Удалить"))
        self.addbutton_tab5.setText(_translate("Dialog", "Создать"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Группы"))
        self.label_3.setText(_translate("Dialog", "Дата периода:"))
        self.label_4.setText(_translate("Dialog", "Группа:"))
        self.clearbutton_tab6.setText(_translate("Dialog", "Очистить"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Отчетность"))
        self.exitButton.setText(_translate("Dialog", "×"))
