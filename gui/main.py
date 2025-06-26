# gui/main.py

import sys
from tcl_interpreter import TclInterpreter

def run_terminal():
    interp = TclInterpreter()
    while True:
        try:
            cmd = input("TCL > ")
            if cmd.strip().lower() in {"exit", "quit"}:
                break
            result = interp.eval(cmd)
            print(result)
        except KeyboardInterrupt:
            print("\nExiting.")
            break

def run_gui():
    from gui_main_window import launch_gui
    launch_gui()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-gui":
        run_gui()
    else:
        run_terminal()

