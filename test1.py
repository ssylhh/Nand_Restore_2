# import ctypes
# import os

# # DLL 로드
# dll_path = os.path.abspath("K23A_YB_x64.dll")  # DLL 파일 경로 지정
# my_dll = ctypes.CDLL(dll_path)

# # 함수 시그니처 설정 (DLL 함수의 정확한 시그니처를 확인하여 설정)
# my_dll.wrapMem_SParamterWriteOpen.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_char_p]
# my_dll.wrapMem_SParamterWriteOpen.restype = ctypes.c_int  # 반환 타입이 int라고 가정

# # 테스트할 경로
# test_path = "D:\\Nand\\NandRestore\\form1.ui"  # 테스트할 경로 지정

# # 테스트 함수
# def test_wrapMem_SParamterWriteOpen(path):
#     # hMethod를 NULL 포인터로 초기화
#     hMethod = ctypes.c_void_p(None)
    
#     # 경로를 바이트로 변환 (널 종료 문자 포함)
#     path_bytes = ctypes.create_string_buffer(path.encode('utf-8') + b'\0')
    
#     # DLL 함수 호출
#     result = my_dll.wrapMem_SParamterWriteOpen(ctypes.byref(hMethod), path_bytes)
    
#     # 결과 출력
#     print(f"Result: {result}")
#     print(f"hMethod: {hMethod.value}")  # hMethod의 값 출력
    
#     return result, hMethod

# # 테스트 실행
# if __name__ == "__main__":
#     result, hMethod = test_wrapMem_SParamterWriteOpen(test_path)
#     if result == 0:  # 성공 코드가 0이라고 가정
#         print("DLL 함수 호출 성공!")
#     else:
#         print(f"DLL 함수 호출 실패! 오류 코드: {result}")
        

import ctypes
import os

# DLL 로드
dll_path = os.path.abspath("K23A_YB_x64.dll")  # DLL 파일 경로 지정
my_dll = ctypes.CDLL(dll_path)

# 함수 시그니처 설정 (hMethod는 void** 이므로 ctypes.POINTER(ctypes.c_void_p) 사용)
my_dll.wrapMem_SParamterWriteOpen.argtypes = [
    ctypes.POINTER(ctypes.c_void_p),  # void**
    ctypes.c_char_p                   # const char*
]
my_dll.wrapMem_SParamterWriteOpen.restype = ctypes.c_int  # 반환 타입은 int로 가정

# 테스트할 경로
test_path = b"D:/Nand/NandRestore/requirements.txt"

# 테스트 함수
def test_wrapMem_SParamterWriteOpen(path):
    # ✅ hMethod를 ctypes.POINTER(ctypes.c_void_p)로 생성
    hMethod = ctypes.c_void_p(None)  # NULL 포인터 초기화
    hMethod_ptr = ctypes.pointer(hMethod)  # void** 포인터 생성

    # DLL 함수 호출 전 hMethod 값 출력
    print(f"hMethod before call: {hMethod.value}")

    # DLL 함수 호출
    result = my_dll.wrapMem_SParamterWriteOpen(hMethod_ptr, path)

    # DLL 함수 호출 후 hMethod 값 출력
    print(f"hMethod after call: {hMethod.value}")

    # 결과 출력
    print(f"Result: {result}")
    
    return result, hMethod.value  # hMethod의 실제 값 반환

# 테스트 실행
if __name__ == "__main__":
    result, hMethod_value = test_wrapMem_SParamterWriteOpen(test_path)
    if result == 0:  # 성공 코드가 0이라고 가정
        print("DLL 함수 호출 성공!")
        print(f"할당된 hMethod 값: {hMethod_value}")
    else:
        print(f"DLL 함수 호출 실패! 오류 코드: {result}")
