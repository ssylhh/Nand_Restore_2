# from ctypes import windll

# my_dll = windll.LoadLibrary("D:/Nand/NandRestore/K23A_YB_x64.dll")  # DLL 로드
# print(dir(my_dll))  # 내보내는 함수 목록 출력



# import pefile

# dll_path = "K23A_YB_x64.dll"
# pe = pefile.PE(dll_path)

# if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
#     for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
#         print(f"Function: {exp.name.decode()} - Address: {hex(pe.OPTIONAL_HEADER.ImageBase + exp.address)}")
        


# import frida

# session = frida.attach("notepad.exe")  # 실행 중인 프로세스에 Attach

# script = session.create_script("""
#     Interceptor.attach(Module.findExportByName("example.dll", "target_function"), {
#         onEnter: function(args) {
#             console.log("Function called! Arg0: " + args[0].toInt32());
#         }
#     });
# """)

# script.load()


import sys
import frida

# pid = 22052
pid = 1724

# session = frida.attach("main_lhh.exe")  # 실행 중인 프로세스에 Attach
session = frida.attach(pid)  # 실행 중인 프로세스에 Attach

script = session.create_script("""
    console.log("Frida script loaded successfully");  // 확인용 로그
    var moduleName = "K23A_YB_x64__re.dll";  // 감시할 DLL 이름
    var module = Module.findBaseAddress(moduleName);
    if (module) {
        var exports = Module.enumerateExports(moduleName);
        exports.forEach(function(exp) {
            Interceptor.attach(Module.findExportByName(moduleName, exp.name), {
                onEnter: function(args) {
                    console.log("[CALL] " + exp.name + " called!");
                }
            });
        });
    }
""")

script.load()
sys.stdout = open("output.log", "w")  # 로그 파일로 출력 리디렉션
print("Monitoring API Calls... Press Ctrl+C to stop.")
input()