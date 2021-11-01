from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import QSize, pyqtSignal
from ui import Ui_MainWindow
import sys
import pyautogui as pg
import threading
import time
import traceback


pg.FAILSAFE=False
class MainWindow(QMainWindow):
    countSignal=pyqtSignal(int)
    def __init__(self):
        super(MainWindow,self).__init__()
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setMinimumSize(1500,500)
        self.setMaximumSize(2000,800)
        self.ui.maxClicks_sbox.setEnabled(False)
        #
        self.ui.statusbar.showMessage("Set Click Delay to 0 at your own risk. You can use 'S' as shorctut for stop.")
        self.ui.enableMax_radio.toggled.connect(self.activate_max)
        #
        #self.ui.delayPerClick_sbox.setMinimum(1)
        self.ui.delaybeforeStart_sbox.setMinimum(1)
        self.ui.maxClicks_sbox.setMinimum(1)
        self.ui.maxClicks_sbox.setMaximum(100000)
        self.ui.stop_btn.setShortcut('S')
        #
        self.is_running=False
        #
        self.countSignal.connect(self.update_click_count)
        self.ui.start_btn.clicked.connect(self.start_fun)
        self.start_delay=5
        self.click_delay=5
        self.use_max=False
        self.max_clicks=None
        self.ui.delaybeforeStart_sbox.setValue(self.start_delay)
        self.ui.delayPerClick_sbox.setValue(self.click_delay)
        self.ui.stop_btn.clicked.connect(self.stop_count)

    def get_data(self):
        self.start_delay=self.ui.delaybeforeStart_sbox.value()
        self.click_delay=self.ui.delayPerClick_sbox.value()
        if self.use_max:
            self.max_clicks=self.ui.maxClicks_sbox.value()

    def activate_max(self):
        if self.ui.enableMax_radio.isChecked():
            self.ui.maxClicks_sbox.setEnabled(True)
            self.use_max=True
        else:
            self.ui.maxClicks_sbox.setEnabled(False)
            self.use_max=False

    def update_click_count(self,num):
        self.ui.countumber.display(num)

    def start_fun(self):
        self.start_thread=threading.Thread(target=self.start_count,daemon=True)
        self.start_thread.start()

    def start_count(self):
        self.get_data()
        self.ui.start_btn.setEnabled(False)
        total_clicks=0
        self.countSignal.emit(total_clicks)
        self.is_running=True
        time.sleep(self.start_delay)
        while self.is_running:
            pg.click()
            total_clicks+=1
            self.countSignal.emit(total_clicks)
            time.sleep(self.click_delay)
            print(f'{total_clicks}/{self.max_clicks}')
            if (self.max_clicks!=None and self.use_max!=False):
                if(self.max_clicks<=total_clicks):
                    self.is_running=False
        self.ui.start_btn.setEnabled(True)


    def stop_count(self):
        self.is_running=False
        self.ui.start_btn.setEnabled(True)
        self.start_thread.join()

def exception_hook(exctype, value, traceback):
    traceback_formated = traceback.format_exception(exctype, value, traceback)
    traceback_string = "".join(traceback_formated)
    print(traceback_string, file=sys.stderr)
    sys.exit(1)


sys._excepthook = sys.excepthook
sys.excepthook = exception_hook
if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())

