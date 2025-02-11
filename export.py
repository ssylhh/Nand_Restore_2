# import pefile

# pe = pefile.PE("K23A_YB_x64.dll")

# for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
#     print(exp.name.decode() if exp.name else "None")
    

# import pefile

# def list_dll_exports(dll_path):
#     pe = pefile.PE(dll_path)
    
#     if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
#         for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
#             print(f"Function: {exp.name.decode() if exp.name else 'N/A'} | Address: {hex(exp.address)}")

# dll_path = "K23A_YB_x64.dll"  # 대상 DLL 경로
# list_dll_exports(dll_path)


# import ctypes

# # DLL 로드
# dll = ctypes.WinDLL("D:/Nand/NandRestore/K23A_YB_x64.dll")

# # GetProcAddress를 사용하여 내부 함수의 주소 찾기
# get_proc_address = ctypes.windll.kernel32.GetProcAddress
# get_proc_address.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
# get_proc_address.restype = ctypes.c_void_p

# # 'doSomething' 함수 이름으로 주소 찾기 (pefile이나 IDA Pro에서 이 주소를 확인)
# internal_func_name = b"K23_Initialize"  # DLL 내부 함수 이름
# internal_func_addr = get_proc_address(dll._handle, internal_func_name)

# if internal_func_addr:
#     # 함수 포인터로 ctypes 함수 타입을 설정
#     func_type = ctypes.CFUNCTYPE(None)  # 반환 타입이 없음 (void 함수)
#     internal_func = func_type(internal_func_addr)
    
#     # # 내부 함수 호출
#     # internal_func()
#     print("Internal function called successfully")
# else:
#     print("Internal function not found")
    

import ctypes

# DLL 로드
dll = ctypes.WinDLL("D:/Nand/NandRestore/K23A_YB_x64.dll")

# GetProcAddress를 사용하여 내부 함수의 주소 찾기
get_proc_address = ctypes.windll.kernel32.GetProcAddress
get_proc_address.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
get_proc_address.restype = ctypes.c_void_p

# 'doSomething' 함수 이름으로 주소 찾기 (pefile이나 IDA Pro에서 이 주소를 확인)
internal_func_name = b"Spara"  # DLL 내부 함수 이름
internal_func_addr = get_proc_address(dll._handle, internal_func_name)

if internal_func_addr:
    # 함수 주소 출력
    print(f"Function address of 'pot': {hex(internal_func_addr)}")
    
    # 함수 포인터로 ctypes 함수 타입을 설정
    func_type = ctypes.CFUNCTYPE(None)  # 반환 타입이 없음 (void 함수)
    internal_func = func_type(internal_func_addr)
    
    # 내부 함수 호출
    # internal_func()
    print("Internal function called successfully")
else:
    print("Internal function not found")
