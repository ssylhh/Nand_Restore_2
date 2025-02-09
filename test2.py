import ctypes

import ctypes

class AllReadWrite:
    def __init__(self, dll_path, gui):
        # DLL 로드 및 초기화
        self.dll = ctypes.CDLL(dll_path)
        self.hARW = ctypes.c_void_p()  # C++ 핸들 초기화

        # GUI 핸들 가져오기 (변환 추가)
        hGUI_value = gui.get_handler() if hasattr(gui, "get_handler") else None
        hGUI = ctypes.c_void_p(hGUI_value) if hGUI_value else ctypes.c_void_p(0)

        # DLL에서 핸들 초기화
        if hasattr(self.dll, '_handle'):
            handle_value = self.dll._handle
            if isinstance(handle_value, ctypes.c_void_p):
                self.hARW = handle_value
                print(f"[DEBUG] _handle을 통해 hARW 초기화됨: {self.hARW}")
            elif isinstance(handle_value, int):
                # _handle이 int일 경우, hARW를 int로 처리
                self.hARW = ctypes.c_int(handle_value)
                print(f"[DEBUG] _handle을 통해 hARW 초기화됨 (int 타입): {self.hARW.value}")
            else:
                raise RuntimeError(f"지원되지 않는 핸들 타입: {type(handle_value)}")
        else:
            raise RuntimeError("핸들 초기화 실패, 유효한 함수나 속성을 찾을 수 없음.")

        # wrapAllReadWrite 함수 설정
        self.dll.wrapAllReadWrite.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p)]
        self.dll.wrapAllReadWrite.restype = ctypes.c_int

        result = self.dll.wrapAllReadWrite(ctypes.byref(hGUI), ctypes.byref(self.hARW))
        if result != 0:
            raise RuntimeError(f"wrapAllReadWrite 실패, 에러 코드: {result}")

        # 데이터 리스트 초기화
        self.datalist = []
        self.get_data()

    def get_data(self):
        if not self.hARW or (hasattr(self.hARW, 'value') and self.hARW.value is None):
            raise RuntimeError("Invalid hARW handle!")

        # wrapAllReadWrite_getCount 함수 설정
        self.dll.wrapAllReadWrite_getCount.argtypes = [ctypes.POINTER(ctypes.c_void_p)]
        self.dll.wrapAllReadWrite_getCount.restype = ctypes.c_int
        total_count = self.dll.wrapAllReadWrite_getCount(ctypes.byref(self.hARW))

        # 그룹과 이름 가져오기
        for i in range(total_count):
            groupname = ctypes.create_string_buffer(512)  # 버퍼 크기 증가
            paramname = ctypes.create_string_buffer(512)

            self._get_group_or_name(i, groupname, paramname)

            self.datalist.append((groupname.value.decode('utf-8').strip(), paramname.value.decode('utf-8').strip()))

    def _get_group_or_name(self, index, groupname, paramname):
        """ 그룹명과 파라미터명을 가져오는 공통 함수 """
        self.dll.wrapAllReadWrite_getGroup.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_int, ctypes.c_char_p]
        self.dll.wrapAllReadWrite_getName.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_int, ctypes.c_char_p]
        
        # 그룹명과 파라미터명 얻기
        self.dll.wrapAllReadWrite_getGroup(ctypes.byref(self.hARW), index, groupname)
        self.dll.wrapAllReadWrite_getName(ctypes.byref(self.hARW), index, paramname)

    def read(self, num, pid, path):
        """ Read 작업 수행 """
        self.dll.wrapAllReadWrite_Read.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
        self.dll.wrapAllReadWrite_Read.restype = ctypes.c_int

        pid_bytes = ctypes.create_string_buffer(pid.encode('utf-8'))
        path_bytes = ctypes.create_string_buffer(path.encode('utf-8'))

        return self.dll.wrapAllReadWrite_Read(ctypes.byref(self.hARW), num, pid_bytes, path_bytes)

    def write(self, num, pid, path):
        """ Write 작업 수행 """
        self.dll.wrapAllReadWrite_Write.argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p]
        self.dll.wrapAllReadWrite_Write.restype = ctypes.c_int

        pid_bytes = ctypes.create_string_buffer(pid.encode('utf-8'))
        path_bytes = ctypes.create_string_buffer(path.encode('utf-8'))

        return self.dll.wrapAllReadWrite_Write(ctypes.byref(self.hARW), num, pid_bytes, path_bytes)
