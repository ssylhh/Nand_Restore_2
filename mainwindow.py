# This Python file uses the following encoding: utf-8
import sys
import configparser

from PySide6.QtWidgets import QApplication, QMainWindow, QCheckBox, QMessageBox
# from PySide6.QtCore import Qt
import os
import threading
import ctypes

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow
import socket
import time
from ping3 import ping, verbose_ping
from dll_wrapper import MyDllWrapper
from test2 import AllReadWrite

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 

        self.initial_setup() 

    def get_handler(self):
        # return int(self.winId())  # 실제 윈도우 핸들 반환 (Windows 환경)
        return id(self)

    def initial_setup(self):

        self.gridLayout = self.ui.gridLayout
        handler = self.get_handler()
        
        # self.ping_ip()
        # threading.Thread(target=self.ping_ip, daemon=True).start()
        self.start_ping_thread()  


        # self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
        if getattr(sys, 'frozen', False):             
            self.current_dir = os.path.dirname(sys.executable)
        else:          
            self.current_dir = os.path.dirname(os.path.abspath(__file__))        
    
    
        # dll_path = os.path.join(self.current_dir, "K23A_YB_x64.dll")
        # self.my_dll = MyDllWrapper(dll_path)

        self.dll_path = self.find_any_dll()

        if not self.dll_path:
            return  

        # try:
        #     self.my_dll = MyDllWrapper(self.dll_path)
        # except Exception as e:
        #     QMessageBox.critical(self, "DLL 로드 오류", f"DLL을 로드하는 중 오류 발생:\n{str(e)}")
        #     return           

        # self.arw_dll = AllReadWrite(self.dll_path, self)              
        
        try:
            self.my_dll = MyDllWrapper(self.dll_path)

            # ✅ AllReadWrite 초기화 (self 전달)
            # self.arw_dll = AllReadWrite(self.dll_path, self)
            # self.arw_dll = AllReadWrite(self.dll_path)
        except Exception as e:
            QMessageBox.critical(self, "DLL 로드 오류", f"DLL을 로드하는 중 오류 발생:\n{str(e)}")
            return        

        self.arw_dll = AllReadWrite(self.dll_path, handler)
       
        self.ui.all_load.clicked.connect(lambda: self.all_load()) 
        self.ui.all_write.clicked.connect(lambda: self.arw())   
        
        # self.ui.checkBox12.stateChanged.connect(self.on_checkbox12_changed)   
        # self.ui.checkBox12.stateChanged.connect(lambda state: self.on_checkbox12_changed(state))     
        # self.ui.checkBox12.clicked.connect(lambda: self.on_checkbox12_clicked())
       
        self.connect_gridLayout_checkboxes()
        self.load_dll_filename_to_ui()
        self.load_ini_info()

    def find_any_dll(self):
        
        dll_files = [f for f in os.listdir(self.current_dir) if f.lower().endswith('.dll')]

        if not dll_files:
            QMessageBox.critical(self, "No Dll files", " DLL file not available!\n"
                                  "Position DLL file at the same directory.")
            return None
        
        selected_dll = dll_files[0] 
        QMessageBox.information(self, "DLL Loading", f"Next DLL will be loaded\n{selected_dll}")
        return os.path.join(self.current_dir, selected_dll)


    def start_ping_thread(self):
        threading.Thread(target=self.ping_ip, daemon=True).start()

    def load_ini_info(self):
        
        ini_file = self.find_ini_file()
        
        if ini_file:
            name_value = self.parse_ini_file(ini_file, "ASIC_Info")
            
            if name_value:
                self.ui.INI_info.setText("ASIC : " + name_value)
            else:
                self.ui.INI_info.setText("ASIC info. Not available")
        else:
            self.ui.INI_info.setText("INI File N.A.")

    def find_ini_file(self):
        
        for file in os.listdir(os.getcwd()):
            if file.endswith(".ini"):
                return file  
        return None
   

    def parse_ini_file(self, ini_file, key_name):
     
        # config = configparser.ConfigParser(strict=False)
        config = self.read_ini_ignore_percent(ini_file)
        # config.read(ini_file, encoding='utf-8')
         
        for section in config.sections():
            if key_name in config[section]:  
                value = config[section][key_name]
                
                if "%" in value:
                    value = value.split("%")[0].strip()  # % 앞부분만 남기고 공백 제거

                return value  

        return None 

    def read_ini_ignore_percent(self, ini_file):
        with open(ini_file, "r", encoding="utf-8") as f:
            lines = f.readlines()            
            
        filtered_lines = [line for line in lines if not line.strip().startswith("%")]
        # config = configparser.ConfigParser()
        config = configparser.ConfigParser(interpolation=None)
        config.read_string("".join(filtered_lines))
        return config


    def load_dll_filename_to_ui(self):

        current_dir = os.getcwd()  
        dll_files = [f for f in os.listdir(current_dir) if f.endswith('.dll')]

        if len(dll_files) == 0:
            # QMessageBox.critical(self, "오류", "DLL 파일이 존재하지 않습니다.")
            self.ui.DLLName.setText("DLL Name : No DLL file")
            return
        elif len(dll_files) > 1:
            # QMessageBox.critical(self, "오류", "DLL 파일이 2개 이상 존재합니다. 하나만 있어야 합니다.")
            self.ui.DLLName.setText("DLL Name : two more DLL files")
            return
       
        self.ui.DLLName.setText("DLL Name : " + dll_files[0])


    def connect_gridLayout_checkboxes(self):
        for row in range(self.gridLayout.rowCount()):
            for col in range(self.gridLayout.columnCount()):
                item = self.gridLayout.itemAtPosition(row, col)
                if item:
                    widget = item.widget()
                    if isinstance(widget, QCheckBox):
                        if widget.objectName() == "checkBox12":
                            widget.stateChanged.connect(self.on_checkbox12_changed)  # 특정 메서드 호출
                        else:
                            widget.stateChanged.connect(self.on_checkbox_changed)  # 기본 메서드 호출


    # def ping_ip(self, timeout=120, buffer_size=32):
    #     # ip_address = "10.106.14.73"
    #     ip_address = "192.168.0.7"
        
    #     try:
    #         response_time = ping(ip_address, timeout=timeout, size=buffer_size)

    #         if not response_time:  
    #             error_msg = "Ping failed: No response"
    #         else:
    #             response_time *= 1000  # Convert to milliseconds
    #             self.ui.tcp_status_label.setText(f"status: success\nresponse_time_ms: {response_time}")
    #             return {"status": "success", "response_time_ms": response_time}

    #     except Exception as e:
    #         error_msg = f"Ping failed: {str(e)}"
       
    #     self.ui.tcp_status_label.setText(f"status: failure\nerror: {error_msg}")
    #     return {"status": "failure", "error": error_msg}            
 
    def ping_ip(self, timeout=120, buffer_size=32):
        ip_address = "192.168.0.7"

        while True:
            try:
                response_time = ping(ip_address, timeout=timeout, size=buffer_size)

                if response_time:  
                    response_time *= 1000  # Convert to milliseconds
                    # self.ui.tcp_status_label.setText(f"status: success\nresponse_time_ms: {response_time}")
                    self.update_ui(status="success", response_time=response_time)
                    return  

            except Exception as e:
                error_msg = f"Ping failed: {str(e)}"

            # self.ui.tcp_status_label.setText(f"status: failure\nRetrying in 5 seconds...")  
            self.update_ui(status="failure", error=None)          
            time.sleep(5)  
            
    def update_ui(self, status, response_time=None, error=None):
        
        if status == "success":
            self.ui.tcp_status_label.setText(f"status: success\nresponse_time_ms: {response_time}")
            self.ui.tcp_status_label.setStyleSheet("color: green;")      
            self.ui.all_load.setStyleSheet("background-color: lightgreen; color: black;")        
        else:
            self.ui.tcp_status_label.setText(f"status: failure\nRetrying in 5 seconds...")
            self.ui.tcp_status_label.setStyleSheet("color: red;")  
            self.ui.all_load.setStyleSheet("background-color: red; color: white;")             
            
    # def on_checkbox12_changed(self, state): 
    def on_checkbox12_changed(self):
        
        # if state == Qt.Checked:  
        if self.ui.checkBox12.isChecked():
            print("checkBox12 checked....other checkbox disabled")

            for i in range(1, 12):  
                checkbox = getattr(self.ui, f'checkBox{i}')
                checkbox.blockSignals(True)  # 시그널 차단
                checkbox.setChecked(False)  
                checkbox.blockSignals(False)  # 시그널 다시 활성화           
         
            print("모든 체크박스가 해제됨.")
        
    def on_checkbox_changed(self):
        
        if self.ui.checkBox12.isChecked():
            print("checkBox12 disabled")

            self.ui.checkBox12.setChecked(False)               
    

    def all_load(self):
        
        checked_options = 0b000000000000  

        if self.ui.checkBox1.isChecked():
            checked_options |= 0b000000000001  
        if self.ui.checkBox2.isChecked():
            checked_options |= 0b000000000010  
        if self.ui.checkBox3.isChecked():
            checked_options |= 0b000000000100  
        if self.ui.checkBox4.isChecked():
            checked_options |= 0b000000001000  
        if self.ui.checkBox5.isChecked():
            checked_options |= 0b000000010000  
        if self.ui.checkBox6.isChecked():
            checked_options |= 0b000000100000                          
        if self.ui.checkBox7.isChecked():
            checked_options |= 0b000001000000  
        if self.ui.checkBox8.isChecked():
            checked_options |= 0b000010000000  
        if self.ui.checkBox9.isChecked():
            checked_options |= 0b000100000000  
        if self.ui.checkBox10.isChecked():
            checked_options |= 0b001000000000  
        if self.ui.checkBox11.isChecked():
            checked_options |= 0b010000000000  
        if self.ui.checkBox12.isChecked():
            checked_options = 0b000000000000                       
            

        print(f"Checked Options (Binary): {bin(checked_options)}")
        print(f"Checked Options : {checked_options}")
        # self.ui.tcp_status_label.setText(f"Checked: {bin(checked_options)}")       
        
        
        # errcode = self.my_dll.k23_all_load("NAND_123\0", self.current_dir + "\0", 0 , True)
        
        # errcode = self.dll.sparam_write("D:\\Nand\\NandRestore\\YB_LW270AHQ-ESGD-YJN-X.ini", "Panel123", self.current_dir, "C:\\nand_reg", True)      
        # print(f'all_load errcode = {errcode}')   
        
        # # 경로 설정
        # strFolderPath = self.current_dir 
        # strReworkSParam_FilePath = strFolderPath + "RYB_LW270AHQ-ESGD-YJN-X.ini"

        # # wrapMem_SParamterWriteOpen 호출
        # error_code, hMethod = self.my_dll.wrapMem_SParamterWriteOpen(strReworkSParam_FilePath)

        # # 결과 출력
        # print(f"wrapMem_SParamterWriteOpen Error Code: {error_code}")
        # print(f"hMethod Handle: {hMethod.value}")    

        # path = r"D:\Nand\NandRestore\YB_LW270AHQ-ESGD-YJN-X.ini"  # 원시 문자열 (r"")
        # if not os.path.exists(path):
        #     print(f"Error: File not found -> {path}")  # 경로 존재 여부 확인 후 실행

        # error_code, hMethod = self.my_dll.wrapMem_SParamterWriteOpen(path)

        
        # error_code, hMethod = self.my_dll.wrapMem_SParamterWriteOpen(strReworkSParam_FilePath)

        # if error_code != 0:
        #     print(f"Error in wrapMem_SParamterWriteOpen: {error_code}")
        # else:
        #     print(f"Success! hMethod: {hMethod.value}")   
            
        # if hMethod.value is None or hMethod.value == 0:
        #     print(f"Error: hMethod is NULL (Memory Allocation Failed)")             


    def arw(self):    

        # hGUI_value = self.get_handler()
        # hGUI = ctypes.c_void_p(hGUI_value) if hGUI_value else ctypes.c_void_p(0)

        # result = self.arw_dll.dll.wrapAllReadWrite(ctypes.byref(hGUI), ctypes.byref(self.arw_dll.hARW))
        
        # if result != 0:
        #     print(f"wrapAllReadWrite failed with error code {result}")
        #     raise RuntimeError(f"wrapAllReadWrite failed with error code {result}")        
    
        
        # if not self.arw_dll.hARW or self.arw_dll.hARW.value is None:
        #     raise RuntimeError("Invalid hARW handle before calling wrapAllReadWrite!")

        # result = self.arw_dll.wrapAllReadWrite(
        #     ctypes.byref(self.arw_dll.hARW), ctypes.byref(ctypes.c_void_p(self))
        # )

        # if result != 0:
        #     raise RuntimeError(f"wrapAllReadWrite failed with error code {result}")

        # print("[DEBUG] wrapAllReadWrite executed successfully")        

        # if not self.arw_dll.hARW or self.arw_dll.hARW.value is None:
        #     raise RuntimeError("Invalid hARW handle before calling wrapAllReadWrite!")

        # result = self.arw_dll.wrap_all_read_write()
        
        # if result != 0:
        #     raise RuntimeError(f"wrapAllReadWrite failed with error code {result}")

        # print("[DEBUG] wrapAllReadWrite executed successfully")
        
        result = self.arw_dll.wrap_all_read_write()  # wrap_all_read_write 호출
        if result:
            print(f"[DEBUG] wrap_all_read_write 성공, 결과: {result}")
        else:
            print("[ERROR] wrap_all_read_write 실패")
            
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())

