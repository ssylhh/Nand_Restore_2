# This Python file uses the following encoding: utf-8


import ctypes

class MyDllWrapper:
    def __init__(self, dll_path):
        # DLL 파일 로드
        self.dll = ctypes.CDLL(dll_path)

        self.dll.K23_ALL_WRITE.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_bool]
        self.dll.K23_ALL_WRITE.restype = ctypes.c_int

        self.dll.K23_ALL_LOAD.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_bool]
        self.dll.K23_ALL_LOAD.restype = ctypes.c_int
        
        # self.dll.sparam_write.argtypes = [
        #     ctypes.c_char_p,  # settPath
        #     ctypes.c_char_p,  # pid
        #     ctypes.c_char_p,  # savePath
        #     ctypes.c_char_p,  # NANDRegPath
        #     ctypes.c_bool      # openDefaultSett
        # ]
        
        # self.dll.sparam_write.restype = ctypes.c_int         
        
        # self.dll.wrapMem_SParamterWriteOpen.argtypes = [
        #     ctypes.POINTER(ctypes.c_void_p),  # void** hMethod (포인터 전달)
        #     ctypes.c_char_p  # char* path (문자열)
        # ]
        # self.dll.wrapMem_SParamterWriteOpen.restype = ctypes.c_int  # 반환 타입 (int)     
        
        # self.dll.wrapMem_SParamterWriteOpen.argtypes = [
        #     ctypes.POINTER(ctypes.c_void_p),  # void** hMethod
        #     ctypes.c_char_p                   # char* path
        # ]
        # self.dll.wrapMem_SParamterWriteOpen.restype = ctypes.c_int  # 반환 타입 설정        
  

    # pid, savepath, resIndex, inEncoding
    def k23_all_load(self, str1: str, str2: str, num: int, flag: bool) -> int:
        # Encode strings to bytes
        str1_encoded = str1.encode('utf-8')
        str2_encoded = str2.encode('utf-8')

        num = 4 #일단 하드코딩 QHD
        flag = True

        return self.dll.K23_ALL_LOAD(str1_encoded, str2_encoded, num, flag)

    # pid, savepath, resIndex, inEncoding
    def k23_all_write(self, str1: str, str2: str, num: int, flag: bool) -> int:
        # Encode strings to bytes
        str1_encoded = str1.encode('utf-8')
        str2_encoded = str2.encode('utf-8')

        return self.dll.K23_ALL_WRITE(str1_encoded, str2_encoded, num, flag)

    # def sparam_write(self, sett_path, pid, save_path, nand_reg_path, open_default_sett):
        
    #     sett_path_bytes = ctypes.create_string_buffer(sett_path.encode('utf-8') + b'\0')
    #     pid_bytes = ctypes.create_string_buffer(pid.encode('utf-8') + b'\0')
    #     save_path_bytes = ctypes.create_string_buffer(save_path.encode('utf-8') + b'\0')
    #     nand_reg_path_bytes = ctypes.create_string_buffer(nand_reg_path.encode('utf-8') + b'\0')

    #     # 함수 호출
    #     result = self.dll.Sparam_Write(
    #         sett_path_bytes,
    #         pid_bytes,
    #         save_path_bytes,
    #         nand_reg_path_bytes,
    #         ctypes.c_bool(open_default_sett)
    #     )

    #     return result  # 반환값 (nErrorCode)
    
    # def wrapMem_SParamterWriteOpen(self, path: str):
    #     # void* 포인터 초기화
    #     hMethod = ctypes.c_void_p(None)

    #     # 문자열을 바이트 형식으로 변환
    #     path_bytes = ctypes.create_string_buffer(path.encode('utf-8') + b'\0')

    #     # DLL 함수 호출
    #     result = self.dll.wrapMem_SParamterWriteOpen(
    #         ctypes.byref(hMethod),  # 포인터 전달
    #         path_bytes
    #     )

    #     return result, hMethod  # 반환된 nErrorCode 값과 핸들   
     
    # def wrapMem_SParamterWriteOpen(self, path: str):
    #     # hMethod를 void* 포인터로 초기화
    #     hMethod = ctypes.c_void_p()  # NULL 포인터 생성
    #     path_bytes = ctypes.create_string_buffer(path.encode('utf-8') + b'\0')

    #     # DLL 함수 호출
    #     result = self.dll.wrapMem_SParamterWriteOpen(
    #         ctypes.byref(hMethod),  # 포인터 전달
    #         path_bytes
    #     )

    #     return result, hMethod  # 결과 코드와 핸들 반환    


