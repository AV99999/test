# gui/tcl_interpreter.py

import ctypes
import os

class TclInterpreter:
    def __init__(self):
        self._load_tcl_lib()
        self._load_custom_tcl_interpreter()
        self._init_interp()

    def _load_tcl_lib(self):
        self.tcl = ctypes.CDLL("libtcl.so")

        self.tcl.Tcl_CreateInterp.restype = ctypes.c_void_p
        self.tcl.Tcl_Eval.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
        self.tcl.Tcl_Eval.restype = ctypes.c_int
        self.tcl.Tcl_GetStringResult.restype = ctypes.c_char_p
        self.tcl.Tcl_GetStringResult.argtypes = [ctypes.c_void_p]

    def _load_custom_tcl_interpreter(self):
        so_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../cpp/build/libtcl_interpreter.so"))

        self.custom = ctypes.CDLL(so_path)

        self.custom.Tclapp_Init.argtypes = [ctypes.c_void_p]
        self.custom.Tclapp_Init.restype = ctypes.c_int

    def _init_interp(self):
        self.interp = self.tcl.Tcl_CreateInterp()
        rc = self.custom.Tclapp_Init(self.interp)
        if rc != 0:
            raise RuntimeError("Failed to initialize Tclapp interpreter")

    def eval(self, command: str) -> str:
        rc = self.tcl.Tcl_Eval(self.interp, command.encode('utf-8'))
        result = self.tcl.Tcl_GetStringResult(self.interp).decode('utf-8')
        if rc != 0:
            return f"[error] {result}"
        return result

