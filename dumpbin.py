import ctypes

# 📌 DLL 파일 경로 (정확한 위치로 수정)
dll_path = "D:/Nand/NandRestore/K23A_YB_x64.dll"

# 📌 DLL 로드
try:
    dll = ctypes.WinDLL(dll_path)  # 또는 ctypes.CDLL(dll_path)
    print("[✅] DLL Loaded Successfully!")
except Exception as e:
    print("[❌] DLL Load Failed:", e)
    exit()

# 📌 DLL의 모든 함수 목록 출력
functions = dir(dll)
print("\n[📌] DLL 지원 함수 목록:")
for func in functions:
    print("-", func)


    
    